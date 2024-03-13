import tkinter as tk
import unittest
from PIL import ImageTk, Image
from card_shop_frame.frame.shop_title_frame.service.shop_title_frame_service_impl import ShopTitleFrameServiceImpl




class TestCardShopFrame(unittest.TestCase):

    def createtitleUiFrame(self, root):
        def switchmenu():
            print("swichtmenu대체")

        shopTitleFrame = ShopTitleFrameServiceImpl.getInstance()
        shopTitleFrame.createShopTitleUiFrame(root, switchmenu)





    def test_rock_paper_scissors(self):
        root = tk.Tk()
        root.geometry("1920x100")
        root.configure(background="#BCA9F5")
        self.createtitleUiFrame(root)
        root.mainloop()


if __name__ == '__main__':
    unittest.main()
