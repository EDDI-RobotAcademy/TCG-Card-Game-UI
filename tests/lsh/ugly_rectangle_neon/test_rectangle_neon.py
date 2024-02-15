import math
import random
import tkinter as tk
import unittest

from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from noise import snoise2
from pyopengltk import OpenGLFrame

# pip3 install noise

class RectDrawingApp(OpenGLFrame):

    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self.inner_left = -0.3
        self.inner_right = 0.3

    def initgl(self):
        glClearColor(0.0, 0.0, 0.0, 0.0)
        gluOrtho2D(-1.0, 1.0, -1.0, 1.0)

    def redraw(self):
        glClear(GL_COLOR_BUFFER_BIT)
        glColor3f(1.0, 1.0, 1.0)

        glBegin(GL_POLYGON)
        glVertex2f(-0.5, -0.5)
        glVertex2f(0.5, -0.5)
        glVertex2f(0.5, 0.5)
        glVertex2f(-0.5, 0.5)
        glEnd()

        self.draw_neon_border(-0.5, -0.5, 0.5, 0.5)
        self.draw_lightning_flickers(-0.5, -0.5, 0.5, 0.5)

        self.tkSwapBuffers()

    def draw_neon_border(self, x1, y1, x2, y2):
        glLineWidth(6.0)
        neon_color = (0.0, 1.0, 0.0, 1.0)

        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

        glColor4fv(neon_color)

        glBegin(GL_LINE_LOOP)
        glVertex2f(x1, y1)
        glVertex2f(x2, y1)
        glVertex2f(x2, y2)
        glVertex2f(x1, y2)
        glEnd()

        glDisable(GL_BLEND)

    def draw_lightning_flickers(self, x1, y1, x2, y2):
        num_flickers = 10  # Adjust the number of flickers
        flicker_intensity = 0.1
        frequency = 0.05

        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

        for _ in range(num_flickers):
            alpha = random.uniform(0.2, 0.8)  # Random alpha value for flickering effect
            flicker_x = random.uniform(x1, x2)
            flicker_y = random.uniform(y1, y2)

            flicker_x2 = random.uniform(x1, x2)
            flicker_y2 = random.uniform(y1, y2)

            glColor4f(1.0, 1.0, 1.0, alpha)

            glBegin(GL_LINES)
            glVertex2f(flicker_x, flicker_y)
            glVertex2f(flicker_x + random.uniform(-0.1, 0.1), flicker_y + random.uniform(-0.1, 0.1))
            glEnd()

            glBegin(GL_LINES)
            glVertex2f(flicker_x2, flicker_y2)
            glVertex2f(flicker_x2 + random.uniform(-0.1, 0.1), flicker_y2 + random.uniform(-0.1, 0.1))
            glEnd()

        glDisable(GL_BLEND)


class TestAppWindow(unittest.TestCase):
    def test_opengl_basic(self):
        root = tk.Tk()
        root.title("OpenGL Rectangle Drawing")

        app = RectDrawingApp(root, width=400, height=400)
        app.pack(side="top", fill="both", expand=True)
        app.animate = 1
        root.mainloop()

if __name__ == '__main__':
    unittest.main()
