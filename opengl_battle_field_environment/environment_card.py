import os

from image_shape.circle_image import CircleImage
from opengl_shape.circle import Circle
from pre_drawed_image_manager.pre_drawed_image import PreDrawedImage


class EnvironmentCard():
    __pre_drawed_image_instance = PreDrawedImage.getInstance()

    def __init__(self, local_translation=(0, 0)):
        self.shapes = []
        self.local_translation = local_translation

    def change_local_translation(self, _translation):
        self.local_translation = _translation

    def get_shapes(self):
        return self.shapes

    def add_shape(self, shape):
        shape.local_translate(self.local_translation)
        self.shapes.append(shape)

    def create_environment_race_illustration_circle(self, image_data, center, radius):
        environment_race_circle = CircleImage(image_data=image_data,
                                              center=center,
                                              radius=radius)
        self.add_shape(environment_race_circle)

    def create_energy_type_illustration_circle(self, image_data, center, radius):
        environment_type_circle = CircleImage(image_data=image_data,
                                              center=center,
                                              radius=radius)
        self.add_shape(environment_type_circle)

    def init_shapes(self, circle_radius, card_number, rectangle_height, rectangle_width):

        self.create_environment_race_illustration_circle(
            image_data=self.__pre_drawed_image_instance.get_pre_draw_card_race_with_card_number(card_number),
            center=(rectangle_width, 0),
            radius=circle_radius)

        self.create_energy_type_illustration_circle(
            image_data=self.__pre_drawed_image_instance.get_pre_draw_card_type_with_card_number(card_number),
            center=(rectangle_width, rectangle_height),
            radius=circle_radius)