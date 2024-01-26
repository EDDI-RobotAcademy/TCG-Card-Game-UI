import tkinter
import unittest

from my_card_frame.renderer.my_card_frame_renderer import MyCardFrameRenderer
from my_card_main_frame.frame.my_card_main_frame import MyCardFrame


class TestMyCardFrame(unittest.TestCase):

    def test_my_card_main_frame(self):
        root = tkinter.Tk()
        root.geometry(f"{root.winfo_screenwidth()}x{root.winfo_screenheight()}-10-10")
        root.deiconify()


        window = MyCardFrame(root)
        window.pack(fill=tkinter.BOTH, expand=1)


        toggle_button = tkinter.Button(root, text="Toggle Visibility", command=window.toggle_visibility)
        toggle_button.place(x=100, y=10)

        root.mainloop()




if __name__ == '__main__':
    unittest.main()