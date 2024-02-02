import tkinter as tk

from text_field.text_entity import TextEntity


class TextBox(TextEntity):
    def __init__(self, master, canvas, on_text_change):
        super().__init__(master, canvas)
        self.master = master
        self.canvas = canvas
        self.on_text_change = on_text_change
        self.textbox_string = tk.StringVar()
        self.textbox_string.trace_add('write', self.update_displayed_text)

    def update_displayed_text(self, *args):
        if self.on_text_change:
            self.on_text_change()

    def text_box(self, font_size=20, lines=1, relx=0.5, rely=0.55):
        font = ("TkDefaultFont", font_size)
        text_entry = tk.Entry(self.canvas, textvariable=self.textbox_string, bg="white", font=font)
        text_entry.place(relx=relx, rely=rely, anchor='center')

    def get_textbox_string(self):
        return self.textbox_string

    def draw(self):
        self.text_box()
