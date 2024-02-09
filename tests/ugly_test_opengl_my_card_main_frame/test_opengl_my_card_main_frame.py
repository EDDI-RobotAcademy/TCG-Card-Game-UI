import unittest
import tkinter as tk
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from pyopengltk import OpenGLFrame

from common.utility import get_project_root
from opengl_shape.image_rectangle_element import ImageRectangleElement
from opengl_shape.rectangle import Rectangle


class RectDrawingApp(OpenGLFrame):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)

        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        self.width = screen_width
        self.height = screen_height

    def initgl(self):
        glClearColor(0.0, 1.0, 0.0, 0.0)
        gluOrtho2D(-1.0, 1.0, -1.0, 1.0)

    def redraw(self):
        project_root = get_project_root()
        glClear(GL_COLOR_BUFFER_BIT)

        # 배경 이미지 도형
        background_rectangle = ImageRectangleElement(image_path=os.path.join(project_root, "local_storage", "image", "battle_lobby", "background.png"),
                                                     vertices=[(-1, -1), (1, -1), (1, 1), (-1, 1)])
        background_rectangle.draw()

        # 나의 덱 도형
        myDeck_regtangle= Rectangle(color=(0.5137, 0.3608, 0.2314, 1.0),
                                    vertices=[(0.45, -1), (1, -1), (1, 1), (0.45, 1)])
        myDeck_regtangle.draw()

        self.tkSwapBuffers()

class TestAppWindow(unittest.TestCase):
    def test_opengl_basic(self):
        root = tk.Tk()
        root.title("OpenGL Rectangle Drawing")
        root.geometry(f"{root.winfo_screenwidth()}x{root.winfo_screenheight()}-0-0")

        app = RectDrawingApp(root)
        app.pack(side="top", fill="both", expand=True)
        app.animate = 1
        root.mainloop()

if __name__ == '__main__':
    unittest.main()