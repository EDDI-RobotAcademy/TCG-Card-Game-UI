import tkinter
import unittest

from tests.lsh.ugly_mouse_picking.test_circle_on_pickable_rectangle import CustomOpenGLFrame


class TestOpenGLClickAndDrop(unittest.TestCase):
    def test_opengl_click_and_drop(self):
        root = tkinter.Tk()
        root.geometry("1200x800")
        card = CustomOpenGLFrame(root, width=800, height=800, bg="white")

        card.pack(fill=tkinter.BOTH, expand=tkinter.YES)
        root.mainloop()

if __name__ == '__main__':
    unittest.main()