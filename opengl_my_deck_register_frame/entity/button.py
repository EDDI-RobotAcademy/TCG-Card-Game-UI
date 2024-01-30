import tkinter as tk
class MyDeckRegisterButtonEntity:
    def __init__(self, master, canvas):
        self.master = master
        self.canvas = canvas

    def add_button_to_canvas(self, x, y, text, command):
        button = tk.Button(self.canvas, text=text, command=command, bg="white")
        button_window = self.canvas.create_window(x, y, anchor='nw', window=button)
        return button, button_window