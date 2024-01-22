from OpenGL.GL import *

from opengl_shape.entity.shape import Shape


class Rectangle(Shape):
    def __init__(self, color, vertices):
        super().__init__(color, vertices)

