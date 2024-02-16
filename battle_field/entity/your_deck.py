from image_shape.rectangle_image import RectangleImage
from pre_drawed_image_manager.pre_drawed_image import PreDrawedImage


class YourDeck:
    __pre_drawed_image_instance = PreDrawedImage.getInstance()

    def __init__(self, local_translation=(0, 0), scale=1):
        self.pre_drawed_opponent_card_deck = None
        self.shapes = []
        self.local_translation = local_translation
        self.scale = scale

    def get_your_deck_shapes(self):
        return self.shapes

    def change_local_translation(self, _translation):
        self.local_translation = _translation

    def add_shape(self, shape):
        shape.local_translate(self.local_translation)
        self.shapes.append(shape)

    def create_your_card_deck(self, image_data, vertices):
        your_card_deck = RectangleImage(image_data=image_data,
                                        vertices=vertices)
        self.add_shape(your_card_deck)

    def init_shapes(self):
        self.__pre_drawed_image_instance.pre_draw_your_card_deck()

        self.create_your_card_deck(
            image_data=self.__pre_drawed_image_instance.get_pre_draw_your_card_deck(),
            vertices=[(1700, 590), (1850, 590), (1850, 790), (1700, 790)])
        self.create_your_card_deck(
            image_data=self.__pre_drawed_image_instance.get_pre_draw_your_card_deck(),
            vertices=[(1705, 595), (1855, 595), (1855, 795), (1705, 795)])
        self.create_your_card_deck(
            image_data=self.__pre_drawed_image_instance.get_pre_draw_your_card_deck(),
            vertices=[(1710, 600), (1860, 600), (1860, 800), (1710, 800)])
        self.create_your_card_deck(
            image_data=self.__pre_drawed_image_instance.get_pre_draw_your_card_deck(),
            vertices=[(1715, 605), (1865, 605), (1865, 805), (1715, 805)])
        self.create_your_card_deck(
            image_data=self.__pre_drawed_image_instance.get_pre_draw_your_card_deck(),
            vertices=[(1720, 610), (1870, 610), (1870, 810), (1720, 810)])
