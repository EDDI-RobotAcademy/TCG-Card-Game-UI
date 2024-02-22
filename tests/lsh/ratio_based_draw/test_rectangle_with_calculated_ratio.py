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

        self.current_width = self.width
        self.current_height = self.height

        self.prev_width = self.width
        self.prev_height = self.height

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

        width_ratio =  self.current_width / self.prev_width
        height_ratio = self.current_height / self.prev_height

        glBegin(GL_QUADS)
        glVertex2f(100 * width_ratio, 100 * height_ratio)
        glVertex2f(400 * width_ratio, 100 * height_ratio)
        glVertex2f(400 * width_ratio, 400 * height_ratio)
        glVertex2f(100 * width_ratio, 400 * height_ratio)
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

        self.prev_width = self.current_width
        self.prev_height = self.current_height

        self.current_width = self.width
        self.current_height = self.height

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


class TestRectangleWithCalculatedRatio(unittest.TestCase):
    def test_rectangle_with_calculated_ratio(self):
        monitor_3 = get_monitors()[2]

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
