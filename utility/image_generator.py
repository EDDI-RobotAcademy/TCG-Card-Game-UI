import os
import random
import tkinter
from tkinter import PhotoImage
from PIL import ImageTk, Image

from card_info_from_csv.repository.card_info_from_csv_repository_impl import CardInfoFromCsvRepositoryImpl
from common.card_grade import CardGrade
from common.utility import get_project_root


class ImageGenerator:
    __instance = None
    __selectedDeckImage = None
    __unselectedDeckImage = None
    __randomCardImage = []

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
        generatedImage0 = PhotoImage(
            os.path.join(os.getcwd(), "../..", "local_storage", "image", directoryName, f"{imageName}.png"))
        print(f"generatedImage0: {generatedImage0.width()}")
        generatedImage = PhotoImage(f"../local_storage/image/{directoryName}/{imageName}.png")
        print(f"generatedImage: {generatedImage.width()}")
        openImage = Image.open(os.path.join(os.getcwd(), "local_storage", "image", directoryName, f"{imageName}.png"))
        print(f"openImage: {openImage}")
        openImage.thumbnail((200, 200), Image.BICUBIC)
        resultImage = ImageTk.PhotoImage(openImage, width=200, height=50)
        print(f"resultImage: {resultImage.width()}")
        return resultImage

    def generateCardImageByName(self, imageName: str):
        print(f"imageName: {imageName}")
        openImage = Image.open(os.path.join(os.getcwd(), "local_storage", "card_images", f"{imageName}.png"))
        resizedImage = openImage.resize((256, 256))
        resultImage = ImageTk.PhotoImage(resizedImage)

        return resultImage

    def initImages(self):
        self.__selectedDeckImage = self.__setImageByDirectoryAndName("battle_lobby", "deck")
        self.__unselectedDeckImage = self.__setImageByDirectoryAndName("battle_lobby", "background")
        csv_repository = CardInfoFromCsvRepositoryImpl.getInstance()
        for card_number in csv_repository.getCardNumber():
            if csv_repository.getCardGradeForCardNumber(card_number) == CardGrade.MYTHICAL.value:
                self.__randomCardImage.append(self.generateCardImageByName(str(card_number)))
                #card_illustration_image_data = os.path.join(get_project_root(), "local_storage", "card_images", f"{card_number}.png")



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
        openDeckImage = Image.open(
            os.path.join(os.getcwd(), "local_storage", "image", directoryName, f"{imageName}.png"))
        # openDeckImage = Image.open(os.path.join(os.getcwd(), "../../../local_storage", "image", directoryName, f"{imageName}.png"))
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

    def getRandomCardImage(self):
        return self.__randomCardImage[random.randrange(0, len(self.__randomCardImage) - 1)]
