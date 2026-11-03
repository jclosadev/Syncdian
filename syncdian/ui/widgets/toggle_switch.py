from PySide6.QtCore import Qt, QPropertyAnimation, QEasingCurve, Property
from PySide6.QtGui import QPainter, QColor, QPen
from PySide6.QtWidgets import QAbstractButton


class ToggleSwitch(QAbstractButton):
    """Interruptor deslizante con el mismo aspecto que Obsidian."""

    def __init__(self, parent=None, checked=False):
        super().__init__(parent)
        self.setCheckable(True)
        self.setCursor(Qt.PointingHandCursor)
        self.setFixedSize(48, 26)

        # Paleta cálida de Obsidian
        self._track_checked = QColor("#2e9e6e")
        self._track_unchecked = QColor("#352c24")
        self._track_checked_hover = QColor("#37ad7a")
        self._track_unchecked_hover = QColor("#41362c")
        self._knob_color = QColor("#f4ede2")
        self._border_color = QColor("#45382e")

        self._knob_position = 25.0 if checked else 3.0

        self._anim = QPropertyAnimation(self, b"knob_position", self)
        self._anim.setDuration(150)
        self._anim.setEasingCurve(QEasingCurve.InOutQuad)

        self.toggled.connect(self._on_toggled)
        self.setChecked(checked)

    def _on_toggled(self, is_checked: bool):
        self._anim.stop()
        self._anim.setStartValue(self._knob_position)
        self._anim.setEndValue(25.0 if is_checked else 3.0)
        self._anim.start()

    def get_knob_position(self) -> float:
        return self._knob_position

    def set_knob_position(self, pos: float):
        self._knob_position = pos
        self.update()

    knob_position = Property(float, get_knob_position, set_knob_position)

    def setChecked(self, checked: bool):
        super().setChecked(checked)
        self._knob_position = 25.0 if checked else 3.0
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # 1. Pista (track)
        if self.isChecked():
            track_color = self._track_checked_hover if self.underMouse() else self._track_checked
        else:
            track_color = self._track_unchecked_hover if self.underMouse() else self._track_unchecked

        painter.setBrush(track_color)
        painter.setPen(QPen(self._border_color, 1))
        painter.drawRoundedRect(1, 1, self.width() - 2, self.height() - 2, 12, 12)

        # 2. Botón deslizable (knob)
        painter.setBrush(self._knob_color)
        painter.setPen(Qt.NoPen)
        knob_size = 20.0
        painter.drawEllipse(int(self._knob_position), 3, int(knob_size), int(knob_size))
        painter.end()

    def enterEvent(self, event):
        self.update()
        super().enterEvent(event)

    def leaveEvent(self, event):
        self.update()
        super().leaveEvent(event)
