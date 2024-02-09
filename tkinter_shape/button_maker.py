import tkinter as tk
from tkinter_shape.shape import Shape

class ButtonMaker(Shape):
    def __init__(self, master, canvas):
        super().__init__(master, canvas)
        self.master = master
        self.canvas = canvas

    def create_button(self, button_name, bg, width=None, height=None):
        self.button = tk.Button(self.canvas, text=button_name, fg="white", bg=bg, width=width, height=height)

        return self.button

    def draw(self, relx=0.5, rely=0.65):
        self.button.place(relx=relx, rely=rely, anchor="center")