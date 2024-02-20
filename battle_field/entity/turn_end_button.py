from image_shape.rectangle_image import RectangleImage
from pre_drawed_image_manager.pre_drawed_image import PreDrawedImage


class TurnEndButton:
    __pre_drawed_image_instance = PreDrawedImage.getInstance()

    def __init__(self, local_translation=(0, 0), scale=1):
        self.shapes = []
        self.local_translation = local_translation
        self.scale = scale

    def get_turn_end_button_shapes(self):
        return self.shapes

    def change_local_translation(self, _translation):
        self.local_translation = _translation

    def add_shape(self, shape):
        shape.local_translate(self.local_translation)
        self.shapes.append(shape)

    def create_turn_end_button(self, image_data, vertices):
        turn_end_button = RectangleImage(image_data=image_data,
                                                vertices=vertices)
        self.add_shape(turn_end_button)

    def init_shapes(self):
        self.create_turn_end_button(image_data=self.__pre_drawed_image_instance.get_pre_draw_turn_end_button(),
                              vertices=[(1700, 490), (1850, 490), (1850, 590), (1700, 590)])
