from datetime import datetime

from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QProgressBar, QFrame, QTableWidget, QTableWidgetItem, QHeaderView
)

from syncdian.config import get_config
from syncdian.i18n import tr
from syncdian.ui.icons import get_icon, ICON_COLOR, ICON_COLOR_ACTIVE
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
        layout.setContentsMargins(28, 24, 28, 24)
        layout.setSpacing(16)

        # 1. CONTENEDOR PRINCIPAL ESTILO OBSIDIAN
        card = QFrame()
        card.setObjectName("obsidianCard")
        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(8, 8, 8, 8)
        card_layout.setSpacing(0)

        # Fila 1: Botón Sincronizar Ahora
        self.sync_now_btn = QPushButton(tr("dash_sync_btn"))
        self.sync_now_btn.setObjectName("primaryButton")
        self.sync_now_btn.setCursor(Qt.PointingHandCursor)
        self.sync_now_btn.setIcon(get_icon("sync", 15, ICON_COLOR_ACTIVE))
        self.sync_now_btn.clicked.connect(self.request_sync_now.emit)

        self.row_sync = SettingRow(
            title=tr("dash_sync_title"),
            description=tr("dash_sync_desc"),
            link_text=tr("dash_sync_link"),
            action_widget=self.sync_now_btn
        )
        card_layout.addWidget(self.row_sync)

        # Fila 2: Próxima copia
        self.next_run_lbl = QLabel(tr("loading"))
        self.next_run_lbl.setObjectName("selectorBadge")
        self.row_next = SettingRow(
            title=tr("dash_next_title"),
            description=tr("dash_next_desc"),
            action_widget=self.next_run_lbl
        )
        card_layout.addWidget(self.row_next)

        # Fila 3: Estado Google Drive
        self.drive_status_lbl = QLabel(tr("verifying"))
        self.drive_status_lbl.setObjectName("statusBadgeNeutral")
        self.row_drive = SettingRow(
            title=tr("dash_drive_title"),
            description=tr("dash_drive_desc"),
            action_widget=self.drive_status_lbl
        )
        card_layout.addWidget(self.row_drive)

        # Barra de progreso y estado
        self.progress_container = QWidget()
        p_layout = QVBoxLayout(self.progress_container)
        p_layout.setContentsMargins(18, 10, 18, 12)
        p_layout.setSpacing(6)

        self.status_detail_lbl = QLabel(tr("preparing"))
        self.status_detail_lbl.setObjectName("accentLabel")
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
        self.vaults_title_lbl = QLabel(tr("dash_vaults_title"))
        self.vaults_title_lbl.setObjectName("cardTitle")
        v_head.addWidget(self.vaults_title_lbl)
        v_head.addStretch()

        self.manage_btn = QPushButton(tr("dash_manage_vaults"))
        self.manage_btn.setIcon(get_icon("vaults", 15, ICON_COLOR))
        self.manage_btn.clicked.connect(lambda: self.open_tab_requested.emit(2))
        v_head.addWidget(self.manage_btn)
        v_layout.addLayout(v_head)

        self.vaults_table = QTableWidget()
        self.vaults_table.setColumnCount(4)
        self.vaults_table.setHorizontalHeaderLabels([
            tr("table_name"), tr("table_path"), tr("table_last_sync"), tr("table_status")
        ])
        self.vaults_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)
        self.vaults_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        self.vaults_table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeToContents)
        self.vaults_table.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeToContents)
        self.vaults_table.verticalHeader().setVisible(False)
        self.vaults_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.vaults_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.vaults_table.setAlternatingRowColors(True)
        self.vaults_table.setMinimumHeight(150)
        v_layout.addWidget(self.vaults_table)

        layout.addWidget(vaults_frame)
        layout.addStretch()

    def retranslate(self):
        self.row_sync.set_texts(
            title=tr("dash_sync_title"),
            description=tr("dash_sync_desc"),
            link_text=tr("dash_sync_link"),
        )
        self.row_next.set_texts(
            title=tr("dash_next_title"),
            description=tr("dash_next_desc"),
        )
        self.row_drive.set_texts(
            title=tr("dash_drive_title"),
            description=tr("dash_drive_desc"),
        )
        self.vaults_title_lbl.setText(tr("dash_vaults_title"))
        self.manage_btn.setText(tr("dash_manage_vaults"))
        self.vaults_table.setHorizontalHeaderLabels([
            tr("table_name"), tr("table_path"), tr("table_last_sync"), tr("table_status")
        ])
        if self.sync_now_btn.isEnabled():
            self.sync_now_btn.setText(tr("dash_sync_btn"))
        else:
            self.sync_now_btn.setText(tr("dash_syncing_btn"))
            self.status_detail_lbl.setText(tr("preparing"))

    def refresh_data(self, next_run_str: str, drive_connected: bool, drive_email: str = ""):
        self.next_run_lbl.setText(next_run_str or tr("dash_schedule_not_set"))

        if drive_connected:
            email_info = tr("dash_drive_email", email=drive_email) if drive_email else ""
            self.drive_status_lbl.setText(tr("dash_drive_connected") + email_info)
            self._set_badge(self.drive_status_lbl, "statusBadgeOk")
        else:
            self.drive_status_lbl.setText(tr("dash_drive_disconnected"))
            self._set_badge(self.drive_status_lbl, "statusBadgeError")

        self.vaults_table.setRowCount(len(self.config_manager.vaults))
        for row, vault in enumerate(self.config_manager.vaults):
            item_name = QTableWidgetItem(vault.name)
            self.vaults_table.setItem(row, 0, item_name)

            item_path = QTableWidgetItem(vault.path)
            self.vaults_table.setItem(row, 1, item_path)

            last_sync_text = tr("never")
            if vault.last_sync:
                try:
                    dt = datetime.fromisoformat(vault.last_sync)
                    last_sync_text = dt.strftime("%d/%m/%Y %H:%M")
                except Exception:
                    last_sync_text = vault.last_sync
            self.vaults_table.setItem(row, 2, QTableWidgetItem(last_sync_text))

            status_map = {
                "success": tr("status_success"),
                "failed": tr("status_failed"),
                "running": tr("status_running"),
                "never": tr("status_never"),
            }
            status_text = status_map.get(vault.last_status, vault.last_status)
            self.vaults_table.setItem(row, 3, QTableWidgetItem(status_text))

    @staticmethod
    def _set_badge(label: QLabel, object_name: str):
        if label.objectName() == object_name:
            return
        label.setObjectName(object_name)
        label.style().unpolish(label)
        label.style().polish(label)

    def set_sync_in_progress(self, in_progress: bool):
        self.sync_now_btn.setEnabled(not in_progress)
        self.progress_container.setVisible(in_progress)
        if in_progress:
            self.sync_now_btn.setText(tr("dash_syncing_btn"))
            self.status_detail_lbl.setText(tr("preparing"))
        else:
            self.sync_now_btn.setText(tr("dash_sync_btn"))
            self.progress_bar.setValue(0)

    def update_sync_progress(self, percent: float, message: str):
        self.progress_bar.setValue(int(percent))
        self.status_detail_lbl.setText(message)
