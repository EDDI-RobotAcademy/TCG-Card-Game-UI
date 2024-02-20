import tkinter
import unittest

from initializer.init_domain import DomainInitializer
from tests.ljs.ugly_test_battle_field_functions.pre_drawed_battle_field_frame.PreDrawedBattleFieldFrameRefactorLJS import \
    PreDrawedBattleFieldFrameRefactorLJS


class TestSurrender(unittest.TestCase):

    def test_boost_energy_with_support_card(self):
        DomainInitializer.initEachDomain()

        root = tkinter.Tk()
        root.geometry(f"{root.winfo_screenwidth()}x{root.winfo_screenheight()}-0-0")
        root.deiconify()

        pre_drawed_battle_field_frame = PreDrawedBattleFieldFrameRefactorLJS(root)
        pre_drawed_battle_field_frame.pack(fill=tkinter.BOTH, expand=1)
        root.update_idletasks()

        def animate():
            pre_drawed_battle_field_frame.redraw()
            root.after(17, animate)

        root.after(0, animate)

        root.mainloop()


if __name__ == '__main__':
    unittest.main()
