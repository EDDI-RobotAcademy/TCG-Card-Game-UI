from OpenGL.GL import *
from PIL.ImageFont import ImageFont
import tkinter as tk
from PIL import ImageFont

class MyDeckRegisterTextEntity:
    def __init__(self, master, canvas, textbox_string, width, height):
        self.master = master
        self.canvas = canvas
        self.textbox_string = textbox_string
        self.width = width
        self.height = height

    def render_text(self):
        glColor3f(0, 0, 0)
        glBegin(GL_QUADS)
        glVertex2f(0, 0)
        glVertex2f(self.width, 0)
        glVertex2f(self.width, self.height)
        glVertex2f(0, self.height)
        glEnd()

        text_to_render = self.textbox_string.get()
        if not text_to_render:
            text_to_render = "덱 이름을 입력하세요!"
        text_color = "blue"

        font_size = 24
        font_path = "/usr/share/fonts/truetype/noto/NotoSansMono-Regular.ttf"
        font = ImageFont.truetype(font_path, font_size)

        text_width, text_height = font.getsize(text_to_render)
        x = (self.width - text_width) // 2
        y = (self.height - text_height) // 2

        self.canvas.create_text(x, y, text=text_to_render, fill=text_color, font=("TkDefaultFont", 24))

    def text_box(self):
        return tk.Entry(self.canvas, textvariable=self.textbox_string, bg="white")
