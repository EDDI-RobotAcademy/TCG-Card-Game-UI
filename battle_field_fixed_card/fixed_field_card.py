from card_info_from_csv.repository.card_info_from_csv_repository_impl import CardInfoFromCsvRepositoryImpl
from image_shape.circle_image import CircleImage
from image_shape.non_background_image import NonBackgroundImage
from image_shape.non_background_number_image import NonBackgroundNumberImage
from image_shape.rectangle_image import RectangleImage
from image_shape.rectangle_kinds import RectangleKinds
from opengl_battle_field_card_controller.card_controller_impl import CardControllerImpl
from opengl_pickable_shape.pickable_rectangle import PickableRectangle
from opengl_shape.circle import Circle
from opengl_shape.rectangle import Rectangle
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
        self.card_controller = CardControllerImpl.getInstance()
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

    def get_local_translation(self):
        return self.local_translation

    def get_fixed_card_base(self):
        return self.fixed_card_base

    def reset_fixed_card_base(self, card_id):
        if card_id == self.card_number:
            self.fixed_card_base = None

    def get_tool_card(self):
        return self.tool_card

    def creat_fixed_card_dark_flame_image_circle(self, image_data, vertices):
        attached_dark_flame_image = NonBackgroundImage(image_data=image_data,
                                                       vertices=vertices)

        attached_dark_flame_image.set_initial_vertices(vertices)
        return attached_dark_flame_image

    def creat_fixed_card_freezing_image_circle(self, image_data, vertices):
        attached_freezing_image = NonBackgroundImage(image_data=image_data,
                                                     vertices=vertices)

        attached_freezing_image.set_initial_vertices(vertices)
        return attached_freezing_image

    def creat_fixed_card_energy_race_circle(self, color, vertices, local_translation):
        attached_energy_circle = Circle(color=color,
                                        local_translation=local_translation,
                                        center=vertices,
                                        radius=5)
        attached_energy_circle.set_initial_vertices(vertices)
        return attached_energy_circle
    def create_attached_tool_card_rectangle(self, color, vertices, local_translation):
        attached_tool_card = Rectangle(color=color,
                                       local_translation=local_translation,
                                       vertices=vertices)
        attached_tool_card.set_draw_gradient(True)
        attached_tool_card.set_visible(False)
        attached_tool_card.set_initial_vertices(vertices)

        return attached_tool_card

    def create_card_background_rectangle(self, image_data, vertices, local_translation):
        card_background_illustration = RectangleImage(image_data=image_data,
                                                      local_translation=local_translation,
                                                      vertices=vertices)
        card_background_illustration.set_visible(False)
        card_background_illustration.set_initial_vertices(vertices)

        return card_background_illustration

    def create_fixed_card_base_rectangle(self, color, vertices, local_translation):
        fixed_card_base = PickableRectangle(color=color,
                                            local_translation=local_translation,
                                            vertices=vertices)

        # fixed_card_base.set_draw_gradient(True)
        fixed_card_base.set_draw_gradient(False)
        fixed_card_base.set_initial_vertices(vertices)

        return fixed_card_base

    def create_card_frame(self, image_data, vertices, local_translation):
        card_frame = RectangleImage(image_data=image_data,
                                    local_translation=local_translation,
                                    vertices=vertices)

        card_frame.set_rectangle_kinds(RectangleKinds.FRAME)
        card_frame.set_initial_vertices(vertices)
        return card_frame

    def create_illustration(self, image_data, vertices, local_translation):
        card_illustration = RectangleImage(image_data=image_data,
                                           local_translation=local_translation,
                                           vertices=vertices)

        card_illustration.set_rectangle_kinds(RectangleKinds.ILLUSTRATION)
        card_illustration.set_initial_vertices(vertices)

        return card_illustration

    def create_equipped_mark(self, image_data, vertices, local_translation):
        card_equipped_mark = RectangleImage(image_data=image_data,
                                            local_translation=local_translation,
                                            vertices=vertices)

        card_equipped_mark.set_visible(False)
        card_equipped_mark.set_initial_vertices(vertices)

        return card_equipped_mark

    def init_card(self, card_number):
        self.set_card_number(card_number)
        rectangle_height = 170
        rectangle_width = 105

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
            self.create_card_frame(
                image_data=self.__pre_drawed_image_instance.get_pre_draw_battle_field_card_frame_for_card_number(card_number),
                local_translation=self.local_translation,
                vertices=basic_fixed_card_base_vertices
            )
        )

        self.fixed_card_base.set_attached_shapes(
            self.create_illustration(
                image_data=self.__pre_drawed_image_instance.get_pre_draw_card_illustration_for_card_number(card_number),
                local_translation=self.local_translation,
                vertices=[(8, 12), (97, 12), (97, 126), (8, 126)]
            )
        )

        # self.pickable_card_base.set_attached_shapes(
        #     self.create_equipped_mark(
        #         image_path=os.path.join(project_root, "local_storage", "card_images", "equip_white.jpg"),
        #         local_translation=self.local_translation,
        #         vertices=[(rectangle_width + 40, 30), (rectangle_width + 80, 30), (rectangle_width + 80, 70), (rectangle_width + 40, 70)]
        #     )
        # )

        card_controller_shapes = (self.card_controller.getCardTypeTable(self.card_info.getCardTypeForCardNumber(card_number)))
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

    def init_card_view_larger(self, card_number):
        self.set_card_number(card_number)
        rectangle_width = 300
        rectangle_height = rectangle_width * 1.618

        basic_fixed_card_base_vertices = [(0, 0), (rectangle_width, 0), (rectangle_width, rectangle_height),
                                          (0, rectangle_height)]

        self.fixed_card_base = (
            self.create_fixed_card_base_rectangle(
                color=(0.0, 0.78, 0.34, 1.0),
                local_translation=self.local_translation,
                vertices=basic_fixed_card_base_vertices
            )
        )

        self.fixed_card_base.set_attached_shapes(
            self.create_card_frame(
                image_data=self.__pre_drawed_image_instance.get_pre_draw_card_frame_for_card_number(card_number),
                local_translation=self.local_translation,
                vertices=basic_fixed_card_base_vertices
            )
        )

        self.fixed_card_base.set_attached_shapes(
            self.create_illustration(
                image_data=self.__pre_drawed_image_instance.get_pre_draw_card_illustration_for_card_number(card_number),
                local_translation=self.local_translation,
                vertices=[(25, 67), (rectangle_width - 25, 67), (rectangle_width - 25, rectangle_height - 195),
                          (25, rectangle_height - 195)]
            )
        )

        card_controller_shapes = (
            self.card_controller.getCardTypeTable(self.card_info.getCardTypeForCardNumber(card_number)))
        card_shapes = card_controller_shapes(self.local_translation, card_number, rectangle_height, rectangle_width)
        for shape in card_shapes:
            shape.set_visible(True)
            self.fixed_card_base.set_attached_shapes(shape)
