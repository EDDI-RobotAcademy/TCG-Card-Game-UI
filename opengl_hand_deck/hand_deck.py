import os

from common.utility import get_project_root
from opengl_shape.image_element import ImageElement
from opengl_shape.rectangle import Rectangle


class HandDeck:
    __imagePath = None

    def __init__(self, local_translation=(0, 0), scale=1):
        self.shapes = []
        self.local_translation = local_translation
        self.scale = scale

    def get_hand_deck_shapes(self):
        return self.shapes
    def change_local_translation(self, _translation):
        self.local_translation = _translation

    def add_shape(self, shape):
        shape.local_translate(self.local_translation)
        self.shapes.append(shape)
    def create_hand_deck_rectangle(self, color, vertices):
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
        self.__imagePath1 = os.path.join(project_root, "local_storage", "image", "battle_field",
                                            "hand_deck1.png")
        self.__imagePath2 = os.path.join(project_root, "local_storage", "image", "battle_field",
                                            "hand_deck2.png")
        self.__imagePath3 = os.path.join(project_root, "local_storage", "image", "battle_field",
                                            "hand_deck3.png")

        self.create_hand_deck_rectangle(color=(0, 0, 0, 1.0),
                                   vertices=[(565, 860), (715, 860), (715, 1060), (565, 1060)])

        self.create_hand_deck_rectangle(color=(0, 0, 0, 1.0),
                                   vertices=[(885, 860), (1035, 860), (1035, 1060), (885, 1060)])

        self.create_hand_deck_rectangle(color=(0, 0, 0, 1.0),
                                   vertices=[(1205, 860), (1345, 860), (1345, 1060), (1205, 1060)])

        self.create_illustration(image_path=self.__imagePath1,
                                 vertices=[(565, 860), (715, 860), (715, 1010), (565, 1010)])

        self.create_illustration(image_path=self.__imagePath2,
                                 vertices=[(885, 860), (1035, 860), (1035, 1010), (885, 1010)])

        self.create_illustration(image_path=self.__imagePath3,
                                 vertices=[(1205, 860), (1345, 860), (1345, 1010), (1205, 1010)])
