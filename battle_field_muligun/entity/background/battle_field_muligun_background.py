from screeninfo import get_monitors

from image_shape.rectangle_image import RectangleImage
from pre_drawed_image_manager.pre_drawed_image import PreDrawedImage


class BattleFieldMuligunBackground:
    __pre_drawed_image_instance = PreDrawedImage.getInstance()

    def __init__(self, local_translation=(0, 0), scale=1):
        self.shapes = []
        self.local_translation = local_translation
        self.scale = scale

    def get_battle_field_muligun_background_shape_list(self):
        print(f"get_battle_field_muligun_background_shape_list(): {self.shapes}")
        return self.shapes

    def change_local_translation(self, _translation):
        self.local_translation = _translation

    def add_shape(self, shape):
        shape.local_translate(self.local_translation)
        self.shapes.append(shape)

    def create_battle_field_muligun_background(self, image_data, vertices):
        tomb_illustration = RectangleImage(image_data=image_data,
                                           vertices=vertices)
        self.add_shape(tomb_illustration)

    def init_shapes(self, width, height):
        print(f"muligun_background init_shapes() -> width: {width}, height: {height}")

        self.__pre_drawed_image_instance.pre_draw_battle_field_muligun_background(width, height)
        # print(f"background: {self.__pre_drawed_image_instance.get_pre_draw_battle_field_muligun_background()}")

        self.create_battle_field_muligun_background(image_data=self.__pre_drawed_image_instance.get_pre_draw_battle_field_muligun_background(),
                                                    vertices=[
                                                        (0, 0),
                                                        (width, 0),
                                                        (width, height),
                                                        (0, height)
                                                    ])
