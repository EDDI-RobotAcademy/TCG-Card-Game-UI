import os
import tkinter as tk
import unittest
from math import cos, sin, pi
from OpenGL.GL import *
from OpenGL.GLUT import glutInit, glutInitDisplayMode, glutInitWindowSize, \
                        glutCreateWindow, glutDisplayFunc, glutMainLoop, \
                        glutSwapBuffers, glutIdleFunc
from OpenGL.raw.GLU import gluOrtho2D
from OpenGL.raw.GLUT import GLUT_DOUBLE, GLUT_RGB, GLUT_DEPTH
from PIL import Image

class CircleIllustrationApp:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.texture_id = None

        glutInit()
        glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
        glutInitWindowSize(width, height)
        glutCreateWindow(b'Circle Illustration App')

        glutDisplayFunc(self.redraw)
        glutIdleFunc(self.redraw)

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
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glBindTexture(GL_TEXTURE_2D, self.texture_id)
        glBegin(GL_TRIANGLE_FAN)
        glColor3f(1.0, 1.0, 1.0)

        for i in range(360):
            angle = i * pi / 180.0
            x = self.width / 2 + 100 * cos(angle)
            y = self.height / 2 + 100 * sin(angle)
            glTexCoord2f(0.5 + 0.5 * cos(angle), 0.5 + 0.5 * sin(angle))
            glVertex2f(x, y)

        glEnd()

        glutSwapBuffers()

    def load_texture(self, image):
        image_data = image.tobytes("raw", "RGB", 0, -1)

        texture_id = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, texture_id)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, image.width, image.height, 0, GL_RGB, GL_UNSIGNED_BYTE, image_data)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

        return texture_id

class TestOpenGLCircleFrame(unittest.TestCase):
    def test_opengl_text_frame(self):
        app = CircleIllustrationApp(800, 600)
        glutMainLoop()

if __name__ == '__main__':
    unittest.main()
