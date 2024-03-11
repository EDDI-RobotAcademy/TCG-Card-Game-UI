import tkinter as tk
import unittest
from PIL import ImageTk, Image




class TestCardShopFrame(unittest.TestCase):

    def createtitleUiFrame(self, root):

        shop_label = tk.Label(root, text="상점", font=("Helvetica", 16), bg="#BCA9F5")
        shop_label.place(x=10, y=10)




    def test_rock_paper_scissors(self):
        root = tk.Tk()
        root.geometry("1920x100")
        root.configure(background="#BCA9F5")
        self.createtitleUiFrame(root)
        root.mainloop()


if __name__ == '__main__':
    unittest.main()
