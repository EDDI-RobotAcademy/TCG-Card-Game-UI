import os

from card_info_from_csv.repository.card_info_from_csv_repository_impl import CardInfoFromCsvRepositoryImpl
from image_shape.rectangle_image import RectangleImage
from opengl_pickable_shape.pickable_rectangle import PickableRectangle
from common.utility import get_project_root
from opengl_shape.image_rectangle_element import ImageRectangleElement
from opengl_shape.rectangle import Rectangle
from opengl_battle_field_card_controller.card_controller_impl import CardControllerImpl
from pre_drawed_image_manager.pre_drawed_image import PreDrawedImage
from tests.lsh.ugly_draw_battle_field.test_draw_battle_field import ImageRectangleElementRefactor


class Card:
    __imagePath = None
    __pre_drawed_image_instance = PreDrawedImage.getInstance()
    def __init__(self, local_translation=(0, 0), scale=200):
        self.tool_card = None
        self.pickable_card_base = None
        self.local_translation = local_translation
        self.scale = scale
        self.card_number = None
        self.card_info = CardInfoFromCsvRepositoryImpl()

    def get_card_number(self):
        return self.card_number

    def set_card_number(self, card_number):
        self.card_number = card_number
        
    def change_local_translation(self, _translation):
        self.local_translation = _translation

    def get_pickable_card_base(self):
        return self.pickable_card_base

    def get_tool_card(self):
        return self.tool_card


    def create_attached_tool_card_rectangle(self, color, vertices, local_translation):
        attached_tool_card = Rectangle(color=color,
                                       local_translation=local_translation,
                                       vertices=vertices)
        attached_tool_card.set_draw_gradient(True)
        attached_tool_card.set_visible(False)
        return attached_tool_card

    def create_card_background_rectangle(self, image_path, vertices, local_translation):
        card_background_illustration = ImageRectangleElement(image_path=image_path,
                                                             local_translation=local_translation,
                                                             vertices=vertices)
        card_background_illustration.set_visible(False)
        return card_background_illustration

    def create_card_base_pickable_rectangle(self, color, vertices, local_translation):
        pickable_card_base = PickableRectangle(color=color,
                                               local_translation=local_translation,
                                               vertices=vertices)
        pickable_card_base.set_draw_gradient(True)
        return pickable_card_base

    def create_illustration(self, image_data, vertices, local_translation):
        card_illustration = RectangleImage(image_data=image_data,
                                           local_translation=local_translation,
                                           vertices=vertices)
        return card_illustration

    def create_equipped_mark(self, image_path, vertices, local_translation):
        card_equipped_mark = ImageRectangleElement(image_path=image_path,
                                                   local_translation=local_translation,
                                                   vertices=vertices)
        card_equipped_mark.set_visible(False)
        return card_equipped_mark


    def init_card(self, card_number):
        self.set_card_number(card_number)
        rectangle_height = self.scale
        rectangle_width = self.scale / 1.618
        project_root = get_project_root()

        print(f"rectangle_width: {rectangle_width}")
        print(f"rectangle_height: {rectangle_height}")

        # cardInfo = CardInfoFromCsvRepositoryImpl.getInstance()
        # csvInfo = cardInfo.readCardData(os.path.join(project_root, 'local_storage', 'card', 'data.csv'))
        # cardInfo.build_dictionaries(csvInfo)

        CardControllerImpl()
        card_controller = CardControllerImpl.getInstance()

        self.tool_card = self.create_attached_tool_card_rectangle(
            color=(0.6, 0.4, 0.6, 1.0),
            local_translation=self.local_translation,
            vertices=[(15, 15), (rectangle_width + 15, 15), (rectangle_width + 15, rectangle_height + 15), (15, rectangle_height + 15)])

        self.pickable_card_base = (
            self.create_card_base_pickable_rectangle(
                color=(0.0, 0.78, 0.34, 1.0),
                local_translation=self.local_translation,
                vertices=[(0, 0), (rectangle_width, 0), (rectangle_width, rectangle_height), (0, rectangle_height)]
            )
        )

        self.pickable_card_base.set_attached_shapes(
            self.create_illustration(
                image_data=self.__pre_drawed_image_instance.get_pre_draw_card_illustration_for_card_number(card_number),
                local_translation=self.local_translation,
                vertices=[(15, 15), (rectangle_width - 15, 15), (rectangle_width - 15, rectangle_width - 15), (15, rectangle_width - 15)]
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
            self.pickable_card_base.set_attached_shapes(shape)

        # self.pickable_card_base.set_attached_shapes(
        #     self.create_card_background_rectangle(
        #         image_path=os.path.join(project_root, "local_storage", "card_images", "background.png"),
        #         local_translation=self.local_translation,
        #         vertices=[(0, 0), (rectangle_width, 0), (rectangle_width, rectangle_height), (0, rectangle_height)]
        #     )
        # )