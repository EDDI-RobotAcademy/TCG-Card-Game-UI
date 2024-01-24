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

    def init_shapes(self, image_path1, image_path2, image_path3, image_path4, image_path5):
        self.__imagePath1 = image_path1
        self.__imagePath2 = image_path2
        self.__imagePath3 = image_path3
        self.__imagePath4 = image_path4
        self.__imagePath5 = image_path5

        self.create_card_deck_rectangle(color=(0.6, 0.4, 0.6, 1.0),
                                   vertices=[(50, 270), (200, 270), (200, 470), (50, 470)])

        self.create_card_deck_rectangle(color=(0.6, 0.4, 0.6, 1.0),
                                   vertices=[(55, 275), (205, 275), (205, 475), (55, 475)])

        self.create_card_deck_rectangle(color=(0.6, 0.4, 0.6, 1.0),
                                   vertices=[(60, 280), (210, 280), (210, 480), (60, 480)])

        self.create_card_deck_rectangle(color=(0.6, 0.4, 0.6, 1.0),
                                   vertices=[(65, 285), (215, 285), (215, 485), (65, 485)])

        self.create_card_deck_rectangle(color=(0.6, 0.4, 0.6, 1.0),
                                   vertices=[(70, 290), (220, 290), (220, 490), (70, 490)])

        self.create_illustration(image_path=self.__imagePath1,
                                 vertices=[(50, 270), (200, 270), (200, 470), (50, 470)])

        self.create_illustration(image_path=self.__imagePath2,
                                 vertices=[(55, 275), (205, 275), (205, 475), (55, 475)])

        self.create_illustration(image_path=self.__imagePath3,
                                 vertices=[(60, 280), (210, 280), (210, 480), (60, 480)])

        self.create_illustration(image_path=self.__imagePath4,
                                 vertices=[(65, 285), (215, 285), (215, 485), (65, 485)])

        self.create_illustration(image_path=self.__imagePath5,
                                 vertices=[(70, 290), (220, 290), (220, 490), (70, 490)])