import os
import tkinter
import unittest
from tkinter import PhotoImage
from PIL import Image, ImageTk

from utility.image_generator import ImageGenerator


class testImageGenerator(unittest.TestCase):

    def test_image_generator(self):
        root = tkinter.Tk()
        script_dir = os.getcwd()
        print(script_dir)
        directory = "battle_lobby"
        image = "deck"
        generatedImage0 = PhotoImage(os.path.join(script_dir,"../..","local_storage","image",directory,image,".png"))
        print(generatedImage0)
        generatedImage = PhotoImage(f"../../local_storage/image/{directory}/{image}.png")
        print(generatedImage)
        self.assertIsNotNone(generatedImage)
        #resultImage = ImageTk.PhotoImage(generatedImage)
        #return resultImage