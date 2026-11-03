from typing import Optional

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QWidget, QHBoxLayout, QVBoxLayout, QLabel, QFrame, QSizePolicy
)


class SettingRow(QFrame):
    """Fila de ajuste con título, descripción, enlace opcional y control a la derecha.

    El diseño imita las filas de preferencias de Obsidian: texto a la izquierda,
    control alineado a la derecha y un separador sutil en la parte inferior.
    """

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

        # Columna de texto (izquierda)
        text_layout = QVBoxLayout()
        text_layout.setSpacing(3)

        self.title_label = QLabel(title)
        self.title_label.setObjectName("settingTitle")
        self.title_label.setWordWrap(True)
        text_layout.addWidget(self.title_label)

        self.desc_label = QLabel(description)
        self.desc_label.setObjectName("settingDesc")
        self.desc_label.setWordWrap(True)
        self.desc_label.setVisible(bool(description))
        text_layout.addWidget(self.desc_label)

        self.link_label = QLabel(link_text)
        self.link_label.setObjectName("settingLink")
        self.link_label.setWordWrap(True)
        self.link_label.setOpenExternalLinks(True)
        self.link_label.setVisible(bool(link_text))
        text_layout.addWidget(self.link_label)
        text_layout.addStretch(1)

        row_content.addLayout(text_layout, stretch=1)

        # Control de acción (derecha)
        if action_widget:
            self.action_widget = action_widget
            self.action_widget.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
            row_content.addWidget(self.action_widget, 0, Qt.AlignRight | Qt.AlignVCenter)
        else:
            self.action_widget = None

        main_layout.addLayout(row_content)

    def set_texts(
        self,
        title: Optional[str] = None,
        description: Optional[str] = None,
        link_text: Optional[str] = None,
    ):
        """Actualiza los textos sin reconstruir la fila (cambio de idioma)."""
        if title is not None:
            self.title_label.setText(title)
        if description is not None:
            self.desc_label.setText(description)
            self.desc_label.setVisible(bool(description))
        if link_text is not None:
            self.link_label.setText(link_text)
            self.link_label.setVisible(bool(link_text))
