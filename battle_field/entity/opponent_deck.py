from image_shape.rectangle_image import RectangleImage
from pre_drawed_image_manager.pre_drawed_image import PreDrawedImage


class OpponentDeck:
    __pre_drawed_image_instance = PreDrawedImage.getInstance()

    def __init__(self, local_translation=(0, 0), scale=1):
        self.pre_drawed_opponent_card_deck = None
        self.shapes = []
        self.local_translation = local_translation
        self.scale = scale

    def get_opponent_deck_shapes(self):
        return self.shapes

    def change_local_translation(self, _translation):
        self.local_translation = _translation

    def add_shape(self, shape):
        shape.local_translate(self.local_translation)
        self.shapes.append(shape)

    def create_opponent_card_deck(self, image_data, vertices):
        opponent_card_deck = RectangleImage(image_data=image_data,
                                            vertices=vertices)
        self.add_shape(opponent_card_deck)

    def init_shapes(self):
        self.__pre_drawed_image_instance.pre_draw_opponent_card_deck()

        self.create_opponent_card_deck(image_data=self.__pre_drawed_image_instance.get_pre_draw_opponent_card_deck(),
                                       vertices=[(50, 270), (200, 270), (200, 470), (50, 470)])
        self.create_opponent_card_deck(image_data=self.__pre_drawed_image_instance.get_pre_draw_opponent_card_deck(),
                                       vertices=[(55, 275), (205, 275), (205, 475), (55, 475)])
        self.create_opponent_card_deck(image_data=self.__pre_drawed_image_instance.get_pre_draw_opponent_card_deck(),
                                       vertices=[(60, 280), (210, 280), (210, 480), (60, 480)])
        self.create_opponent_card_deck(image_data=self.__pre_drawed_image_instance.get_pre_draw_opponent_card_deck(),
                                       vertices=[(65, 285), (215, 285), (215, 485), (65, 485)])
        self.create_opponent_card_deck(image_data=self.__pre_drawed_image_instance.get_pre_draw_opponent_card_deck(),
                                       vertices=[(70, 290), (220, 290), (220, 490), (70, 490)])