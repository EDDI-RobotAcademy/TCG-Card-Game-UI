import tkinter


class ShopTitleFrame(tkinter.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.configure(bg="#FFDEAD", width=1920, height=100)
