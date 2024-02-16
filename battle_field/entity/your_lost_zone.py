from image_shape.rectangle_image import RectangleImage
from pre_drawed_image_manager.pre_drawed_image import PreDrawedImage


class YourLostZone:
    __pre_drawed_image_instance = PreDrawedImage.getInstance()

    def __init__(self, local_translation=(0, 0), scale=1):
        self.pre_drawed_lost_zone = None
        self.shapes = []
        self.local_translation = local_translation
        self.scale = scale

    def get_lost_zone_shapes(self):
        return self.shapes

    def change_local_translation(self, _translation):
        self.local_translation = _translation

    def add_shape(self, shape):
        shape.local_translate(self.local_translation)
        self.shapes.append(shape)

    def create_lost_zone(self, image_data, vertices):
        lost_zone_illustration = RectangleImage(image_data=image_data,
                                                vertices=vertices)
        self.add_shape(lost_zone_illustration)

    def init_shapes(self):
        self.__pre_drawed_image_instance.pre_draw_your_lost_zone()
        # -1620, 300
        self.create_lost_zone(image_data=self.__pre_drawed_image_instance.get_pre_draw_your_lost_zone(),
                              vertices=[(50, 590), (250, 590), (250, 790), (50, 790)])
