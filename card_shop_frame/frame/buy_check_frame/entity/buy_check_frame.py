import tkinter


class BuyCheckFrame(tkinter.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.configure(bg="#F7F8E0", width=600, height=400)
