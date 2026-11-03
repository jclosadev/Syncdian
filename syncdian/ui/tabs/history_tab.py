import os
from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QTableWidget, QTableWidgetItem, QHeaderView, QTextEdit,
    QFileDialog, QMessageBox, QSplitter, QFrame
)

from syncdian.config import get_config


class HistoryTab(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.config_manager = get_config()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 20, 24, 20)
        layout.setSpacing(14)

        # Header con acciones
        top_bar = QHBoxLayout()
        title = QLabel("Historial de Respaldos y Consola")
        title.setStyleSheet("font-size: 15px; font-weight: 600; color: #e6dcce;")
        top_bar.addWidget(title)
        top_bar.addStretch()

        export_btn = QPushButton("Exportar Logs")
        export_btn.clicked.connect(self._export_logs)
        top_bar.addWidget(export_btn)

        clear_btn = QPushButton("Limpiar")
        clear_btn.setObjectName("dangerButton")
        clear_btn.clicked.connect(self._clear_history)
        top_bar.addWidget(clear_btn)

        layout.addLayout(top_bar)

        splitter = QSplitter(Qt.Vertical)

        # 1. Tabla de Historial
        table_card = QFrame()
        table_card.setObjectName("obsidianCard")
        tc_layout = QVBoxLayout(table_card)
        tc_layout.setContentsMargins(8, 8, 8, 8)

        self.history_table = QTableWidget()
        self.history_table.setColumnCount(6)
        self.history_table.setHorizontalHeaderLabels([
            "Fecha y Hora", "Bóveda", "Estado", "Archivos", "Tamaño", "Detalle"
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
        tc_layout.addWidget(self.history_table)
        splitter.addWidget(table_card)

        # 2. Consola de Logs
        log_card = QFrame()
        log_card.setObjectName("obsidianCard")
        lc_layout = QVBoxLayout(log_card)
        lc_layout.setContentsMargins(8, 8, 8, 8)

        self.log_viewer = QTextEdit()
        self.log_viewer.setReadOnly(True)
        self.log_viewer.setStyleSheet("background-color: #120e0b; border: none; font-family: 'Consolas', monospace; font-size: 12px; color: #3ea86d; padding: 6px;")
        lc_layout.addWidget(self.log_viewer)
        splitter.addWidget(log_card)

        splitter.setSizes([260, 180])
        layout.addWidget(splitter)

        self.refresh_history_table()

    def refresh_history_table(self):
        records = list(reversed(self.config_manager.history))
        self.history_table.setRowCount(len(records))

        for row, rec in enumerate(records):
            self.history_table.setItem(row, 0, QTableWidgetItem(rec.timestamp))
            self.history_table.setItem(row, 1, QTableWidgetItem(rec.vault_name))
            status_str = "🟢 Éxito" if rec.status == "success" else "🔴 Error"
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
        res = QMessageBox.question(self, "Limpiar Historial", "¿Seguro que deseas vaciar el historial?", QMessageBox.Yes | QMessageBox.No)
        if res == QMessageBox.Yes:
            self.config_manager.history.clear()
            self.config_manager.save()
            self.refresh_history_table()

    def _export_logs(self):
        file_path, _ = QFileDialog.getSaveFileName(self, "Guardar Logs", "syncdian_log.txt", "Archivos de texto (*.txt);;Todos los archivos (*.*)")
        if file_path:
            try:
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(self.log_viewer.toPlainText())
                QMessageBox.information(self, "Exportado", "Logs guardados correctamente.")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"No se pudo guardar: {e}")
