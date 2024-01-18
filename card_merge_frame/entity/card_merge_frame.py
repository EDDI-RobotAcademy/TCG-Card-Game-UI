import tkinter


class CardMergeFrame(tkinter.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.configure(bg="#000000", width=670, height=490)

        #self.configure(bg="#AE905E", width=600, height=600)