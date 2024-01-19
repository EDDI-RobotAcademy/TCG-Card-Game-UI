import os
import tkinter
from tkinter import PhotoImage
from PIL import ImageTk, Image


class ImageGenerator:
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

    def generateImageByDirectoryAndName(self, directoryName: str, imageName: str):
        generatedImage0 = PhotoImage(os.path.join(os.getcwd(), "../..", "local_storage", "image", directoryName, f"{imageName}.png"))
        print(f"generatedImage0: {generatedImage0.width()}")
        generatedImage = PhotoImage(f"../local_storage/image/{directoryName}/{imageName}.png")
        print(f"generatedImage: {generatedImage}")
        return generatedImage

    def generateImageByName(self, imageName: str):
        generatedImage = Image.open(f"../local_storage/image/{imageName}.png")
        resultImage = ImageTk.PhotoImage(generatedImage)
        return resultImage
