import os

from card_info_from_csv.repository.card_info_from_csv_repository_impl import CardInfoFromCsvRepositoryImpl
from common.utility import get_project_root
from opengl_shape.circle import Circle
from opengl_shape.image_circle_element import ImageCircleElement


class ItemCard:
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
        # extend

    def create_item_energy_circle(self, color, center, radius):
        item_energy_circle = Circle(color=color,
                                    center=center,
                                    radius=radius)
        self.add_shape(item_energy_circle)

    def create_item_race_illustration_circle(self, image_path, center, radius):
        item_race_circle = ImageCircleElement(image_path=image_path,
                                              center=center,
                                              radius=radius)
        print(f"type {type(item_race_circle)}")
        self.add_shape(item_race_circle)

    def create_item_type_illustration_circle(self, image_path, center, radius):
        item_type_circle = ImageCircleElement(image_path=image_path,
                                              center=center,
                                              radius=radius)
        self.add_shape(item_type_circle)


    def init_shapes(self, circle_radius, card_number, rectangle_height, rectangle_width):

        project_root = get_project_root()

        self.create_item_energy_circle(color=(1.0, 0.33, 0.34, 1.0),
                                       center=(0, 0),
                                       radius=circle_radius)

        self.create_item_race_illustration_circle(
            image_path=os.path.join(project_root, "local_storage", "card_race_image", f"{self.cardInfoFromCsvRepositoryImpl.getCardRaceForCardNumber(card_number)}.png"),
            center=(rectangle_width, 0),
            radius=circle_radius)

        self.create_item_type_illustration_circle(
            image_path=os.path.join(project_root, "local_storage", "card_type_image", f"{self.cardInfoFromCsvRepositoryImpl.getCardTypeForCardNumber(card_number)}.png"),
            center=(rectangle_width, rectangle_height),
            radius=circle_radius)