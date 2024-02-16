import os

from tests.battle_field_unit_card_legacy.entity.unit_card import UnitCard
from tests.battle_field_unit_card_legacy.repository.battle_field_unit_card_repository import BattleFieldUnitCardRepository
from tests.jsh.opengl_shape_legacy.entity.circle import Circle
from tests.jsh.opengl_shape_legacy.entity.image_item import ImageItem
from tests.jsh.opengl_shape_legacy.entity.rectangle import Rectangle


class BattleFieldUnitCardRepositoryImpl(BattleFieldUnitCardRepository):
    __shapes = []

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

    def create_card_base(self):
        CARD_BASE_X_MAX = self.__CARD_BASE_X_MAX
        CARD_BASE_Y_MAX = self.__CARD_BASE_Y_MAX

        card_base_rectangle = Rectangle(color=self.__MYTHOLOGY_COLOR,
                                        vertices=[(0, 0),
                                                  (CARD_BASE_X_MAX, 0),
                                                  (CARD_BASE_X_MAX, CARD_BASE_Y_MAX),
                                                  (0, CARD_BASE_Y_MAX)])

        self.__shapes.append(card_base_rectangle)

    def create_illustration(self, current_directory, image_filename):
        CARD_ILLUSTRATION_X_MAX = self.__CARD_ILLUSTRATION_X_MAX + self.__CARD_ILLUSTRATION_BIAS
        CARD_ILLUSTRATION_Y_MAX = self.__CARD_ILLUSTRATION_Y_MAX + self.__CARD_ILLUSTRATION_BIAS
        CARD_ILLUSTARTION_X_MIN = self.__CARD_ILLUSTRATION_BIAS
        CARD_ILLUSTARTION_Y_MIN = self.__CARD_ILLUSTRATION_BIAS

        card_illustrate_background_rectangle = Rectangle(color=self.__WHITE_COLOR,
                                                         vertices=[(CARD_ILLUSTARTION_X_MIN, CARD_ILLUSTARTION_Y_MIN),
                                                                   (CARD_ILLUSTRATION_X_MAX, CARD_ILLUSTARTION_Y_MIN),
                                                                   (CARD_ILLUSTRATION_X_MAX, CARD_ILLUSTRATION_Y_MAX),
                                                                   (CARD_ILLUSTARTION_X_MIN, CARD_ILLUSTRATION_Y_MAX)])
        self.__shapes.append(card_illustrate_background_rectangle)

        real_image_path = os.path.join(current_directory, "../../local_storage/card_images/", image_filename)
        card_illustration_image = ImageItem(color=(),
                                            vertices=[(CARD_ILLUSTARTION_X_MIN, CARD_ILLUSTARTION_Y_MIN),
                                                      (CARD_ILLUSTRATION_X_MAX, CARD_ILLUSTARTION_Y_MIN),
                                                      (CARD_ILLUSTRATION_X_MAX, CARD_ILLUSTRATION_Y_MAX),
                                                      (CARD_ILLUSTARTION_X_MIN, CARD_ILLUSTRATION_Y_MAX)],
                                            image_path=real_image_path)
        self.__shapes.append(card_illustration_image)

    def create_card_basic_information(self):
        CIRCLE_X_MAX = self.__CIRCLE_X_MAX
        CIRCLE_Y_MAX = self.__CIRCLE_Y_MAX

        circle_radius = 30
        circle_center_coordinates = [(0, 0), (CIRCLE_X_MAX, 0), (CIRCLE_X_MAX, CIRCLE_Y_MAX), (0, CIRCLE_Y_MAX)]
        for center in circle_center_coordinates:
            card_circle_info = Circle(color=(1.0, 0.33, 0.34, 1.0),
                                      center=center,
                                      radius=circle_radius)
            self.__shapes.append(card_circle_info)

    def create_attached_tool_card(self):
        EQUIP_CARD_X_MIN = self.__EQUIP_CARD_BIAS
        EQUIP_CARD_Y_MIN = self.__EQUIP_CARD_BIAS
        EQUIP_CARD_X_MAX = self.__EQUIP_CARD_BIAS + self.__CARD_BASE_X_MAX
        EQUIP_CARD_Y_MAX = self.__EQUIP_CARD_BIAS + self.__CARD_BASE_Y_MAX

        attached_tool_card = Rectangle(color=self.__EQUIP_COLOR,
                                       vertices=[(EQUIP_CARD_X_MIN, EQUIP_CARD_Y_MIN),
                                                 (EQUIP_CARD_X_MAX, EQUIP_CARD_Y_MIN),
                                                 (EQUIP_CARD_X_MAX, EQUIP_CARD_Y_MAX),
                                                 (EQUIP_CARD_X_MIN, EQUIP_CARD_Y_MAX)])
        self.__shapes.append(attached_tool_card)

    def create_attached_tool_mark(self, current_directory):
        EQUIP_MARK_X_MIN = self.__EQUIP_MARK_X_BIAS
        EQUIP_MARK_Y_MIN = self.__EQUIP_MARK_Y_BIAS
        EQUIP_MARK_X_MAX = self.__EQUIP_MARK_X_BIAS + self.__EQUIP_MARK_SIZE
        EQUIP_MARK_Y_MAX = self.__EQUIP_MARK_Y_BIAS + self.__EQUIP_MARK_SIZE

        equiped_mark_base = Rectangle(color=self.__WHITE_COLOR,
                                      vertices=[(EQUIP_MARK_X_MIN, EQUIP_MARK_Y_MIN),
                                                (EQUIP_MARK_X_MAX, EQUIP_MARK_Y_MIN),
                                                (EQUIP_MARK_X_MAX, EQUIP_MARK_Y_MAX),
                                                (EQUIP_MARK_X_MIN, EQUIP_MARK_Y_MAX)])
        self.__shapes.append(equiped_mark_base)

        equip_image_path = os.path.join(current_directory, "../../local_storage/card_images/equip_white.jpg")
        equiped_image = ImageItem(color=(),
                                  vertices=[(EQUIP_MARK_X_MIN, EQUIP_MARK_Y_MIN),
                                            (EQUIP_MARK_X_MAX, EQUIP_MARK_Y_MIN),
                                            (EQUIP_MARK_X_MAX, EQUIP_MARK_Y_MAX),
                                            (EQUIP_MARK_X_MIN, EQUIP_MARK_Y_MAX)],
                                  image_path=equip_image_path)
        self.__shapes.append(equiped_image)

    def create_battle_field_unit_card(self, image_filename):
        print("BattleFieldUnitCardRepositoryImpl: create_battle_field_unit_card()")

        current_directory = os.getcwd()

        self.create_card_base()
        self.create_illustration(current_directory, image_filename)
        self.create_card_basic_information()
        self.create_attached_tool_card()
        self.create_attached_tool_mark(current_directory)

        # TODO: 여기에 나머지 특성, 에너지, 설명 등등의 UI 를 표현합니다 (가이드 문서 참고)




