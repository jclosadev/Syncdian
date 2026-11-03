from pathlib import Path

from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QFrame, QFileDialog, QLineEdit, QSpinBox, QComboBox,
    QDialog, QMessageBox
)

from syncdian.config import get_config, VaultConfig
from syncdian.constants import MODE_SNAPSHOT_ZIP, MODE_MIRROR_SYNC
from syncdian.core.vault_manager import VaultManager
from syncdian.i18n import tr
from syncdian.ui.icons import get_icon, ICON_COLOR, ICON_COLOR_ACTIVE
from syncdian.ui.widgets.setting_row import SettingRow
from syncdian.ui.widgets.toggle_switch import ToggleSwitch


class VaultDialog(QDialog):
    def __init__(self, parent=None, vault: VaultConfig = None):
        super().__init__(parent)
        self.vault = vault
        self.setWindowTitle(tr("dlg_edit_vault") if vault else tr("dlg_add_vault"))
        self.resize(560, 400)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 20, 24, 20)
        layout.setSpacing(14)

        card = QFrame()
        card.setObjectName("obsidianCard")
        card_l = QVBoxLayout(card)
        card_l.setContentsMargins(8, 8, 8, 8)
        card_l.setSpacing(0)

        # Nombre
        self.name_edit = QLineEdit()
        self.name_edit.setPlaceholderText(tr("dlg_name_placeholder"))
        if self.vault:
            self.name_edit.setText(self.vault.name)
        card_l.addWidget(SettingRow(
            tr("dlg_vault_name"), tr("dlg_name_hint"), self.name_edit
        ))

        # Ruta
        path_box = QWidget()
        pb_l = QHBoxLayout(path_box)
        pb_l.setContentsMargins(0, 0, 0, 0)
        pb_l.setSpacing(8)
        self.path_edit = QLineEdit()
        self.path_edit.setPlaceholderText(tr("dlg_path_placeholder"))
        if self.vault:
            self.path_edit.setText(self.vault.path)
        browse_btn = QPushButton(tr("dlg_browse"))
        browse_btn.setIcon(get_icon("folder_open", 15, ICON_COLOR))
        browse_btn.clicked.connect(self._browse_folder)
        pb_l.addWidget(self.path_edit)
        pb_l.addWidget(browse_btn)
        card_l.addWidget(SettingRow(
            tr("dlg_vault_path"), tr("dlg_path_hint"), path_box
        ))

        # Modo
        self.mode_combo = QComboBox()
        self.mode_combo.addItem(tr("dlg_mode_zip_option"), MODE_SNAPSHOT_ZIP)
        self.mode_combo.addItem(tr("dlg_mode_mirror_option"), MODE_MIRROR_SYNC)
        if self.vault and self.vault.backup_mode == MODE_MIRROR_SYNC:
            self.mode_combo.setCurrentIndex(1)
        card_l.addWidget(SettingRow(
            tr("dlg_backup_mode"), tr("dlg_mode_hint"), self.mode_combo
        ))

        # Retención
        self.retention_spin = QSpinBox()
        self.retention_spin.setRange(1, 100)
        self.retention_spin.setValue(self.vault.retention_count if self.vault else 10)
        self.retention_spin.setEnabled(self.mode_combo.currentData() == MODE_SNAPSHOT_ZIP)
        self.mode_combo.currentIndexChanged.connect(
            lambda: self.retention_spin.setEnabled(
                self.mode_combo.currentData() == MODE_SNAPSHOT_ZIP
            )
        )
        card_l.addWidget(SettingRow(
            tr("dlg_retention"), tr("dlg_retention_hint"), self.retention_spin
        ))

        # Activo
        self.toggle_active = ToggleSwitch(checked=self.vault.enabled if self.vault else True)
        card_l.addWidget(SettingRow(
            tr("dlg_active"), tr("dlg_active_hint"), self.toggle_active
        ))

        layout.addWidget(card)

        # Botones
        btns = QHBoxLayout()
        btns.addStretch()
        cancel_btn = QPushButton(tr("dlg_cancel"))
        cancel_btn.clicked.connect(self.reject)
        save_btn = QPushButton(tr("dlg_save"))
        save_btn.setObjectName("primaryButton")
        save_btn.setIcon(get_icon("save", 15, ICON_COLOR_ACTIVE))
        save_btn.clicked.connect(self._save)
        btns.addWidget(cancel_btn)
        btns.addWidget(save_btn)
        layout.addLayout(btns)

    def _browse_folder(self):
        folder = QFileDialog.getExistingDirectory(self, tr("dlg_select_folder_title"))
        if folder:
            self.path_edit.setText(folder)
            if not self.name_edit.text():
                self.name_edit.setText(Path(folder).name)

    def _save(self):
        name = self.name_edit.text().strip()
        path = self.path_edit.text().strip()
        if not name:
            QMessageBox.warning(
                self, tr("dlg_name_required_title"), tr("dlg_name_required_msg")
            )
            return
        if not path or not Path(path).exists():
            QMessageBox.warning(
                self, tr("dlg_name_required_title"), tr("dlg_path_invalid_msg")
            )
            return

        self.accept()

    def get_data(self):
        return {
            "name": self.name_edit.text().strip(),
            "path": self.path_edit.text().strip(),
            "backup_mode": self.mode_combo.currentData(),
            "retention_count": self.retention_spin.value(),
            "enabled": self.toggle_active.isChecked()
        }


class VaultsTab(QWidget):
    vaults_changed = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.config_manager = get_config()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(28, 24, 28, 24)
        layout.setSpacing(16)

        # Acciones superiores estilo Obsidian
        top_card = QFrame()
        top_card.setObjectName("obsidianCard")
        top_l = QVBoxLayout(top_card)
        top_l.setContentsMargins(8, 8, 8, 8)
        top_l.setSpacing(0)

        self.auto_btn = QPushButton(tr("vaults_autodetect_btn"))
        self.auto_btn.setIcon(get_icon("search", 15, ICON_COLOR))
        self.auto_btn.clicked.connect(self._auto_detect_vaults)
        self.row_auto = SettingRow(
            title=tr("vaults_autodetect_title"),
            description=tr("vaults_autodetect_desc"),
            action_widget=self.auto_btn
        )
        top_l.addWidget(self.row_auto)

        self.add_btn = QPushButton(tr("vaults_add_btn"))
        self.add_btn.setObjectName("primaryButton")
        self.add_btn.setIcon(get_icon("plus", 15, ICON_COLOR_ACTIVE))
        self.add_btn.clicked.connect(self._add_vault)
        self.row_add = SettingRow(
            title=tr("vaults_add_title"),
            description=tr("vaults_add_desc"),
            action_widget=self.add_btn
        )
        top_l.addWidget(self.row_add)

        layout.addWidget(top_card)

        # Lista de bóvedas configuradas
        self.vaults_container_card = QFrame()
        self.vaults_container_card.setObjectName("obsidianCard")
        self.vaults_layout = QVBoxLayout(self.vaults_container_card)
        self.vaults_layout.setContentsMargins(8, 8, 8, 8)
        self.vaults_layout.setSpacing(0)

        layout.addWidget(self.vaults_container_card)
        layout.addStretch()

        self.refresh_vault_cards()

    def retranslate(self):
        self.row_auto.set_texts(
            title=tr("vaults_autodetect_title"),
            description=tr("vaults_autodetect_desc"),
        )
        self.auto_btn.setText(tr("vaults_autodetect_btn"))

        self.row_add.set_texts(
            title=tr("vaults_add_title"),
            description=tr("vaults_add_desc"),
        )
        self.add_btn.setText(tr("vaults_add_btn"))

        self.refresh_vault_cards()

    def _clear_vault_rows(self):
        while self.vaults_layout.count() > 0:
            item = self.vaults_layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.setParent(None)
                widget.deleteLater()

    def refresh_vault_cards(self):
        self._clear_vault_rows()

        if not self.config_manager.vaults:
            empty_lbl = QLabel(tr("vaults_empty"))
            empty_lbl.setObjectName("emptyState")
            empty_lbl.setAlignment(Qt.AlignCenter)
            self.vaults_layout.addWidget(empty_lbl)
            return

        for vault in self.config_manager.vaults:
            row_actions = QWidget()
            ra_layout = QHBoxLayout(row_actions)
            ra_layout.setContentsMargins(0, 0, 0, 0)
            ra_layout.setSpacing(8)

            chk = ToggleSwitch(checked=vault.enabled)
            chk.toggled.connect(lambda checked, v=vault: self._toggle_vault(v, checked))
            ra_layout.addWidget(chk)

            edit_btn = QPushButton(tr("vault_edit"))
            edit_btn.setIcon(get_icon("edit", 14, ICON_COLOR))
            edit_btn.clicked.connect(lambda _, v=vault: self._edit_vault(v))
            ra_layout.addWidget(edit_btn)

            del_btn = QPushButton(tr("vault_delete"))
            del_btn.setObjectName("dangerButton")
            del_btn.setIcon(get_icon("trash", 14, "#e88c7c"))
            del_btn.clicked.connect(lambda _, v=vault: self._delete_vault(v))
            ra_layout.addWidget(del_btn)

            mode_label = tr("vault_mode_zip") if vault.backup_mode == MODE_SNAPSHOT_ZIP else tr("vault_mode_mirror")
            description = tr("vault_path_prefix", path=vault.path)
            if vault.backup_mode == MODE_SNAPSHOT_ZIP:
                description += " • " + tr("vault_saved_versions", count=vault.retention_count)
            row = SettingRow(
                title=vault.name,
                description=description,
                link_text=tr("vault_mode_prefix", mode=mode_label),
                action_widget=row_actions
            )
            self.vaults_layout.addWidget(row)

    def _toggle_vault(self, vault: VaultConfig, enabled: bool):
        vault.enabled = enabled
        self.config_manager.update_vault(vault)
        self.vaults_changed.emit()

    def _add_vault(self):
        dlg = VaultDialog(self)
        if dlg.exec():
            data = dlg.get_data()
            v = self.config_manager.add_vault(
                name=data["name"],
                path=data["path"],
                backup_mode=data["backup_mode"]
            )
            v.retention_count = data["retention_count"]
            v.enabled = data["enabled"]
            self.config_manager.update_vault(v)
            self.refresh_vault_cards()
            self.vaults_changed.emit()

    def _edit_vault(self, vault: VaultConfig):
        dlg = VaultDialog(self, vault=vault)
        if dlg.exec():
            data = dlg.get_data()
            vault.name = data["name"]
            vault.path = data["path"]
            vault.backup_mode = data["backup_mode"]
            vault.retention_count = data["retention_count"]
            vault.enabled = data["enabled"]
            self.config_manager.update_vault(vault)
            self.refresh_vault_cards()
            self.vaults_changed.emit()

    def _delete_vault(self, vault: VaultConfig):
        res = QMessageBox.question(
            self,
            tr("dlg_delete_title"),
            tr("dlg_delete_msg", name=vault.name),
            QMessageBox.Yes | QMessageBox.No
        )
        if res == QMessageBox.Yes:
            self.config_manager.remove_vault(vault.id)
            self.refresh_vault_cards()
            self.vaults_changed.emit()

    def _auto_detect_vaults(self):
        detected = VaultManager.detect_obsidian_vaults()
        if not detected:
            QMessageBox.information(
                self,
                tr("vaults_autodetect_none_title"),
                tr("vaults_autodetect_none_msg")
            )
            return

        added = 0
        existing_paths = {Path(v.path).resolve() for v in self.config_manager.vaults}
        for item in detected:
            p = Path(item["path"]).resolve()
            if p not in existing_paths:
                self.config_manager.add_vault(item["name"], str(p), MODE_SNAPSHOT_ZIP)
                existing_paths.add(p)
                added += 1

        self.refresh_vault_cards()
        self.vaults_changed.emit()
        if added > 0:
            QMessageBox.information(
                self,
                tr("vaults_autodetect_added_title"),
                tr("vaults_autodetect_added_msg", count=added)
            )
        else:
            QMessageBox.information(
                self,
                tr("vaults_autodetect_none_title"),
                tr("vaults_autodetect_existing_msg")
            )
