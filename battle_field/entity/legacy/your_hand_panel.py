from image_shape.rectangle_image import RectangleImage
from pre_drawed_image_manager.pre_drawed_image import PreDrawedImage


class YourHandPanel:
    __pre_drawed_image_instance = PreDrawedImage.getInstance()

    def __init__(self, local_translation=(0, 0), scale=1):
        self.pre_drawed_your_hand = None
        self.shapes = []
        self.local_translation = local_translation
        self.scale = scale

        self.pickable_card_list = []

    def change_local_translation(self, _translation):
        self.local_translation = _translation

    def get_your_hand_panel_shapes(self):
        return self.shapes

    def get_pickable_card_list(self):
        return self.pickable_card_list

    def add_shape(self, shape):
        shape.local_translate(self.local_translation)
        self.shapes.append(shape)

    def create_hand_panel(self, image_data, vertices):
        hand_panel = RectangleImage(image_data=image_data,
                                    vertices=vertices)
        self.add_shape(hand_panel)

    def init_shapes(self):
        self.__pre_drawed_image_instance.pre_draw_your_hand_panel()

        self.create_hand_panel(image_data=self.__pre_drawed_image_instance.get_pre_draw_your_hand_panel(),
                               vertices=[(300, 830), (1600, 830), (1600, 980), (300, 980)])
