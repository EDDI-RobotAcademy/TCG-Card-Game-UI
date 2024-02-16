from OpenGL import GL
from PIL import Image
import numpy as np

class MyCardFrameRenderer:
    def __init__(self, scene, window):
        self.scene = scene
        self.window = window

    def render(self):
        self.window.tkMakeCurrent()
        GL.glClear(GL.GL_COLOR_BUFFER_BIT | GL.GL_DEPTH_BUFFER_BIT)

        for shape in self.scene.shapes:
            self._render_shape(shape)

        for image in self.scene.images:
            self._render_image(image)

        self.window.tkSwapBuffers()

    def _render_shape(self, shape):
        shape.draw()

    def _render_image(self, image):
        if image.get_visible():
            #white_rect = Rectangle(color=(1.0, 1.0, 1.0, 1.0),
            #                        vertices=[(0, 0), (image.size[0], 0), (image.size[0], image.size[1]),
            #                                  (0, image.size[1])],
            #                        translation=(
            #                        image.position[0] + image.translation[0], image.position[1] + image.translation[1]))
            # white_rect.draw()
            #
            # image_data = self._load_image_data(image.path)
            # texture_ids = GL.glGenTextures(1)
            #
            # GL.glBindTexture(GL.GL_TEXTURE_2D, texture_ids)
            # GL.glTexParameteri(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_MAG_FILTER, GL.GL_LINEAR)
            # GL.glTexParameteri(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_MIN_FILTER, GL.GL_LINEAR)
            # GL.glTexImage2D(GL.GL_TEXTURE_2D, 0, GL.GL_RGBA, image_data.shape[1], image_data.shape[0],
            #                 0, GL.GL_RGBA, GL.GL_UNSIGNED_BYTE, image_data)
            #
            # GL.glEnable(GL.GL_TEXTURE_2D)
            # GL.glBindTexture(GL.GL_TEXTURE_2D, texture_ids)
            # glColor4f(1.0, 0.0, 0.0, 1.0)
            GL.glBegin(GL.GL_QUADS)
            GL.glTexCoord2f(0, 0)
            GL.glVertex2f(image.position[0] + image.translation[0], image.position[1] + image.translation[1])
            GL.glTexCoord2f(1, 0)
            GL.glVertex2f(image.position[0] + image.size[0] + image.translation[0],
                          image.position[1] + image.translation[1])
            GL.glTexCoord2f(1, 1)
            GL.glVertex2f(image.position[0] + image.size[0] + image.translation[0],
                          image.position[1] + image.size[1] + image.translation[1])
            GL.glTexCoord2f(0, 1)
            GL.glVertex2f(image.position[0] + image.translation[0],
                          image.position[1] + image.size[1] + image.translation[1])
            GL.glEnd()

            # GL.glDisable(GL.GL_TEXTURE_2D)

    # def _load_image_data(self, path):
    #     image = Image.open(path)
    #     resized_image = image.resize((300, 300))
    #
    #     rgba_image = resized_image.convert("RGBA")
    #     img_data = np.array(rgba_image)
    #
    #     return img_data
