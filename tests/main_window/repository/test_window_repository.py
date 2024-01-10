import unittest

from app_window.entity.window import Window
from app_window.repository.window_repository_impl import WindowRepositoryImpl


class TestWindowRepositoryClass(unittest.TestCase):

    def test_create_new_window(self):
        window_repository = WindowRepositoryImpl.getInstance()
        menu_name = "TestMenu"
        new_window = Window("TestMenu", "1024x768", "#00FF00", (True, True))

        window_repository.createNewWindow(menu_name, new_window)

        self.assertEqual(window_repository.getWindowFrameList().get(menu_name), new_window)


if __name__ == '__main__':
    unittest.main()
