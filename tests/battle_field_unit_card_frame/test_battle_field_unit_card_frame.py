import tkinter
import unittest

from battle_field_unit_card_frame.frame.battle_field_unit_card_frame import BattleFieldUnitCardFrame


class TestBattleFieldUnitCardFrame(unittest.TestCase):

    def test_battle_field_unit_card_frame(self):
        root = tkinter.Tk()
        root.geometry(f"{root.winfo_screenwidth()}x{root.winfo_screenheight()}+0+0")
        root.deiconify()

        window = BattleFieldUnitCardFrame(root)
        window.pack(fill=tkinter.BOTH, expand=1)

        toggle_button = tkinter.Button(root, text="Toggle Visibility", command=window.toggle_visibility)
        toggle_button.place(x=100, y=10)

        # def toggle_fullscreen(event):
        #     root.attributes('-fullscreen', not root.attributes('-fullscreen'))
        #
        # root.bind('<Double-Button-1>', toggle_fullscreen)

        root.mainloop()




if __name__ == '__main__':
    unittest.main()