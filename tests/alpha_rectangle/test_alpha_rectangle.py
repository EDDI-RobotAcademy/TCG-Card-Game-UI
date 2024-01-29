import unittest

import tkinter as tk
import unittest

from PIL import Image, ImageDraw, ImageFont, ImageTk

from pyopengltk import OpenGLFrame
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

class CanvasWithAlphaRectangles(OpenGLFrame):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        self.width = screen_width
        self.height = screen_height
        print(f"screen width: {screen_width}, screen height: {screen_height}")

        self.transparent_rect_visible = False

        self.images = []  # to hold the newly created image
        self.canvas = tk.Canvas(self, width=self.width, height=self.height)
        self.canvas.pack()

        self.button = tk.Button(self.master, text="버튼", command=self.button_click, bg="white")
        self.button.pack()

    def initgl(self):
        # glClearColor(0, 0, 0, 0)
        # gluOrtho2D(0, self.width, 0, self.height)
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
        glClear(GL_COLOR_BUFFER_BIT)

        self.canvas.delete("all")

        self.create_alpha_rectangle(10, 10, 200, 100, fill='blue')
        self.create_alpha_rectangle(50, 50, 250, 150, fill='green', alpha=0.5)
        self.create_alpha_rectangle(0, 0, self.width, self.height, fill='black', alpha=0.8)

        if self.transparent_rect_visible:
            self.create_alpha_rectangle(int(self.width * 0.25), int(self.height * 0.25),
                                        int(self.width * 0.75), int(self.height * 0.75), fill='yellow', alpha=1.0)
            self.render_text()

        self.tkSwapBuffers()

    def button_click(self):
        self.transparent_rect_visible = not self.transparent_rect_visible
        self.redraw()

    def create_alpha_rectangle(self, x1, y1, x2, y2, **kwargs):
        if 'alpha' in kwargs:
            alpha = int(kwargs.pop('alpha') * 255)
            fill = kwargs.pop('fill')
            fill = self.master.winfo_rgb(fill) + (alpha,)
            image = Image.new('RGBA', (x2 - x1, y2 - y1), fill)
            self.images.append(ImageTk.PhotoImage(image))
            self.canvas.create_image(x1, y1, image=self.images[-1], anchor='nw')
        self.canvas.create_rectangle(x1, y1, x2, y2, **kwargs)

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

        # self.canvas.delete("all")

        self.canvas.create_text(x, y, text=text_to_render, fill=text_color, font=("TkDefaultFont", 24))

class TestAppWindow(unittest.TestCase):
    def test_button_click_visual(self):
        root = tk.Tk()
        root.geometry(f"{root.winfo_screenwidth()}x{root.winfo_screenheight()}+0+0")
        root.deiconify()

        app = CanvasWithAlphaRectangles(root)
        app.initgl()
        app.pack(fill=tk.BOTH, expand=tk.YES)
        app.render_text()

        root.mainloop()


if __name__ == '__main__':
    unittest.main()