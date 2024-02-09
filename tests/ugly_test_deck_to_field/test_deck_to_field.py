import unittest
import tkinter

from tests.ugly_test_deck_to_field.frame.deck_to_field_frame import DeckToFieldFrame


class TestDeckToField(unittest.TestCase):
    def test_deck_to_field(self):
        root = tkinter.Tk()
        root.geometry(f"{root.winfo_screenwidth()}x{root.winfo_screenheight()}-0-0")
        root.deiconify()

        window = DeckToFieldFrame(root)
        window.pack(fill=tkinter.BOTH, expand=1)

        root.mainloop()


if __name__ == '__main__':
    unittest.main()