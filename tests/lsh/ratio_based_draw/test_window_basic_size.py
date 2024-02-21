from OpenGL import GL

import tkinter
import unittest

from OpenGL.GL import *
from OpenGL.GLU import *
from pyopengltk import OpenGLFrame
from screeninfo import get_monitors


class ResizableRectangle(OpenGLFrame):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)

        self.width = self.winfo_screenwidth()
        self.height = self.winfo_screenheight()

        self.bind("<Configure>", self.on_resize)

    def initgl(self):
        glClearColor(1.0, 1.0, 1.0, 1.0)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluOrtho2D(0, self.width, self.height, 0)

        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

    def draw_rectangle2(self):
        glColor3f(0.0, 1.0, 0.0)

        glBegin(GL_QUADS)
        glVertex2f(100 / 1848 * 1386, 100 / 1016 * 752)
        glVertex2f(400 / 1848 * 1386, 100 / 1016 * 752)
        glVertex2f(400 / 1848 * 1386, 400 / 1016 * 752)
        glVertex2f(100 / 1848 * 1386, 400 / 1016 * 752)
        glEnd()

    def draw_rectangle(self):
        glColor3f(0.0, 1.0, 0.0)

        original_coordinates = [(100, 100), (400, 100), (400, 400), (100, 400)]

        adjusted_coordinates = [(x / 1920 * self.width, y / 1080 * self.height) for x, y in original_coordinates]

        glBegin(GL_QUADS)
        for x, y in adjusted_coordinates:
            glVertex2f(x, y)
        glEnd()

    def reshape(self, width, height):
        print(f"Reshaping window to width={width}, height={height}")
        self.width = width
        self.height = height
        glViewport(0, 0, width, height)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()

        gluOrtho2D(0, width, height, 0)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

    def on_resize(self, event):
        print("Handling resize event")
        self.reshape(event.width, event.height)
        self.redraw()

    def redraw(self):
        self.tkMakeCurrent()
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        self.draw_rectangle()

        self.tkSwapBuffers()



class FullScreenWindow(tkinter.Tk):
    def __init__(self):
        super().__init__()

        monitors = get_monitors()
        target_monitor = monitors[2] if len(monitors) > 2 else monitors[0]

        self.title("Full Screen Window")
        self.geometry(f"{target_monitor.width}x{target_monitor.height}+{target_monitor.x}+{target_monitor.y}")
        self.configure(bg="white")
        self.resizable(True, True)


class TestResizableRectangle(unittest.TestCase):
    def test_resizable_rectangle(self):
        monitor_3 = get_monitors()[2]

        # Tkinter 윈도우 생성
        root = FullScreenWindow()

        resizable_rectangle = ResizableRectangle(root)
        resizable_rectangle.pack(fill=tkinter.BOTH, expand=1)

        def animate():
            resizable_rectangle.redraw()
            root.after(33, animate)

        root.after(0, animate)

        root.mainloop()

if __name__ == '__main__':
    unittest.main()
