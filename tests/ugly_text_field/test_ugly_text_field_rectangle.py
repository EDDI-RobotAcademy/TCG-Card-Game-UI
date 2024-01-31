import unittest

import numpy as np
import tkinter as tk
from PIL.ImageFont import ImageFont

from opengl_shape.rectangle import Rectangle
from opengl_shape.shape import Shape

from PIL import Image, ImageFont
from OpenGL import GL


class TextFieldRectangle(Shape):
    def __init__(self, text, vertices, global_translation=(0, 0), local_translation=(0, 0)):
        super().__init__(vertices, global_translation, local_translation)
        self.text = text
        self.is_visible = True

    def set_visible(self, visible):
        self.is_visible = visible

    def get_visible(self):
        return self.is_visible

    def draw(self):
        if self.get_visible():
            white_rect = Rectangle(color=(1.0, 1.0, 1.0, 1.0),
                                   vertices=self.vertices,
                                   global_translation=self.global_translation,
                                   local_translation=self.local_translation)
            white_rect.draw()

            canvas = tk.Canvas(width=198,height=102)
            canvas.pack()

            GL.glBegin(GL.GL_QUADS)
            GL.glTexCoord2f(0, 0)
            print(
                f"x: {self.vertices[0][0] + self.local_translation[0]}, y: {self.vertices[0][1] + self.local_translation[1]}")
            GL.glVertex2f(self.vertices[0][0] + self.local_translation[0] + self.global_translation[0],
                          self.vertices[0][1] + self.local_translation[1] + self.global_translation[1])

            GL.glTexCoord2f(1, 0)
            GL.glVertex2f(self.vertices[1][0] + self.local_translation[0] + self.global_translation[0],
                          self.vertices[1][1] + self.local_translation[1] + self.global_translation[1])

            GL.glTexCoord2f(1, 1)
            GL.glVertex2f(self.vertices[2][0] + self.local_translation[0] + self.global_translation[0],
                          self.vertices[2][1] + self.local_translation[1] + self.global_translation[1])

            GL.glTexCoord2f(0, 1)
            GL.glVertex2f(self.vertices[3][0] + self.local_translation[0] + self.global_translation[0],
                          self.vertices[3][1] + self.local_translation[1] + self.global_translation[1])
            GL.glEnd()

            text_color = "blue"

            font = ImageFont.load_default()

            text_width, text_height = font.getsize(self.text)
            x = 198
            y = 102


            canvas.delete("all")

            canvas.create_text(x, y, text=self.text, fill=text_color, font=("TkDefaultFont", 12))
