import json
import logging
import os
import shutil
from pathlib import Path
from typing import Optional, Dict, Any, List, Callable, Tuple

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload

from syncdian.constants import TOKEN_FILE, CREDENTIALS_FILE, DRIVE_SCOPES

logger = logging.getLogger(__name__)


class GoogleDriveService:
    def __init__(self, token_path: Path = TOKEN_FILE, credentials_path: Path = CREDENTIALS_FILE):
        self.token_path = Path(token_path)
        self.credentials_path = Path(credentials_path)
        self.creds: Optional[Credentials] = None
        self.service = None
        self._load_cached_credentials()

    def _load_cached_credentials(self) -> bool:
        """Intenta cargar credenciales guardadas en token.json si existen y son válidas."""
        try:
            if self.token_path.exists():
                self.creds = Credentials.from_authorized_user_file(str(self.token_path), DRIVE_SCOPES)
                if self.creds and self.creds.expired and self.creds.refresh_token:
                    logger.info("El token ha expirado. Refrescando...")
                    self.creds.refresh(Request())
                    with open(self.token_path, "w", encoding="utf-8") as token_f:
                        token_f.write(self.creds.to_json())
                if self.creds and self.creds.valid:
                    self.service = build("drive", "v3", credentials=self.creds)
                    return True
        except Exception as e:
            logger.warning(f"No se pudieron cargar credenciales existentes: {e}")
            self.creds = None
            self.service = None
        return False

    def is_authenticated(self) -> bool:
        if not self.creds or not self.creds.valid:
            return self._load_cached_credentials()
        return True

    def authenticate_with_credentials_file(self, json_file_path: Path) -> Dict[str, Any]:
        """Inicia el flujo OAuth2 usando un archivo credentials.json."""
        json_file_path = Path(json_file_path)
        if not json_file_path.exists():
            raise FileNotFoundError(f"Archivo de credenciales no encontrado en {json_file_path}")

        # Copiar credenciales al directorio de AppData para persistencia
        self.credentials_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(json_file_path, self.credentials_path)

        flow = InstalledAppFlow.from_client_secrets_file(
            str(self.credentials_path),
            DRIVE_SCOPES
        )
        self.creds = flow.run_local_server(port=0, open_browser=True)

        with open(self.token_path, "w", encoding="utf-8") as token_file:
            token_file.write(self.creds.to_json())

        self.service = build("drive", "v3", credentials=self.creds)
        return self.get_account_info()

    def authenticate_with_client_keys(self, client_id: str, client_secret: str) -> Dict[str, Any]:
        """Inicia el flujo OAuth2 usando Client ID y Client Secret directamente."""
        client_config = {
            "installed": {
                "client_id": client_id.strip(),
                "client_secret": client_secret.strip(),
                "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                "token_uri": "https://oauth2.googleapis.com/token",
                "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
                "redirect_uris": ["http://localhost"]
            }
        }
        self.credentials_path.parent.mkdir(parents=True, exist_ok=True)
        with open(self.credentials_path, "w", encoding="utf-8") as f:
            json.dump(client_config, f, indent=2)

        flow = InstalledAppFlow.from_client_config(client_config, DRIVE_SCOPES)
        self.creds = flow.run_local_server(port=0, open_browser=True)

        with open(self.token_path, "w", encoding="utf-8") as token_file:
            token_file.write(self.creds.to_json())

        self.service = build("drive", "v3", credentials=self.creds)
        return self.get_account_info()

    def disconnect(self):
        """Desconecta la cuenta y borra los tokens locales."""
        try:
            if self.token_path.exists():
                self.token_path.unlink()
        except Exception as e:
            logger.warning(f"Error al eliminar token: {e}")
        self.creds = None
        self.service = None

    def get_account_info(self) -> Dict[str, Any]:
        """Obtiene información sobre el usuario y el almacenamiento de Google Drive."""
        if not self.is_authenticated():
            raise PermissionError("No hay sesión autenticada con Google Drive.")

        about = self.service.about().get(fields="user(displayName, emailAddress, photoLink), storageQuota").execute()
        user = about.get("user", {})
        quota = about.get("storageQuota", {})
        
        limit_bytes = int(quota.get("limit", 0)) if quota.get("limit") else None
        usage_bytes = int(quota.get("usage", 0)) if quota.get("usage") else 0

        return {
            "display_name": user.get("displayName", "Usuario"),
            "email": user.get("emailAddress", ""),
            "avatar_url": user.get("photoLink", ""),
            "storage_usage_bytes": usage_bytes,
            "storage_limit_bytes": limit_bytes,
        }

    def get_or_create_folder(self, folder_name: str, parent_id: Optional[str] = None) -> str:
        """Busca una carpeta por nombre dentro de parent_id (o root). Si no existe, la crea."""
        if not self.is_authenticated():
            raise PermissionError("No autenticado.")

        parent_clause = f"'{parent_id}' in parents" if parent_id else "'root' in parents"
        query = (
            f"name = '{folder_name}' and "
            f"mimeType = 'application/vnd.google-apps.folder' and "
            f"trashed = false and "
            f"{parent_clause}"
        )

        response = self.service.files().list(
            q=query,
            spaces="drive",
            fields="files(id, name)",
            pageSize=10
        ).execute()

        files = response.get("files", [])
        if files:
            return files[0]["id"]

        # Crear la carpeta
        folder_metadata = {
            "name": folder_name,
            "mimeType": "application/vnd.google-apps.folder"
        }
        if parent_id:
            folder_metadata["parents"] = [parent_id]

        folder = self.service.files().create(
            body=folder_metadata,
            fields="id"
        ).execute()

        logger.info(f"Carpeta creada en Google Drive: '{folder_name}' (ID: {folder.get('id')})")
        return folder.get("id")

    def upload_file_resumable(
        self,
        local_path: Path,
        parent_id: str,
        custom_name: Optional[str] = None,
        mime_type: Optional[str] = None,
        progress_callback: Optional[Callable[[float, int, int], None]] = None
    ) -> Dict[str, Any]:
        """
        Sube un archivo a Google Drive con soporte resumable y reporte de progreso por fragmentos.
        """
        if not self.is_authenticated():
            raise PermissionError("No autenticado en Google Drive.")

        local_path = Path(local_path)
        if not local_path.exists():
            raise FileNotFoundError(f"Archivo a subir no existe: {local_path}")

        file_name = custom_name or local_path.name
        total_size = local_path.stat().st_size

        file_metadata = {
            "name": file_name,
            "parents": [parent_id]
        }

        media = MediaFileUpload(
            str(local_path),
            mimetype=mime_type or "application/octet-stream",
            resumable=True,
            chunksize=1024 * 1024 * 2  # 2MB chunks para estabilidad
        )

        request = self.service.files().create(
            body=file_metadata,
            media_body=media,
            fields="id, name, size, md5Checksum, webViewLink"
        )

        response = None
        while response is None:
            status, response = request.next_chunk()
            if status and progress_callback:
                progress_callback(status.progress(), status.resumable_progress, total_size)

        if progress_callback:
            progress_callback(1.0, total_size, total_size)

        logger.info(f"Archivo subido exitosamente: {file_name} (ID: {response.get('id')})")
        return response

    def list_snapshots_for_vault(self, folder_id: str, vault_name: str) -> List[Dict[str, Any]]:
        """Lista los archivos zip de respaldo de un vault ordenados cronológicamente."""
        if not self.is_authenticated():
            return []

        safe_name = "".join(c for c in vault_name if c.isalnum() or c in ("-", "_", " ")).strip()
        query = (
            f"'{folder_id}' in parents and "
            f"name contains '{safe_name}_' and "
            f"trashed = false"
        )

        response = self.service.files().list(
            q=query,
            orderBy="createdTime desc",
            fields="files(id, name, size, createdTime, webViewLink)",
            pageSize=100
        ).execute()

        return response.get("files", [])

    def apply_retention_policy(self, folder_id: str, vault_name: str, keep_count: int) -> int:
        """
        Elimina copias de seguridad antiguas que excedan el límite de retención configurado.
        Retorna la cantidad de archivos eliminados.
        """
        if keep_count <= 0:
            return 0

        snapshots = self.list_snapshots_for_vault(folder_id, vault_name)
        if len(snapshots) <= keep_count:
            return 0

        deleted_count = 0
        to_delete = snapshots[keep_count:]
        for item in to_delete:
            try:
                self.service.files().delete(fileId=item["id"]).execute()
                deleted_count += 1
                logger.info(f"Retención: Eliminado snapshot antiguo '{item['name']}' ({item['id']})")
            except Exception as e:
                logger.warning(f"No se pudo eliminar snapshot antiguo {item['id']}: {e}")

        return deleted_count

