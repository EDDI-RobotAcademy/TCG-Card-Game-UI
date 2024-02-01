import os
import tkinter
import unittest
from math import cos, sin, pi
from PIL import Image
import tkinter as tk
from OpenGL.GL import *
from OpenGL.GLU import *
from pyopengltk import OpenGLFrame

class ImageOvalElement(OpenGLFrame):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)

        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        self.width = screen_width
        self.height = screen_height


    def initgl(self):
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        glEnable(GL_TEXTURE_2D)
        glClearColor(0.8, 0.8, 0.8, 1.0)
        gluOrtho2D(0, self.width, 0, self.height)

        current_directory = os.getcwd()
        parent_directory = os.path.abspath(os.path.join(current_directory, os.pardir, os.pardir))
        image_path = os.path.join(parent_directory, 'local_storage', 'card_images', 'card1.png')

        image = Image.open(image_path)
        self.texture_id = self.load_texture(image)

    def redraw(self):
        self.tkMakeCurrent()

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        glBindTexture(GL_TEXTURE_2D, self.texture_id)
        glBegin(GL_TRIANGLE_FAN)
        glColor3f(1.0, 1.0, 1.0)

        radius_x = 300.0
        radius_y = 100.0

        for i in range(361):
            angle = i * pi / 180.0
            x = self.width / 2 + radius_x * cos(angle)
            y = self.height / 2 + radius_y * sin(angle)
            glTexCoord2f(0.5 + 0.5 * cos(angle), 0.5 + 0.5 * sin(angle))
            glVertex2f(x, y)

        glEnd()

        self.tkSwapBuffers()

    def load_texture(self, image):
        image_data = image.tobytes("raw", "RGB", 0, -1)

        texture_id = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, texture_id)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, image.width, image.height, 0, GL_RGB, GL_UNSIGNED_BYTE, image_data)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

        return texture_id