import os
from pathlib import Path
from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QFrame, QFileDialog, QLineEdit, QSpinBox, QComboBox,
    QDialog, QMessageBox, QScrollArea
)

from syncdian.config import get_config, VaultConfig
from syncdian.constants import MODE_SNAPSHOT_ZIP, MODE_MIRROR_SYNC
from syncdian.core.vault_manager import VaultManager
from syncdian.ui.widgets.setting_row import SettingRow
from syncdian.ui.widgets.toggle_switch import ToggleSwitch


class VaultDialog(QDialog):
    def __init__(self, parent=None, vault: VaultConfig = None):
        super().__init__(parent)
        self.vault = vault
        self.setWindowTitle("Configurar Bóveda de Obsidian" if vault else "Añadir Nueva Bóveda")
        self.resize(520, 360)
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
        self.name_edit.setPlaceholderText("Ej: Mis Notas Personales")
        if self.vault:
            self.name_edit.setText(self.vault.name)
        card_l.addWidget(SettingRow("Nombre de la Bóveda", "Etiqueta identificativa", self.name_edit))

        # Ruta
        path_box = QWidget()
        pb_l = QHBoxLayout(path_box)
        pb_l.setContentsMargins(0, 0, 0, 0)
        self.path_edit = QLineEdit()
        self.path_edit.setPlaceholderText("C:\\Ruta\\A\\Tu\\Vault")
        if self.vault:
            self.path_edit.setText(self.vault.path)
        browse_btn = QPushButton("Examinar...")
        browse_btn.clicked.connect(self._browse_folder)
        pb_l.addWidget(self.path_edit)
        pb_l.addWidget(browse_btn)
        card_l.addWidget(SettingRow("Ruta de la Carpeta", "Ubicación local en tu disco", path_box))

        # Modo
        self.mode_combo = QComboBox()
        self.mode_combo.addItem("📦 Snapshots ZIP con versiones (Recomendado)", MODE_SNAPSHOT_ZIP)
        self.mode_combo.addItem("📂 Mirror de archivos directos", MODE_MIRROR_SYNC)
        if self.vault and self.vault.backup_mode == MODE_MIRROR_SYNC:
            self.mode_combo.setCurrentIndex(1)
        card_l.addWidget(SettingRow("Modo de Respaldo", "Estrategia de copia en Google Drive", self.mode_combo))

        # Retención
        self.retention_spin = QSpinBox()
        self.retention_spin.setRange(1, 100)
        self.retention_spin.setValue(self.vault.retention_count if self.vault else 10)
        card_l.addWidget(SettingRow("Copias a conservar", "Elimina automáticamente las copias más antiguas", self.retention_spin))

        # Activo
        self.toggle_active = ToggleSwitch(checked=self.vault.enabled if self.vault else True)
        card_l.addWidget(SettingRow("Activar Sincronización", "Habilita la copia para esta bóveda", self.toggle_active))

        layout.addWidget(card)

        # Botones
        btns = QHBoxLayout()
        btns.addStretch()
        cancel_btn = QPushButton("Cancelar")
        cancel_btn.clicked.connect(self.reject)
        save_btn = QPushButton("Guardar Bóveda")
        save_btn.setObjectName("primaryButton")
        save_btn.clicked.connect(self._save)
        btns.addWidget(cancel_btn)
        btns.addWidget(save_btn)
        layout.addLayout(btns)

    def _browse_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "Seleccionar Carpeta de Obsidian Vault")
        if folder:
            self.path_edit.setText(folder)
            if not self.name_edit.text():
                self.name_edit.setText(Path(folder).name)

    def _save(self):
        name = self.name_edit.text().strip()
        path = self.path_edit.text().strip()
        if not name:
            QMessageBox.warning(self, "Aviso", "Por favor ingresa un nombre para la bóveda.")
            return
        if not path or not Path(path).exists():
            QMessageBox.warning(self, "Aviso", "La ruta especificada no existe en tu equipo.")
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
        layout.setContentsMargins(24, 20, 24, 20)
        layout.setSpacing(16)

        # Acciones superiores estilo Obsidian
        top_card = QFrame()
        top_card.setObjectName("obsidianCard")
        top_l = QVBoxLayout(top_card)
        top_l.setContentsMargins(8, 8, 8, 8)
        top_l.setSpacing(0)

        auto_btn = QPushButton("🔍 Auto-detectar")
        auto_btn.clicked.connect(self._auto_detect_vaults)
        row_auto = SettingRow(
            title="Auto-detectar Bóvedas de Obsidian",
            description="Lee la configuración oficial de Obsidian en tu equipo e importa automáticamente tus bóvedas.",
            action_widget=auto_btn
        )
        top_l.addWidget(row_auto)

        add_btn = QPushButton("➕ Añadir Manualmente")
        add_btn.setObjectName("primaryButton")
        add_btn.clicked.connect(self._add_vault)
        row_add = SettingRow(
            title="Añadir Nueva Bóveda",
            description="Especifica manualmente una ruta local de notas para respaldarla en Google Drive.",
            action_widget=add_btn
        )
        top_l.addWidget(row_add)

        layout.addWidget(top_card)

        # Lista de vaults configuradas
        self.vaults_container_card = QFrame()
        self.vaults_container_card.setObjectName("obsidianCard")
        self.vaults_layout = QVBoxLayout(self.vaults_container_card)
        self.vaults_layout.setContentsMargins(8, 8, 8, 8)
        self.vaults_layout.setSpacing(0)

        layout.addWidget(self.vaults_container_card)
        layout.addStretch()

        self.refresh_vault_cards()

    def refresh_vault_cards(self):
        while self.vaults_layout.count() > 0:
            item = self.vaults_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        if not self.config_manager.vaults:
            empty_lbl = QLabel("No hay bóvedas configuradas aún.\nHaz clic en 'Auto-detectar' o 'Añadir Manualmente' para comenzar.")
            empty_lbl.setAlignment(Qt.AlignCenter)
            empty_lbl.setStyleSheet("color: #7d6e5f; font-size: 13px; padding: 30px;")
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

            edit_btn = QPushButton("Editar")
            edit_btn.clicked.connect(lambda _, v=vault: self._edit_vault(v))
            ra_layout.addWidget(edit_btn)

            del_btn = QPushButton("Eliminar")
            del_btn.setObjectName("dangerButton")
            del_btn.clicked.connect(lambda _, v=vault: self._delete_vault(v))
            ra_layout.addWidget(del_btn)

            desc = f"Ruta: {vault.path} • {vault.retention_count} versiones guardadas"
            row = SettingRow(
                title=f"📁 {vault.name}",
                description=desc,
                link_text=f"Modo: {'Snapshots ZIP' if vault.backup_mode == MODE_SNAPSHOT_ZIP else 'Mirror'}",
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
            "Confirmar eliminación",
            f"¿Deseas desvincular '{vault.name}' de Syncdian?\n(Tus notas y copias en Drive NO se eliminarán).",
            QMessageBox.Yes | QMessageBox.No
        )
        if res == QMessageBox.Yes:
            self.config_manager.remove_vault(vault.id)
            self.refresh_vault_cards()
            self.vaults_changed.emit()

    def _auto_detect_vaults(self):
        detected = VaultManager.detect_obsidian_vaults()
        if not detected:
            QMessageBox.information(self, "Auto-detección", "No se encontraron bóvedas registradas en Obsidian.")
            return

        added = 0
        existing_paths = {Path(v.path).resolve() for v in self.config_manager.vaults}
        for item in detected:
            p = Path(item["path"]).resolve()
            if p not in existing_paths:
                v = self.config_manager.add_vault(item["name"], str(p), MODE_SNAPSHOT_ZIP)
                existing_paths.add(p)
                added += 1

        self.refresh_vault_cards()
        self.vaults_changed.emit()
        if added > 0:
            QMessageBox.information(self, "Bóvedas Detectadas", f"Se han importado {added} bóveda(s) de Obsidian.")
        else:
            QMessageBox.information(self, "Auto-detección", "Todas tus bóvedas ya estaban agregadas.")
