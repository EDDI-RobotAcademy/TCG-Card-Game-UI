from OpenGL.GL import *
import math

from battle_field_unit_card_frame.entity.shape import Shape


class Circle(Shape):
    def __init__(self, color, center, radius, translation=(0, 0)):
        super().__init__(color, [center], translation)
        self.radius = radius
        self.draw_border = True

    def set_draw_border(self, value):
        self.draw_border = value

    def draw(self):
        glColor4f(*self.color)
        glBegin(GL_POLYGON)
        for i in range(100):
            theta = 2.0 * math.pi * i / 100
            x = self.radius * math.cos(theta) + self.vertices[0][0] + self.translation[0]
            y = self.radius * math.sin(theta) + self.vertices[0][1] + self.translation[1]
            glVertex2f(x, y)
        glEnd()

        if self.draw_border:
            glLineWidth(2.0)
            glColor4f(0.0, 0.0, 0.0, 1.0)
            glBegin(GL_LINE_LOOP)
            for i in range(100):
                theta = 2.0 * math.pi * i / 100
                x = self.radius * math.cos(theta) + self.vertices[0][0] + self.translation[0] - 1
                y = self.radius * math.sin(theta) + self.vertices[0][1] + self.translation[1] - 1
                glVertex2f(x, y)
            glEnd()
