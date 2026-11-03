from typing import Optional
from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QWidget, QHBoxLayout, QVBoxLayout, QLabel, QFrame, QSizePolicy
)


class SettingRow(QFrame):
    def __init__(
        self,
        title: str,
        description: str = "",
        action_widget: Optional[QWidget] = None,
        link_text: str = "",
        parent=None
    ):
        super().__init__(parent)
        self.setObjectName("settingRow")

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(18, 14, 18, 14)
        main_layout.setSpacing(0)

        row_content = QHBoxLayout()
        row_content.setSpacing(20)

        # Columna de texto (Izquierda)
        text_layout = QVBoxLayout()
        text_layout.setSpacing(4)

        self.title_label = QLabel(title)
        self.title_label.setObjectName("settingTitle")
        self.title_label.setStyleSheet("font-size: 14px; font-weight: 600; color: #ded3c5;")
        text_layout.addWidget(self.title_label)

        if description:
            self.desc_label = QLabel(description)
            self.desc_label.setObjectName("settingDesc")
            self.desc_label.setWordWrap(True)
            self.desc_label.setStyleSheet("font-size: 12px; color: #948473; line-height: 1.35;")
            text_layout.addWidget(self.desc_label)
        else:
            self.desc_label = None

        if link_text:
            self.link_label = QLabel(link_text)
            self.link_label.setObjectName("settingLink")
            self.link_label.setStyleSheet("font-size: 12px; color: #e06c58; font-weight: 500;")
            self.link_label.setOpenExternalLinks(True)
            text_layout.addWidget(self.link_label)
        else:
            self.link_label = None

        row_content.addLayout(text_layout, stretch=1)

        # Control de acción (Derecha)
        if action_widget:
            self.action_widget = action_widget
            self.action_widget.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
            row_content.addWidget(self.action_widget, 0, Qt.AlignRight | Qt.AlignVCenter)
        else:
            self.action_widget = None

        main_layout.addLayout(row_content)

        self.setStyleSheet("""
            QFrame#settingRow {
                background-color: transparent;
                border: none;
                border-bottom: 1px solid #2a2018;
            }
            QFrame#settingRow:hover {
                background-color: rgba(255, 255, 255, 0.012);
            }
        """)
