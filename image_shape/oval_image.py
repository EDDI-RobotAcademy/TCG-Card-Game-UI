import math

from opengl_shape.oval import Oval
from opengl_shape.shape import Shape
from OpenGL import GL

from OpenGL.GL import *


class OvalImage(Shape):
    def __init__(self, image_data, center, radius_x, radius_y, global_translation=(0, 0), local_translation=(0, 0)):
        super().__init__([center], global_translation, local_translation)
        self.radius_x = radius_x
        self.radius_y = radius_y
        self.center = center
        self.image_data = image_data
        self.is_visible = True
        self.texture_id = None

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

            image_info = self.image_data

            if image_info is not None:
                width, height, image_data = image_info

                if self.texture_id is None:
                    self.texture_id = glGenTextures(1)
                    glBindTexture(GL.GL_TEXTURE_2D, self.texture_id)
                    glTexImage2D(GL.GL_TEXTURE_2D, 0, GL.GL_RGB, width, height, 0, GL.GL_RGB, GL.GL_UNSIGNED_BYTE,
                                 image_data)
                    glTexParameteri(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_MIN_FILTER, GL.GL_LINEAR)
                    glTexParameteri(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_MAG_FILTER, GL.GL_LINEAR)

                GL.glEnable(GL.GL_TEXTURE_2D)
                GL.glBindTexture(GL.GL_TEXTURE_2D, self.texture_id)

                glBegin(GL_TRIANGLE_FAN)
                glColor3f(1.0, 1.0, 1.0)

                for i in range(361):
                    angle = i * math.pi / 180.0
                    x = self.radius_x * math.cos(angle) + self.center[0] + self.global_translation[0] + \
                        self.local_translation[0] - 1
                    y = self.radius_y * math.sin(angle) + self.center[1] + self.global_translation[1] + \
                        self.local_translation[1] - 1
                    glTexCoord2f(0.5 + 0.5 * math.cos(angle), 0.5 + 0.5 * math.sin(angle))
                    glVertex2f(x, y)

                glEnd()
                GL.glDisable(GL.GL_TEXTURE_2D)
                