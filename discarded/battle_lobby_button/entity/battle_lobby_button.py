import tkinter


class BattleLobbyButton(tkinter.Button):

    __instance = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
        return cls.__instance

    @classmethod
    def getInstance(cls):
        if cls.__instance is None:
            cls.__instance = cls()
        return cls.__instance

    def generateBattleLobbyButton(self, master, text="hello"):
        button = tkinter.Button(master)
        button.configure(bg="#663300", padx=200, pady=50, text=text, font=("Arial",10))
        return button