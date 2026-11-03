import os
from datetime import datetime
from pathlib import Path
from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QProgressBar, QFrame, QTableWidget, QTableWidgetItem, QHeaderView
)

from syncdian.config import get_config
from syncdian.constants import APP_DISPLAY_NAME
from syncdian.ui.widgets.setting_row import SettingRow


class DashboardTab(QWidget):
    request_sync_now = Signal()
    open_tab_requested = Signal(int)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.config_manager = get_config()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 20, 24, 20)
        layout.setSpacing(16)

        # 1. CONTENEDOR PRINCIPAL ESTILO OBSIDIAN
        card = QFrame()
        card.setObjectName("obsidianCard")
        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(8, 8, 8, 8)
        card_layout.setSpacing(0)

        # Fila 1: Botón Sincronizar Ahora
        self.sync_now_btn = QPushButton("Sincronizar Ahora")
        self.sync_now_btn.setObjectName("primaryButton")
        self.sync_now_btn.setCursor(Qt.PointingHandCursor)
        self.sync_now_btn.clicked.connect(self.request_sync_now.emit)

        row_sync = SettingRow(
            title="Copia y Sincronización Inmediata",
            description="Empaqueta tus bóvedas activas de Obsidian y sube los cambios a tu nube de Google Drive.",
            link_text="Ver detalles de la última copia de seguridad.",
            action_widget=self.sync_now_btn
        )
        card_layout.addWidget(row_sync)

        # Fila 2: Próxima copia
        self.next_run_lbl = QLabel("Cargando...")
        self.next_run_lbl.setStyleSheet("font-size: 13px; font-weight: bold; color: #df9b20; background: #261d16; padding: 5px 12px; border-radius: 6px; border: 1px solid #3d2d21;")
        row_next = SettingRow(
            title="Próxima Sincronización Automática",
            description="El servicio en segundo plano se ejecutará automáticamente a la hora prevista sin interrumpirte.",
            action_widget=self.next_run_lbl
        )
        card_layout.addWidget(row_next)

        # Fila 3: Estado Google Drive
        self.drive_status_lbl = QLabel("Verificando...")
        self.drive_status_lbl.setStyleSheet("font-size: 13px; font-weight: 600; padding: 5px 12px; border-radius: 6px;")
        row_drive = SettingRow(
            title="Estado de Google Drive",
            description="Almacenamiento seguro en tu nube personal con cifrado y control de versiones.",
            action_widget=self.drive_status_lbl
        )
        card_layout.addWidget(row_drive)

        # Barra de progreso y estado
        self.progress_container = QWidget()
        p_layout = QVBoxLayout(self.progress_container)
        p_layout.setContentsMargins(16, 10, 16, 12)
        p_layout.setSpacing(6)

        self.status_detail_lbl = QLabel("Preparando...")
        self.status_detail_lbl.setStyleSheet("color: #df9b20; font-weight: 500; font-size: 12px;")
        p_layout.addWidget(self.status_detail_lbl)

        self.progress_bar = QProgressBar()
        self.progress_bar.setValue(0)
        self.progress_bar.setTextVisible(True)
        p_layout.addWidget(self.progress_bar)

        self.progress_container.setVisible(False)
        card_layout.addWidget(self.progress_container)

        layout.addWidget(card)

        # 2. RESUMEN DE BÓVEDAS
        vaults_frame = QFrame()
        vaults_frame.setObjectName("obsidianCard")
        v_layout = QVBoxLayout(vaults_frame)
        v_layout.setContentsMargins(16, 16, 16, 16)
        v_layout.setSpacing(12)

        v_head = QHBoxLayout()
        v_title = QLabel("Bóvedas Vinculadas")
        v_title.setStyleSheet("font-size: 14px; font-weight: 600; color: #e6dcce;")
        v_head.addWidget(v_title)
        v_head.addStretch()

        manage_btn = QPushButton("Gestionar Bóvedas")
        manage_btn.clicked.connect(lambda: self.open_tab_requested.emit(1))
        v_head.addWidget(manage_btn)
        v_layout.addLayout(v_head)

        self.vaults_table = QTableWidget()
        self.vaults_table.setColumnCount(4)
        self.vaults_table.setHorizontalHeaderLabels(["Nombre", "Ruta Local", "Última Sincronización", "Estado"])
        self.vaults_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)
        self.vaults_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        self.vaults_table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeToContents)
        self.vaults_table.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeToContents)
        self.vaults_table.verticalHeader().setVisible(False)
        self.vaults_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.vaults_table.setSelectionBehavior(QTableWidget.SelectRows)
        v_layout.addWidget(self.vaults_table)

        layout.addWidget(vaults_frame)

    def refresh_data(self, next_run_str: str, drive_connected: bool, drive_email: str = ""):
        self.next_run_lbl.setText(f"⏰ {next_run_str}")

        if drive_connected:
            email_info = f" ({drive_email})" if drive_email else ""
            self.drive_status_lbl.setText(f"Conectado{email_info}")
            self.drive_status_lbl.setStyleSheet("font-size: 13px; font-weight: bold; color: #3ea86d; background: #1c271e; border: 1px solid #28442e; padding: 5px 12px; border-radius: 6px;")
        else:
            self.drive_status_lbl.setText("Desconectado")
            self.drive_status_lbl.setStyleSheet("font-size: 13px; font-weight: bold; color: #e06c58; background: #2b1c18; border: 1px solid #4a2820; padding: 5px 12px; border-radius: 6px;")

        self.vaults_table.setRowCount(len(self.config_manager.vaults))
        for row, vault in enumerate(self.config_manager.vaults):
            item_name = QTableWidgetItem(f"📁 {vault.name}")
            self.vaults_table.setItem(row, 0, item_name)

            item_path = QTableWidgetItem(vault.path)
            self.vaults_table.setItem(row, 1, item_path)

            last_sync_text = "Nunca"
            if vault.last_sync:
                try:
                    dt = datetime.fromisoformat(vault.last_sync)
                    last_sync_text = dt.strftime("%d/%m/%Y %H:%M")
                except Exception:
                    last_sync_text = vault.last_sync
            item_sync = QTableWidgetItem(last_sync_text)
            self.vaults_table.setItem(row, 2, item_sync)

            status_map = {
                "success": "Éxito",
                "failed": "Falló",
                "running": "En curso",
                "never": "Pendiente"
            }
            status_text = status_map.get(vault.last_status, vault.last_status)
            item_status = QTableWidgetItem(status_text)
            self.vaults_table.setItem(row, 3, item_status)

    def set_sync_in_progress(self, in_progress: bool):
        self.sync_now_btn.setEnabled(not in_progress)
        self.progress_container.setVisible(in_progress)
        if in_progress:
            self.sync_now_btn.setText("Sincronizando...")
        else:
            self.sync_now_btn.setText("Sincronizar Ahora")
            self.progress_bar.setValue(0)

    def update_sync_progress(self, percent: float, message: str):
        self.progress_bar.setValue(int(percent))
        self.status_detail_lbl.setText(message)
