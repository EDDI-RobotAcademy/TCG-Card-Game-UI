from tkinter import Label
import tkinter
from PIL import Image, ImageTk
import unittest

from card_shop_frame.frame.my_game_money_frame.entity.my_game_money_frame import MyGameMoneyFrame


class TestMyDeckRegisterFrame(unittest.TestCase):

    def test_my_deck_register_frame(self):
        root = tkinter.Tk()
        root.geometry(f"{root.winfo_screenwidth()}x{root.winfo_screenheight()}+0+0")
        root.deiconify()
        window = MyGameMoneyFrame(root)
        window.pack(fill=tkinter.BOTH, expand=1)

        image_path = '/home/eddi/proj/TCG-Card-Game-UI/images/game_money.png'
        original_image = Image.open(image_path)
        resized_image = original_image.resize((15, 15), Image.LANCZOS)
        money_image = ImageTk.PhotoImage(resized_image)
        label_GameMoney = Label(window, text=1000, image=money_image, compound="left",
                                font=("Arial", 12))
        label_GameMoney.pack()


        root.mainloop()


if __name__ == '__main__':
    unittest.main()