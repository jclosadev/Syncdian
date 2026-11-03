import os
from pathlib import Path
from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QFrame, QComboBox, QMessageBox
)

from syncdian.config import get_config
from syncdian.constants import APP_VERSION
from syncdian.i18n import tr, set_current_language, get_current_language
from syncdian.ui.widgets.setting_row import SettingRow
from syncdian.ui.widgets.toggle_switch import ToggleSwitch


class AboutTab(QWidget):
    language_changed = Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.config_manager = get_config()
        self.init_ui()

    def init_ui(self):
        # Limpiar si ya había layout
        if self.layout():
            QWidget().setLayout(self.layout())

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(24, 20, 24, 20)
        main_layout.setSpacing(16)

        card = QFrame()
        card.setObjectName("obsidianCard")
        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(8, 8, 8, 8)
        card_layout.setSpacing(0)

        # Fila 1: Versión
        check_update_btn = QPushButton(tr("about_check_updates"))
        check_update_btn.clicked.connect(self._check_updates)
        row_version = SettingRow(
            title=tr("about_version_title", version=APP_VERSION),
            description=tr("about_version_desc"),
            link_text=tr("about_version_link"),
            action_widget=check_update_btn
        )
        card_layout.addWidget(row_version)

        # Fila 2: Bóveda detectada
        open_folder_btn = QPushButton(tr("about_open_folder"))
        open_folder_btn.clicked.connect(self._open_vault_folder)
        vault_path = self.config_manager.vaults[0].path if self.config_manager.vaults else "---"
        row_vault = SettingRow(
            title=tr("about_vault_title"),
            description=tr("about_vault_desc", path=vault_path),
            link_text=tr("about_vault_link"),
            action_widget=open_folder_btn
        )
        card_layout.addWidget(row_vault)

        # Fila 3: Comprobación automática
        toggle_updates = ToggleSwitch(checked=True)
        row_auto_updates = SettingRow(
            title=tr("about_startup_check_title"),
            description=tr("about_startup_check_desc"),
            action_widget=toggle_updates
        )
        card_layout.addWidget(row_auto_updates)

        # Fila 4: Selector de Idioma (Español / English)
        self.lang_combo = QComboBox()
        self.lang_combo.addItem("Español", "es")
        self.lang_combo.addItem("English", "en")
        self.lang_combo.setFixedWidth(130)

        current_lang = self.config_manager.settings.language or get_current_language()
        idx = 1 if current_lang == "en" else 0
        self.lang_combo.setCurrentIndex(idx)
        self.lang_combo.currentIndexChanged.connect(self._on_language_changed)

        row_lang = SettingRow(
            title=tr("about_lang_title"),
            description=tr("about_lang_desc"),
            link_text=tr("about_lang_link"),
            action_widget=self.lang_combo
        )
        card_layout.addWidget(row_lang)

        main_layout.addWidget(card)
        main_layout.addStretch()

    def _on_language_changed(self, index: int):
        lang_code = self.lang_combo.currentData()
        if lang_code:
            set_current_language(lang_code)
            self.config_manager.settings.language = lang_code
            self.config_manager.save()
            self.language_changed.emit(lang_code)

    def _check_updates(self):
        msg = f"Syncdian v{APP_VERSION} is up to date!" if get_current_language() == "en" else f"¡Syncdian v{APP_VERSION} está actualizado!\nTienes la versión más reciente instalada."
        title = "Updates" if get_current_language() == "en" else "Actualizaciones"
        QMessageBox.information(self, title, msg)

    def _open_vault_folder(self):
        if self.config_manager.vaults:
            p = self.config_manager.vaults[0].path
            if Path(p).exists():
                os.startfile(p)
            else:
                QMessageBox.warning(self, "Syncdian", f"Path {p} does not exist.")
        else:
            QMessageBox.information(self, "Syncdian", "No vaults configured.")
