import tkinter


class Window(tkinter.Tk):
    def __init__(self, title, geometry, background_color, resizable):
        super().__init__()
        self.title(title)
        self.geometry(geometry)
        self.configure(bg=background_color)
        self.resizable(*resizable)

