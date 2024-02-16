import math

from image_shape.oval_image import OvalImage
from pre_drawed_image_manager.pre_drawed_image import PreDrawedImage


class YourMainCharacter:
    __pre_drawed_image_instance = PreDrawedImage.getInstance()

    def __init__(self, local_translation=(0, 0), scale=1):
        self.pre_drawed_main_character = None
        self.shapes = []
        self.local_translation = local_translation
        self.scale = scale

    def change_main_character_translation(self, _translation):
        self.local_translation = _translation

    def get_main_character_shapes(self):
        return self.shapes

    def add_shape(self, shape):
        shape.local_translate(self.local_translation)
        self.shapes.append(shape)

    def create_main_character(self, image_data, center, radius_x, radius_y):
        main_character_illustration = OvalImage(image_data=image_data,
                                                center=center,
                                                radius_x=radius_x,
                                                radius_y=radius_y)
        print(f"main_character_illustration{main_character_illustration}")
        print(type(main_character_illustration))
        self.add_shape(main_character_illustration)

    def init_your_main_character_shapes(self):
        radius_y = 40
        radius_x = radius_y * ((1 + math.sqrt(5)) / 2)
        self.__pre_drawed_image_instance.pre_draw_your_main_character()

        self.create_main_character(image_data=self.__pre_drawed_image_instance.get_pre_draw_your_main_character(),
                                   center=(960, 1034),
                                   radius_x=radius_x,
                                   radius_y=radius_y)
