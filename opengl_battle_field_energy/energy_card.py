import os

from card_info_from_csv.repository.card_info_from_csv_repository_impl import CardInfoFromCsvRepositoryImpl
from image_shape.circle_image import CircleImage
from image_shape.non_background_image import NonBackgroundImage
from opengl_shape.circle import Circle
from pre_drawed_image_manager.pre_drawed_image import PreDrawedImage


class EnergyCard:
    __pre_drawed_image_instance = PreDrawedImage.getInstance()
    __card_info_from_csv_repository = CardInfoFromCsvRepositoryImpl.getInstance()

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

    def create_non_background_energy_card_type(self, image_data, center, radius):
        start_x = center[0] - radius * 1.2
        end_x = center[0] + radius * 1.2
        start_y = center[1] - radius * 1.2
        end_y = center[1] + radius * 1.2

        vertices = [
            (start_x, start_y),
            (end_x, start_y),
            (end_x, end_y),
            (start_x, end_y),
        ]

        energy_card_type_image = NonBackgroundImage(image_data=image_data,
                                                    vertices=vertices)
        energy_card_type_image.set_initial_vertices(vertices)
        self.add_shape(energy_card_type_image)

    def create_non_background_energy_card_race(self, image_data, center, radius):
        start_x = center[0] - radius * 1.2
        end_x = center[0] + radius * 1.2
        start_y = center[1] - radius * 1.2
        end_y = center[1] + radius * 1.2

        vertices = [
            (start_x, start_y),
            (end_x, start_y),
            (end_x, end_y),
            (start_x, end_y),
        ]

        energy_card_race_image = NonBackgroundImage(image_data=image_data,
                                                    vertices=vertices)
        energy_card_race_image.set_initial_vertices(vertices)
        self.add_shape(energy_card_race_image)

    def init_shapes(self, circle_radius, card_number, rectangle_height, rectangle_width):
        race_number = self.__card_info_from_csv_repository.getCardRaceForCardNumber(card_number)
        type_number = self.__card_info_from_csv_repository.getCardTypeForCardNumber(card_number)


        self.create_non_background_energy_card_type(
            image_data=self.__pre_drawed_image_instance.get_pre_draw_card_type_mark(type_number),
            center=(rectangle_width, rectangle_height),
            radius=circle_radius)

        self.create_non_background_energy_card_race(
            image_data=self.__pre_drawed_image_instance.get_pre_draw_unit_race(race_number),
            center=(rectangle_width, 0),
            radius=circle_radius)