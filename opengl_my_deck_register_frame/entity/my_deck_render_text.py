from OpenGL.GL import *
from PIL.ImageFont import ImageFont
import tkinter as tk
from PIL import ImageFont

class MyDeckRegisterTextEntity:
    def __init__(self, master, canvas, on_text_change, width, height):
        self.master = master
        self.canvas = canvas
        self.on_text_change = on_text_change
        self.width = width
        self.height = height
        self.textbox_string = tk.StringVar()
        self.textbox_string.trace_add('write', self.update_displayed_text)

    def update_displayed_text(self, *args):
        if self.on_text_change:
            self.on_text_change()

    def render_text(self, x=None, y=None, custom_text=None, text_color='black', font_size='20'):
        glColor3f(0, 0, 0)
        glBegin(GL_QUADS)
        glVertex2f(0, 0)
        glVertex2f(self.width, 0)
        glVertex2f(self.width, self.height)
        glVertex2f(0, self.height)
        glEnd()

        text_to_render = custom_text if custom_text is not None else self.textbox_string.get()
        if not text_to_render:
            text_to_render = "생성할 덱 이름을 입력하세요."

        font_path = "/usr/share/fonts/truetype/noto/NotoSansMono-Regular.ttf"
        font = ImageFont.truetype(font_path, int(font_size))
        text_width, text_height = font.getsize(text_to_render)

        if x is None:
            x = (self.width - text_width) // 2
        if y is None:
            y = (self.height - text_height) // 2

        self.canvas.create_text(x, y, text=text_to_render, fill=text_color, font=("TkDefaultFont", font_size))

    def text_box(self, font_size=20, lines=1):
        font = ("TkDefaultFont", font_size)
        return tk.Entry(self.canvas, textvariable=self.textbox_string, bg="white", font=font)
