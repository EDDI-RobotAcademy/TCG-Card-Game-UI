import tkinter


class SelectRaceUiFrame(tkinter.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.configure(bg="green", width=1720, height=980)
