import tkinter
import unittest

from tests.ugly_mouse_picking.entity.pickable_object import PickableObject
from tests.ugly_mouse_picking.frame.pickable_frame import PickableFrame
from tests.ugly_mouse_picking.renderer.pickable_renderer import PickableRenderer


class TestUglyAnimationFrame(unittest.TestCase):
    def test_animation_frame(self, tk=None):
        root = tkinter.Tk()
        objects = [PickableObject(100, 100, 50, 50), PickableObject(200, 200, 50, 50)]
        renderer = PickableRenderer(objects)
        app = PickableFrame(root, renderer=renderer, width=400, height=400, bg="white")
        app.pack(fill=tkinter.BOTH, expand=tkinter.YES)
        app.mainloop()

if __name__ == '__main__':
    unittest.main()