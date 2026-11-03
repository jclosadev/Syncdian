"""
Tema visual de Syncdian inspirado en Obsidian 1.15.

- Tipografía del sistema con jerarquía clara (Inter / Segoe UI Variable).
- Paleta oscura cálida, acento ámbar y verdes suaves para estados.
- Controles redondeados, separadores discretos e iconos lineales estilo Flaticon.
"""

from syncdian.ui.icons import svg_file

_CHECK = svg_file("check", "#241a09", size=14, stroke_width=2.4)
_CHEVRON = svg_file("chevron_down", "#a29483", size=14, stroke_width=2.0)
_CHEVRON_UP = svg_file("chevron_up", "#a29483", size=9, stroke_width=2.0)
_CHEVRON_DOWN = svg_file("chevron_down", "#a29483", size=9, stroke_width=2.0)

_QSS = """
/* ============================================================
   Base
   ============================================================ */
QMainWindow, QDialog {
    background-color: #1e1b18;
}
QWidget {
    color: #ded4c7;
    font-family: "Inter", "Segoe UI Variable Text", "Segoe UI", "Noto Sans", Arial, sans-serif;
    font-size: 13px;
    outline: none;
}
QLabel {
    background: transparent;
}
QWidget#centralWidget {
    background-color: #1e1b18;
}

/* ============================================================
   Barra lateral
   ============================================================ */
QWidget#sidebarWidget {
    background-color: #1b1815;
    border-right: 1px solid #2b2520;
}
QWidget#navContainer, QWidget#brandBox {
    background: transparent;
}

/* Buscador */
QLineEdit#searchBar {
    background-color: #141210;
    border: 1px solid #2f2822;
    border-radius: 8px;
    padding: 7px 10px;
    color: #d8ccbe;
    selection-background-color: #e2a01b;
    selection-color: #241a09;
    min-height: 18px;
}
QLineEdit#searchBar:hover {
    border-color: #3c332b;
}
QLineEdit#searchBar:focus {
    border: 1px solid #a8791d;
    background-color: #171411;
}

/* Navegación */
QPushButton#navButton {
    background-color: transparent;
    border: 1px solid transparent;
    border-radius: 8px;
    padding: 0px 12px;
    text-align: left;
    color: #c8b9a8;
    font-size: 13px;
    font-weight: 500;
    min-height: 34px;
    max-height: 34px;
}
QPushButton#navButton:hover {
    background-color: #27221d;
    color: #f2e8db;
}
QPushButton#navButton:checked {
    background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                      stop:0 #e8ac2e, stop:1 #d9971b);
    color: #241a09;
    border: 1px solid #f0b63d;
    font-weight: 600;
}
QPushButton#navButton:checked:hover {
    background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                      stop:0 #f0b840, stop:1 #e0a022);
}
QPushButton#navButton:disabled {
    color: #6f6357;
}
QLabel#sidebarCategoryHeader {
    color: #9b8165;
    font-size: 10px;
    font-weight: 700;
    letter-spacing: 1.4px;
    padding: 12px 12px 5px 12px;
}
QLabel#navEmpty {
    color: #8a7258;
    padding: 14px 12px;
    font-size: 12px;
}

/* ============================================================
   Contenido
   ============================================================ */
QScrollArea#contentScrollArea {
    background-color: #211d19;
    border: none;
}
QScrollArea#contentScrollArea QWidget#qt_scrollarea_viewport {
    background-color: #211d19;
}
QStackedWidget#contentStack {
    background-color: #211d19;
    border: none;
}
QWidget#contentWidget {
    background-color: #211d19;
}
QFrame#obsidianCard {
    background-color: #24201c;
    border: 1px solid #2f2822;
    border-radius: 10px;
}
QFrame#settingRow {
    background-color: transparent;
    border: none;
    border-bottom: 1px solid #322a24;
}
QFrame#settingRow:hover {
    background-color: rgba(255, 255, 255, 0.014);
}
QLabel#pageTitle {
    font-size: 18px;
    font-weight: 600;
    color: #e7dccd;
}
QLabel#cardTitle {
    font-size: 14px;
    font-weight: 600;
    color: #e5dacb;
}
QLabel#settingTitle {
    font-size: 14px;
    font-weight: 600;
    color: #e0d5c7;
}
QLabel#settingDesc {
    font-size: 12px;
    color: #a29483;
}
QLabel#settingLink {
    font-size: 12px;
    color: #e06c58;
    font-weight: 500;
}
QLabel#emptyState {
    color: #8a7a69;
    font-size: 13px;
    padding: 30px;
}
QLabel#statusBadge {
    font-size: 12px;
    font-weight: 600;
    padding: 4px 10px;
    border-radius: 6px;
}
QLabel#statusBadgeOk {
    font-size: 12px;
    font-weight: 600;
    padding: 4px 10px;
    border-radius: 6px;
    color: #6ed39e;
    background-color: #18261f;
    border: 1px solid #264536;
}
QLabel#statusBadgeError {
    font-size: 12px;
    font-weight: 600;
    padding: 4px 10px;
    border-radius: 6px;
    color: #ef9d8d;
    background-color: #2a1b17;
    border: 1px solid #4a2a22;
}
QLabel#statusBadgeNeutral {
    font-size: 12px;
    font-weight: 600;
    padding: 4px 10px;
    border-radius: 6px;
    color: #d9c7a8;
    background-color: #2a231b;
    border: 1px solid #3d3327;
}
QLabel#selectorBadge {
    font-size: 12px;
    font-weight: 600;
    color: #f0b13a;
    background-color: #2a2115;
    border: 1px solid #48371d;
    border-radius: 6px;
    padding: 4px 10px;
}
QLabel#accentLabel {
    color: #e2a01b;
    font-weight: 600;
}

/* ============================================================
   Campos de entrada
   ============================================================ */
QLineEdit, QSpinBox, QDoubleSpinBox, QTimeEdit, QDateEdit, QComboBox,
QPlainTextEdit, QTextEdit {
    background-color: #191613;
    border: 1px solid #3a322a;
    border-radius: 7px;
    padding: 7px 10px;
    color: #e2d7c9;
    selection-background-color: #e2a01b;
    selection-color: #241a09;
    min-height: 18px;
}
QLineEdit:hover, QSpinBox:hover, QDoubleSpinBox:hover, QTimeEdit:hover,
QDateEdit:hover, QComboBox:hover, QPlainTextEdit:hover, QTextEdit:hover {
    border-color: #4b4036;
}
QLineEdit:focus, QSpinBox:focus, QDoubleSpinBox:focus, QTimeEdit:focus,
QDateEdit:focus, QComboBox:focus, QPlainTextEdit:focus, QTextEdit:focus {
    border: 1px solid #a8791d;
    background-color: #1d1915;
}
QLineEdit:disabled, QSpinBox:disabled, QTimeEdit:disabled, QComboBox:disabled {
    color: #7e7164;
    background-color: #171411;
    border-color: #2c2620;
}
QSpinBox::up-button, QSpinBox::down-button,
QTimeEdit::up-button, QTimeEdit::down-button {
    background-color: transparent;
    border: none;
    width: 16px;
}
QSpinBox::up-button:hover, QSpinBox::down-button:hover,
QTimeEdit::up-button:hover, QTimeEdit::down-button:hover {
    background-color: #2a241e;
    border-radius: 3px;
}
QSpinBox::up-arrow, QTimeEdit::up-arrow {
    image: url("__CHEVRON_UP__");
    width: 8px;
    height: 8px;
}
QSpinBox::down-arrow, QTimeEdit::down-arrow {
    image: url("__CHEVRON_DOWN__");
    width: 8px;
    height: 8px;
}

/* ============================================================
   Desplegables
   ============================================================ */
QComboBox {
    padding-right: 28px;
}
QComboBox::drop-down {
    border: none;
    width: 28px;
}
QComboBox::down-arrow {
    image: url("__CHEVRON__");
    width: 14px;
    height: 14px;
}
QComboBox QAbstractItemView {
    background-color: #26211c;
    border: 1px solid #443a30;
    selection-background-color: #e2a01b;
    selection-color: #241a09;
    color: #e2d7c9;
    border-radius: 7px;
    outline: none;
    padding: 4px;
}
QComboBox QAbstractItemView::item {
    padding: 6px 10px;
    border-radius: 5px;
    min-height: 20px;
}

/* ============================================================
   Botones
   ============================================================ */
QPushButton {
    background-color: #2e2822;
    color: #e2d7c9;
    border: 1px solid #443a30;
    border-radius: 7px;
    padding: 6px 14px;
    font-weight: 600;
    min-height: 20px;
}
QPushButton:hover {
    background-color: #39312a;
    border-color: #584a3c;
    color: #fff5e8;
}
QPushButton:pressed {
    background-color: #251f1a;
}
QPushButton:disabled {
    background-color: #241f1a;
    color: #796b5a;
    border-color: #332b24;
}
QPushButton#primaryButton {
    background-color: #dda01f;
    color: #241a09;
    border: 1px solid #efb43a;
    padding: 7px 16px;
    font-weight: 700;
}
QPushButton#primaryButton:hover {
    background-color: #ecb039;
    border-color: #f5c153;
    color: #1e1507;
}
QPushButton#primaryButton:pressed {
    background-color: #c98d14;
}
QPushButton#primaryButton:disabled {
    background-color: #4a3a1f;
    color: #9a8359;
    border-color: #5a4726;
}
QPushButton#dangerButton {
    background-color: transparent;
    color: #e88c7c;
    border: 1px solid #4d3029;
    padding: 6px 13px;
}
QPushButton#dangerButton:hover {
    background-color: #34221d;
    border-color: #704138;
    color: #ffc4b8;
}
QPushButton#flatButton {
    background-color: transparent;
    color: #b9aa99;
    border: 1px solid transparent;
    padding: 5px 9px;
}
QPushButton#flatButton:hover {
    background-color: #2c2620;
    color: #f1e6d8;
}

/* ============================================================
   Progreso y checks
   ============================================================ */
QProgressBar {
    background-color: #191613;
    border: 1px solid #3a322a;
    border-radius: 6px;
    text-align: center;
    color: #f1e6d8;
    font-weight: 600;
    min-height: 16px;
    max-height: 16px;
}
QProgressBar::chunk {
    background-color: #dda01f;
    border-radius: 5px;
}
QCheckBox {
    spacing: 9px;
    color: #ded4c7;
}
QCheckBox::indicator {
    width: 17px;
    height: 17px;
    border: 1px solid #6a5845;
    border-radius: 4px;
    background: #191613;
}
QCheckBox::indicator:hover {
    border-color: #bd8120;
}
QCheckBox::indicator:checked {
    background: #e2a01b;
    border-color: #efb43a;
    image: url("__CHECK__");
}

/* ============================================================
   Tablas y listas
   ============================================================ */
QTableWidget, QListWidget {
    background-color: #1b1815;
    alternate-background-color: #211d19;
    border: 1px solid #332c25;
    border-radius: 8px;
    gridline-color: #2b2520;
    color: #ded4c7;
    selection-background-color: #3a3025;
    selection-color: #fff1dc;
}
QTableWidget::item {
    padding: 6px 8px;
}
QTableWidget::item:selected {
    background-color: #3a3025;
}
QHeaderView::section {
    background-color: #211d19;
    color: #a99a89;
    padding: 9px 8px;
    border: none;
    border-bottom: 1px solid #332c25;
    font-weight: 600;
    font-size: 12px;
}
QListWidget::item {
    padding: 5px 6px;
    border-radius: 4px;
}
QListWidget::item:selected {
    background-color: #3a3025;
    color: #fff1dc;
}

/* ============================================================
   Scrollbars
   ============================================================ */
QScrollBar:vertical {
    border: none;
    background: transparent;
    width: 9px;
    margin: 2px;
}
QScrollBar::handle:vertical {
    background: #453a2f;
    min-height: 28px;
    border-radius: 4px;
}
QScrollBar::handle:vertical:hover {
    background: #6b5742;
}
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
    height: 0px;
}
QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
    background: transparent;
}
QScrollBar:horizontal {
    border: none;
    background: transparent;
    height: 9px;
    margin: 2px;
}
QScrollBar::handle:horizontal {
    background: #453a2f;
    min-width: 28px;
    border-radius: 4px;
}
QScrollBar::handle:horizontal:hover {
    background: #6b5742;
}
QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {
    width: 0px;
}

/* ============================================================
   Menús y tooltips
   ============================================================ */
QMenu {
    background-color: #26211c;
    border: 1px solid #443a30;
    border-radius: 8px;
    padding: 6px;
}
QMenu::item {
    padding: 7px 24px 7px 10px;
    color: #ded4c7;
    border-radius: 5px;
    margin: 1px 0;
}
QMenu::icon {
    padding-left: 8px;
}
QMenu::item:selected {
    background-color: #e2a01b;
    color: #241a09;
    font-weight: 600;
}
QMenu::separator {
    height: 1px;
    background: #443a30;
    margin: 5px 8px;
}
QToolTip {
    background-color: #2a241e;
    color: #f2e6d7;
    border: 1px solid #5a4938;
    padding: 5px 8px;
    border-radius: 6px;
}
QSplitter::handle {
    background-color: #2b2520;
    height: 2px;
}
"""

OBSIDIAN_THEME_QSS = (
    _QSS.replace("__CHECK__", _CHECK)
    .replace("__CHEVRON_UP__", _CHEVRON_UP)
    .replace("__CHEVRON_DOWN__", _CHEVRON_DOWN)
    .replace("__CHEVRON__", _CHEVRON)
)
DARK_THEME_QSS = OBSIDIAN_THEME_QSS
