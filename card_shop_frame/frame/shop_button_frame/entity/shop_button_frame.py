import tkinter


class ShopButtonFrame(tkinter.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.configure(bg="blue", width=200, height=980)
