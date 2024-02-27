import tkinter


class MyGameMoneyFrame(tkinter.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.configure(bg="#444444", width=30, height=20)
