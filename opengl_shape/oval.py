from OpenGL.GL import *
import math

from opengl_shape.shape import Shape


class Oval(Shape):
    def __init__(self, color, center, radius_x, radius_y, local_translation=(0, 0), global_translation=(0, 0)):
        super().__init__([center], local_translation, global_translation)
        self.color = color
        self.radius_x = radius_x
        self.radius_y = radius_y
        self.draw_border = True

    def set_draw_border(self, value):
        self.draw_border = value

    def draw(self):
        glColor4f(*self.color)
        glBegin(GL_POLYGON)
        num_segments = 100
        for i in range(num_segments):
            theta = 2.0 * math.pi * float(i) / float(num_segments)
            x = self.radius_x * math.cos(theta) + self.vertices[0][0] + self.global_translation[0] + \
                self.local_translation[0]
            y = self.radius_y * math.sin(theta) + self.vertices[0][1] + self.global_translation[1] + \
                self.local_translation[1]
            glVertex2f(x, y)
        glEnd()

        if self.draw_border:
            glLineWidth(2.0)
            glColor4f(0.0, 0.0, 0.0, 1.0)
            glBegin(GL_LINE_LOOP)
            for i in range(num_segments):
                theta = 2.0 * math.pi * float(i) / float(num_segments)
                x = self.radius_x * math.cos(theta) + self.vertices[0][0] + self.global_translation[0] + \
                    self.local_translation[0] - 1
                y = self.radius_y * math.sin(theta) + self.vertices[0][1] + self.global_translation[1] + \
                    self.local_translation[1] - 1
                glVertex2f(x, y)
            glEnd()