from OpenGL import GL

import tkinter
import unittest

from OpenGL.GL import *
from OpenGL.GLU import *
from pyopengltk import OpenGLFrame
from screeninfo import get_monitors

from opengl_shape.rectangle import Rectangle


class ResizableRectangle(OpenGLFrame):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)

        monitors = get_monitors()
        target_monitor = monitors[2] if len(monitors) > 2 else monitors[0]

        self.width = target_monitor.width
        self.height = target_monitor.height

        print(f"Constructor width: {self.width}, height: {self.height}")

        self.is_reshape_not_complete = True

        self.current_width = self.width
        self.current_height = self.height

        self.prev_width = self.width
        self.prev_height = self.height

        self.width_ratio = 1.0
        self.height_ratio = 1.0

        self.opengl_rectangle = Rectangle(
            (0.77, 0.34, 0.2, 1.0),
            [(100, 100), (400, 100), (400, 400), (100, 400)],
            (0, 0),
            (0, 0))

        self.bind("<Configure>", self.on_resize)

    def initgl(self):
        glClearColor(1.0, 1.0, 1.0, 1.0)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluOrtho2D(0, self.width, self.height, 0)
        print(f"initgl width: {self.width}, height: {self.height}")

        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

    def reshape(self, width, height):
        print(f"Reshaping window to width={width}, height={height}")

        if self.is_reshape_not_complete:
            self.width = width
            self.height = height

            self.current_width = self.width
            self.current_height = self.height

            self.prev_width = self.width
            self.prev_height = self.height
            self.is_reshape_not_complete = False

        self.prev_width = self.current_width
        self.prev_height = self.current_height

        self.current_width = self.width
        self.current_height = self.height

        self.width_ratio = self.current_width / self.prev_width
        self.height_ratio = self.current_height / self.prev_height
        print(f"Reshaping window to width_ratio={self.width_ratio}, height_ratio={self.height_ratio}")

        glViewport(0, 0, width, height)

    def on_resize(self, event):
        print("Handling resize event")
        self.reshape(event.width, event.height)
        self.redraw()

    def redraw(self):
        if self.is_reshape_not_complete:
            return

        self.tkMakeCurrent()
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        self.opengl_rectangle.set_width_ratio(self.width_ratio)
        self.opengl_rectangle.set_height_ratio(self.height_ratio)

        self.opengl_rectangle.draw()

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


class TestCustomRectangleWithCalculatedRatio(unittest.TestCase):
    def test_custom_rectangle_with_calculated_ratio(self):
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
