import os

from card_info_from_csv.repository.card_info_from_csv_repository_impl import CardInfoFromCsvRepositoryImpl
from common.utility import get_project_root
from opengl_shape.image_circle_element import ImageCircleElement


class SupportCard():
    __imagePath = None

    def __init__(self, local_translation=(0, 0)):
        self.shapes = []
        self.local_translation = local_translation
        self.cardInfoFromCsvRepositoryImpl = CardInfoFromCsvRepositoryImpl()

    def change_local_translation(self, _translation):
        self.local_translation = _translation

    def get_shapes(self):
        return self.shapes

    def add_shape(self, shape):
        shape.local_translate(self.local_translation)
        self.shapes.append(shape)

    def create_support_race_illustration_circle(self, image_path, center, radius):
        support_race_circle = ImageCircleElement(image_path=image_path,
                                                 center=center,
                                                 radius=radius)
        self.add_shape(support_race_circle)

    def create_support_type_illustration_circle(self, image_path, center, radius):
        support_type_circle = ImageCircleElement(image_path=image_path,
                                                 center=center,
                                                 radius=radius)
        self.add_shape(support_type_circle)


    def init_shapes(self, circle_radius, card_number, rectangle_height, rectangle_width):
        project_root = get_project_root()

        self.create_support_race_illustration_circle(
            image_path=os.path.join(project_root, "local_storage", "card_race_image",
                                    f"{self.cardInfoFromCsvRepositoryImpl.getCardRaceForCardNumber(card_number)}.png"),
            center=(rectangle_width, 0),
            radius=circle_radius)

        self.create_support_type_illustration_circle(
            image_path=os.path.join(project_root, "local_storage", "card_type_image",
                                    f"{self.cardInfoFromCsvRepositoryImpl.getCardTypeForCardNumber(card_number)}.png"),
            center=(rectangle_width, rectangle_height),
            radius=circle_radius)