import tkinter


class CheckRockPaperScissorsWinnerFrame(tkinter.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.configure(bg="#1C1C1C", width=1920, height=1080)
