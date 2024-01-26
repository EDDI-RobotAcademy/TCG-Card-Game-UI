import os

from common.utility import get_project_root
from opengl_shape.image_element import ImageElement
from opengl_shape.rectangle import Rectangle


class CardDeck:
    __imagePath = None

    def __init__(self, local_translation=(0, 0), scale=1):
        self.shapes = []
        self.local_translation = local_translation
        self.scale = scale

    def get_card_deck_shapes(self):
        return self.shapes
    def change_local_translation(self, _translation):
        self.local_translation = _translation

    def add_shape(self, shape):
        shape.local_translate(self.local_translation)
        self.shapes.append(shape)
    def create_card_deck_rectangle(self, color, vertices):
        tomb_base = Rectangle(color=color,
                                       vertices=vertices)
        tomb_base.set_visible(True)
        self.add_shape(tomb_base)

    def create_illustration(self, image_path, vertices):
        unit_illustration = ImageElement(image_path=image_path,
                                         vertices=vertices)
        self.add_shape(unit_illustration)

    def init_opponent_shapes(self):
        project_root = get_project_root()
        self.__imagePath = os.path.join(project_root, "local_storage", "image", "battle_field",
                                            "opponent_card_deck.png")
        self.create_card_deck_rectangle(color=(0, 0, 0, 1.0),
                                   vertices=[(50, 270), (200, 270), (200, 470), (50, 470)])

        self.create_card_deck_rectangle(color=(0, 0, 0, 1.0),
                                   vertices=[(55, 275), (205, 275), (205, 475), (55, 475)])

        self.create_card_deck_rectangle(color=(0, 0, 0, 1.0),
                                   vertices=[(60, 280), (210, 280), (210, 480), (60, 480)])

        self.create_card_deck_rectangle(color=(0, 0, 0, 1.0),
                                   vertices=[(65, 285), (215, 285), (215, 485), (65, 485)])

        self.create_card_deck_rectangle(color=(0, 0, 0, 1.0),
                                   vertices=[(70, 290), (220, 290), (220, 490), (70, 490)])

        self.create_illustration(image_path=self.__imagePath,
                                 vertices=[(50, 270), (200, 270), (200, 470), (50, 470)])

        self.create_illustration(image_path=self.__imagePath,
                                 vertices=[(55, 275), (205, 275), (205, 475), (55, 475)])

        self.create_illustration(image_path=self.__imagePath,
                                 vertices=[(60, 280), (210, 280), (210, 480), (60, 480)])

        self.create_illustration(image_path=self.__imagePath,
                                 vertices=[(65, 285), (215, 285), (215, 485), (65, 485)])

        self.create_illustration(image_path=self.__imagePath,
                                 vertices=[(70, 290), (220, 290), (220, 490), (70, 490)])

    def init_your_shapes(self):
        project_root = get_project_root()
        self.__imagePath = os.path.join(project_root, "local_storage", "image", "battle_field",
                                            "your_card_deck.png")

        self.create_card_deck_rectangle(color=(0, 0, 0, 1.0),
                                   vertices=[(1700, 590), (1850, 590), (1850, 790), (1700, 790)])

        self.create_card_deck_rectangle(color=(0, 0, 0, 1.0),
                                   vertices=[(1705, 595), (1855, 595), (1855, 795), (1705, 795)])

        self.create_card_deck_rectangle(color=(0, 0, 0, 1.0),
                                   vertices=[(1710, 600), (1860, 600), (1860, 800), (1710, 800)])

        self.create_card_deck_rectangle(color=(0, 0, 0, 1.0),
                                   vertices=[(1715, 605), (1865, 605), (1865, 805), (1715, 805)])

        self.create_card_deck_rectangle(color=(0, 0, 0, 1.0),
                                   vertices=[(1720, 610), (1870, 610), (1870, 810), (1720, 810)])

        self.create_illustration(image_path=self.__imagePath,
                                 vertices=[(1700, 590), (1850, 590), (1850, 790), (1700, 790)])

        self.create_illustration(image_path=self.__imagePath,
                                 vertices=[(1705, 595), (1855, 595), (1855, 795), (1705, 795)])

        self.create_illustration(image_path=self.__imagePath,
                                 vertices=[(1710, 600), (1860, 600), (1860, 800), (1710, 800)])

        self.create_illustration(image_path=self.__imagePath,
                                 vertices=[(1715, 605), (1865, 605), (1865, 805), (1715, 805)])

        self.create_illustration(image_path=self.__imagePath,
                                 vertices=[(1720, 610), (1870, 610), (1870, 810), (1720, 810)])