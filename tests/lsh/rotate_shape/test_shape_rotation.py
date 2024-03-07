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
        self.rotation_angle = 0.0
        self.animation_speed = 2.0

    def redraw(self):
        glClear(GL_COLOR_BUFFER_BIT)
        glLoadIdentity()

        glRotatef(self.rotation_angle, 0, 0, 1)

        glColor3f(1.0, 1.0, 1.0)

        glBegin(GL_POLYGON)
        glVertex2f(-0.5, -0.5)
        glVertex2f(0.5, -0.5)
        glVertex2f(0.5, 0.5)
        glVertex2f(-0.5, 0.5)
        glEnd()

        self.tkSwapBuffers()

    def animate_rotation(self):
        if self.rotation_angle < 45.0:
            self.rotation_angle += self.animation_speed
            self.after(10, self.animate_rotation)
        else:
            self.rotation_angle = 0.0

    def on_key_press(self, event):
        if event.keysym == 'r' and self.rotation_angle == 0.0:
            self.animate_rotation()

class TestAppWindow(unittest.TestCase):
    def test_rotate_basic(self):
        root = tk.Tk()
        root.title("OpenGL Rectangle Drawing")

        app = RectDrawingApp(root, width=400, height=400)
        app.pack(side="top", fill="both", expand=True)
        app.animate = 1

        root.bind("<KeyPress>", app.on_key_press)

        root.mainloop()

if __name__ == '__main__':
    unittest.main()
