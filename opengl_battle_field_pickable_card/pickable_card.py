from card_info_from_csv.repository.card_info_from_csv_repository_impl import CardInfoFromCsvRepositoryImpl
from image_shape.rectangle_image import RectangleImage
from image_shape.rectangle_kinds import RectangleKinds
from opengl_battle_field_card_controller.card_controller_impl import CardControllerImpl
from opengl_pickable_shape.pickable_rectangle import PickableRectangle
from opengl_shape.image_rectangle_element import ImageRectangleElement
from opengl_shape.rectangle import Rectangle
from pre_drawed_image_manager.pre_drawed_image import PreDrawedImage


class PickableCard:
    __imagePath = None
    __pre_drawed_image_instance = PreDrawedImage.getInstance()

    def __init__(self, local_translation=(0, 0), scale=1):
        self.tool_card = None
        self.pickable_card_base = None
        self.local_translation = local_translation
        self.scale = scale
        self.card_number = None
        self.initial_vertices = None
        self.index = 0

        self.card_info = CardInfoFromCsvRepositoryImpl.getInstance()
        self.card_controller = CardControllerImpl.getInstance()

    def get_card_number(self):
        return self.card_number

    def set_card_number(self, card_number):
        self.card_number = card_number

    def get_index(self):
        return self.index

    def set_index(self, index):
        self.index = index

    # TODO: Need to consider place this function
    # def set_initial_vertices(self, initial_pickable_card_base_vertices):
    #     self.initial_vertices = initial_pickable_card_base_vertices
    #
    # def get_initial_vertices(self):
    #     return self.initial_vertices
        
    def change_local_translation(self, _translation):
        self.local_translation = _translation

    def get_pickable_card_base(self):
        return self.pickable_card_base

    def get_tool_card(self):
        return self.tool_card


    # def create_attached_tool_card_rectangle(self, color, vertices, local_translation):
    #     attached_tool_card = Rectangle(color=color,
    #                                    local_translation=local_translation,
    #                                    vertices=vertices)
    #     attached_tool_card.set_draw_gradient(True)
    #     attached_tool_card.set_visible(False)
    #     attached_tool_card.set_initial_vertices(vertices)
    #     return attached_tool_card
    #
    # def create_card_background_rectangle(self, image_path, vertices, local_translation):
    #     card_background_illustration = ImageRectangleElement(image_path=image_path,
    #                                                          local_translation=local_translation,
    #                                                          vertices=vertices)
    #     card_background_illustration.set_visible(False)
    #     return card_background_illustration

    def create_card_base_pickable_rectangle(self, color, vertices, local_translation):
        pickable_card_base = PickableRectangle(color=color,
                                               local_translation=local_translation,
                                               vertices=vertices)

        # pickable_card_base.set_draw_gradient(True)
        pickable_card_base.set_initial_vertices(vertices)
        return pickable_card_base

    # def create_illustration(self, image_data, vertices, local_translation):
    #     card_illustration = RectangleImage(image_data=image_data,
    #                                        local_translation=local_translation,
    #                                        vertices=vertices)
    #
    #     card_illustration.set_rectangle_kinds(RectangleKinds.ILLUSTRATION)
    #     card_illustration.set_initial_vertices(vertices)
    #     return card_illustration

    def create_card_frame(self, image_data, vertices, local_translation):
        card_frame = RectangleImage(image_data=image_data,
                                    local_translation=local_translation,
                                    vertices=vertices)

        card_frame.set_rectangle_kinds(RectangleKinds.FRAME)
        card_frame.set_initial_vertices(vertices)
        return card_frame

    # def create_equipped_mark(self, image_path, vertices, local_translation):
    #     card_equipped_mark = ImageRectangleElement(image_path=image_path,
    #                                                local_translation=local_translation,
    #                                                vertices=vertices)
    #     card_equipped_mark.set_visible(False)
    #     return card_equipped_mark


    def init_card(self, card_number):
        self.set_card_number(card_number)
        rectangle_height = 170
        rectangle_width = 105

        # self.tool_card = self.create_attached_tool_card_rectangle(
        #     color=(0.6, 0.4, 0.6, 1.0),
        #     local_translation=self.local_translation,
        #     vertices=[(15, 15), (120, 15), (120, 185), (15, 185)])

        basic_pickable_card_base_vertices = [(0, 0), (105, 0), (105, 170), (0, 170)]

        self.pickable_card_base = (
            self.create_card_base_pickable_rectangle(
                color=(0.0, 0.78, 0.34, 1.0),
                local_translation=self.local_translation,
                vertices=basic_pickable_card_base_vertices
            )
        )

        self.pickable_card_base.set_attached_shapes(
            self.create_card_frame(
                image_data=self.__pre_drawed_image_instance.get_pre_draw_battle_field_card_frame_for_card_number(card_number),
                local_translation=self.local_translation,
                vertices=basic_pickable_card_base_vertices
            )
        )

        # self.pickable_card_base.set_attached_shapes(
        #     self.create_illustration(
        #         image_data=self.__pre_drawed_image_instance.get_pre_draw_card_illustration_for_card_number(card_number),
        #         local_translation=self.local_translation,
        #         vertices=[(8, 12), (97, 12), (97, 126), (8, 126)]
        #     )
        # )

        card_controller_shapes = self.card_controller.getCardTypeTable(self.card_info.getCardTypeForCardNumber(card_number))
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

    def init_card_scale(self, card_number):
        self.set_card_number(card_number)

        rectangle_width = 300
        rectangle_height = rectangle_width * 1.618


        print(f"rectangle_width: {rectangle_width}")
        print(f"rectangle_height: {rectangle_height}")

        # self.tool_card = self.create_attached_tool_card_rectangle(
        #     color=(0.6, 0.4, 0.6, 1.0),
        #     local_translation=self.local_translation,
        #     vertices=[(15, 15), (rectangle_width + 15, 15), (rectangle_width + 15, rectangle_height + 15),
        #               (15, rectangle_height + 15)])

        basic_pickable_card_base_vertices = [(0, 0), (rectangle_width, 0), (rectangle_width, rectangle_height),
                                             (0, rectangle_height)]

        self.pickable_card_base = (
            self.create_card_base_pickable_rectangle(
                color=(0.0, 0.78, 0.34, 1.0),
                local_translation=self.local_translation,
                vertices=basic_pickable_card_base_vertices
            )
        )

        self.pickable_card_base.set_attached_shapes(
            self.create_card_frame(
                image_data=self.__pre_drawed_image_instance.get_pre_draw_card_frame_for_card_number(card_number),
                local_translation=self.local_translation,
                vertices=basic_pickable_card_base_vertices
            )
        )

        # self.pickable_card_base.set_attached_shapes(
        #     self.create_illustration(
        #         image_data=self.__pre_drawed_image_instance.get_pre_draw_card_illustration_for_card_number(
        #             card_number),
        #         local_translation=self.local_translation,
        #         vertices=[(25, 67), (rectangle_width - 25, 67), (rectangle_width - 25, rectangle_height - 195),
        #                   (25, rectangle_height - 195)]
        #     )
        # )

        card_controller_shapes = self.card_controller.getCardTypeTable(
            self.card_info.getCardTypeForCardNumber(card_number)
        )
        card_shapes = card_controller_shapes(self.local_translation, card_number, rectangle_height, rectangle_width)
        for shape in card_shapes:
            self.pickable_card_base.set_attached_shapes(shape)

    def init_card_in_my_card_frame(self, card_number, total_width, total_height):
        self.set_card_number(card_number)

        rectangle_width = 350
        # 실제 카드의 비율은 1.615
        rectangle_height = rectangle_width * 1.615

        print(f"rectangle_width: {rectangle_width}")
        print(f"rectangle_height: {rectangle_height}")

        # self.tool_card = self.create_attached_tool_card_rectangle(
        #     color=(0.6, 0.4, 0.6, 1.0),
        #     local_translation=self.local_translation,
        #     vertices=[(15, 15), (rectangle_width + 15, 15), (rectangle_width + 15, rectangle_height + 15),
        #               (15, rectangle_height + 15)])

        basic_pickable_card_base_vertices = [(0, 0), (rectangle_width, 0), (rectangle_width, rectangle_height),
                                             (0, rectangle_height)]

        self.pickable_card_base = (
            self.create_card_base_pickable_rectangle(
                color=(0.0, 0.78, 0.34, 1.0),
                local_translation=self.local_translation,
                vertices=basic_pickable_card_base_vertices
            )
        )

        self.pickable_card_base.set_attached_shapes(
            self.create_card_frame(
                image_data=self.__pre_drawed_image_instance.get_pre_draw_card_frame_for_card_number(card_number),
                local_translation=self.local_translation,
                vertices=basic_pickable_card_base_vertices
            )
        )

        # self.pickable_card_base.set_attached_shapes(
        #     self.create_illustration(
        #         image_data=self.__pre_drawed_image_instance.get_pre_draw_card_illustration_for_card_number(
        #             card_number),
        #         local_translation=self.local_translation,
        #         vertices=[(17, 50), (rectangle_width - 17, 50), (rectangle_width - 17, rectangle_height - 155),
        #                   (17, rectangle_height - 155)]
        #     )
        # )

        card_controller_shapes = self.card_controller.getCardTypeTable(
            self.card_info.getCardTypeForCardNumber(card_number)
        )
        card_shapes = card_controller_shapes(self.local_translation, card_number, rectangle_height, rectangle_width)
        for shape in card_shapes:
            self.pickable_card_base.set_attached_shapes(shape)

    def init_random_buy_card(self, card_number):
        self.set_card_number(card_number)

        rectangle_width = 200
        rectangle_height = rectangle_width * 1.615

        basic_pickable_card_base_vertices = [
            (0, 0),
            (rectangle_width, 0),
            (rectangle_width, rectangle_height),
            (0, rectangle_height)
        ]

        self.pickable_card_base = (
            self.create_card_base_pickable_rectangle(
                color=(0.0, 0.78, 0.34, 1.0),
                local_translation=self.local_translation,
                vertices=basic_pickable_card_base_vertices
            )
        )

        self.pickable_card_base.set_attached_shapes(
            self.create_card_frame(
                image_data=self.__pre_drawed_image_instance.get_pre_draw_random_buy_card_frame_for_card_number(card_number),
                local_translation=self.local_translation,
                vertices=basic_pickable_card_base_vertices
            )
        )

        card_controller_shapes = self.card_controller.getCardTypeTable(
            self.card_info.getCardTypeForCardNumber(card_number))
        card_shapes = card_controller_shapes(self.local_translation, card_number, rectangle_height, rectangle_width)
        for shape in card_shapes:
            self.pickable_card_base.set_attached_shapes(shape)


