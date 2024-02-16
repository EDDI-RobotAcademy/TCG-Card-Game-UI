import unittest

from app_window.service.window_service_impl import WindowServiceImpl


class TestWindowServiceImpl(unittest.TestCase):

    def test_create_start_window(self):
        window_service = WindowServiceImpl.getInstance()
        menu_name = "TestMenu"

        window_service.createRootWindow(menu_name)

        window_service.createRootWindow(
            menu_name
        )

if __name__ == '__main__':
    unittest.main()
