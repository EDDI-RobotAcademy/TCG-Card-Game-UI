from OpenGL.GL import *
from colorama import Fore, Style

from opengl_shape.shape import Shape


class NonBackgroundNumberImage(Shape):
    __circle_kinds = None

    def __init__(self, image_data, vertices, number, global_translation=(0, 0), local_translation=(0, 0)):
        super().__init__(vertices, global_translation, local_translation)
        self.image_data = image_data
        self.is_visible = True
        self.number = number
        self.texture_id = None
        self.texture_initialized = False

        self.rotation_angle = 0

    def update_rotation_angle(self, angle):
        self.rotation_angle = angle

    def set_visible(self, visible):
        self.is_visible = visible

    def get_visible(self):
        return self.is_visible

    def set_circle_kinds(self, circle_kinds):
        self.__circle_kinds = circle_kinds

    def get_circle_kinds(self):
        return self.__circle_kinds

    def get_number(self):
        return self.number

    def set_number(self, number):
        self.number = number

    def set_image_data(self, image_data):
        self.image_data = image_data
        self.texture_initialized = False
        self.delete_texture()

    def delete_texture(self):
        if self.texture_id is not None:
            glDeleteTextures([self.texture_id])
            self.texture_id = None

    def update_texture_with_image_data(self, image_data):
        if self.texture_id is not None:
            glDeleteTextures([self.texture_id])
            self.texture_id = None

        self.image_data = image_data
        self.draw()

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

            glPushMatrix()

            # print(f"{Fore.RED}vertices[0][0]: {Fore.GREEN} {self.vertices[0][0]}{Style.RESET_ALL}")
            # print(f"{Fore.RED}vertices[1][0]: {Fore.GREEN} {self.vertices[1][0]}{Style.RESET_ALL}")
            # print(f"{Fore.RED}vertices[2][0]: {Fore.GREEN} {self.vertices[2][0]}{Style.RESET_ALL}")
            # print(f"{Fore.RED}vertices[3][0]: {Fore.GREEN} {self.vertices[3][0]}{Style.RESET_ALL}")
            # print(f"{Fore.RED}local_translation[0]: {Fore.GREEN} {self.local_translation[0]}{Style.RESET_ALL}")
            #
            # print(f"{Fore.RED}vertices[0][1]: {Fore.GREEN} {self.vertices[0][1]}{Style.RESET_ALL}")
            # print(f"{Fore.RED}vertices[1][1]: {Fore.GREEN} {self.vertices[1][1]}{Style.RESET_ALL}")
            # print(f"{Fore.RED}vertices[2][1]: {Fore.GREEN} {self.vertices[2][1]}{Style.RESET_ALL}")
            # print(f"{Fore.RED}vertices[3][1]: {Fore.GREEN} {self.vertices[3][1]}{Style.RESET_ALL}")
            # print(f"{Fore.RED}local_translation[1]: {Fore.GREEN} {self.local_translation[1]}{Style.RESET_ALL}")
            # glTranslatef(-self.local_translation[0] * self.width_ratio,
            # glTranslatef(-self.vertices[0][0] + 5 - self.local_translation[0] * self.width_ratio,
            #              -self.vertices[0][1] * self.height_ratio + self.local_translation[1] * self.height_ratio, 0)
            # glTranslatef(-80 - 25 - self.local_translation[0] * self.width_ratio,
            #              # -self.vertices[0][1] * self.height_ratio + self.local_translation[1] * self.height_ratio,
            #              1041 - (self.vertices[0][1] * self.height_ratio + self.local_translation[1] * self.height_ratio),
            #              0)
            glRotatef(self.rotation_angle, 0, 0, 1)
            # glTranslatef(self.local_translation[0], self.local_translation[1], 0)
            # glTranslatef(-self.local_translation[0], -self.local_translation[1], 0)

            glBegin(GL_QUADS)
            glTexCoord2f(0, 0)
            glVertex2f(self.vertices[0][0] * self.width_ratio + self.local_translation[0] * self.width_ratio + self.global_translation[0],
                       self.vertices[0][1] * self.height_ratio + self.local_translation[1] * self.height_ratio + self.global_translation[1])

            glTexCoord2f(1, 0)
            glVertex2f(self.vertices[1][0] * self.width_ratio + self.local_translation[0] * self.width_ratio + self.global_translation[0],
                       self.vertices[1][1] * self.height_ratio + self.local_translation[1] * self.height_ratio + self.global_translation[1])

            glTexCoord2f(1, 1)
            glVertex2f(self.vertices[2][0] * self.width_ratio + self.local_translation[0] * self.width_ratio + self.global_translation[0],
                       self.vertices[2][1] * self.height_ratio + self.local_translation[1] * self.height_ratio + self.global_translation[1])

            glTexCoord2f(0, 1)
            glVertex2f(self.vertices[3][0] * self.width_ratio + self.local_translation[0] * self.width_ratio + self.global_translation[0],
                       self.vertices[3][1] * self.height_ratio + self.local_translation[1] * self.height_ratio + self.global_translation[1])
            glEnd()

            glPopMatrix()

            glDisable(GL_TEXTURE_2D)
            glBindTexture(GL_TEXTURE_2D, 0)

            glDisable(GL_BLEND)

