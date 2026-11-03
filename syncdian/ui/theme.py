"""
Tema cálido inspirado en la interfaz de ajustes de Obsidian.
Paleta oscura, acento ámbar, superficies discretas y controles consistentes.
"""
from syncdian.ui.icons import svg_file

_CHECK = svg_file("check", "#21180d")
_CHEVRON = svg_file("chevron-down", "#b09a80")

_QSS = """
QMainWindow, QDialog, QWidget {
    background-color: #29231e;
    color: #e7d8c5;
    font-family: "Segoe UI Variable", "Segoe UI", Arial, sans-serif;
    font-size: 13px;
    border: none;
    outline: none;
}
QLabel { background: transparent; }

/* ---------- Barra lateral ---------- */
QWidget#sidebarWidget {
    background-color: #241f1a;
    border-right: 1px solid #372e26;
}
QWidget#navContainer { background: transparent; }
QWidget#brandBox { background: transparent; }
QLabel#brandTitle {
    font-size: 16px;
    font-weight: 700;
    color: #f5e8d6;
    letter-spacing: 0.3px;
}
QLabel#brandSubtitle { font-size: 11px; color: #8d7960; }

QScrollArea#contentScrollArea, QStackedWidget#contentStack, QWidget#contentWidget {
    background-color: #29231e;
    border: none;
}
QFrame#obsidianCard {
    background-color: #302a24;
    border: 1px solid #40362c;
    border-radius: 12px;
}

/* Buscador */
QLineEdit#searchBar {
    background-color: #1d1814;
    border: 1px solid #382f27;
    border-radius: 10px;
    padding: 8px 10px;
    color: #eadbc8;
    selection-background-color: #e2a01b;
    selection-color: #21180d;
}
QLineEdit#searchBar:focus {
    border: 1px solid #bd8120;
    background-color: #211b16;
}

/* Navegación */
QFrame#navIndicator {
    background-color: rgba(226, 160, 27, 0.14);
    border: 1px solid rgba(226, 160, 27, 0.28);
    border-radius: 9px;
}
QFrame#navAccent { background-color: #e2a01b; border-radius: 1px; }
QPushButton#navButton {
    background-color: transparent;
    border: 1px solid transparent;
    border-radius: 9px;
    padding: 0px 12px;
    text-align: left;
    color: #b8a38b;
    font-size: 13px;
    font-weight: 500;
}
QPushButton#navButton:hover { background-color: rgba(255, 235, 205, 0.05); color: #f1e4d3; }
QPushButton#navButton:checked { background-color: transparent; color: #f6c254; font-weight: 650; }
QPushButton#navButton:checked:hover { background-color: transparent; color: #ffd57a; }
QLabel#sidebarCategoryHeader {
    color: #8a7258;
    font-size: 10px;
    font-weight: 700;
    letter-spacing: 1.6px;
    padding: 10px 12px 4px 12px;
}
QLabel#navEmpty { color: #8a7258; padding: 14px 12px; font-size: 12px; }

/* Tarjeta de estado */
QFrame#statusCard {
    background-color: #2d2620;
    border: 1px solid #3c3228;
    border-radius: 12px;
}
QLabel#statusTitle { font-size: 13px; font-weight: 650; color: #f0e2cf; }
QLabel#statusSub { font-size: 11px; color: #957f64; }
QProgressBar#miniProgress {
    background-color: #1d1814;
    border: none;
    border-radius: 2px;
    min-height: 4px;
    max-height: 4px;
}
QProgressBar#miniProgress::chunk { background-color: #e2a01b; border-radius: 2px; }

/* ---------- Campos ---------- */
QLineEdit, QSpinBox, QDoubleSpinBox, QTimeEdit, QDateEdit, QComboBox,
QPlainTextEdit, QTextEdit {
    background-color: #211c18;
    border: 1px solid #40362d;
    border-radius: 8px;
    padding: 8px 11px;
    color: #eadbc8;
    selection-background-color: #e2a01b;
    selection-color: #21180d;
}
QLineEdit:hover, QSpinBox:hover, QTimeEdit:hover, QComboBox:hover { border-color: #55453a; }
QLineEdit:focus, QSpinBox:focus, QDoubleSpinBox:focus, QTimeEdit:focus,
QDateEdit:focus, QComboBox:focus, QPlainTextEdit:focus, QTextEdit:focus {
    border: 1px solid #bd8120;
    background-color: #261f19;
}

/* ---------- Botones ---------- */
QPushButton {
    background-color: #332b24;
    color: #e5d5c1;
    border: 1px solid #493b2f;
    border-radius: 8px;
    padding: 8px 15px;
    font-weight: 600;
}
QPushButton:hover { background-color: #40352b; border-color: #5a4938; color: #fff5e8; }
QPushButton:pressed { background-color: #251e18; }
QPushButton:disabled { background-color: #2a241e; color: #796b5a; border-color: #393027; }
QPushButton#primaryButton {
    background-color: #e2a01b;
    color: #21180d;
    border: 1px solid #edac2b;
    padding: 9px 18px;
    font-weight: 700;
}
QPushButton#primaryButton:hover { background-color: #efb33b; border-color: #f3bd50; color: #1b1309; }
QPushButton#primaryButton:pressed { background-color: #c98914; }
QPushButton#primaryButton:disabled { background-color: #4a3a1f; color: #9a8359; border-color: #5a4726; }
QPushButton#dangerButton {
    background-color: #442522;
    color: #f2b4a9;
    border: 1px solid #65362f;
    padding: 7px 13px;
}
QPushButton#dangerButton:hover { background-color: #57302a; color: #ffe2dc; }

/* ---------- Desplegables ---------- */
QComboBox { padding-right: 26px; }
QComboBox::drop-down { border: none; width: 26px; }
QComboBox::down-arrow { image: url(__CHEVRON__); width: 12px; height: 12px; }
QComboBox QAbstractItemView {
    background-color: #302a24;
    border: 1px solid #493b2f;
    selection-background-color: #e2a01b;
    selection-color: #21180d;
    color: #eadbc8;
    border-radius: 7px;
    outline: none;
    padding: 4px;
}

/* ---------- Scrollbars ---------- */
QScrollBar:vertical { border: none; background: transparent; width: 9px; margin: 2px; }
QScrollBar::handle:vertical { background: #4a3d31; min-height: 28px; border-radius: 4px; }
QScrollBar::handle:vertical:hover { background: #705a43; }
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical { height: 0px; }
QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical { background: transparent; }
QScrollBar:horizontal { border: none; background: transparent; height: 9px; margin: 2px; }
QScrollBar::handle:horizontal { background: #4a3d31; min-width: 28px; border-radius: 4px; }
QScrollBar::handle:horizontal:hover { background: #705a43; }
QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal { width: 0px; }

/* ---------- Tablas ---------- */
QTableWidget {
    background-color: #211c18;
    alternate-background-color: #27211c;
    border: 1px solid #40362d;
    border-radius: 10px;
    gridline-color: #342b23;
    color: #e7d8c5;
    selection-background-color: #493a29;
    selection-color: #fff0d9;
}
QTableWidget::item { padding: 6px 8px; }
QHeaderView::section {
    background-color: #26201b;
    color: #ad9678;
    padding: 10px 9px;
    border: none;
    border-bottom: 1px solid #40362d;
    font-weight: 650;
    font-size: 12px;
}

/* ---------- Progreso y checks ---------- */
QProgressBar {
    background-color: #211c18;
    border: 1px solid #40362d;
    border-radius: 8px;
    text-align: center;
    color: #f5e8d8;
    font-weight: 650;
    min-height: 18px;
}
QProgressBar::chunk { background-color: #e2a01b; border-radius: 7px; }
QCheckBox { spacing: 9px; color: #dfd0bd; }
QCheckBox::indicator {
    width: 17px;
    height: 17px;
    border: 1px solid #6a5845;
    border-radius: 5px;
    background: #211c18;
}
QCheckBox::indicator:hover { border-color: #bd8120; }
QCheckBox::indicator:checked {
    background: #e2a01b;
    border-color: #edac2b;
    image: url(__CHECK__);
}

/* ---------- Menús y tooltips ---------- */
QMenu {
    background-color: #302a24;
    border: 1px solid #493b2f;
    border-radius: 10px;
    padding: 6px;
}
QMenu::item { padding: 8px 22px 8px 10px; color: #e7d8c5; border-radius: 6px; margin: 1px 0; }
QMenu::icon { padding-left: 8px; }
QMenu::item:selected { background-color: #e2a01b; color: #21180d; font-weight: 700; }
QMenu::separator { height: 1px; background: #493b2f; margin: 5px 8px; }
QToolTip {
    background-color: #302a24;
    color: #f2e4d2;
    border: 1px solid #5a4938;
    padding: 5px 8px;
    border-radius: 6px;
}
"""

OBSIDIAN_THEME_QSS = _QSS.replace("__CHECK__", _CHECK).replace("__CHEVRON__", _CHEVRON)
DARK_THEME_QSS = OBSIDIAN_THEME_QSS
