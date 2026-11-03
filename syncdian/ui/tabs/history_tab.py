from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QTableWidget, QTableWidgetItem, QHeaderView, QTextEdit,
    QFileDialog, QMessageBox, QSplitter, QFrame
)

from syncdian.config import get_config
from syncdian.i18n import tr
from syncdian.ui.icons import get_icon, ICON_COLOR


class HistoryTab(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.config_manager = get_config()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(28, 24, 28, 24)
        layout.setSpacing(14)

        # Cabecera con acciones
        top_bar = QHBoxLayout()
        self.title_lbl = QLabel(tr("hist_title"))
        self.title_lbl.setObjectName("pageTitle")
        top_bar.addWidget(self.title_lbl)
        top_bar.addStretch()

        self.export_btn = QPushButton(tr("hist_export"))
        self.export_btn.setIcon(get_icon("download", 14, ICON_COLOR))
        self.export_btn.clicked.connect(self._export_logs)
        top_bar.addWidget(self.export_btn)

        self.clear_btn = QPushButton(tr("hist_clear"))
        self.clear_btn.setObjectName("dangerButton")
        self.clear_btn.setIcon(get_icon("trash", 14, "#e88c7c"))
        self.clear_btn.clicked.connect(self._clear_history)
        top_bar.addWidget(self.clear_btn)

        layout.addLayout(top_bar)

        splitter = QSplitter(Qt.Vertical)

        # 1. Tabla de historial
        table_card = QFrame()
        table_card.setObjectName("obsidianCard")
        tc_layout = QVBoxLayout(table_card)
        tc_layout.setContentsMargins(8, 8, 8, 8)

        self.history_table = QTableWidget()
        self.history_table.setColumnCount(6)
        self.history_table.setHorizontalHeaderLabels([
            tr("hist_col_date"), tr("hist_col_vault"), tr("hist_col_status"),
            tr("hist_col_files"), tr("hist_col_size"), tr("hist_col_details")
        ])
        self.history_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)
        self.history_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeToContents)
        self.history_table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeToContents)
        self.history_table.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeToContents)
        self.history_table.horizontalHeader().setSectionResizeMode(4, QHeaderView.ResizeToContents)
        self.history_table.horizontalHeader().setSectionResizeMode(5, QHeaderView.Stretch)
        self.history_table.verticalHeader().setVisible(False)
        self.history_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.history_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.history_table.setAlternatingRowColors(True)
        tc_layout.addWidget(self.history_table)
        splitter.addWidget(table_card)

        # 2. Consola de logs
        log_card = QFrame()
        log_card.setObjectName("obsidianCard")
        lc_layout = QVBoxLayout(log_card)
        lc_layout.setContentsMargins(8, 8, 8, 8)

        self.log_viewer = QTextEdit()
        self.log_viewer.setReadOnly(True)
        self.log_viewer.setStyleSheet(
            "background-color: #141210; border: none; border-radius: 6px;"
            "font-family: 'Cascadia Mono', 'Consolas', monospace; font-size: 12px;"
            "color: #9ad8b2; padding: 8px;"
        )
        lc_layout.addWidget(self.log_viewer)
        splitter.addWidget(log_card)

        splitter.setSizes([300, 190])
        layout.addWidget(splitter)

        self.refresh_history_table()

    def retranslate(self):
        self.title_lbl.setText(tr("hist_title"))
        self.export_btn.setText(tr("hist_export"))
        self.clear_btn.setText(tr("hist_clear"))
        self.history_table.setHorizontalHeaderLabels([
            tr("hist_col_date"), tr("hist_col_vault"), tr("hist_col_status"),
            tr("hist_col_files"), tr("hist_col_size"), tr("hist_col_details")
        ])
        self.refresh_history_table()

    def refresh_history_table(self):
        records = list(reversed(self.config_manager.history))
        self.history_table.setRowCount(len(records))

        for row, rec in enumerate(records):
            self.history_table.setItem(row, 0, QTableWidgetItem(rec.timestamp))
            self.history_table.setItem(row, 1, QTableWidgetItem(rec.vault_name))
            status_str = tr("status_success") if rec.status == "success" else tr("status_failed")
            self.history_table.setItem(row, 2, QTableWidgetItem(status_str))
            self.history_table.setItem(row, 3, QTableWidgetItem(str(rec.files_count)))
            size_mb = rec.size_bytes / (1024 * 1024)
            size_str = f"{size_mb:.2f} MB" if size_mb >= 0.1 else f"{rec.size_bytes / 1024:.1f} KB"
            self.history_table.setItem(row, 4, QTableWidgetItem(size_str))
            self.history_table.setItem(row, 5, QTableWidgetItem(rec.message))

    def append_log(self, text: str):
        self.log_viewer.append(text)
        sb = self.log_viewer.verticalScrollBar()
        sb.setValue(sb.maximum())

    def _clear_history(self):
        res = QMessageBox.question(
            self,
            tr("hist_clear_title"),
            tr("hist_clear_msg"),
            QMessageBox.Yes | QMessageBox.No
        )
        if res == QMessageBox.Yes:
            self.config_manager.history.clear()
            self.config_manager.save()
            self.refresh_history_table()

    def _export_logs(self):
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            tr("hist_export_title"),
            tr("hist_default_filename"),
            tr("hist_export_filter")
        )
        if file_path:
            try:
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(self.log_viewer.toPlainText())
                QMessageBox.information(
                    self, tr("hist_exported_title"), tr("hist_exported_msg")
                )
            except Exception as e:
                QMessageBox.critical(
                    self, tr("hist_export_error_title"),
                    tr("hist_export_error_msg", error=e)
                )
