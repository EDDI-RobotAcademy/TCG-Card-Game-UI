import tkinter
from PIL import ImageTk, Image
import os

from rock_paper_scissors.repository.rock_paper_scissors_repository_impl import RockPaperScissorsRepositoryImpl


class PaperButton:
    __instance = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
            cls.__instance.__rockPaperScissorsRepositoryImpl = RockPaperScissorsRepositoryImpl.getInstance()
        return cls.__instance

    @classmethod
    def getInstance(cls):
        if cls.__instance is None:
            cls.__instance = cls()
        return cls.__instance


    def create_paper_button(self, root, label_x, label_y):
        def on_image_click(event):
            self.__rockPaperScissorsRepositoryImpl.setRPS("보")
            RPS_label.config(text=self.__rockPaperScissorsRepositoryImpl.getRPS())

        image_path = "/home/eddi/proj/TCG-Card-Game-UI/local_storage/rock_paper_scissors_image/paper.png"
        original_image = Image.open(image_path)
        resized_image = original_image.resize((300, 250), Image.LANCZOS)
        self.__RPS_image = ImageTk.PhotoImage(resized_image)

        label = tkinter.Label(root, image=self.__RPS_image)
        label.place(x=label_x, y=label_y)
        label.bind("<Button-1>", on_image_click)
