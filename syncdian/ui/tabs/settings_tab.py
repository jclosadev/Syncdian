from PySide6.QtCore import Signal
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QFrame, QListWidget, QLineEdit, QMessageBox
)

from syncdian.config import get_config
from syncdian.constants import DEFAULT_EXCLUSIONS
from syncdian.core.autostart import WindowsAutostart
from syncdian.i18n import tr
from syncdian.ui.icons import get_icon, ICON_COLOR
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
        layout.setContentsMargins(28, 24, 28, 24)
        layout.setSpacing(16)

        # 1. Comportamiento en Windows (tarjeta estilo Obsidian)
        card = QFrame()
        card.setObjectName("obsidianCard")
        card_l = QVBoxLayout(card)
        card_l.setContentsMargins(8, 8, 8, 8)
        card_l.setSpacing(0)

        # Autostart Windows
        self.toggle_autostart = ToggleSwitch(checked=WindowsAutostart.is_enabled())
        self.toggle_autostart.toggled.connect(self._toggle_autostart)
        self.row_autostart = SettingRow(
            title=tr("set_win_autostart_title"),
            description=tr("set_win_autostart_desc"),
            action_widget=self.toggle_autostart
        )
        card_l.addWidget(self.row_autostart)

        # Minimizar a la bandeja
        self.toggle_tray = ToggleSwitch(checked=self.config_manager.settings.minimize_to_tray)
        self.toggle_tray.toggled.connect(self._save_settings)
        self.row_tray = SettingRow(
            title=tr("set_tray_title"),
            description=tr("set_tray_desc"),
            action_widget=self.toggle_tray
        )
        card_l.addWidget(self.row_tray)

        # Notificaciones
        self.toggle_notify = ToggleSwitch(checked=self.config_manager.settings.notify_on_sync)
        self.toggle_notify.toggled.connect(self._save_settings)
        self.row_notify = SettingRow(
            title=tr("set_notify_title"),
            description=tr("set_notify_desc"),
            action_widget=self.toggle_notify
        )
        card_l.addWidget(self.row_notify)

        layout.addWidget(card)

        # 2. Exclusiones de archivos
        excl_card = QFrame()
        excl_card.setObjectName("obsidianCard")
        excl_l = QVBoxLayout(excl_card)
        excl_l.setContentsMargins(18, 16, 18, 16)
        excl_l.setSpacing(12)

        excl_head = QHBoxLayout()
        self.excl_title_lbl = QLabel(tr("set_excl_title"))
        self.excl_title_lbl.setObjectName("cardTitle")
        excl_head.addWidget(self.excl_title_lbl)
        excl_head.addStretch()

        self.reset_btn = QPushButton(tr("set_excl_reset"))
        self.reset_btn.setIcon(get_icon("sync", 14, ICON_COLOR))
        self.reset_btn.clicked.connect(self._reset_exclusions)
        excl_head.addWidget(self.reset_btn)
        excl_l.addLayout(excl_head)

        self.excl_desc_lbl = QLabel(tr("set_excl_desc"))
        self.excl_desc_lbl.setObjectName("settingDesc")
        self.excl_desc_lbl.setWordWrap(True)
        excl_l.addWidget(self.excl_desc_lbl)

        self.exclusions_list = QListWidget()
        self.exclusions_list.addItems(self.config_manager.settings.exclude_patterns)
        self.exclusions_list.setFixedHeight(130)
        excl_l.addWidget(self.exclusions_list)

        add_box = QHBoxLayout()
        add_box.setSpacing(8)
        self.new_pattern_edit = QLineEdit()
        self.new_pattern_edit.setPlaceholderText(tr("set_excl_placeholder"))
        self.add_btn = QPushButton(tr("set_excl_add"))
        self.add_btn.setIcon(get_icon("plus", 14, ICON_COLOR))
        self.add_btn.clicked.connect(self._add_exclusion)
        self.del_btn = QPushButton(tr("set_excl_del"))
        self.del_btn.setObjectName("dangerButton")
        self.del_btn.setIcon(get_icon("trash", 14, "#e88c7c"))
        self.del_btn.clicked.connect(self._remove_exclusion)

        add_box.addWidget(self.new_pattern_edit)
        add_box.addWidget(self.add_btn)
        add_box.addWidget(self.del_btn)
        excl_l.addLayout(add_box)

        layout.addWidget(excl_card)
        layout.addStretch()

    def retranslate(self):
        self.row_autostart.set_texts(
            title=tr("set_win_autostart_title"),
            description=tr("set_win_autostart_desc"),
        )
        self.row_tray.set_texts(
            title=tr("set_tray_title"),
            description=tr("set_tray_desc"),
        )
        self.row_notify.set_texts(
            title=tr("set_notify_title"),
            description=tr("set_notify_desc"),
        )
        self.excl_title_lbl.setText(tr("set_excl_title"))
        self.excl_desc_lbl.setText(tr("set_excl_desc"))
        self.reset_btn.setText(tr("set_excl_reset"))
        self.add_btn.setText(tr("set_excl_add"))
        self.del_btn.setText(tr("set_excl_del"))
        self.new_pattern_edit.setPlaceholderText(tr("set_excl_placeholder"))

    def _toggle_autostart(self, enabled: bool):
        success = WindowsAutostart.set_enabled(enabled)
        if not success:
            self.toggle_autostart.blockSignals(True)
            self.toggle_autostart.setChecked(not enabled)
            self.toggle_autostart.blockSignals(False)
            QMessageBox.warning(
                self,
                tr("set_autostart_error_title"),
                tr("set_autostart_error_msg")
            )
        else:
            self.config_manager.settings.start_with_windows = enabled
            self.config_manager.save()

    def _save_settings(self):
        self.config_manager.settings.minimize_to_tray = self.toggle_tray.isChecked()
        self.config_manager.settings.notify_on_sync = self.toggle_notify.isChecked()
        self.config_manager.save()
        self.settings_changed.emit()

    def _add_exclusion(self):
        pattern = self.new_pattern_edit.text().strip()
        if pattern and pattern not in self.config_manager.settings.exclude_patterns:
            self.config_manager.settings.exclude_patterns.append(pattern)
            self.config_manager.save()
            self.exclusions_list.addItem(pattern)
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
