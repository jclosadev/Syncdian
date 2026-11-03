import logging
import time
import uuid
from datetime import datetime
from pathlib import Path
from typing import Optional, Callable, Dict, Any, List

from syncdian.config import get_config, VaultConfig, SyncHistoryRecord
from syncdian.constants import MODE_SNAPSHOT_ZIP, MODE_MIRROR_SYNC
from syncdian.core.gdrive import GoogleDriveService
from syncdian.core.vault_manager import VaultManager

logger = logging.getLogger(__name__)


class SyncEngine:
    def __init__(
        self,
        gdrive_service: Optional[GoogleDriveService] = None,
        progress_callback: Optional[Callable[[float, str], None]] = None,
        log_callback: Optional[Callable[[str], None]] = None
    ):
        self.config_manager = get_config()
        self.gdrive = gdrive_service or GoogleDriveService()
        self.progress_callback = progress_callback
        self.log_callback = log_callback
        self._is_cancelled = False

    def cancel(self):
        self._is_cancelled = True

    def _log(self, message: str):
        logger.info(message)
        if self.log_callback:
            self.log_callback(message)

    def _update_progress(self, percent: float, message: str):
        if self.progress_callback:
            self.progress_callback(percent, message)

    def sync_all_vaults(self) -> Dict[str, Any]:
        """Sincroniza todos los vaults que estén marcados como habilitados."""
        self._is_cancelled = False
        enabled_vaults = [v for v in self.config_manager.vaults if v.enabled]
        
        if not enabled_vaults:
            self._log("No hay ningún vault de Obsidian configurado o habilitado para sincronizar.")
            return {"status": "skipped", "message": "No hay vaults habilitados"}

        if not self.gdrive.is_authenticated():
            err_msg = "Google Drive no está conectado o la sesión ha expirado."
            self._log(f"ERROR: {err_msg}")
            return {"status": "error", "message": err_msg}

        self._log(f"Iniciando sincronización de {len(enabled_vaults)} vault(s)...")
        results = []

        total_vaults = len(enabled_vaults)
        for idx, vault in enumerate(enabled_vaults):
            if self._is_cancelled:
                self._log("Sincronización cancelada por el usuario.")
                break

            base_percent = (idx / total_vaults) * 100.0
            self._log(f"--- Procesando Vault [{idx+1}/{total_vaults}]: {vault.name} ---")

            res = self.sync_single_vault(
                vault,
                step_progress_weight=(1.0 / total_vaults),
                current_base_percent=base_percent
            )
            results.append(res)

        self._update_progress(100.0, "Sincronización finalizada.")
        return {"status": "done", "results": results}

    def sync_single_vault(
        self,
        vault: VaultConfig,
        step_progress_weight: float = 1.0,
        current_base_percent: float = 0.0
    ) -> Dict[str, Any]:
        start_time = time.time()
        vault.last_status = "running"
        self.config_manager.update_vault(vault)

        vault_path = Path(vault.path)
        if not vault_path.exists():
            err = f"La carpeta del vault '{vault.path}' no existe en el disco."
            self._log(f"ERROR: {err}")
            vault.last_status = "failed"
            vault.last_error = err
            self.config_manager.update_vault(vault)
            self._record_history(vault, "failed", 0, 0, time.time() - start_time, err)
            return {"vault": vault.name, "status": "failed", "error": err}

        temp_zip: Optional[Path] = None
        try:
            # 1. Obtener o crear carpeta raíz en Google Drive
            root_folder_name = self.config_manager.google_drive.root_folder_name or "Syncdian Obsidian Backups"
            self._update_progress(
                current_base_percent + 5.0 * step_progress_weight,
                f"Verificando carpeta en Google Drive ({root_folder_name})..."
            )
            root_id = self.gdrive.get_or_create_folder(root_folder_name)
            self.config_manager.google_drive.root_folder_id = root_id
            self.config_manager.save()

            # Carpeta específica para este vault dentro de la raíz
            vault_folder_id = self.gdrive.get_or_create_folder(vault.name, parent_id=root_id)

            exclusions = self.config_manager.settings.exclude_patterns

            # 2. Modo Snapshot ZIP
            if vault.backup_mode == MODE_SNAPSHOT_ZIP or True:  # Por defecto y más seguro
                self._update_progress(
                    current_base_percent + 15.0 * step_progress_weight,
                    f"Comprimiendo vault '{vault.name}'..."
                )

                def zip_cb(current, total, cur_file):
                    pct = 15.0 + (current / max(total, 1)) * 35.0
                    self._update_progress(
                        current_base_percent + pct * step_progress_weight,
                        f"Comprimiendo [{current}/{total}]: {Path(cur_file).name}"
                    )

                temp_zip, total_files, zip_size = VaultManager.create_vault_zip_snapshot(
                    vault_name=vault.name,
                    vault_path=vault_path,
                    exclusions=exclusions,
                    progress_callback=zip_cb
                )

                # 3. Subida a Google Drive
                self._log(f"Subiendo {temp_zip.name} ({zip_size / 1024 / 1024:.2f} MB) a Google Drive...")

                def upload_cb(progress, uploaded_bytes, total_bytes):
                    pct = 50.0 + (progress * 40.0)
                    mb_up = uploaded_bytes / (1024 * 1024)
                    mb_tot = total_bytes / (1024 * 1024)
                    self._update_progress(
                        current_base_percent + pct * step_progress_weight,
                        f"Subiendo a Google Drive: {mb_up:.1f}MB / {mb_tot:.1f}MB ({int(progress*100)}%)"
                    )

                upload_res = self.gdrive.upload_file_resumable(
                    local_path=temp_zip,
                    parent_id=vault_folder_id,
                    mime_type="application/zip",
                    progress_callback=upload_cb
                )

                # 4. Gestión de retención (mantener últimos N)
                deleted_old = self.gdrive.apply_retention_policy(
                    folder_id=vault_folder_id,
                    vault_name=vault.name,
                    keep_count=vault.retention_count
                )
                if deleted_old > 0:
                    self._log(f"Política de retención: Se limpiaron {deleted_old} copias antiguas.")

                duration = time.time() - start_time
                vault.last_status = "success"
                vault.last_sync = datetime.now().isoformat()
                vault.last_error = None
                self.config_manager.update_vault(vault)

                success_msg = f"Copia completada con éxito ({total_files} archivos, {zip_size / 1024 / 1024:.2f} MB en {duration:.1f}s)"
                self._log(f"ÉXITO: {vault.name} -> {success_msg}")
                self._record_history(vault, "success", total_files, zip_size, duration, success_msg)

                return {
                    "vault": vault.name,
                    "status": "success",
                    "files": total_files,
                    "size_bytes": zip_size,
                    "duration": duration,
                    "drive_file_id": upload_res.get("id")
                }

        except Exception as e:
            duration = time.time() - start_time
            err_msg = f"Error durante la sincronización: {str(e)}"
            logger.exception(err_msg)
            self._log(f"ERROR en {vault.name}: {err_msg}")
            vault.last_status = "failed"
            vault.last_error = str(e)
            self.config_manager.update_vault(vault)
            self._record_history(vault, "failed", 0, 0, duration, err_msg)
            return {"vault": vault.name, "status": "failed", "error": str(e)}

        finally:
            # Limpiar archivo temporal .zip
            if temp_zip and temp_zip.exists():
                try:
                    temp_zip.unlink()
                except Exception as e:
                    logger.debug(f"No se pudo borrar zip temporal {temp_zip}: {e}")

    def _record_history(
        self,
        vault: VaultConfig,
        status: str,
        files_count: int,
        size_bytes: int,
        duration: float,
        message: str
    ):
        record = SyncHistoryRecord(
            id=str(uuid.uuid4())[:8],
            timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            vault_name=vault.name,
            status=status,
            mode=vault.backup_mode,
            files_count=files_count,
            size_bytes=size_bytes,
            duration_seconds=round(duration, 2),
            message=message
        )
        self.config_manager.add_history_record(record)

