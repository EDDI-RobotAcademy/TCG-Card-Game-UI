import pygame
from OpenGL.GL import glDrawPixels
from OpenGL.raw.GL.VERSION.GL_1_0 import GL_UNSIGNED_BYTE, GL_RGBA
from OpenGL.raw.GL.VERSION.GL_1_4 import glWindowPos2d

from opengl_shape.rectangle import Rectangle


class UnitCardAbility:
    def __init__(self, local_translation=(0, 0)):
        self.shapes = []
        self.passive_list = []
        self.skill_list = []
        self.local_translation = local_translation

    def get_unit_shapes(self):
        return self.shapes

    def add_shape(self, shape):
        shape.local_translate(self.local_translation)
        self.shapes.append(shape)

    def create_card_ability_rectangle(self, color, vertices):
        unit_card_ability = Rectangle(color=color,
                                      vertices=vertices)
        unit_card_ability.set_draw_gradient(True)
        self.add_shape(unit_card_ability)

    def drawText(self, x, y, text):
        font = pygame.font.SysFont('arial', 64)
        textSurface = font.render(text, True, (125, 125, 125, 255)).convert_alpha()
        textData = pygame.image.tostring(textSurface, "RGBA", True)
        glWindowPos2d(x - textSurface.get_width() / 2, y - textSurface.get_height() / 2)
        glDrawPixels(textSurface.get_width(), textSurface.get_height(), GL_RGBA,
                     GL_UNSIGNED_BYTE, textData)

    def init_shapes(self):
        self.create_card_ability_rectangle(color=(0.0, 0.78, 0.34, 1.0),
                                           vertices=[(0, 0), (350, 0), (350, 500), (0, 500)])