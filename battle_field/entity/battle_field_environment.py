from image_shape.rectangle_image import RectangleImage
from pre_drawed_image_manager.pre_drawed_image import PreDrawedImage


class BattleFieldEnvironment:
    __pre_drawed_image_instance = PreDrawedImage.getInstance()

    def __init__(self, local_translation=(0, 0), scale=1):
        self.shapes = []
        self.local_translation = local_translation
        self.scale = scale

    def get_environment_shapes(self):
        return self.shapes

    def change_local_translation(self, _translation):
        self.local_translation = _translation

    def add_shape(self, shape):
        shape.local_translate(self.local_translation)
        self.shapes.append(shape)

    def create_environment(self, image_data, vertices):
        environment_illustration = RectangleImage(image_data=image_data,
                                                  vertices=vertices)
        self.add_shape(environment_illustration)

    def init_shapes(self):
        self.__pre_drawed_image_instance.pre_draw_battle_field_environment()

        self.create_environment(image_data=self.__pre_drawed_image_instance.get_pre_draw_battle_field_environment(),
                                vertices=[(400, 490), (500, 490), (500, 590), (400, 590)])
