import tkinter
import unittest
from time import sleep

from opengl_battle_field.frame.battle_field_frame import BattleFieldFrame


class TestAdjustCardSize(unittest.TestCase):

    def test_battle_field_frame(self):
        root = tkinter.Tk()
        root.geometry(f"{root.winfo_screenwidth()}x{root.winfo_screenheight()}-10-10")
        root.deiconify()

        window = BattleFieldFrame(root)
        window.pack(fill=tkinter.BOTH, expand=1)

        toggle_button = tkinter.Button(root, text="Toggle Visibility", command=window.toggle_visibility)
        toggle_button.place(x=100, y=10)

        summon_button = tkinter.Button(root, text="Summon", command=window.summon_units)

        summon_button.place(x=400, y=10)

        sleep(1)

        root.mainloop()


if __name__ == '__main__':
    unittest.main()