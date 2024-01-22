from OpenGL.GL import *
import random

from battle_field_unit_card_frame.entity.shape import Shape


class Rectangle(Shape):
    def __init__(self, color, vertices):
        super().__init__(color, vertices)

    def draw(self):
        glBegin(GL_QUADS)

        for vertex in self.vertices:
            glColor4f(*self.color)
            glVertex2f(vertex[0] + self.translation[0] + self.local_translation[0],
                       vertex[1] + self.translation[1] + self.local_translation[1])

        glEnd()

