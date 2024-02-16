import unittest
import tkinter as tk
from OpenGL.GL import *
from OpenGL.raw.GLU import gluOrtho2D
from OpenGL.GLUT import glutBitmapCharacter
from PIL import Image, ImageDraw, ImageFont
from pyopengltk import OpenGLFrame

class OpenGLTextFrame(OpenGLFrame):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        self.width = screen_width
        self.height = screen_height

        self.canvas = tk.Canvas(self, width=self.width, height=self.height)
        self.canvas.pack()

    def initgl(self):
        glClearColor(0, 0, 0, 0)
        gluOrtho2D(0, self.width, 0, self.height)

    def redraw(self):
        glClear(GL_COLOR_BUFFER_BIT)

        self.render_text()

        self.tkSwapBuffers()

    def render_text(self):
        glColor3f(0, 0, 0)
        glBegin(GL_QUADS)
        glVertex2f(0, 0)
        glVertex2f(self.width, 0)
        glVertex2f(self.width, self.height)
        glVertex2f(0, self.height)
        glEnd()

        text_to_render = "Hello, PyOpenGLTK!"
        text_color = "blue"

        font = ImageFont.load_default()

        text_width, text_height = font.getsize(text_to_render)
        x = (self.width - text_width) // 2
        y = (self.height - text_height) // 2

        self.canvas.delete("all")

        self.canvas.create_text(x, y, text=text_to_render, fill=text_color, font=("TkDefaultFont", 24))

class TestOpenGLTextFrame(unittest.TestCase):
    def test_opengl_text_frame(self):
        root = tk.Tk()
        app = OpenGLTextFrame(root, width=400, height=400)
        app.pack(expand=tk.YES, fill=tk.BOTH)

        app.redraw()

        root.mainloop()

if __name__ == '__main__':
    unittest.main()
