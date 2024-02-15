import math
import random
import tkinter as tk
import unittest

from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from pyopengltk import OpenGLFrame

class RectDrawingApp(OpenGLFrame):
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

        self.tkSwapBuffers()

    def draw_neon_border(self, x1, y1, x2, y2):
        glLineWidth(6.0)
        num_layers = 10
        flicker_probability = 0.1

        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

        for i in range(num_layers):
            if random.random() < flicker_probability:
                alpha = random.uniform(0.2, 0.8)
                neon_color = (0.0, 1.0, 0.0, alpha)

                glColor4fv(neon_color)
                glBegin(GL_LINE_LOOP)
                glVertex2f(x1 - 0.01 * i, y1 - 0.01 * i)
                glVertex2f(x2 + 0.01 * i, y1 - 0.01 * i)
                glVertex2f(x2 + 0.01 * i, y2 + 0.01 * i)
                glVertex2f(x1 - 0.01 * i, y2 + 0.01 * i)
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
