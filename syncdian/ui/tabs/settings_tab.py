from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QFrame, QListWidget, QLineEdit, QMessageBox
)

from syncdian.config import get_config
from syncdian.constants import DEFAULT_EXCLUSIONS
from syncdian.core.autostart import WindowsAutostart
from syncdian.ui.widgets.setting_row import SettingRow
from syncdian.ui.widgets.toggle_switch import ToggleSwitch


class SettingsTab(QWidget):
    settings_changed = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.config_manager = get_config()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 20, 24, 20)
        layout.setSpacing(16)

        # 1. Comportamiento en Windows (Tarjeta estilo Obsidian)
        card = QFrame()
        card.setObjectName("obsidianCard")
        card_l = QVBoxLayout(card)
        card_l.setContentsMargins(8, 8, 8, 8)
        card_l.setSpacing(0)

        # Autostart Windows (ToggleSwitch)
        self.toggle_autostart = ToggleSwitch(checked=WindowsAutostart.is_enabled())
        self.toggle_autostart.toggled.connect(self._toggle_autostart)
        row_autostart = SettingRow(
            title="Iniciar con Windows en Segundo Plano",
            description="Arranca Syncdian automáticamente y minimizado al encender el equipo.",
            action_widget=self.toggle_autostart
        )
        card_l.addWidget(row_autostart)

        # Minimizar a Tray (ToggleSwitch)
        self.toggle_tray = ToggleSwitch(checked=self.config_manager.settings.minimize_to_tray)
        self.toggle_tray.toggled.connect(self._save_settings)
        row_tray = SettingRow(
            title="Minimizar a la Bandeja del Sistema",
            description="Al pulsar la 'X' para cerrar la ventana, Syncdian se oculta en el área de notificación para seguir trabajando.",
            action_widget=self.toggle_tray
        )
        card_l.addWidget(row_tray)

        # Notificaciones (ToggleSwitch)
        self.toggle_notify = ToggleSwitch(checked=self.config_manager.settings.notify_on_sync)
        self.toggle_notify.toggled.connect(self._save_settings)
        row_notify = SettingRow(
            title="Notificaciones de Escritorio",
            description="Muestra avisos del sistema al completar o fallar una sincronización programada.",
            action_widget=self.toggle_notify
        )
        card_l.addWidget(row_notify)

        layout.addWidget(card)

        # 2. Exclusiones de Archivos
        excl_card = QFrame()
        excl_card.setObjectName("obsidianCard")
        excl_l = QVBoxLayout(excl_card)
        excl_l.setContentsMargins(16, 16, 16, 16)
        excl_l.setSpacing(12)

        excl_head = QHBoxLayout()
        excl_title = QLabel("Filtros de Exclusión")
        excl_title.setStyleSheet("font-size: 14px; font-weight: 600; color: #e6dcce;")
        excl_head.addWidget(excl_title)
        excl_head.addStretch()

        reset_btn = QPushButton("Restablecer")
        reset_btn.clicked.connect(self._reset_exclusions)
        excl_head.addWidget(reset_btn)
        excl_l.addLayout(excl_head)

        excl_desc = QLabel("Los archivos y carpetas que coincidan con estos patrones no se subirán a Google Drive:")
        excl_desc.setStyleSheet("color: #9c8e7e; font-size: 12px;")
        excl_l.addWidget(excl_desc)

        self.exclusions_list = QListWidget()
        self.exclusions_list.setStyleSheet("background-color: #17120e; border: 1px solid #29201a; border-radius: 6px; padding: 4px; color: #e6dcce;")
        self.exclusions_list.addItems(self.config_manager.settings.exclude_patterns)
        self.exclusions_list.setFixedHeight(120)
        excl_l.addWidget(self.exclusions_list)

        add_box = QHBoxLayout()
        self.new_pattern_edit = QLineEdit()
        self.new_pattern_edit.setPlaceholderText("Ej: .trash, *.tmp, .git")
        add_btn = QPushButton("Añadir")
        add_btn.clicked.connect(self._add_exclusion)
        del_btn = QPushButton("Eliminar")
        del_btn.setObjectName("dangerButton")
        del_btn.clicked.connect(self._remove_exclusion)

        add_box.addWidget(self.new_pattern_edit)
        add_box.addWidget(add_btn)
        add_box.addWidget(del_btn)
        excl_l.addLayout(add_box)

        layout.addWidget(excl_card)
        layout.addStretch()

    def _toggle_autostart(self, enabled: bool):
        success = WindowsAutostart.set_enabled(enabled)
        if not success:
            self.toggle_autostart.blockSignals(True)
            self.toggle_autostart.setChecked(not enabled)
            self.toggle_autostart.blockSignals(False)
            QMessageBox.warning(self, "Aviso", "No se pudo modificar el registro de inicio de Windows.")
        else:
            self.config_manager.settings.start_with_windows = enabled
            self.config_manager.save()

    def _save_settings(self):
        self.config_manager.settings.minimize_to_tray = self.toggle_tray.isChecked()
        self.config_manager.settings.notify_on_sync = self.toggle_notify.isChecked()
        self.config_manager.save()
        self.settings_changed.emit()

    def _add_exclusion(self):
        pat = self.new_pattern_edit.text().strip()
        if pat and pat not in self.config_manager.settings.exclude_patterns:
            self.config_manager.settings.exclude_patterns.append(pat)
            self.config_manager.save()
            self.exclusions_list.addItem(pat)
            self.new_pattern_edit.clear()

    def _remove_exclusion(self):
        row = self.exclusions_list.currentRow()
        if row >= 0:
            item = self.exclusions_list.takeItem(row)
            if item.text() in self.config_manager.settings.exclude_patterns:
                self.config_manager.settings.exclude_patterns.remove(item.text())
                self.config_manager.save()

    def _reset_exclusions(self):
        self.config_manager.settings.exclude_patterns = list(DEFAULT_EXCLUSIONS)
        self.config_manager.save()
        self.exclusions_list.clear()
        self.exclusions_list.addItems(self.config_manager.settings.exclude_patterns)
