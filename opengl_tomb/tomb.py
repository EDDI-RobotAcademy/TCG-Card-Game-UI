import os

from common.utility import get_project_root
from opengl_shape.image_element import ImageElement
from opengl_shape.rectangle import Rectangle


class Tomb:
    __imagePath = None

    def __init__(self, local_translation=(0, 0), scale=1):
        self.shapes = []
        self.local_translation = local_translation
        self.scale = scale

    def change_local_translation(self, _translation):
        self.local_translation = _translation

    def add_shape(self, shape):
        shape.local_translate(self.local_translation)
        self.shapes.append(shape)
    def create_tomb_rectangle(self, color, vertices):
        tomb_base = Rectangle(color=color,
                                       vertices=vertices)
        tomb_base.set_visible(False)
        self.add_shape(tomb_base)
    def init_shapes(self):
        self.create_tomb_rectangle(color=(0.6, 0.4, 0.6, 1.0),
                                                 vertices=[(0, 0), (370, 20), (370, 520), (20, 520)])