import os
import unittest

os.environ["QT_QPA_PLATFORM"] = "offscreen"

from PySide6.QtWidgets import QApplication
from syncdian.ui.main_window import MainWindow
from syncdian.i18n import get_current_language, set_current_language


class TestUI(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = QApplication.instance()
        if cls.app is None:
            cls.app = QApplication([])

    def test_main_window_instantiation(self):
        window = MainWindow()
        self.assertIsNotNone(window)
        
        # 7 vistas en el stacked widget
        self.assertEqual(window.stacked_widget.count(), 7)
        self.assertEqual(len(window.nav_buttons), 7)

        # Probar cambio de pestaña
        window.select_tab(1)
        self.assertEqual(window.stacked_widget.currentIndex(), 1)

        # Probar búsqueda / filtro
        window._filter_nav_items("google")
        gdrive_btn = [btn for btn, idx, _, _ in window.nav_buttons if idx == 4][0]
        self.assertFalse(gdrive_btn.isHidden())

        # Probar cambio de idioma
        window._on_language_changed("en")
        self.assertEqual(get_current_language(), "en")
        window._on_language_changed("es")
        self.assertEqual(get_current_language(), "es")

        window.quit_application()


if __name__ == "__main__":
    unittest.main()
