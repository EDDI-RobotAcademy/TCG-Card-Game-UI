from opengl_shape.shape import Shape
from OpenGL import GL

from opengl_shape.rectangle import Rectangle


class RectangleImage(Shape):
    def __init__(self, image_data, vertices, global_translation=(0, 0), local_translation=(0, 0)):
        super().__init__(vertices, global_translation, local_translation)
        self.image_data = image_data
        self.is_visible = True

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

            image_data = self.image_data
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
            GL.glBindTexture(GL.GL_TEXTURE_2D, 0)

# class RectangleImage(Shape):
#     def __init__(self, image_data, vertices, global_translation=(0, 0), local_translation=(0, 0)):
#         super().__init__(vertices, global_translation, local_translation)
#         self.image_data = image_data
#         self.texture_id = None
#         self.is_visible = True
#         self.load_texture()
#
#     def load_texture(self):
#         self.texture_id = GL.glGenTextures(1)
#         GL.glBindTexture(GL.GL_TEXTURE_2D, self.texture_id)
#         GL.glTexParameteri(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_MAG_FILTER, GL.GL_LINEAR)
#         GL.glTexParameteri(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_MIN_FILTER, GL.GL_LINEAR)
#         GL.glTexImage2D(
#             GL.GL_TEXTURE_2D, 0, GL.GL_RGBA, self.image_data.shape[1], self.image_data.shape[0],
#             0, GL.GL_RGBA, GL.GL_UNSIGNED_BYTE, self.image_data
#         )
#
#     def set_visible(self, visible):
#         self.is_visible = visible
#
#     def get_visible(self):
#         return self.is_visible
#
#     def draw(self):
#         if self.get_visible():
#             GL.glEnable(GL.GL_TEXTURE_2D)
#             GL.glBindTexture(GL.GL_TEXTURE_2D, self.texture_id)
#
#             GL.glBegin(GL.GL_QUADS)
#             GL.glTexCoord2f(0, 0)
#             GL.glVertex2f(self.vertices[0][0] + self.local_translation[0] + self.global_translation[0],
#                           self.vertices[0][1] + self.local_translation[1] + self.global_translation[1])
#
#             GL.glTexCoord2f(1, 0)
#             GL.glVertex2f(self.vertices[1][0] + self.local_translation[0] + self.global_translation[0],
#                           self.vertices[1][1] + self.local_translation[1] + self.global_translation[1])
#
#             GL.glTexCoord2f(1, 1)
#             GL.glVertex2f(self.vertices[2][0] + self.local_translation[0] + self.global_translation[0],
#                           self.vertices[2][1] + self.local_translation[1] + self.global_translation[1])
#
#             GL.glTexCoord2f(0, 1)
#             GL.glVertex2f(self.vertices[3][0] + self.local_translation[0] + self.global_translation[0],
#                           self.vertices[3][1] + self.local_translation[1] + self.global_translation[1])
#             GL.glEnd()
#
#             GL.glDisable(GL.GL_TEXTURE_2D)

# class RectangleImage(Shape):
#     def __init__(self, image_data, vertices, global_translation=(0, 0), local_translation=(0, 0)):
#         super().__init__(vertices, global_translation, local_translation)
#         self.image_data = image_data
#         self.is_visible = True
#         self.texture_id = None
#         self.initialize_texture()
#
#     def initialize_texture(self):
#         if self.texture_id is None:
#             self.texture_id = GL.glGenTextures(1)
#             GL.glBindTexture(GL.GL_TEXTURE_2D, self.texture_id)
#             GL.glTexParameteri(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_MAG_FILTER, GL.GL_LINEAR)
#             GL.glTexParameteri(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_MIN_FILTER, GL.GL_LINEAR)
#             GL.glTexImage2D(GL.GL_TEXTURE_2D, 0, GL.GL_RGBA, self.image_data.shape[1], self.image_data.shape[0],
#                             0, GL.GL_RGBA, GL.GL_UNSIGNED_BYTE, self.image_data)
#             GL.glBindTexture(GL.GL_TEXTURE_2D, 0)
#
#     def set_visible(self, visible):
#         self.is_visible = visible
#
#     def get_visible(self):
#         return self.is_visible
#
#     def draw(self):
#         if self.get_visible():
#             white_rect = Rectangle(color=(1.0, 1.0, 1.0, 1.0),
#                                    vertices=self.vertices,
#                                    global_translation=self.global_translation,
#                                    local_translation=self.local_translation)
#             white_rect.draw()
#
#             image_data = self.image_data
#             texture_ids = GL.glGenTextures(1)
#
#             GL.glBindTexture(GL.GL_TEXTURE_2D, texture_ids)
#             GL.glTexParameteri(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_MAG_FILTER, GL.GL_LINEAR)
#             GL.glTexParameteri(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_MIN_FILTER, GL.GL_LINEAR)
#             GL.glTexImage2D(GL.GL_TEXTURE_2D, 0, GL.GL_RGBA, image_data.shape[1], image_data.shape[0],
#                             0, GL.GL_RGBA, GL.GL_UNSIGNED_BYTE, image_data)
#
#             GL.glEnable(GL.GL_TEXTURE_2D)
#             GL.glBindTexture(GL.GL_TEXTURE_2D, texture_ids)
#
#             GL.glBegin(GL.GL_QUADS)
#             GL.glTexCoord2f(0, 0)
#
#             GL.glVertex2f(self.vertices[0][0] + self.local_translation[0] + self.global_translation[0],
#                           self.vertices[0][1] + self.local_translation[1] + self.global_translation[1])
#
#             GL.glTexCoord2f(1, 0)
#             GL.glVertex2f(self.vertices[1][0] + self.local_translation[0] + self.global_translation[0],
#                           self.vertices[1][1] + self.local_translation[1] + self.global_translation[1])
#
#             GL.glTexCoord2f(1, 1)
#             GL.glVertex2f(self.vertices[2][0] + self.local_translation[0] + self.global_translation[0],
#                           self.vertices[2][1] + self.local_translation[1] + self.global_translation[1])
#
#             GL.glTexCoord2f(0, 1)
#             GL.glVertex2f(self.vertices[3][0] + self.local_translation[0] + self.global_translation[0],
#                           self.vertices[3][1] + self.local_translation[1] + self.global_translation[1])
#             GL.glEnd()
#
#             GL.glDisable(GL.GL_TEXTURE_2D)
#             GL.glBindTexture(GL.GL_TEXTURE_2D, 0)

# class RectangleImage(Shape):
#     def __init__(self, image_data, vertices, global_translation=(0, 0), local_translation=(0, 0)):
#         super().__init__(vertices, global_translation, local_translation)
#         self.image_data = image_data
#         self.is_visible = True
#         self.texture_id = None
#         self.initialize_texture()
#
#     def initialize_texture(self):
#         if self.texture_id is None:
#             self.texture_id = GL.glGenTextures(1)
#             GL.glBindTexture(GL.GL_TEXTURE_2D, self.texture_id)
#             GL.glTexParameteri(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_MAG_FILTER, GL.GL_LINEAR)
#             GL.glTexParameteri(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_MIN_FILTER, GL.GL_LINEAR)
#             GL.glTexImage2D(GL.GL_TEXTURE_2D, 0, GL.GL_RGBA, self.image_data.shape[1], self.image_data.shape[0],
#                             0, GL.GL_RGBA, GL.GL_UNSIGNED_BYTE, self.image_data)
#             GL.glBindTexture(GL.GL_TEXTURE_2D, 0)
#
#     def set_visible(self, visible):
#         self.is_visible = visible
#
#     def get_visible(self):
#         return self.is_visible
#
#     def draw(self):
#         if self.get_visible():
#             white_rect = Rectangle(color=(1.0, 1.0, 1.0, 1.0),
#                                    vertices=self.vertices,
#                                    global_translation=self.global_translation,
#                                    local_translation=self.local_translation)
#             white_rect.draw()
#
#             GL.glEnable(GL.GL_TEXTURE_2D)
#             GL.glBindTexture(GL.GL_TEXTURE_2D, self.texture_id)
#
#             GL.glBegin(GL.GL_QUADS)
#             GL.glTexCoord2f(0, 0)
#             GL.glVertex2f(self.vertices[0][0] + self.local_translation[0] + self.global_translation[0],
#                           self.vertices[0][1] + self.local_translation[1] + self.global_translation[1])
#
#             GL.glTexCoord2f(1, 0)
#             GL.glVertex2f(self.vertices[1][0] + self.local_translation[0] + self.global_translation[0],
#                           self.vertices[1][1] + self.local_translation[1] + self.global_translation[1])
#
#             GL.glTexCoord2f(1, 1)
#             GL.glVertex2f(self.vertices[2][0] + self.local_translation[0] + self.global_translation[0],
#                           self.vertices[2][1] + self.local_translation[1] + self.global_translation[1])
#
#             GL.glTexCoord2f(0, 1)
#             GL.glVertex2f(self.vertices[3][0] + self.local_translation[0] + self.global_translation[0],
#                           self.vertices[3][1] + self.local_translation[1] + self.global_translation[1])
#             GL.glEnd()
#
#             GL.glDisable(GL.GL_TEXTURE_2D)
#             GL.glBindTexture(GL.GL_TEXTURE_2D, 0)
