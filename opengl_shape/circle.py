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
        self.center = center
        # print("Circle -> center = ", self.center)

        self.local_translation = local_translation

    def set_draw_border(self, value):
        self.draw_border = value

    def draw(self):
        # print(f"circle -> radius: {self.radius}, "
        #       # f"convert_radius: {self.radius * min(self.width_ratio, self.height_ratio) * math.cos(2.0 * math.pi * 0 / 100)}, "
        #       # f"width_ratio: {self.width_ratio}, "
        #       # f"height_ratio: {self.height_ratio}, "
        #       f"local_translation: {self.local_translation}, "
        #       f"vertices[0][0]: {self.vertices[0][0]}, "
        #       f"vertices[0][1]: {self.vertices[0][1]}, "
        #       f"center: {self.center}")
        glColor4f(*self.color)
        glBegin(GL_POLYGON)

        # print(f"circle -> x: {self.radius * min(self.width_ratio, self.height_ratio) * math.cos(2.0 * math.pi * 0 / 360) + self.vertices[0][0] * self.width_ratio + self.global_translation[0] + self.local_translation[0] * self.width_ratio - 1}, y: {self.radius * min(self.width_ratio, self.height_ratio) * math.sin(2.0 * math.pi * 0 / 360) + self.vertices[0][1] * self.height_ratio + self.global_translation[1] + self.local_translation[1] * self.height_ratio - 1}")
        # print(f"circle -> x: {self.radius * min(self.width_ratio, self.height_ratio) * math.cos(2.0 * math.pi * 0 / 360) + self.center[0] + self.local_translation[0]}, y: {self.radius * min(self.width_ratio, self.height_ratio) * math.sin(2.0 * math.pi * 0 / 360) + self.center[1] + self.local_translation[1]}")
        # print(f"circle -> x: {self.radius * min(self.width_ratio, self.height_ratio) * math.cos(2.0 * math.pi * 0 / 360) + self.center[0] * self.width_ratio + self.local_translation[0] * self.width_ratio - 1}")
        # print(f"circle -> y: {self.radius * min(self.width_ratio, self.height_ratio) * math.sin(2.0 * math.pi * 0 / 360) + self.center[1] * self.height_ratio + self.local_translation[1] * self.height_ratio - 1}")

        for i in range(100):
            theta = 2.0 * math.pi * i / 100
            # x = self.radius * min(self.width_ratio, self.height_ratio) * math.cos(theta) + self.vertices[0][0] * self.width_ratio  + self.global_translation[0] + self.local_translation[0] * self.width_ratio
            # y = self.radius * min(self.width_ratio, self.height_ratio) * math.sin(theta) + self.vertices[0][1] * self.height_ratio + self.global_translation[1] + self.local_translation[1] * self.height_ratio

            # x = self.radius * min(self.width_ratio, self.height_ratio) * math.cos(theta) + \
            #     self.vertices[0][0] * self.width_ratio + \
            #     self.global_translation[0] + \
            #     self.local_translation[0]
            #
            # y = self.radius * min(self.width_ratio, self.height_ratio) * math.sin(theta) + \
            #     self.vertices[0][1] * self.height_ratio + \
            #     self.global_translation[1] + \
            #     self.local_translation[1]

            # x = self.radius * min(self.width_ratio, self.height_ratio) * math.cos(theta) + \
            #     self.vertices[0][0] + \
            #     self.global_translation[0] + \
            #     self.local_translation[0] * self.width_ratio
            #
            # y = self.radius * min(self.width_ratio, self.height_ratio) * math.sin(theta) + \
            #     self.vertices[0][1] + \
            #     self.global_translation[1] + \
            #     self.local_translation[1] * self.height_ratio

            # x = self.radius * min(self.width_ratio, self.height_ratio) * math.cos(theta) + \
            #     self.vertices[0][0] + \
            #     self.global_translation[0] + \
            #     self.local_translation[0] * self.width_ratio
            #
            # y = self.radius * min(self.width_ratio, self.height_ratio) * math.sin(theta) + \
            #     self.vertices[0][1] + \
            #     self.global_translation[1] + \
            #     self.local_translation[1] * self.height_ratio

            # print(f"circle -> x: {x}, y: {y}")

            glVertex2f(self.radius * min(self.width_ratio, self.height_ratio) * math.cos(theta) +
                       self.center[0] * self.width_ratio +
                       self.local_translation[0] * self.width_ratio - 1,
                       self.radius * min(self.width_ratio, self.height_ratio) * math.sin(theta) +
                       self.center[1] * self.height_ratio +
                       self.local_translation[1] * self.height_ratio - 1)
        glEnd()

        if self.draw_border:
            glLineWidth(2.0)
            glColor4f(0.0, 0.0, 0.0, 1.0)
            glBegin(GL_LINE_LOOP)
            for i in range(100):
                theta = 2.0 * math.pi * i / 100
                # x = self.radius * min(self.width_ratio, self.height_ratio) * math.cos(theta) + self.vertices[0][0] * self.width_ratio  + self.global_translation[0] + self.local_translation[0] * self.width_ratio  - 1
                # y = self.radius * min(self.width_ratio, self.height_ratio) * math.sin(theta) + self.vertices[0][1] * self.height_ratio + self.global_translation[1] + self.local_translation[1] * self.height_ratio - 1
                # x = self.radius * min(self.width_ratio, self.height_ratio) * math.cos(theta) + self.vertices[0][0] * self.width_ratio  + self.global_translation[0] + self.local_translation[0] - 1
                # y = self.radius * min(self.width_ratio, self.height_ratio) * math.sin(theta) + self.vertices[0][1] * self.height_ratio + self.global_translation[1] + self.local_translation[1] - 1

                # x = self.radius * min(self.width_ratio, self.height_ratio) * math.cos(theta) + \
                #     self.vertices[0][0] * self.width_ratio + \
                #     self.global_translation[0] + \
                #     self.local_translation[0] - 1
                #
                # y = self.radius * min(self.width_ratio, self.height_ratio) * math.sin(theta) + \
                #     self.vertices[0][1] * self.height_ratio + \
                #     self.global_translation[1] + \
                #     self.local_translation[1] - 1

                # x = self.radius * min(self.width_ratio, self.height_ratio) * math.cos(theta) + \
                #     self.vertices[0][0] + \
                #     self.global_translation[0] + \
                #     self.local_translation[0] - 1
                #
                # y = self.radius * min(self.width_ratio, self.height_ratio) * math.sin(theta) + \
                #     self.vertices[0][1] + \
                #     self.global_translation[1] + \
                #     self.local_translation[1] - 1

                # print(f"circle -> x: {x}, y: {y}")

                glVertex2f(self.radius * min(self.width_ratio, self.height_ratio) * math.cos(theta) +
                           self.center[0] * self.width_ratio +
                           self.local_translation[0] * self.width_ratio - 1,
                           self.radius * min(self.width_ratio, self.height_ratio) * math.sin(theta) +
                           self.center[1] * self.height_ratio +
                           self.local_translation[1] * self.height_ratio - 1)

            glEnd()


