import tkinter
import unittest

from my_card_frame.frame.my_card_frame import MyCardFrame
from my_deck_frame.frame.my_deck_frame import MyDeckFrame


class TestMyCardFrame(unittest.TestCase):

    def test_my_card_main_frame(self):
        root = tkinter.Tk()
        root.geometry(f"{root.winfo_screenwidth()}x{root.winfo_screenheight()}-10-10")
        root.deiconify()


        # window = MyDeckFrame(root)
        # window.pack(fill=tkinter.BOTH, expand=1)
        #
        window = MyCardFrame(root)
        window.pack(fill=tkinter.BOTH, expand=1)

        root.mainloop()




if __name__ == '__main__':
    unittest.main()