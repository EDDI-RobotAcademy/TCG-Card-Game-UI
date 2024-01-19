import tkinter


class BattleRoomButton(tkinter.Button):

    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.configure(bg="#663300")


    def generateRoomButton(self, master, text="hello"):
        room = tkinter.Button(master)
        room.configure(bg="#663300", padx=400, pady=50, text=text, font=("Arial",10))
        return room