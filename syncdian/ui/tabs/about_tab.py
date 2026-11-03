from pathlib import Path

from PySide6.QtCore import Signal, QUrl
from PySide6.QtGui import QDesktopServices
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QPushButton, QFrame, QComboBox, QMessageBox
)

from syncdian.config import get_config
from syncdian.constants import APP_VERSION
from syncdian.i18n import tr, set_current_language, get_current_language, available_languages
from syncdian.ui.icons import get_icon, ICON_COLOR
from syncdian.ui.widgets.setting_row import SettingRow
from syncdian.ui.widgets.toggle_switch import ToggleSwitch


class AboutTab(QWidget):
    language_changed = Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.config_manager = get_config()
        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(28, 24, 28, 24)
        main_layout.setSpacing(16)

        card = QFrame()
        card.setObjectName("obsidianCard")
        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(8, 8, 8, 8)
        card_layout.setSpacing(0)

        # Fila 1: Versión
        self.check_update_btn = QPushButton(tr("about_check_updates"))
        self.check_update_btn.setIcon(get_icon("download", 15, ICON_COLOR))
        self.check_update_btn.clicked.connect(self._check_updates)
        self.row_version = SettingRow(
            title=tr("about_version_title", version=APP_VERSION),
            description=tr("about_version_desc"),
            link_text=tr("about_version_link"),
            action_widget=self.check_update_btn
        )
        card_layout.addWidget(self.row_version)

        # Fila 2: Bóveda detectada
        self.open_folder_btn = QPushButton(tr("about_open_folder"))
        self.open_folder_btn.setIcon(get_icon("folder_open", 15, ICON_COLOR))
        self.open_folder_btn.clicked.connect(self._open_vault_folder)
        vault_path = self.config_manager.vaults[0].path if self.config_manager.vaults else "---"
        self.row_vault = SettingRow(
            title=tr("about_vault_title"),
            description=tr("about_vault_desc", path=vault_path),
            link_text=tr("about_vault_link"),
            action_widget=self.open_folder_btn
        )
        card_layout.addWidget(self.row_vault)

        # Fila 3: Comprobación automática al iniciar
        self.toggle_startup_check = ToggleSwitch(
            checked=getattr(self.config_manager.settings, "startup_check", True)
        )
        self.toggle_startup_check.toggled.connect(self._on_startup_check_toggled)
        self.row_auto_updates = SettingRow(
            title=tr("about_startup_check_title"),
            description=tr("about_startup_check_desc"),
            action_widget=self.toggle_startup_check
        )
        card_layout.addWidget(self.row_auto_updates)

        # Fila 4: Selector de Idioma (Español / English)
        self.lang_combo = QComboBox()
        for code, native_name in available_languages().items():
            self.lang_combo.addItem(native_name, code)
        self.lang_combo.setFixedWidth(140)
        self.lang_combo.setIconSize(self.lang_combo.iconSize())
        self._sync_language_combo()
        self.lang_combo.currentIndexChanged.connect(self._on_language_changed)

        self.row_lang = SettingRow(
            title=tr("about_lang_title"),
            description=tr("about_lang_desc"),
            link_text=tr("about_lang_link"),
            action_widget=self.lang_combo
        )
        card_layout.addWidget(self.row_lang)

        main_layout.addWidget(card)
        main_layout.addStretch()

    def _sync_language_combo(self):
        current_lang = self.config_manager.settings.language or get_current_language()
        index = self.lang_combo.findData(current_lang)
        if index < 0:
            index = 0
        self.lang_combo.blockSignals(True)
        self.lang_combo.setCurrentIndex(index)
        self.lang_combo.blockSignals(False)

    def retranslate(self):
        self.row_version.set_texts(
            title=tr("about_version_title", version=APP_VERSION),
            description=tr("about_version_desc"),
            link_text=tr("about_version_link"),
        )
        self.check_update_btn.setText(tr("about_check_updates"))

        vault_path = self.config_manager.vaults[0].path if self.config_manager.vaults else "---"
        self.row_vault.set_texts(
            title=tr("about_vault_title"),
            description=tr("about_vault_desc", path=vault_path),
            link_text=tr("about_vault_link"),
        )
        self.open_folder_btn.setText(tr("about_open_folder"))

        self.row_auto_updates.set_texts(
            title=tr("about_startup_check_title"),
            description=tr("about_startup_check_desc"),
        )
        self.row_lang.set_texts(
            title=tr("about_lang_title"),
            description=tr("about_lang_desc"),
            link_text=tr("about_lang_link"),
        )

        # Los nombres de idioma se muestran siempre en su idioma nativo.
        self._sync_language_combo()

    def _on_startup_check_toggled(self, enabled: bool):
        self.config_manager.settings.startup_check = enabled
        self.config_manager.save()

    def _on_language_changed(self, index: int):
        lang_code = self.lang_combo.currentData()
        if lang_code and lang_code != get_current_language():
            set_current_language(lang_code)
            self.config_manager.settings.language = lang_code
            self.config_manager.save()
            self.language_changed.emit(lang_code)

    def _check_updates(self):
        QMessageBox.information(
            self,
            tr("about_up_to_date_title"),
            tr("about_up_to_date_msg", version=APP_VERSION)
        )

    def _open_vault_folder(self):
        if self.config_manager.vaults:
            path = self.config_manager.vaults[0].path
            if Path(path).exists():
                QDesktopServices.openUrl(QUrl.fromLocalFile(path))
            else:
                QMessageBox.warning(
                    self,
                    tr("about_path_not_exist_title"),
                    tr("about_path_not_exist_msg", path=path)
                )
        else:
            QMessageBox.information(
                self,
                tr("about_no_vaults_title"),
                tr("about_no_vaults_msg")
            )
