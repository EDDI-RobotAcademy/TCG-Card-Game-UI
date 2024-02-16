import unittest

from app_window.entity.window import Window


class TestWindowClass(unittest.TestCase):

    def test_default_values(self):
        window = Window()
        self.assertEqual(window.get_title(), "")
        self.assertEqual(window.get_geometry(), "800x600")
        self.assertEqual(window.get_background_color(), "#FFFFFF")
        self.assertEqual(window.get_resizable(), (True, True))

    def test_set_values(self):
        window = Window("Custom Title", "1024x768", "#00FF00", (False, True))

        self.assertEqual(window.get_title(), "Custom Title")
        self.assertEqual(window.get_geometry(), "1024x768")
        self.assertEqual(window.get_background_color(), "#00FF00")
        self.assertEqual(window.get_resizable(), (False, True))

if __name__ == '__main__':
    unittest.main()
