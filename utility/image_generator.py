import os
import tkinter
from tkinter import PhotoImage
from PIL import ImageTk, Image


class ImageGenerator:
    __instance = None
    __selectedDeckImage = None
    __unselectedDeckImage = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
            cls.__instance.initImages()
           # cls.__instance.__deckImage = ImageTk.PhotoImage( Image.open(os.path.join(os.getcwd(), "local_storage", "image", "battle_lobby", "deck.png")).thumbnail((200,50),Image.BICUBIC), width=200,height=50)
           # cls.__instance.__backgroundImage = ImageTk.PhotoImage(Image.open(os.path.join(os.getcwd(), "local_storage", "image", "battle_lobby", "background.png")),width=200,height=50)
        return cls.__instance

    @classmethod
    def getInstance(cls):
        if cls.__instance is None:
            cls.__instance = cls()

        return cls.__instance

    def generateImageByDirectoryAndName(self, directoryName: str, imageName: str):
        generatedImage0 = PhotoImage(os.path.join(os.getcwd(), "../..", "local_storage", "image", directoryName, f"{imageName}.png"))
        print(f"generatedImage0: {generatedImage0.width()}")
        generatedImage = PhotoImage(f"../local_storage/image/{directoryName}/{imageName}.png")
        print(f"generatedImage: {generatedImage.width()}")
        openImage = Image.open(os.path.join(os.getcwd(), "local_storage", "image", directoryName, f"{imageName}.png"))
        print(f"openImage: {openImage}")
        openImage.thumbnail((200, 200), Image.BICUBIC)
        resultImage = ImageTk.PhotoImage(openImage, width=200, height=50)
        print(f"resultImage: {resultImage.width()}")
        return resultImage

    def initImages(self):
        self.__selectedDeckImage = self.__setImageByDirectoryAndName("battle_lobby", "deck")
        self.__unselectedDeckImage = self.__setImageByDirectoryAndName( "battle_lobby", "background")

        # openDeckImage = Image.open(os.path.join(os.getcwd(), "local_storage", "image", "battle_lobby", "deck.png"))
        # thumbnailImage = openDeckImage.copy()
        # thumbnailImage.thumbnail((300,300),)
        # self.__deckImage = ImageTk.PhotoImage(thumbnailImage)
        #
        # selectedDeckImage = Image.open(os.path.join(os.getcwd(), "local_storage", "image", "battle_lobby", "background.png"))
        # thumbnailImage2 = selectedDeckImage.copy()
        # thumbnailImage2.thumbnail((300,300))
        # self.__backgroundImage = ImageTk.PhotoImage(thumbnailImage2)

    def __setImageByDirectoryAndName(self, directoryName, imageName):
        openDeckImage = Image.open(os.path.join(os.getcwd(), "local_storage", "image", directoryName, f"{imageName}.png"))
        thumbnailImage = openDeckImage.copy()
        thumbnailImage.thumbnail((300, 300), )
        result = ImageTk.PhotoImage(thumbnailImage)
        return result



    def generateImageByName(self, imageName: str):
        generatedImage = Image.open(f"../local_storage/image/{imageName}.png")
        resultImage = ImageTk.PhotoImage(generatedImage)
        return resultImage

    def getSelectedDeckImage(self):
        return self.__selectedDeckImage

    def getUnselectedDeckImage(self):
        return self.__unselectedDeckImage
