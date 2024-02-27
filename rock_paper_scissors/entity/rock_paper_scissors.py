import tkinter


class RockPaperScissors(tkinter.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.configure(bg="#B9A898")
