import numpy as np

from opengl_shape.rectangle import Rectangle
from opengl_shape.shape import Shape

from PIL import Image
from OpenGL import GL

import tkinter
import unittest

from OpenGL.GL import *
from OpenGL.GLU import *
from pyopengltk import OpenGLFrame

from pre_drawed_image_manager.pre_drawed_image import PreDrawedImage


class DrawTomb(Shape):
    __pre_draw_image_instance = PreDrawedImage.getInstance()

    def __init__(self, vertices, global_translation=(0, 0), local_translation=(0, 0)):
        super().__init__(vertices, global_translation, local_translation)
        self.is_visible = True
        self.__pre_draw_image_instance.pre_draw_tomb()

    def set_visible(self, visible):
        self.is_visible = visible

    def get_visible(self):
        return self.is_visible

    def draw(self):
        if self.get_visible():
            white_rect = Rectangle(color=(1.0, 1.0, 1.0, 1.0),
                                   vertices=self.vertices,
                                   global_translation=self.global_translation,
                                   local_translation=self.local_translation)
            white_rect.draw()

            image_data = self.__pre_draw_image_instance.get_pre_draw_tomb()
            print(f"image_data = {image_data}")
            texture_ids = GL.glGenTextures(1)

            GL.glBindTexture(GL.GL_TEXTURE_2D, texture_ids)
            GL.glTexParameteri(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_MAG_FILTER, GL.GL_LINEAR)
            GL.glTexParameteri(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_MIN_FILTER, GL.GL_LINEAR)
            GL.glTexImage2D(GL.GL_TEXTURE_2D, 0, GL.GL_RGBA, image_data.shape[1], image_data.shape[0],
                            0, GL.GL_RGBA, GL.GL_UNSIGNED_BYTE, image_data)

            GL.glEnable(GL.GL_TEXTURE_2D)
            GL.glBindTexture(GL.GL_TEXTURE_2D, texture_ids)

            GL.glBegin(GL.GL_QUADS)
            GL.glTexCoord2f(0, 0)
            print(f"x: {self.vertices[0][0] + self.local_translation[0]}, y: {self.vertices[0][1] + self.local_translation[1]}")
            GL.glVertex2f(self.vertices[0][0] + self.local_translation[0] + self.global_translation[0],
                          self.vertices[0][1] + self.local_translation[1] + self.global_translation[1])

            GL.glTexCoord2f(1, 0)
            GL.glVertex2f(self.vertices[1][0] + self.local_translation[0] + self.global_translation[0],
                          self.vertices[1][1] + self.local_translation[1] + self.global_translation[1])

            GL.glTexCoord2f(1, 1)
            GL.glVertex2f(self.vertices[2][0] + self.local_translation[0] + self.global_translation[0],
                          self.vertices[2][1] + self.local_translation[1] + self.global_translation[1])

            GL.glTexCoord2f(0, 1)
            GL.glVertex2f(self.vertices[3][0] + self.local_translation[0] + self.global_translation[0],
                          self.vertices[3][1] + self.local_translation[1] + self.global_translation[1])
            GL.glEnd()

            GL.glDisable(GL.GL_TEXTURE_2D)

class PreDrawedTombFrame(OpenGLFrame):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)

        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        self.width = screen_width
        self.height = screen_height

        self.tomb = DrawTomb(vertices=[(50, 50), (200, 50), (200, 250), (50, 250)])

        self.bind("<Configure>", self.on_resize)

    def initgl(self):
        glClearColor(1.0, 1.0, 1.0, 0.0)
        glOrtho(0, self.width, self.height, 0, -1, 1)

    def reshape(self, width, height):
        print(f"Reshaping window to width={width}, height={height}")
        glViewport(0, 0, width, height)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluOrtho2D(0, width, height, 0)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

    def on_resize(self, event):
        print("Handling resize event")
        self.reshape(event.width, event.height)

    def redraw(self):
        self.tkMakeCurrent()
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        self.tomb.draw()

        self.tkSwapBuffers()



class TestPreDrawedImage(unittest.TestCase):

    def test_pre_drawed_image(self):
        root = tkinter.Tk()
        root.geometry(f"{root.winfo_screenwidth()}x{root.winfo_screenheight()}-0-0")
        root.deiconify()

        pre_drawed_tomb_frame = PreDrawedTombFrame(root)
        pre_drawed_tomb_frame.pack(fill=tkinter.BOTH, expand=1)
        root.update_idletasks()

        def animate():
            pre_drawed_tomb_frame.redraw()
            root.after(17, animate)

        root.after(0, animate)

        root.mainloop()


if __name__ == '__main__':
    unittest.main()