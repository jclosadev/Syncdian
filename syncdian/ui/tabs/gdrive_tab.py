from pathlib import Path

from PySide6.QtCore import Qt, Signal, QThread
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QFrame, QFileDialog, QLineEdit, QMessageBox
)

from syncdian.config import get_config
from syncdian.core.gdrive import GoogleDriveService
from syncdian.i18n import tr
from syncdian.ui.icons import get_icon, ICON_COLOR, ICON_COLOR_ACTIVE
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
        self._storage_info_cache = None
        self.init_ui()

    def init_ui(self):
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(28, 24, 28, 24)
        self.main_layout.setSpacing(16)

        self.content_widget = QWidget()
        self.content_layout = QVBoxLayout(self.content_widget)
        self.content_layout.setContentsMargins(0, 0, 0, 0)
        self.content_layout.setSpacing(16)
        self.main_layout.addWidget(self.content_widget)

        self.main_layout.addStretch()
        self.refresh_status_view()

    def retranslate(self):
        self.refresh_status_view()

    def refresh_status_view(self):
        # Conservar los valores escritos por el usuario al cambiar de idioma.
        current_view = getattr(self, "_current_view", None)
        saved_json = self.json_path_edit.text() if current_view == "disconnected" else ""
        saved_cid = self.client_id_edit.text() if current_view == "disconnected" else ""
        saved_csecret = self.client_secret_edit.text() if current_view == "disconnected" else ""
        saved_folder = self.folder_name_edit.text() if current_view == "connected" else ""

        while self.content_layout.count() > 0:
            item = self.content_layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.setParent(None)
                widget.deleteLater()

        if self.gdrive.is_authenticated():
            self._build_connected_view()
            self._current_view = "connected"
        else:
            self._build_disconnected_view()
            self._current_view = "disconnected"

        if self._current_view == "disconnected":
            if saved_json:
                self.json_path_edit.setText(saved_json)
            if saved_cid:
                self.client_id_edit.setText(saved_cid)
            if saved_csecret:
                self.client_secret_edit.setText(saved_csecret)
        elif saved_folder:
            self.folder_name_edit.setText(saved_folder)

    def _build_connected_view(self):
        card = QFrame()
        card.setObjectName("obsidianCard")
        card_l = QVBoxLayout(card)
        card_l.setContentsMargins(8, 8, 8, 8)
        card_l.setSpacing(0)

        # Fila Estado y Desconexión
        disc_btn = QPushButton(tr("gdrive_disconnect"))
        disc_btn.setObjectName("dangerButton")
        disc_btn.setIcon(get_icon("unplug", 14, "#e88c7c"))
        disc_btn.clicked.connect(self._disconnect)

        user_email = self.config_manager.google_drive.user_email or tr("gdrive_account_connected")
        row_status = SettingRow(
            title=tr("gdrive_acc_title"),
            description=tr("gdrive_acc_desc", email=user_email),
            link_text=tr("gdrive_api_scope"),
            action_widget=disc_btn
        )
        card_l.addWidget(row_status)

        # Fila Almacenamiento (datos cacheados para que el cambio de idioma sea instantáneo)
        if self._storage_info_cache is None:
            try:
                info = self.gdrive.get_account_info()
                self._storage_info_cache = {
                    "used_gb": info.get("storage_usage_bytes", 0) / (1024 ** 3),
                    "limit_gb": (info.get("storage_limit_bytes") or 0) / (1024 ** 3),
                }
            except Exception:
                self._storage_info_cache = {"used_gb": None, "limit_gb": None}

        cache = self._storage_info_cache
        if cache["used_gb"] is None:
            storage_text = tr("gdrive_storage_available")
        elif cache["limit_gb"]:
            storage_text = tr(
                "gdrive_storage_of",
                used=f"{cache['used_gb']:.2f}",
                total=f"{cache['limit_gb']:.2f}",
            )
        else:
            storage_text = tr("gdrive_storage_used", used=f"{cache['used_gb']:.2f}")

        storage_lbl = QLabel(storage_text)
        storage_lbl.setObjectName("selectorBadge")
        row_storage = SettingRow(
            title=tr("gdrive_storage_title"),
            description=tr("gdrive_storage_desc"),
            action_widget=storage_lbl
        )
        card_l.addWidget(row_storage)

        # Fila Carpeta Raíz
        folder_box = QWidget()
        fb_l = QHBoxLayout(folder_box)
        fb_l.setContentsMargins(0, 0, 0, 0)
        fb_l.setSpacing(8)
        self.folder_name_edit = QLineEdit(
            self.config_manager.google_drive.root_folder_name or "Syncdian Obsidian Backups"
        )
        self.folder_name_edit.setFixedWidth(210)
        save_folder_btn = QPushButton(tr("gdrive_save_folder"))
        save_folder_btn.setIcon(get_icon("save", 14, ICON_COLOR))
        save_folder_btn.clicked.connect(self._update_folder_name)
        fb_l.addWidget(self.folder_name_edit)
        fb_l.addWidget(save_folder_btn)

        row_folder = SettingRow(
            title=tr("gdrive_folder_title"),
            description=tr("gdrive_folder_desc"),
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
        fb_l.setSpacing(8)
        self.json_path_edit = QLineEdit()
        self.json_path_edit.setPlaceholderText(tr("gdrive_json_placeholder"))
        self.json_path_edit.setFixedWidth(210)
        browse_btn = QPushButton(tr("dlg_browse"))
        browse_btn.setIcon(get_icon("folder_open", 14, ICON_COLOR))
        browse_btn.clicked.connect(self._browse_credentials_file)
        connect_json_btn = QPushButton(tr("gdrive_connect_btn"))
        connect_json_btn.setObjectName("primaryButton")
        connect_json_btn.setIcon(get_icon("link", 14, ICON_COLOR_ACTIVE))
        connect_json_btn.clicked.connect(self._auth_via_json)
        fb_l.addWidget(self.json_path_edit)
        fb_l.addWidget(browse_btn)
        fb_l.addWidget(connect_json_btn)

        row_json = SettingRow(
            title=tr("gdrive_json_title"),
            description=tr("gdrive_json_desc"),
            link_text=tr("gdrive_json_link"),
            action_widget=file_box
        )
        card_l.addWidget(row_json)

        # Opción 2: Claves manuales
        keys_box = QWidget()
        kb_l = QVBoxLayout(keys_box)
        kb_l.setContentsMargins(0, 0, 0, 0)
        kb_l.setSpacing(6)
        self.client_id_edit = QLineEdit()
        self.client_id_edit.setPlaceholderText("Client ID")
        self.client_id_edit.setFixedWidth(290)
        self.client_id_edit.setText(self.config_manager.google_drive.client_id)
        self.client_secret_edit = QLineEdit()
        self.client_secret_edit.setPlaceholderText("Client Secret")
        self.client_secret_edit.setEchoMode(QLineEdit.Password)
        self.client_secret_edit.setFixedWidth(290)
        self.client_secret_edit.setText(self.config_manager.google_drive.client_secret)
        btn_keys = QPushButton(tr("gdrive_keys_btn"))
        btn_keys.setIcon(get_icon("shield", 14, ICON_COLOR))
        btn_keys.clicked.connect(self._auth_via_keys)
        kb_l.addWidget(self.client_id_edit)
        kb_l.addWidget(self.client_secret_edit)
        kb_l.addWidget(btn_keys)

        row_keys = SettingRow(
            title=tr("gdrive_keys_title"),
            description=tr("gdrive_keys_desc"),
            action_widget=keys_box
        )
        card_l.addWidget(row_keys)

        self.content_layout.addWidget(card)

        # Guía paso a paso en tarjeta limpia
        guide_card = QFrame()
        guide_card.setObjectName("obsidianCard")
        g_layout = QVBoxLayout(guide_card)
        g_layout.setContentsMargins(18, 16, 18, 16)
        g_layout.setSpacing(8)

        g_head = QHBoxLayout()
        g_icon = QLabel()
        g_icon.setPixmap(get_icon("globe", 16, "#e2a01b").pixmap(16, 16))
        g_title = QLabel(tr("gdrive_guide_title"))
        g_title.setObjectName("accentLabel")
        g_head.addWidget(g_icon)
        g_head.addWidget(g_title)
        g_head.addStretch()
        g_layout.addLayout(g_head)

        lbl_guide = QLabel(tr("gdrive_guide_steps"))
        lbl_guide.setOpenExternalLinks(True)
        lbl_guide.setWordWrap(True)
        lbl_guide.setObjectName("settingDesc")
        lbl_guide.setTextFormat(Qt.RichText)
        g_layout.addWidget(lbl_guide)

        self.content_layout.addWidget(guide_card)

    def _browse_credentials_file(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            tr("gdrive_browse_json_title"),
            "",
            tr("gdrive_json_filter")
        )
        if file_path:
            self.json_path_edit.setText(file_path)

    def _auth_via_json(self):
        path = self.json_path_edit.text().strip()
        if not path or not Path(path).exists():
            QMessageBox.warning(
                self, tr("gdrive_invalid_json_title"), tr("gdrive_invalid_json_msg")
            )
            return

        self._start_auth("file", file_path=path)

    def _auth_via_keys(self):
        cid = self.client_id_edit.text().strip()
        csec = self.client_secret_edit.text().strip()
        if not cid or not csec:
            QMessageBox.warning(
                self, tr("gdrive_missing_keys_title"), tr("gdrive_missing_keys_msg")
            )
            return

        self.config_manager.google_drive.client_id = cid
        self.config_manager.google_drive.client_secret = csec
        self.config_manager.save()
        self._start_auth("keys", client_id=cid, client_secret=csec)

    def _start_auth(self, mode: str, **kwargs):
        QMessageBox.information(
            self,
            tr("gdrive_auth_title"),
            tr("gdrive_auth_msg")
        )
        self.auth_worker = AuthWorker(mode, **kwargs)
        self.auth_worker.auth_success.connect(self._on_success)
        self.auth_worker.auth_failed.connect(self._on_failed)
        self.auth_worker.start()

    def _on_success(self, info: dict):
        email = info.get("email", "")
        self._storage_info_cache = None
        self.config_manager.google_drive.user_email = email
        self.config_manager.google_drive.authenticated = True
        self.config_manager.save()
        QMessageBox.information(
            self,
            tr("gdrive_auth_success_title"),
            tr("gdrive_auth_success_msg", email=email)
        )
        self.refresh_status_view()
        self.connection_changed.emit(True)

    def _on_failed(self, err: str):
        QMessageBox.critical(
            self,
            tr("gdrive_auth_error_title"),
            tr("gdrive_auth_error_msg", error=err)
        )

    def _disconnect(self):
        res = QMessageBox.question(
            self,
            tr("gdrive_disconnect_title"),
            tr("gdrive_disconnect_msg"),
            QMessageBox.Yes | QMessageBox.No
        )
        if res == QMessageBox.Yes:
            self.gdrive.disconnect()
            self._storage_info_cache = None
            self.config_manager.google_drive.authenticated = False
            self.config_manager.google_drive.user_email = ""
            self.config_manager.save()
            self.refresh_status_view()
            self.connection_changed.emit(False)

    def _update_folder_name(self):
        name = self.folder_name_edit.text().strip()
        if name:
            self.config_manager.google_drive.root_folder_name = name
            self.config_manager.save()
            QMessageBox.information(
                self, tr("gdrive_updated_title"), tr("gdrive_folder_saved")
            )
