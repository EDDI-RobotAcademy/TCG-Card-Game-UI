import os

from common.utility import get_project_root
from opengl_shape.image_element import ImageElement
from opengl_shape.rectangle import Rectangle


class Environment:
    __imagePath = None

    def __init__(self, local_translation=(0, 0), scale=1):
        self.shapes = []
        self.local_translation = local_translation
        self.scale = scale

    def get_environment_shapes(self):
        return self.shapes
    def change_local_translation(self, _translation):
        self.local_translation = _translation

    def add_shape(self, shape):
        shape.local_translate(self.local_translation)
        self.shapes.append(shape)
    def create_environment_rectangle(self, color, vertices):
        tomb_base = Rectangle(color=color,
                                       vertices=vertices)
        tomb_base.set_visible(True)
        self.add_shape(tomb_base)

    def create_illustration(self, image_path, vertices):
        unit_illustration = ImageElement(image_path=image_path,
                                         vertices=vertices)
        self.add_shape(unit_illustration)

    def init_shapes(self):
        project_root = get_project_root()
        self.__image_path = os.path.join(project_root, "local_storage", "image", "battle_field", "environment.jpeg")
        self.create_environment_rectangle(color=(0, 0, 0, 1.0),
                                   vertices=[(400, 490), (500, 490), (500, 590), (400, 590)])

        self.create_illustration(self.__image_path,
                                 vertices=[(400, 490), (500, 490), (500, 590), (400, 590)])