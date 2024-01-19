import tkinter

class TransparentBackgroundFrame(tkinter.Frame):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self.canvas = tkinter.Canvas(self, width=1200, height=800, bg="white", highlightthickness=0)
        self.canvas.pack(expand=True, fill="both")