import tkinter
import unittest

from battle_field_unit_card_frame.frame.battle_field_unit_card_frame import BattleFieldUnitCardFrame


class TestBattleFieldUnitCardFrame(unittest.TestCase):

    def test_battle_field_card_frame(self):
        root = tkinter.Tk()
        window = BattleFieldUnitCardFrame(root, width=800, height=800)
        window.pack(fill=tkinter.BOTH, expand=1)

        toggle_button = tkinter.Button(root, text="Toggle Visibility", command=window.toggle_visibility)
        toggle_button.place(x=100, y=10)

        root.mainloop()




if __name__ == '__main__':
    unittest.main()