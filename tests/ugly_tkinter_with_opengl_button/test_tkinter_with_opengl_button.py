import tkinter as tk
import unittest

from PIL import Image, ImageDraw, ImageFont

from pyopengltk import OpenGLFrame
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *


class AppWindow(OpenGLFrame):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        self.width = screen_width
        self.height = screen_height

        self.transparent_rect_visible = False

        self.bind("<Configure>", self.on_resize)

        self.button = tk.Button(self.master, text="버튼", command=self.button_click, bg="white")
        self.button.pack()

    def initgl(self):
        print("initgl")
        glClearColor(1.0, 1.0, 1.0, 1.0)

        glViewport(0, 0, self.width, self.height)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluOrtho2D(0, self.width, self.height, 0)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

        # glEnable(GL_DEPTH_TEST)
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

    def redraw(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()

        glColor3f(1.0, 0.0, 0.0)  # 빨간색
        glBegin(GL_QUADS)
        glVertex3f(100, 100, 0)
        glVertex3f(200, 100, 0)
        glVertex3f(200, 200, 0)
        glVertex3f(100, 200, 0)
        glEnd()

        if self.transparent_rect_visible:
            glColor4f(0.0, 0.0, 0.0, 0.8)  # 검은색 (알파 채널 0.5로 투명도 조절)
            glBegin(GL_QUADS)
            glVertex3f(0, 0, 0)
            glVertex3f(0, self.height, 0)
            glVertex3f(self.width, self.height, 0)
            glVertex3f(self.width, 0, 0)
            glEnd()

            glColor4f(1.0, 1.0, 0.0, 1.0)
            glBegin(GL_QUADS)
            glVertex3f(self.width * 0.25, self.height * 0.25, 0)
            glVertex3f(self.width * 0.25, self.height * 0.75, 0)
            glVertex3f(self.width * 0.75, self.height * 0.75, 0)
            glVertex3f(self.width * 0.75, self.height * 0.25, 0)
            glEnd()

        self.tkSwapBuffers()

    def button_click(self):
        self.transparent_rect_visible = not self.transparent_rect_visible
        self.redraw()

    def reshape(self, width, height):
        glViewport(0, 0, width, height)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluOrtho2D(0, width, height, 0)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

    def on_resize(self, event):
        self.reshape(event.width, event.height)

class TestAppWindow(unittest.TestCase):
    def test_button_click_visual(self):
        root = tk.Tk()
        root.geometry(f"{root.winfo_screenwidth()}x{root.winfo_screenheight()}+0+0")
        root.deiconify()

        app = AppWindow(root)
        app.initgl()
        app.pack(fill=tk.BOTH, expand=tk.YES)

        root.update_idletasks()
        root.mainloop()


if __name__ == '__main__':
    unittest.main()
