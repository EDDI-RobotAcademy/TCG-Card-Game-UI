import tkinter


class CardRightBottomRendering(tkinter.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.configure(bg="yellow")
        self.canvas = tkinter.Canvas(self, width=50, height=50)
        self.canvas.pack()