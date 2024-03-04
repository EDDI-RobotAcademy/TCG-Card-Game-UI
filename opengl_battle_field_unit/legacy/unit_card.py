import os

from card_info_from_csv.repository.card_info_from_csv_repository_impl import CardInfoFromCsvRepositoryImpl
from common.utility import get_project_root
from image_shape.circle_image import CircleImage
from image_shape.circle_kinds import CircleKinds
from image_shape.circle_number_image import CircleNumberImage
from image_shape.non_background_image import NonBackgroundImage
from image_shape.non_background_number_image import NonBackgroundNumberImage
from opengl_pickable_shape.pickable_rectangle import PickableRectangle
from opengl_shape.circle import Circle
from opengl_shape.image_rectangle_element import ImageRectangleElement
from opengl_shape.rectangle import Rectangle
from pre_drawed_image_manager.pre_drawed_image import PreDrawedImage


#from tests.ugly_text_field.test_ugly_text_field_rectangle import TextFieldRectangle


class LegacyUnitCard:
    __imagePath = None
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


    # def create_attached_tool_card_rectangle(self, color, vertices, local_translation):
    #     attached_tool_card = Rectangle(color=color,
    #                                    local_translation=local_translation,
    #                                    vertices=vertices)
    #     attached_tool_card.set_draw_gradient(True)
    #     attached_tool_card.set_visible(False)
    #     return attached_tool_card
    #
    # def create_card_base_pickable_rectangle(self, color, vertices, local_translation):
    #     pickable_unit_card_base = PickableRectangle(color=color,
    #                                                 local_translation=local_translation,
    #                                                 vertices=vertices)
    #     pickable_unit_card_base.set_draw_gradient(True)
    #     return pickable_unit_card_base
    #
    # def create_illustration(self, image_path, vertices, local_translation):
    #     unit_illustration = ImageRectangleElement(image_path=image_path,
    #                                      local_translation=local_translation,
    #                                      vertices=vertices)
    #     return unit_illustration
    #
    # # def create_text_field(self, text, vertices, local_translation):
    # #     unit_text_field = TextFieldRectangle(text=text,
    # #                                          local_translation=local_translation,
    # #                                          vertices=vertices)
    # #     return unit_text_field
    #
    # def create_equipped_mark(self, image_path, vertices, local_translation):
    #     unit_equipped_mark = ImageRectangleElement(image_path=image_path,
    #                                       local_translation=local_translation,
    #                                       vertices=vertices)
    #     unit_equipped_mark.set_visible(False)
    #     return unit_equipped_mark

    def create_unit_energy_circle(self, image_data, energy_number, center, radius):
        unit_energy_circle = CircleNumberImage(image_data=image_data,
                                               center=center,
                                               radius=radius,
                                               number=energy_number)
        unit_energy_circle.set_circle_kinds(CircleKinds.ENERGY)
        unit_energy_circle.set_visible(False)
        self.add_shape(unit_energy_circle)

    # def create_unit_energy_circle(self, image_data, energy_number, center, radius):
    #     # 가로 대비 세로 => 1.343
    #     # 양측으로 벌리니까 => 1.1715
    #     vertices = [
    #         (center[0] - radius, center[1] + radius * 1.343),
    #         (center[0] + radius, center[1] + radius * 1.343),
    #         (center[0] + radius, center[1] - radius * 1.343),
    #         (center[0] - radius, center[1] - radius * 1.343),
    #     ]
    #     image_data = self.__pre_drawed_image_instance.get_pre_draw_unit_energy(energy_number)
    #     unit_energy_image = NonBackgroundNumberImage(image_data=image_data,
    #                                                  vertices=vertices,
    #                                                  number=energy_number)
    #
    #     unit_energy_image.set_circle_kinds(CircleKinds.ENERGY)
    #     unit_energy_image.set_visible(False)
    #     self.add_shape(unit_energy_image)

    def create_unit_race_illustration_circle(self, image_data, center, radius):
        # print(f"create_unit_race_illustration_circle -> center: {center}")
        unit_race_circle = CircleImage(image_data=image_data,
                                       center=center,
                                       radius=radius)
        self.add_shape(unit_race_circle)

        # vertices = [
        #     (center[0] - radius, center[1] - radius),
        #     (center[0] + radius, center[1] - radius),
        #     (center[0] + radius, center[1] + radius),
        #     (center[0] - radius, center[1] + radius),
        # ]
        #
        # unit_race_image = NonBackgroundImage(image_data=image_data,
        #                                      vertices=vertices)
        # unit_race_image.set_initial_vertices(vertices)
        # self.add_shape(unit_race_image)

    def create_unit_attack_circle(self, image_data, attack_number, center, radius):
        unit_attack_circle = CircleNumberImage(image_data=image_data,
                                               center=center,
                                               radius=radius,
                                               number=attack_number)
        unit_attack_circle.set_circle_kinds(CircleKinds.ATTACK)
        self.add_shape(unit_attack_circle)

    def create_unit_hp_circle(self, image_data, hp_number, center, radius):
        unit_hp_circle = CircleNumberImage(image_data=image_data,
                                           center=center,
                                           radius=radius,
                                           number=hp_number)
        unit_hp_circle.set_circle_kinds(CircleKinds.HP)
        self.add_shape(unit_hp_circle)

    def init_shapes(self, circle_radius, card_number, rectangle_height, rectangle_width):

        self.create_unit_energy_circle(
            image_data=self.__pre_drawed_image_instance.get_pre_draw_number_image(0),
            energy_number=0,
            center=(0, 0),
            radius=circle_radius
        )

        # race_number = self.__card_info_from_csv_repository.getCardRaceForCardNumber(card_number)
        # image_data = self.__pre_drawed_image_instance.get_pre_draw_unit_race(race_number)

        self.create_unit_race_illustration_circle(
            image_data=self.__pre_drawed_image_instance.get_pre_draw_card_race_with_card_number(card_number),
            # image_data=image_data,
            center=(rectangle_width, 0),
            radius=circle_radius)

        self.create_unit_attack_circle(
            image_data=self.__pre_drawed_image_instance.get_pre_draw_card_attack_with_card_number(card_number),
            attack_number=self.__card_info_from_csv_repository.getCardAttackForCardNumber(card_number),
            center=(rectangle_width, rectangle_height),
            radius=circle_radius)

        self.create_unit_hp_circle(
            image_data=self.__pre_drawed_image_instance.get_pre_draw_card_hp_with_card_number(card_number),
            hp_number=self.__card_info_from_csv_repository.getCardHpForCardNumber(card_number),
            center=(0, rectangle_height),
            radius=circle_radius)

        # self.__imagePath = image_path
        # self.tool_card = self.create_attached_tool_card_rectangle(
        #     color=(0.6, 0.4, 0.6, 1.0),
        #     local_translation=self.local_translation,
        #     vertices=[(20, 20), (370, 20), (370, 520), (20, 520)])
        #
        # self.pickable_card_base = (
        #     self.create_card_base_pickable_rectangle(
        #         color=(0.0, 0.78, 0.34, 1.0),
        #         local_translation=self.local_translation,
        #         vertices=[(0, 0), (350, 0), (350, 500), (0, 500)]))
        #
        # self.pickable_card_base.set_attached_shapes(
        #     self.create_illustration(
        #         image_path=self.__imagePath,
        #         local_translation=self.local_translation,
        #         vertices=[(25, 25), (325, 25), (325, 325), (25, 325)]))
        #
        # # self.pickable_card_base.set_attached_shapes(
        # #     self.create_text_field(
        # #         text="Unit Card Ability",
        # #         local_translation=self.local_translation,
        # #         vertices=[(25, 350), (325, 350), (325, 450), (25, 450)]))
        #
        # project_root = get_project_root()
        # self.pickable_card_base.set_attached_shapes(
        #     self.create_equipped_mark(
        #         image_path=os.path.join(project_root, "local_storage", "card_images", "equip_white.jpg"),
        #         local_translation=self.local_translation,
        #         vertices=[(390, 30), (430, 30), (430, 70), (390, 70)]))

