from OpenGL.GL import *
import math

from opengl_shape.shape import Shape


class Circle(Shape):
    def __init__(self, color, center, radius, local_translation=(0, 0), global_translation=(0, 0)):
        super().__init__([center], local_translation, global_translation)
        self.color = color
        self.radius = radius
        self.draw_border = True
        self.set_initial_vertices([center])

    def set_draw_border(self, value):
        self.draw_border = value

    def draw(self):
        glColor4f(*self.color)
        glBegin(GL_POLYGON)
        for i in range(100):
            theta = 2.0 * math.pi * i / 100
            x = self.radius * math.cos(theta) + self.vertices[0][0] + self.global_translation[0] + self.local_translation[0]
            y = self.radius * math.sin(theta) + self.vertices[0][1] + self.global_translation[1] + self.local_translation[1]
            glVertex2f(x, y)
        glEnd()

        if self.draw_border:
            glLineWidth(2.0)
            glColor4f(0.0, 0.0, 0.0, 1.0)
            glBegin(GL_LINE_LOOP)
            for i in range(100):
                theta = 2.0 * math.pi * i / 100
                x = self.radius * math.cos(theta) + self.vertices[0][0] + self.global_translation[0] + self.local_translation[0] - 1
                y = self.radius * math.sin(theta) + self.vertices[0][1] + self.global_translation[1] + self.local_translation[1] - 1
                glVertex2f(x, y)
            glEnd()


