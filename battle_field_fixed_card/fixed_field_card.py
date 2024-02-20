import os

from card_info_from_csv.repository.card_info_from_csv_repository_impl import CardInfoFromCsvRepositoryImpl
from image_shape.rectangle_image import RectangleImage
from opengl_pickable_shape.pickable_rectangle import PickableRectangle
from common.utility import get_project_root
from opengl_shape.image_rectangle_element import ImageRectangleElement
from opengl_shape.rectangle import Rectangle
from opengl_battle_field_card_controller.card_controller_impl import CardControllerImpl
from pre_drawed_image_manager.pre_drawed_image import PreDrawedImage


class FixedFieldCard:
    __pre_drawed_image_instance = PreDrawedImage.getInstance()

    def __init__(self, local_translation=(0, 0), scale=1):
        self.tool_card = None
        self.fixed_card_base = None
        self.local_translation = local_translation
        self.scale = scale
        self.card_number = None
        self.card_info = CardInfoFromCsvRepositoryImpl.getInstance()
        self.index = 0

    def get_card_number(self):
        return self.card_number

    def set_card_number(self, card_number):
        self.card_number = card_number

    def get_index(self):
        return self.index

    def set_index(self, index):
        self.index = index

    def change_local_translation(self, _translation):
        self.local_translation = _translation

    def get_fixed_card_base(self):
        return self.fixed_card_base

    def get_tool_card(self):
        return self.tool_card

    def create_attached_tool_card_rectangle(self, color, vertices, local_translation):
        attached_tool_card = Rectangle(color=color,
                                       local_translation=local_translation,
                                       vertices=vertices)
        attached_tool_card.set_draw_gradient(True)
        attached_tool_card.set_visible(False)
        return attached_tool_card

    def create_card_background_rectangle(self, image_data, vertices, local_translation):
        card_background_illustration = RectangleImage(image_data=image_data,
                                                      local_translation=local_translation,
                                                      vertices=vertices)
        card_background_illustration.set_visible(False)
        return card_background_illustration

    def create_fixed_card_base_rectangle(self, color, vertices, local_translation):
        fixed_card_base = PickableRectangle(color=color,
                                            local_translation=local_translation,
                                            vertices=vertices)
        fixed_card_base.set_draw_gradient(True)
        return fixed_card_base

    def create_illustration(self, image_data, vertices, local_translation):
        card_illustration = RectangleImage(image_data=image_data,
                                           local_translation=local_translation,
                                           vertices=vertices)
        return card_illustration

    def create_equipped_mark(self, image_data, vertices, local_translation):
        card_equipped_mark = RectangleImage(image_data=image_data,
                                            local_translation=local_translation,
                                            vertices=vertices)
        card_equipped_mark.set_visible(False)
        return card_equipped_mark

    def init_card(self, card_number):
        self.set_card_number(card_number)
        rectangle_height = 170
        rectangle_width = 105

        print(f"rectangle_width: {rectangle_width}")
        print(f"rectangle_height: {rectangle_height}")

        # cardInfo = CardInfoFromCsvRepositoryImpl.getInstance()
        # csvInfo = cardInfo.readCardData(os.path.join(project_root, 'local_storage', 'card', 'data.csv'))
        # cardInfo.build_dictionaries(csvInfo)

        # CardControllerImpl()
        card_controller = CardControllerImpl.getInstance()

        self.tool_card = self.create_attached_tool_card_rectangle(
            color=(0.6, 0.4, 0.6, 1.0),
            local_translation=self.local_translation,
            vertices=[(15, 15), (120, 15), (120, 185), (15, 185)])

        basic_fixed_card_base_vertices = [(0, 0), (105, 0), (105, 170), (0, 170)]

        self.fixed_card_base = (
            self.create_fixed_card_base_rectangle(
                color=(0.0, 0.78, 0.34, 1.0),
                local_translation=self.local_translation,
                vertices=basic_fixed_card_base_vertices
            )
        )

        self.fixed_card_base.set_attached_shapes(
            self.create_illustration(
                image_data=self.__pre_drawed_image_instance.get_pre_draw_card_illustration_for_card_number(card_number),
                local_translation=self.local_translation,
                vertices=[(15, 15), (90, 15), (90, 90), (15, 90)]
            )
        )

        # self.pickable_card_base.set_attached_shapes(
        #     self.create_equipped_mark(
        #         image_path=os.path.join(project_root, "local_storage", "card_images", "equip_white.jpg"),
        #         local_translation=self.local_translation,
        #         vertices=[(rectangle_width + 40, 30), (rectangle_width + 80, 30), (rectangle_width + 80, 70), (rectangle_width + 40, 70)]
        #     )
        # )

        card_controller_shapes = card_controller.getCardTypeTable(self.card_info.getCardTypeForCardNumber(card_number))
        card_shapes = card_controller_shapes(self.local_translation, card_number, rectangle_height, rectangle_width)
        for shape in card_shapes:
            shape.set_visible(True)
            self.fixed_card_base.set_attached_shapes(shape)

        # self.pickable_card_base.set_attached_shapes(
        #     self.create_card_background_rectangle(
        #         image_path=os.path.join(project_root, "local_storage", "card_images", "background.png"),
        #         local_translation=self.local_translation,
        #         vertices=[(0, 0), (rectangle_width, 0), (rectangle_width, rectangle_height), (0, rectangle_height)]
        #     )
        # )