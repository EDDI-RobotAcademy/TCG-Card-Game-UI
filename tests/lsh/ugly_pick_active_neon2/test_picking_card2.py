import tkinter
import unittest

from tests.lsh.ugly_pick_active_neon2.frame.picking_card_frame2 import PickingCardLightningBorderFrame2


class TestPickActionLightningBorder2(unittest.TestCase):
    def test_animation_frame2(self):
        root = tkinter.Tk()
        root.geometry(f"{root.winfo_screenwidth()}x{root.winfo_screenheight()}-0-0")
        root.deiconify()

        picking_app = PickingCardLightningBorderFrame2(root)
        picking_app.pack(fill=tkinter.BOTH, expand=1)

        toggle_button = tkinter.Button(root, text="Toggle Visibility", command=picking_app.toggle_visibility)
        toggle_button.place(x=100, y=10)
        root.update_idletasks()

        def animate():
            picking_app.redraw()
            root.after(16, animate)

        root.after(0, animate)

        root.mainloop()

if __name__ == '__main__':
    unittest.main()
