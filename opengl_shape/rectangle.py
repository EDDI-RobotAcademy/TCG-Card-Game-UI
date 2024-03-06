from OpenGL.GL import *
import random

from opengl_shape.shape import Shape


class Rectangle(Shape):
    __rectangle_kinds = None
    def __init__(self, color, vertices, global_translation=(0, 0), local_translation=(0, 0)):
        super().__init__(vertices, global_translation, local_translation)

        # self.width_ratio = 1
        # self.height_ratio = 1

        self.color = color
        self.draw_border = True
        self.draw_gradient = False
        self.is_visible = True

    # def set_width_ratio(self, width_ratio):
    #     self.width_ratio = width_ratio
    #
    # def set_height_ratio(self, height_ratio):
    #     self.height_ratio = height_ratio

    def set_rectangle_kinds(self, rectangle_kinds):
        self.__rectangle_kinds = rectangle_kinds

    def get_rectangle_kinds(self):
        return self.__rectangle_kinds

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

        # print(f"width_ratio: {self.width_ratio}, height_ratio: {self.height_ratio}")

        if self.draw_border:
            # print(f"width_ratio: {self.width_ratio}, height_ratio: {self.height_ratio}")
            # Draw border
            glLineWidth(2.0)
            glColor4f(0.0, 0.0, 0.0, 1.0)
            glBegin(GL_LINE_LOOP)
            glVertex2f(self.vertices[0][0] * self.width_ratio  + self.global_translation[0] + self.local_translation[0] * self.width_ratio - 1,
                       self.vertices[0][1] * self.height_ratio + self.global_translation[1] + self.local_translation[1] * self.height_ratio - 1)
            glVertex2f(self.vertices[1][0] * self.width_ratio  + self.global_translation[0] + self.local_translation[0] * self.width_ratio + 1,
                       self.vertices[1][1] * self.height_ratio + self.global_translation[1] + self.local_translation[1] * self.height_ratio - 1)
            glVertex2f(self.vertices[2][0] * self.width_ratio  + self.global_translation[0] + self.local_translation[0] * self.width_ratio + 1,
                       self.vertices[2][1] * self.height_ratio + self.global_translation[1] + self.local_translation[1] * self.height_ratio + 1)
            glVertex2f(self.vertices[3][0] * self.width_ratio  + self.global_translation[0] + self.local_translation[0] * self.width_ratio - 1,
                       self.vertices[3][1] * self.height_ratio + self.global_translation[1] + self.local_translation[1] * self.height_ratio + 1)
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
                glVertex2f(vertex[0] * self.width_ratio  + self.global_translation[0] + self.local_translation[0] * self.width_ratio,
                           vertex[1] * self.height_ratio + self.global_translation[1] + self.local_translation[1] * self.height_ratio)
        else:
            for vertex in self.vertices:
                glColor4f(*self.color)

                glVertex2f(vertex[0] * self.width_ratio  + self.global_translation[0] + self.local_translation[0] * self.width_ratio,
                           vertex[1] * self.height_ratio + self.global_translation[1] + self.local_translation[1] * self.height_ratio)

                # x = round(
                #         vertex[0] * self.width_ratio +
                #         self.global_translation[0] +
                #         self.local_translation[0] * self.width_ratio
                # )
                # y = round(
                #         vertex[1] * self.height_ratio +
                #         self.global_translation[1] +
                #         self.local_translation[1] * self.height_ratio
                # )
                # print(f"Rectangle -> x: {x}, y: {y}")
                # glVertex2f(x, y)

        glEnd()

