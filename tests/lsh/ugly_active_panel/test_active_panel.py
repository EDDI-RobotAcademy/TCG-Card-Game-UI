import tkinter
import unittest

from tests.lsh.ugly_active_panel.frame.picking_card_frame import PickingCardLightningBorderWithActivePanelFrame


class TestActivePanel(unittest.TestCase):
    def test_animation_frame(self):
        root = tkinter.Tk()
        root.geometry(f"{root.winfo_screenwidth()}x{root.winfo_screenheight()}-0-0")
        root.deiconify()

        # picking_app = PickingCardFrame(root, width=f"{root.winfo_screenwidth()}", height=f"{root.winfo_screenheight()}", bg="white")
        picking_app = PickingCardLightningBorderWithActivePanelFrame(root)
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