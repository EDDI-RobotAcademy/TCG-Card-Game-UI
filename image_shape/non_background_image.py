from OpenGL.GL import *

from opengl_shape.shape import Shape


class NonBackgroundImage(Shape):
    def __init__(self, image_data, vertices, global_translation=(0, 0), local_translation=(0, 0)):
        super().__init__(vertices, global_translation, local_translation)
        self.image_data = image_data
        self.is_visible = True
        self.texture_id = None
        self.texture_initialized = False

    def set_visible(self, visible):
        self.is_visible = visible

    def get_visible(self):
        return self.is_visible

    def draw(self):
        if self.get_visible():
            glEnable(GL_BLEND)
            glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

            image_data = self.image_data

            if self.texture_id is None:
                self.texture_id = glGenTextures(1)

            if not self.texture_initialized:
                glBindTexture(GL_TEXTURE_2D, self.texture_id)
                glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
                glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)

                glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, image_data.shape[1], image_data.shape[0],
                             0, GL_RGBA, GL_UNSIGNED_BYTE, image_data)
                self.texture_initialized = True

            glEnable(GL_TEXTURE_2D)
            glBindTexture(GL_TEXTURE_2D, self.texture_id)

            glBegin(GL_QUADS)
            glTexCoord2f(0, 0)
            glVertex2f(self.vertices[0][0] + self.local_translation[0] + self.global_translation[0],
                       self.vertices[0][1] + self.local_translation[1] + self.global_translation[1])

            glTexCoord2f(1, 0)
            glVertex2f(self.vertices[1][0] + self.local_translation[0] + self.global_translation[0],
                       self.vertices[1][1] + self.local_translation[1] + self.global_translation[1])

            glTexCoord2f(1, 1)
            glVertex2f(self.vertices[2][0] + self.local_translation[0] + self.global_translation[0],
                       self.vertices[2][1] + self.local_translation[1] + self.global_translation[1])

            glTexCoord2f(0, 1)
            glVertex2f(self.vertices[3][0] + self.local_translation[0] + self.global_translation[0],
                       self.vertices[3][1] + self.local_translation[1] + self.global_translation[1])
            glEnd()

            glDisable(GL_TEXTURE_2D)
            glBindTexture(GL_TEXTURE_2D, 0)

            glDisable(GL_BLEND)
