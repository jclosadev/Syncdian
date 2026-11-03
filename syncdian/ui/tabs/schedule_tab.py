from PySide6.QtCore import Signal, QTime
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QFrame,
    QTimeEdit, QComboBox, QMessageBox
)

from syncdian.config import get_config
from syncdian.constants import SCHEDULE_DAILY, SCHEDULE_INTERVAL
from syncdian.i18n import tr
from syncdian.ui.icons import get_icon, ICON_COLOR_ACTIVE
from syncdian.ui.widgets.setting_row import SettingRow
from syncdian.ui.widgets.toggle_switch import ToggleSwitch


class ScheduleTab(QWidget):
    schedule_updated = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.config_manager = get_config()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(28, 24, 28, 24)
        layout.setSpacing(16)

        # Contenedor estilo tarjeta de Obsidian
        card = QFrame()
        card.setObjectName("obsidianCard")
        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(8, 8, 8, 8)
        card_layout.setSpacing(0)

        # Fila 1: Toggle de programación
        self.toggle_enable = ToggleSwitch(checked=self.config_manager.schedule.enabled)
        self.toggle_enable.toggled.connect(self._on_toggle_enabled)
        self.row_enabled = SettingRow(
            title=tr("sched_auto_title"),
            description=tr("sched_auto_desc"),
            action_widget=self.toggle_enable
        )
        card_layout.addWidget(self.row_enabled)

        # Fila 2: Hora fija diaria (21:00)
        self.time_picker = QTimeEdit()
        self.time_picker.setDisplayFormat("HH:mm")
        try:
            parts = self.config_manager.schedule.daily_time.split(":")
            self.time_picker.setTime(QTime(int(parts[0]), int(parts[1])))
        except Exception:
            self.time_picker.setTime(QTime(21, 0))
        self.time_picker.setFixedWidth(110)
        self.row_time = SettingRow(
            title=tr("sched_time_title"),
            description=tr("sched_time_desc"),
            link_text=tr("sched_time_link"),
            action_widget=self.time_picker
        )
        card_layout.addWidget(self.row_time)

        # Fila 3: Modo de frecuencia
        self.freq_combo = QComboBox()
        self.freq_combo.addItem(tr("sched_freq_daily"), SCHEDULE_DAILY)
        for hours in (2, 4, 6, 12, 24):
            self.freq_combo.addItem(tr("sched_freq_hours", h=hours), hours)
        self.freq_combo.setFixedWidth(240)

        if self.config_manager.schedule.mode == SCHEDULE_INTERVAL:
            idx = self.freq_combo.findData(self.config_manager.schedule.interval_hours)
            if idx >= 0:
                self.freq_combo.setCurrentIndex(idx)
        else:
            self.freq_combo.setCurrentIndex(0)

        self.row_freq = SettingRow(
            title=tr("sched_freq_title"),
            description=tr("sched_freq_desc"),
            action_widget=self.freq_combo
        )
        card_layout.addWidget(self.row_freq)

        # Fila 4: Ejecutar al inicio
        self.toggle_startup_sync = ToggleSwitch(checked=self.config_manager.schedule.run_on_startup)
        self.row_startup = SettingRow(
            title=tr("sched_startup_title"),
            description=tr("sched_startup_desc"),
            action_widget=self.toggle_startup_sync
        )
        card_layout.addWidget(self.row_startup)

        layout.addWidget(card)
        layout.addStretch()

        # Botón Guardar
        btn_box = QHBoxLayout()
        btn_box.addStretch()
        self.save_btn = QPushButton(tr("sched_save_btn"))
        self.save_btn.setObjectName("primaryButton")
        self.save_btn.setIcon(get_icon("save", 15, ICON_COLOR_ACTIVE))
        self.save_btn.clicked.connect(self._save_schedule)
        btn_box.addWidget(self.save_btn)
        layout.addLayout(btn_box)

        self._on_toggle_enabled(self.toggle_enable.isChecked())

    def retranslate(self):
        self.row_enabled.set_texts(
            title=tr("sched_auto_title"),
            description=tr("sched_auto_desc"),
        )
        self.row_time.set_texts(
            title=tr("sched_time_title"),
            description=tr("sched_time_desc"),
            link_text=tr("sched_time_link"),
        )
        self.row_freq.set_texts(
            title=tr("sched_freq_title"),
            description=tr("sched_freq_desc"),
        )
        self.row_startup.set_texts(
            title=tr("sched_startup_title"),
            description=tr("sched_startup_desc"),
        )
        self.save_btn.setText(tr("sched_save_btn"))

        # Actualizar las opciones del desplegable conservando la selección
        self.freq_combo.blockSignals(True)
        for i in range(self.freq_combo.count()):
            data = self.freq_combo.itemData(i)
            if data == SCHEDULE_DAILY:
                self.freq_combo.setItemText(i, tr("sched_freq_daily"))
            else:
                self.freq_combo.setItemText(i, tr("sched_freq_hours", h=data))
        self.freq_combo.blockSignals(False)

    def _on_toggle_enabled(self, enabled: bool):
        self.time_picker.setEnabled(enabled)
        self.freq_combo.setEnabled(enabled)
        self.toggle_startup_sync.setEnabled(enabled)

    def _save_schedule(self):
        sched = self.config_manager.schedule
        sched.enabled = self.toggle_enable.isChecked()

        selected_data = self.freq_combo.currentData()
        if selected_data == SCHEDULE_DAILY:
            sched.mode = SCHEDULE_DAILY
        else:
            sched.mode = SCHEDULE_INTERVAL
            sched.interval_hours = int(selected_data)

        sched.daily_time = self.time_picker.time().toString("HH:mm")
        sched.run_on_startup = self.toggle_startup_sync.isChecked()

        self.config_manager.save()
        self.schedule_updated.emit()

        QMessageBox.information(
            self,
            tr("sched_saved_title"),
            tr("sched_saved_msg")
        )
