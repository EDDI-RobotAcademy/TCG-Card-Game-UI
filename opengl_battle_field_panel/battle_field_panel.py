import os

from common.utility import get_project_root
from opengl_shape.image_rectangle_element import ImageRectangleElement
from opengl_shape.rectangle import Rectangle


class BattleFieldPanel:
    __imagePath = None

    def __init__(self, local_translation=(0, 0), scale=1):
        self.shapes = []
        self.local_translation = local_translation
        self.scale = scale

    def get_battle_field_panel_shapes(self):
        return self.shapes
    def change_local_translation(self, _translation):
        self.local_translation = _translation
    def add_shape(self, shape):
        shape.local_translate(self.local_translation)
        self.shapes.append(shape)
    def create_battle_field_panel_rectangle(self, color, vertices):
        battle_field_panel_base = Rectangle(color=color,
                                       vertices=vertices)
        battle_field_panel_base.set_visible(True)
        self.add_shape(battle_field_panel_base)

    def create_illustration(self, image_path, vertices):
        battle_field_panel_illustration = ImageRectangleElement(image_path=image_path,
                                         vertices=vertices)
        self.add_shape(battle_field_panel_illustration)

    def init_shapes(self):
        project_root = get_project_root()

        self.create_battle_field_panel_rectangle(color=(0, 0, 0, 1.0),
                                   vertices=[(0, 0), (1920, 0), (1920, 1080), (0, 1080)])

        self.create_illustration(image_path=os.path.join(project_root, "local_storage", "image", "battle_field", "battle_field_panel.png"),
                                 vertices=[(0, 0), (1920, 0), (1920, 1080), (0, 1080)])

