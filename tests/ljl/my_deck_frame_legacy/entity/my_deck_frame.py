import tkinter


class MyDeckFrame(tkinter.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.configure(bg="#D7AC87", width=400, height=800)