import tkinter


class MakeMyDeckFrame(tkinter.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.configure(bg="#E18B6B", width=400, height=250)