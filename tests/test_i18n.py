import unittest

from syncdian.i18n import (
    TRANSLATIONS,
    available_languages,
    get_current_language,
    set_current_language,
    tr,
)


class TestI18n(unittest.TestCase):
    def tearDown(self):
        set_current_language("es")

    def test_spanish_and_english_have_the_same_keys(self):
        es = set(TRANSLATIONS["es"])
        en = set(TRANSLATIONS["en"])
        self.assertEqual(es - en, set())
        self.assertEqual(en - es, set())

    def test_switching_language_changes_text(self):
        set_current_language("es")
        self.assertEqual(tr("nav_about"), "Acerca De")
        set_current_language("en")
        self.assertEqual(tr("nav_about"), "About")
        self.assertEqual(get_current_language(), "en")

    def test_missing_english_key_falls_back_to_spanish(self):
        TRANSLATIONS["es"]["_test_only_key"] = "Solo español"
        try:
            set_current_language("en")
            self.assertEqual(tr("_test_only_key"), "Solo español")
            self.assertEqual(tr("_clave_inexistente_"), "_clave_inexistente_")
        finally:
            del TRANSLATIONS["es"]["_test_only_key"]

    def test_format_parameters(self):
        set_current_language("en")
        self.assertIn("3", tr("vaults_autodetect_added_msg", count=3))

    def test_unknown_language_is_ignored(self):
        set_current_language("es")
        set_current_language("fr")
        self.assertEqual(get_current_language(), "es")

    def test_language_names_are_native(self):
        self.assertEqual(available_languages(), {"es": "Español", "en": "English"})


if __name__ == "__main__":
    unittest.main()
