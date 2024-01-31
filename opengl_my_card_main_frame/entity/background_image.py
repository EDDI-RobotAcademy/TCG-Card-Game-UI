from tkinter import *
from PIL import Image, ImageTk

class MyCardMainFramImage:
    def __init__(self, master, canvas):
        self.master = master
        self.canvas = canvas
        self.images = []

    def create_background_image(self, width, height, image_path=None):
        image = Image.open(image_path)
        image = image.resize((width, height), Image.ANTIALIAS)
        self.images.append(ImageTk.PhotoImage(image))
        self.canvas.create_image(0, 0, image=self.images[-1], anchor='nw')
