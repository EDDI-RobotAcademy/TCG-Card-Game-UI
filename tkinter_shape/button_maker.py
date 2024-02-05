import tkinter as tk
from tkinter_shape.shape import Shape

class ButtonMaker(Shape):
    def __init__(self, master, canvas):
        super().__init__(master, canvas)
        self.master = master
        self.canvas = canvas

    def create_button(self, button_name, bg,  relx=0.5, rely=0.65, width=None, height=None, work=None):
        self.button = tk.Button(self.canvas, text=button_name, fg="white", bg=bg, width=width, height=height)
        self.button.place(relx=relx, rely=rely, anchor="center")
        self.button.bind("<Button-1>", lambda event: work())

        return self.button

    def draw(self):
        self.create_button()