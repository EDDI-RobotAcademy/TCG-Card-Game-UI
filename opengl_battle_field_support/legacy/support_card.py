import os

from card_info_from_csv.repository.card_info_from_csv_repository_impl import CardInfoFromCsvRepositoryImpl
from common.utility import get_project_root
from image_shape.circle_image import CircleImage
from opengl_shape.image_circle_element import ImageCircleElement
from pre_drawed_image_manager.pre_drawed_image import PreDrawedImage


class LegacySupportCard():
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

    def create_support_race_illustration_circle(self, image_data, center, radius):
        print(f"create_support_race_illustration_circle: {center}")
        support_race_circle = CircleImage(image_data=image_data,
                                          center=center,
                                          radius=radius)
        self.add_shape(support_race_circle)

    def create_support_type_illustration_circle(self, image_data, center, radius):
        support_type_circle = CircleImage(image_data=image_data,
                                          center=center,
                                          radius=radius)
        self.add_shape(support_type_circle)


    def init_shapes(self, circle_radius, card_number, rectangle_height, rectangle_width):

        self.create_support_race_illustration_circle(
            image_data=self.__pre_drawed_image_instance.get_pre_draw_card_race_with_card_number(card_number),
            center=(rectangle_width, 0),
            radius=circle_radius)

        self.create_support_type_illustration_circle(
            image_data=self.__pre_drawed_image_instance.get_pre_draw_card_type_with_card_number(card_number),
            center=(rectangle_width, rectangle_height),
            radius=circle_radius)