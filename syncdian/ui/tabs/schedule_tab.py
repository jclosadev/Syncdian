from PySide6.QtCore import Qt, Signal, QTime
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QFrame, QTimeEdit, QComboBox, QMessageBox
)

from syncdian.config import get_config
from syncdian.constants import SCHEDULE_DAILY, SCHEDULE_INTERVAL
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
        layout.setContentsMargins(24, 20, 24, 20)
        layout.setSpacing(16)

        # Contenedor estilo tarjeta de Obsidian
        card = QFrame()
        card.setObjectName("obsidianCard")
        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(8, 8, 8, 8)
        card_layout.setSpacing(0)

        # Fila 1: Toggle Switch de programación (Idéntico a la imagen)
        self.toggle_enable = ToggleSwitch(checked=self.config_manager.schedule.enabled)
        self.toggle_enable.toggled.connect(self._on_toggle_enabled)
        row_enabled = SettingRow(
            title="Sincronización Automática Programada",
            description="Si lo desactiva, el servicio en segundo plano pausará las copias recurrentes.",
            action_widget=self.toggle_enable
        )
        card_layout.addWidget(row_enabled)

        # Fila 2: Hora fija diaria (21:00)
        self.time_picker = QTimeEdit()
        self.time_picker.setDisplayFormat("HH:mm")
        try:
            parts = self.config_manager.schedule.daily_time.split(":")
            self.time_picker.setTime(QTime(int(parts[0]), int(parts[1])))
        except Exception:
            self.time_picker.setTime(QTime(21, 0))
        self.time_picker.setFixedWidth(110)
        row_time = SettingRow(
            title="Hora de Copia Diaria Recurrente",
            description="Hora programada en la que Syncdian empaquetará y subirá tus notas a Google Drive.",
            link_text="Por defecto configurado todos los días a las 21:00.",
            action_widget=self.time_picker
        )
        card_layout.addWidget(row_time)

        # Fila 3: Modo de frecuencia (ComboBox como el de Idioma en la imagen)
        self.freq_combo = QComboBox()
        self.freq_combo.addItem("Diaria (a la hora fija elegida)", SCHEDULE_DAILY)
        self.freq_combo.addItem("Repetir cada 2 horas", 2)
        self.freq_combo.addItem("Repetir cada 4 horas", 4)
        self.freq_combo.addItem("Repetir cada 6 horas", 6)
        self.freq_combo.addItem("Repetir cada 12 horas", 12)
        self.freq_combo.addItem("Repetir cada 24 horas", 24)
        self.freq_combo.setFixedWidth(230)

        if self.config_manager.schedule.mode == SCHEDULE_INTERVAL:
            idx = self.freq_combo.findData(self.config_manager.schedule.interval_hours)
            if idx >= 0:
                self.freq_combo.setCurrentIndex(idx)
        else:
            self.freq_combo.setCurrentIndex(0)

        row_freq = SettingRow(
            title="Frecuencia de Respaldo",
            description="Elige entre una copia diaria única o repetición a intervalos regulares.",
            action_widget=self.freq_combo
        )
        card_layout.addWidget(row_freq)

        # Fila 4: Ejecutar al inicio (Toggle Switch)
        self.toggle_startup_sync = ToggleSwitch(checked=self.config_manager.schedule.run_on_startup)
        row_startup = SettingRow(
            title="Copia Inmediata al Iniciar Syncdian",
            description="Realiza una verificación y respaldo al abrir el programa o arrancar Windows.",
            action_widget=self.toggle_startup_sync
        )
        card_layout.addWidget(row_startup)

        layout.addWidget(card)

        layout.addStretch()

        # Botón Guardar (Dorado/Ámbar Obsidian)
        btn_box = QHBoxLayout()
        btn_box.addStretch()
        save_btn = QPushButton("Guardar Programación")
        save_btn.setObjectName("primaryButton")
        save_btn.clicked.connect(self._save_schedule)
        btn_box.addWidget(save_btn)
        layout.addLayout(btn_box)

        self._on_toggle_enabled(self.toggle_enable.isChecked())

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
            "Programación Guardada",
            "La programación ha sido actualizada y aplicada al servicio en segundo plano."
        )
