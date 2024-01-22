import tkinter


class CardLeftUpRendering(tkinter.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.configure(bg="red")
        self.canvas = tkinter.Canvas(self, width=50, height=50)
        self.canvas.pack()