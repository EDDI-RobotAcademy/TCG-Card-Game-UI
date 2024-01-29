from OpenGL.GL import *
import random

from tests.battle_field_unit_card_frame.entity.shape import Shape


class Rectangle(Shape):
    def __init__(self, color, vertices, translation=(0, 0), local_translation=(0, 0)):
        super().__init__(color, vertices, translation, local_translation)
        self.draw_border = True
        self.draw_gradient = False
        self.is_visible = True

    def set_visible(self, visible):
        self.is_visible = visible

    def get_visible(self):
        return self.is_visible

    def set_draw_border(self, value):
        self.draw_border = value

    def set_draw_gradient(self, value):
        self.draw_gradient = value

    def draw(self):
        if not self.is_visible:
            return

        if self.draw_border:
            # Draw border
            glLineWidth(2.0)
            glColor4f(0.0, 0.0, 0.0, 1.0)
            glBegin(GL_LINE_LOOP)
            glVertex2f(self.vertices[0][0] + self.translation[0] + self.local_translation[0] - 1,
                       self.vertices[0][1] + self.translation[1] + self.local_translation[1] - 1)
            glVertex2f(self.vertices[1][0] + self.translation[0] + self.local_translation[0] + 1,
                       self.vertices[1][1] + self.translation[1] + self.local_translation[1]  - 1)
            glVertex2f(self.vertices[2][0] + self.translation[0] + self.local_translation[0]  + 1,
                       self.vertices[2][1] + self.translation[1] + self.local_translation[1]  + 1)
            glVertex2f(self.vertices[3][0] + self.translation[0] + self.local_translation[0]  - 1,
                       self.vertices[3][1] + self.translation[1] + self.local_translation[1]  + 1)
            glEnd()

        glBegin(GL_QUADS)

        if self.draw_gradient:
            color_variation = random.uniform(1.7, 2.9)
            colored_border = [c * color_variation for c in self.color]

            for i, vertex in enumerate(self.vertices):
                gradient_factor = i / (len(self.vertices) - 1)  # Normalize to [0, 1]
                interpolated_color = [c * (1.0 - gradient_factor) + rc * gradient_factor for c, rc in
                                      zip(self.color, colored_border)]

                glColor4f(*interpolated_color)
                glVertex2f(vertex[0] + self.translation[0] + self.local_translation[0],
                           vertex[1] + self.translation[1] + self.local_translation[1])
        else:
            for vertex in self.vertices:
                glColor4f(*self.color)
                glVertex2f(vertex[0] + self.translation[0] + self.local_translation[0],
                           vertex[1] + self.translation[1] + self.local_translation[1])

        glEnd()

