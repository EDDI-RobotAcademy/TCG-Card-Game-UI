import tkinter


class CardBackFrame(tkinter.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.configure(bg="white", width=120, height=240)

        #self.configure(bg="#AE905E", width=600, height=600)