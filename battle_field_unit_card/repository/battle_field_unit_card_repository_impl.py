import os

from battle_field_unit_card.entity.unit_card import UnitCard
from battle_field_unit_card.repository.battle_field_unit_card_repository import BattleFieldUnitCardRepository
from opengl_shape.entity.circle import Circle
from opengl_shape.entity.image_item import ImageItem
from opengl_shape.entity.rectangle import Rectangle


class BattleFieldUnitCardRepositoryImpl(BattleFieldUnitCardRepository):
    __instance = None
    __unit_card = UnitCard()

    __CARD_BASE_X_MAX = 250
    __CARD_BASE_Y_MAX = 400

    __CARD_ILLUSTRATION_BIAS = 25
    __CARD_ILLUSTRATION_X_MAX = 200
    __CARD_ILLUSTRATION_Y_MAX = 200

    __CIRCLE_RADIUS = 30
    __CIRCLE_X_MAX = 250
    __CIRCLE_Y_MAX = 400

    __EQUIP_CARD_BIAS = 20

    __EQUIP_MARK_X_BIAS = 290
    __EQUIP_MARK_Y_BIAS = 30
    __EQUIP_MARK_SIZE = 40

    __MYTHOLOGY_COLOR = (0.0, 0.78, 0.34, 1.0)
    __EQUIP_COLOR = (0.6, 0.4, 0.6, 1.0)
    __WHITE_COLOR = (1.0, 1.0, 1.0, 1.0)

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
        return cls.__instance

    @classmethod
    def getInstance(cls):
        if cls.__instance is None:
            cls.__instance = cls()
        return cls.__instance

    def get_unit_card(self):
        return self.__unit_card

    def create_battle_field_unit_card(self, image_filename):
        print("BattleFieldUnitCardRepositoryImpl: create_battle_field_unit_card()")

        CARD_BASE_X_MAX = self.__CARD_BASE_X_MAX
        CARD_BASE_Y_MAX = self.__CARD_BASE_Y_MAX

        CARD_ILLUSTRATION_X_MAX = self.__CARD_ILLUSTRATION_X_MAX + self.__CARD_ILLUSTRATION_BIAS
        CARD_ILLUSTRATION_Y_MAX = self.__CARD_ILLUSTRATION_Y_MAX + self.__CARD_ILLUSTRATION_BIAS
        CARD_ILLUSTARTION_X_MIN = self.__CARD_ILLUSTRATION_BIAS
        CARD_ILLUSTARTION_Y_MIN = self.__CARD_ILLUSTRATION_BIAS

        EQUIP_CARD_X_MIN = self.__EQUIP_CARD_BIAS
        EQUIP_CARD_Y_MIN = self.__EQUIP_CARD_BIAS
        EQUIP_CARD_X_MAX = self.__EQUIP_CARD_BIAS + CARD_BASE_X_MAX
        EQUIP_CARD_Y_MAX = self.__EQUIP_CARD_BIAS + CARD_BASE_Y_MAX

        CIRCLE_X_MAX = self.__CIRCLE_X_MAX
        CIRCLE_Y_MAX = self.__CIRCLE_Y_MAX

        EQUIP_MARK_X_MIN = self.__EQUIP_MARK_X_BIAS
        EQUIP_MARK_Y_MIN = self.__EQUIP_MARK_Y_BIAS
        EQUIP_MARK_X_MAX = self.__EQUIP_MARK_X_BIAS + self.__EQUIP_MARK_SIZE
        EQUIP_MARK_Y_MAX = self.__EQUIP_MARK_Y_BIAS + self.__EQUIP_MARK_SIZE

        shapes = []

        card_base_rectangle = Rectangle(color=self.__MYTHOLOGY_COLOR,
                                        vertices=[(0, 0),
                                                  (CARD_BASE_X_MAX, 0),
                                                  (CARD_BASE_X_MAX, CARD_BASE_Y_MAX),
                                                  (0, CARD_BASE_Y_MAX)])
        shapes.append(card_base_rectangle)

        card_illustrate_background_rectangle = Rectangle(color=self.__WHITE_COLOR,
                                                         vertices=[(CARD_ILLUSTARTION_X_MIN, CARD_ILLUSTARTION_Y_MIN),
                                                                   (CARD_ILLUSTRATION_X_MAX, CARD_ILLUSTARTION_Y_MIN),
                                                                   (CARD_ILLUSTRATION_X_MAX, CARD_ILLUSTRATION_Y_MAX),
                                                                   (CARD_ILLUSTARTION_X_MIN, CARD_ILLUSTRATION_Y_MAX)])
        shapes.append(card_illustrate_background_rectangle)

        current_directory = os.getcwd()
        real_image_path = os.path.join(current_directory, "../../local_storage/card_images/", image_filename)
        card_illustration_image = ImageItem(color=(),
                                            vertices=[(CARD_ILLUSTARTION_X_MIN, CARD_ILLUSTARTION_Y_MIN),
                                                      (CARD_ILLUSTRATION_X_MAX, CARD_ILLUSTARTION_Y_MIN),
                                                      (CARD_ILLUSTRATION_X_MAX, CARD_ILLUSTRATION_Y_MAX),
                                                      (CARD_ILLUSTARTION_X_MIN, CARD_ILLUSTRATION_Y_MAX)],
                                            image_path=real_image_path)
        shapes.append(card_illustration_image)

        circle_radius = 30
        circle_center_coordinates = [(0, 0), (CIRCLE_X_MAX, 0), (CIRCLE_X_MAX, CIRCLE_Y_MAX), (0, CIRCLE_Y_MAX)]
        for center in circle_center_coordinates:
            card_circle_info = Circle(color=(1.0, 0.33, 0.34, 1.0),
                                      center=center,
                                      radius=circle_radius)
            shapes.append(card_circle_info)

        attached_tool_card = Rectangle(color=self.__EQUIP_COLOR,
                                       vertices=[(EQUIP_CARD_X_MIN, EQUIP_CARD_Y_MIN),
                                                 (EQUIP_CARD_X_MAX, EQUIP_CARD_Y_MIN),
                                                 (EQUIP_CARD_X_MAX, EQUIP_CARD_Y_MAX),
                                                 (EQUIP_CARD_X_MIN, EQUIP_CARD_Y_MAX)])
        shapes.append(attached_tool_card)

        equiped_mark_base = Rectangle(color=self.__WHITE_COLOR,
                                      vertices=[(EQUIP_MARK_X_MIN, EQUIP_MARK_Y_MIN),
                                                (EQUIP_MARK_X_MAX, EQUIP_MARK_Y_MIN),
                                                (EQUIP_MARK_X_MAX, EQUIP_MARK_Y_MAX),
                                                (EQUIP_MARK_X_MIN, EQUIP_MARK_Y_MAX)])
        shapes.append(equiped_mark_base)

        equip_image_path = os.path.join(current_directory, "../../local_storage/card_images/equip_white.jpg")
        equiped_image = ImageItem(color=(),
                                  vertices=[(EQUIP_MARK_X_MIN, EQUIP_MARK_Y_MIN),
                                            (EQUIP_MARK_X_MAX, EQUIP_MARK_Y_MIN),
                                            (EQUIP_MARK_X_MAX, EQUIP_MARK_Y_MAX),
                                            (EQUIP_MARK_X_MIN, EQUIP_MARK_Y_MAX)],
                                  image_path=equip_image_path)
        shapes.append(equiped_image)

        self.__unit_card.set_shapes(shapes)




