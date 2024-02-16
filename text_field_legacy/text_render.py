from text_field_legacy.text_entity import TextEntity
from OpenGL.GL import *
from PIL.ImageFont import ImageFont
import tkinter as tk
from PIL import ImageFont

class TextRender(TextEntity):
    def __init__(self, master, canvas, on_text_change, width, height):
        super().__init__(master, canvas)
        self.master = master
        self.canvas = canvas
        self.on_text_change = on_text_change
        self.width = width
        self.height = height

    def render_text(self, x=None, y=None, custom_text=None, text_color='black', font_size=20):
        glColor3f(0, 0, 0)
        glBegin(GL_QUADS)
        glVertex2f(0, 0)
        glVertex2f(self.width, 0)
        glVertex2f(self.width, self.height)
        glVertex2f(0, self.height)
        glEnd()

        text_to_render = custom_text

        font_path = "/usr/share/fonts/truetype/noto/NotoSansMono-Regular.ttf"
        font = ImageFont.truetype(font_path, font_size)
        text_width, text_height = font.getsize(text_to_render)

        if x is None:
            x = (self.width - text_width) // 2
        if y is None:
            y = (self.height - text_height) // 2

        self.canvas.create_text(x, y, text=text_to_render, fill=text_color, font=("TkDefaultFont", font_size))

    def draw(self):
        self.render_text()