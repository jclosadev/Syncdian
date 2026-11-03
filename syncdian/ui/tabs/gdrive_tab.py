import os
from pathlib import Path
from PySide6.QtCore import Qt, Signal, QThread
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QFrame, QFileDialog, QLineEdit, QMessageBox, QTabWidget
)

from syncdian.config import get_config
from syncdian.core.gdrive import GoogleDriveService
from syncdian.ui.widgets.setting_row import SettingRow


class AuthWorker(QThread):
    auth_success = Signal(dict)
    auth_failed = Signal(str)

    def __init__(self, mode: str, file_path: str = "", client_id: str = "", client_secret: str = ""):
        super().__init__()
        self.mode = mode
        self.file_path = file_path
        self.client_id = client_id
        self.client_secret = client_secret

    def run(self):
        try:
            service = GoogleDriveService()
            if self.mode == "file":
                info = service.authenticate_with_credentials_file(Path(self.file_path))
            else:
                info = service.authenticate_with_client_keys(self.client_id, self.client_secret)
            self.auth_success.emit(info)
        except Exception as e:
            self.auth_failed.emit(str(e))


class GoogleDriveTab(QWidget):
    connection_changed = Signal(bool)

    def __init__(self, gdrive_service: GoogleDriveService, parent=None):
        super().__init__(parent)
        self.config_manager = get_config()
        self.gdrive = gdrive_service
        self.auth_worker = None
        self.init_ui()

    def init_ui(self):
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(24, 20, 24, 20)
        self.main_layout.setSpacing(16)

        self.content_widget = QWidget()
        self.content_layout = QVBoxLayout(self.content_widget)
        self.content_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.addWidget(self.content_widget)

        self.main_layout.addStretch()
        self.refresh_status_view()

    def refresh_status_view(self):
        while self.content_layout.count() > 0:
            item = self.content_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        if self.gdrive.is_authenticated():
            self._build_connected_view()
        else:
            self._build_disconnected_view()

    def _build_connected_view(self):
        card = QFrame()
        card.setObjectName("obsidianCard")
        card_l = QVBoxLayout(card)
        card_l.setContentsMargins(8, 8, 8, 8)
        card_l.setSpacing(0)

        # Fila Estado y Desconexión
        disc_btn = QPushButton("Desconectar Cuenta")
        disc_btn.setObjectName("dangerButton")
        disc_btn.clicked.connect(self._disconnect)

        user_email = self.config_manager.google_drive.user_email or "Cuenta Conectada"
        row_status = SettingRow(
            title="Cuenta de Google Drive Vinculada",
            description=f"Sesión activa como: {user_email}",
            link_text="Google Drive API conectada de forma segura (ámbito: drive.file).",
            action_widget=disc_btn
        )
        card_l.addWidget(row_status)

        # Fila Almacenamiento
        try:
            info = self.gdrive.get_account_info()
            usage_mb = info.get("storage_usage_bytes", 0) / (1024 * 1024)
            limit_mb = (info.get("storage_limit_bytes", 0) or 0) / (1024 * 1024)
            storage_text = f"{usage_mb/1024:.2f} GB de {limit_mb/1024:.2f} GB" if limit_mb > 0 else f"{usage_mb/1024:.2f} GB usados"
        except Exception:
            storage_text = "Disponible"

        storage_lbl = QLabel(storage_text)
        storage_lbl.setStyleSheet("color: #df9b20; font-weight: bold;")
        row_storage = SettingRow(
            title="Espacio de Almacenamiento",
            description="Uso actual de almacenamiento en tu cuenta de Google Drive.",
            action_widget=storage_lbl
        )
        card_l.addWidget(row_storage)

        # Fila Carpeta Raíz
        folder_box = QWidget()
        fb_l = QHBoxLayout(folder_box)
        fb_l.setContentsMargins(0, 0, 0, 0)
        self.folder_name_edit = QLineEdit(self.config_manager.google_drive.root_folder_name or "Syncdian Obsidian Backups")
        self.folder_name_edit.setFixedWidth(200)
        save_folder_btn = QPushButton("Guardar")
        save_folder_btn.clicked.connect(self._update_folder_name)
        fb_l.addWidget(self.folder_name_edit)
        fb_l.addWidget(save_folder_btn)

        row_folder = SettingRow(
            title="Carpeta Destino en Drive",
            description="Nombre de la carpeta principal creada en tu Google Drive donde se guardarán los vaults.",
            action_widget=folder_box
        )
        card_l.addWidget(row_folder)

        self.content_layout.addWidget(card)

    def _build_disconnected_view(self):
        card = QFrame()
        card.setObjectName("obsidianCard")
        card_l = QVBoxLayout(card)
        card_l.setContentsMargins(8, 8, 8, 8)
        card_l.setSpacing(0)

        # Opción 1: Archivo JSON
        file_box = QWidget()
        fb_l = QHBoxLayout(file_box)
        fb_l.setContentsMargins(0, 0, 0, 0)
        self.json_path_edit = QLineEdit()
        self.json_path_edit.setPlaceholderText("Ruta a credentials.json...")
        self.json_path_edit.setFixedWidth(220)
        browse_btn = QPushButton("Examinar...")
        browse_btn.clicked.connect(self._browse_credentials_file)
        connect_json_btn = QPushButton("Conectar")
        connect_json_btn.setObjectName("primaryButton")
        connect_json_btn.clicked.connect(self._auth_via_json)
        fb_l.addWidget(self.json_path_edit)
        fb_l.addWidget(browse_btn)
        fb_l.addWidget(connect_json_btn)

        row_json = SettingRow(
            title="Vincular con credentials.json",
            description="Carga el archivo de credenciales de escritorio descargado de Google Cloud Console.",
            link_text="Opción recomendada y más rápida.",
            action_widget=file_box
        )
        card_l.addWidget(row_json)

        # Opción 2: Claves manuales
        keys_box = QWidget()
        kb_l = QVBoxLayout(keys_box)
        kb_l.setContentsMargins(0, 0, 0, 0)
        self.client_id_edit = QLineEdit()
        self.client_id_edit.setPlaceholderText("Client ID")
        self.client_id_edit.setFixedWidth(280)
        self.client_id_edit.setText(self.config_manager.google_drive.client_id)
        self.client_secret_edit = QLineEdit()
        self.client_secret_edit.setPlaceholderText("Client Secret")
        self.client_secret_edit.setEchoMode(QLineEdit.Password)
        self.client_secret_edit.setFixedWidth(280)
        self.client_secret_edit.setText(self.config_manager.google_drive.client_secret)
        btn_keys = QPushButton("Iniciar Sesión con Claves")
        btn_keys.clicked.connect(self._auth_via_keys)
        kb_l.addWidget(self.client_id_edit)
        kb_l.addWidget(self.client_secret_edit)
        kb_l.addWidget(btn_keys)

        row_keys = SettingRow(
            title="Vincular con Client ID y Secret",
            description="Ingresa manualmente tus identificadores de cliente de OAuth.",
            action_widget=keys_box
        )
        card_l.addWidget(row_keys)

        self.content_layout.addWidget(card)

        # Guía paso a paso en tarjeta limpia
        guide_card = QFrame()
        guide_card.setObjectName("obsidianCard")
        g_layout = QVBoxLayout(guide_card)
        g_layout.setContentsMargins(16, 16, 16, 16)
        g_layout.setSpacing(10)

        g_title = QLabel("📖 Pasos para obtener tus credenciales en Google Cloud Console:")
        g_title.setStyleSheet("font-weight: 600; color: #df9b20; font-size: 13px;")
        g_layout.addWidget(g_title)

        guide_text = (
            "1. Abre <a style='color: #df9b20;' href='https://console.cloud.google.com/'>Google Cloud Console</a> y crea un proyecto llamado <b>Syncdian</b>.<br>"
            "2. En <b>Biblioteca de APIs</b>, busca y activa <b>Google Drive API</b>.<br>"
            "3. En <b>Pantalla de consentimiento de OAuth</b>, elige 'Externo' y añade tu propio correo en 'Usuarios de prueba'.<br>"
            "4. En <b>Credenciales</b>, pulsa <b>+ Crear credenciales</b> > <b>ID de cliente de OAuth</b> y selecciona tipo <b>App de escritorio</b>.<br>"
            "5. Descarga el archivo JSON o copia tus claves, selecciona el archivo arriba y pulsa <b>Conectar</b>."
        )
        lbl_guide = QLabel(guide_text)
        lbl_guide.setOpenExternalLinks(True)
        lbl_guide.setWordWrap(True)
        lbl_guide.setStyleSheet("color: #9c8e7e; font-size: 12px; line-height: 1.5;")
        g_layout.addWidget(lbl_guide)

        self.content_layout.addWidget(guide_card)

    def _browse_credentials_file(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Seleccionar credentials.json",
            "",
            "Archivos JSON (*.json);;Todos los archivos (*.*)"
        )
        if file_path:
            self.json_path_edit.setText(file_path)

    def _auth_via_json(self):
        path = self.json_path_edit.text().strip()
        if not path or not Path(path).exists():
            QMessageBox.warning(self, "Aviso", "Por favor selecciona un archivo credentials.json válido.")
            return

        self._start_auth("file", file_path=path)

    def _auth_via_keys(self):
        cid = self.client_id_edit.text().strip()
        csec = self.client_secret_edit.text().strip()
        if not cid or not csec:
            QMessageBox.warning(self, "Aviso", "Por favor ingresa Client ID y Client Secret.")
            return

        self.config_manager.google_drive.client_id = cid
        self.config_manager.google_drive.client_secret = csec
        self.config_manager.save()
        self._start_auth("keys", client_id=cid, client_secret=csec)

    def _start_auth(self, mode: str, **kwargs):
        QMessageBox.information(
            self,
            "Autenticación con Google",
            "Se abrirá tu navegador para que inicies sesión en Google y autorices a Syncdian."
        )
        self.auth_worker = AuthWorker(mode, **kwargs)
        self.auth_worker.auth_success.connect(self._on_success)
        self.auth_worker.auth_failed.connect(self._on_failed)
        self.auth_worker.start()

    def _on_success(self, info: dict):
        email = info.get("email", "")
        self.config_manager.google_drive.user_email = email
        self.config_manager.google_drive.authenticated = True
        self.config_manager.save()
        QMessageBox.information(self, "¡Conexión Exitosa!", f"Google Drive vinculado exitosamente con:\n{email}")
        self.refresh_status_view()
        self.connection_changed.emit(True)

    def _on_failed(self, err: str):
        QMessageBox.critical(self, "Error de Conexión", f"No se pudo completar la conexión:\n{err}")

    def _disconnect(self):
        res = QMessageBox.question(self, "Desconectar", "¿Deseas desconectar tu cuenta de Google Drive?", QMessageBox.Yes | QMessageBox.No)
        if res == QMessageBox.Yes:
            self.gdrive.disconnect()
            self.config_manager.google_drive.authenticated = False
            self.config_manager.google_drive.user_email = ""
            self.config_manager.save()
            self.refresh_status_view()
            self.connection_changed.emit(False)

    def _update_folder_name(self):
        n = self.folder_name_edit.text().strip()
        if n:
            self.config_manager.google_drive.root_folder_name = n
            self.config_manager.save()
            QMessageBox.information(self, "Actualizado", "Nombre de carpeta destino guardado.")
