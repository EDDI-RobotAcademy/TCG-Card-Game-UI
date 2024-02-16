from image_shape.rectangle_image import RectangleImage
from pre_drawed_image_manager.pre_drawed_image import PreDrawedImage


class OpponentTomb:
    __pre_drawed_image_instance = PreDrawedImage.getInstance()

    def __init__(self, local_translation=(0, 0), scale=1):
        self.pre_drawed_tomb = None
        self.shapes = []
        self.local_translation = local_translation
        self.scale = scale

    def get_tomb_shapes(self):
        return self.shapes

    def change_local_translation(self, _translation):
        self.local_translation = _translation

    def add_shape(self, shape):
        shape.local_translate(self.local_translation)
        self.shapes.append(shape)

    def create_tomb(self, image_data, vertices):
        tomb_illustration = RectangleImage(image_data=image_data,
                                           vertices=vertices)
        self.add_shape(tomb_illustration)

    def init_shapes(self):
        self.__pre_drawed_image_instance.pre_draw_opponent_tomb()

        self.create_tomb(image_data=self.__pre_drawed_image_instance.get_pre_draw_opponent_tomb(),
                         vertices=[(50, 50), (200, 50), (200, 250), (50, 250)])