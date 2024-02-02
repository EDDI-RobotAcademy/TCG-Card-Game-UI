import math
from math import cos, sin, pi
from OpenGL import GL
from PIL import Image
from OpenGL.GL import *
from opengl_shape.oval import Oval
from opengl_shape.shape import Shape


class ImageOvalElement(Shape):
    def __init__(self, image_path, center, radius_x, radius_y, global_translation=(0, 0), local_translation=(0, 0)):
        super().__init__([center], global_translation, local_translation)
        self.radius_x = radius_x
        self.radius_y = radius_y
        self.center = center
        self.image_path = image_path
        self.is_visible = True

    def set_visible(self, visible):
        self.is_visible = visible

    def get_visible(self):
        return self.is_visible

    def draw(self):
        if self.get_visible():
            white_oval = Oval(color=(1.0, 1.0, 1.0, 1.0),
                              center=self.center,
                              radius_x=self.radius_x,
                              radius_y=self.radius_y,
                              local_translation=self.local_translation,
                              global_translation=self.global_translation)
            white_oval.draw()

            image_data = self.load_image_date(self.image_path)
            print(f"image_data{image_data}")

            GL.glEnable(GL.GL_TEXTURE_2D)
            GL.glBindTexture(GL.GL_TEXTURE_2D, image_data)

            glBegin(GL_TRIANGLE_FAN)
            glColor3f(1.0, 1.0, 1.0)

            for i in range(361):
                angle = i * pi / 180.0
                x = self.radius_x * math.cos(angle) + self.vertices[0][0] + self.global_translation[0] + \
                    self.local_translation[0] - 1
                y = self.radius_y * math.sin(angle) + self.vertices[0][1] + self.global_translation[1] + \
                    self.local_translation[1] - 1
                glTexCoord2f(0.5 + 0.5 * cos(angle), 0.5 + 0.5 * sin(angle))
                glVertex2f(x, y)
            glEnd()
            GL.glDisable(GL.GL_TEXTURE_2D)

    def load_image_date(self, image_path):
        image = Image.open(image_path)
        width, height = image.size
        image_data = image.tobytes("raw", "RGB", 0, 0)
        texture_id = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, texture_id)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, width, height, 0, GL_RGB, GL_UNSIGNED_BYTE, image_data)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

        return texture_id

    # def crop_center(self, original_image, width, height):
    #     left = (original_image.width - width) // 2 + 24
    #     top = (original_image.height - height) // 2 - 312
    #     right = left + width
    #     bottom = top + height
    #
    #     cropped_image = original_image.crop((left, top, right, bottom))
    #
    #     return cropped_image
