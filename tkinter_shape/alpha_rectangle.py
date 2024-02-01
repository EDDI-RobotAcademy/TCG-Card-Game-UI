from PIL import Image, ImageTk

from tkinter_shape.shape import Shape

class AlphaRectangle(Shape):
    def __init__(self, master, canvas):
        super().__init__(master, canvas)
        self.master = master
        self.canvas = canvas
        self.images = []

    def create_alpha_rectangle(self, x1, y1, x2, y2, **kwargs):
        if 'alpha' in kwargs:
            alpha = int(kwargs.pop('alpha') * 255)
            fill = kwargs.pop('fill')
            fill = self.master.winfo_rgb(fill) + (alpha,)
            image = Image.new('RGBA', (x2 - x1, y2 - y1), fill)
            self.images.append(ImageTk.PhotoImage(image))
            self.canvas.create_image(x1, y1, image=self.images[-1], anchor='nw')
        self.canvas.create_rectangle(x1, y1, x2, y2, **kwargs)

    def draw(self):
        self.create_alpha_rectangle()