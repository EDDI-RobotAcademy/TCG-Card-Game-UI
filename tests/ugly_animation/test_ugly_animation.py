from OpenGL.GL import *
import tkinter as tk
import unittest

from pyopengltk import OpenGLFrame


class AnimationFrame(OpenGLFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, kwargs)
        self.angle = 0.0

    def initgl(self):
        self.angle = 0.0

    def redraw(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        self.draw_rotating_square()

        self.tkSwapBuffers()

        self.angle += 1.0
        self.after(16, self.redraw)

    def draw_rotating_square(self):
        size = 0.5

        glRotatef(float(self.angle), 0.0, 0.0, 1.0)
        glColor4f(0.7, 0.7, 0.2, 0.0)

        glBegin(GL_QUADS)
        glVertex2f(-size, -size)
        glVertex2f(size, -size)
        glVertex2f(size, size)
        glVertex2f(-size, size)
        glEnd()


class TestUglyAnimationFrame(unittest.TestCase):

    def test_animation_frame(self):
        root = tk.Tk()
        root.geometry(f"{root.winfo_screenwidth()}x{root.winfo_screenheight()}+0+0")
        root.deiconify()

        window = AnimationFrame(root)
        window.pack(fill=tk.BOTH, expand=1)

        window.redraw()  # 초기 렌더링을 위해 redraw 호출

        root.mainloop()


if __name__ == '__main__':
    unittest.main()
