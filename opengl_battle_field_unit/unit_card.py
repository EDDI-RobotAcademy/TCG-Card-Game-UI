import os

from common.utility import get_project_root
from opengl_pickable_shape.pickable_rectangle import PickableRectangle
from opengl_shape.circle import Circle
from opengl_shape.image_rectangle_element import ImageRectangleElement
from opengl_shape.rectangle import Rectangle
#from tests.ugly_text_field.test_ugly_text_field_rectangle import TextFieldRectangle


class UnitCard:
    __imagePath = None

    def __init__(self, local_translation=(0, 0), scale=1):
        self.tool_card = None
        self.pickable_card_base = None
        self.local_translation = local_translation
        self.scale = scale

    def change_local_translation(self, _translation):
        self.local_translation = _translation

    def get_pickable_unit_card_base(self):
        return self.pickable_card_base

    def get_tool_card(self):
        return self.tool_card

    def add_shape(self, shape):
        shape.local_translate(self.local_translation)
        self.shapes.append(shape)

    def create_attached_tool_card_rectangle(self, color, vertices, local_translation):
        attached_tool_card = Rectangle(color=color,
                                       local_translation=local_translation,
                                       vertices=vertices)
        attached_tool_card.set_draw_gradient(True)
        attached_tool_card.set_visible(False)
        return attached_tool_card

    def create_card_base_pickable_rectangle(self, color, vertices, local_translation):
        pickable_unit_card_base = PickableRectangle(color=color,
                                                    local_translation=local_translation,
                                                    vertices=vertices)
        pickable_unit_card_base.set_draw_gradient(True)
        return pickable_unit_card_base

    def create_illustration(self, image_path, vertices, local_translation):
        unit_illustration = ImageRectangleElement(image_path=image_path,
                                         local_translation=local_translation,
                                         vertices=vertices)
        return unit_illustration

    # def create_text_field(self, text, vertices, local_translation):
    #     unit_text_field = TextFieldRectangle(text=text,
    #                                          local_translation=local_translation,
    #                                          vertices=vertices)
    #     return unit_text_field

    def create_equipped_mark(self, image_path, vertices, local_translation):
        unit_equipped_mark = ImageRectangleElement(image_path=image_path,
                                          local_translation=local_translation,
                                          vertices=vertices)
        unit_equipped_mark.set_visible(False)
        return unit_equipped_mark

    def create_unit_energy_circle(self, color, center, radius, local_translation):
        unit_energy_circle = Circle(color=color,
                                    local_translation=local_translation,
                                    center=center,
                                    radius=radius)
        return unit_energy_circle

    def create_unit_race_circle(self, color, center, radius, local_translation):
        unit_race_circle = Circle(color=color,
                                  local_translation=local_translation,
                                  center=center,
                                  radius=radius)
        return unit_race_circle

    def create_unit_attack_circle(self, color, center, radius, local_translation):
        unit_attack_circle = Circle(color=color,
                                    local_translation=local_translation,
                                    center=center,
                                    radius=radius)
        return unit_attack_circle

    def create_unit_hp_circle(self, color, center, radius, local_translation):
        unit_hp_circle = Circle(color=color,
                                local_translation=local_translation,
                                center=center,
                                radius=radius)
        return unit_hp_circle

    def init_unit_card(self, image_path):
        self.__imagePath = image_path
        self.tool_card = self.create_attached_tool_card_rectangle(
            color=(0.6, 0.4, 0.6, 1.0),
            local_translation=self.local_translation,
            vertices=[(20, 20), (370, 20), (370, 520), (20, 520)])

        self.pickable_card_base = (
            self.create_card_base_pickable_rectangle(
                color=(0.0, 0.78, 0.34, 1.0),
                local_translation=self.local_translation,
                vertices=[(0, 0), (350, 0), (350, 500), (0, 500)]))

        self.pickable_card_base.set_attached_shapes(
            self.create_illustration(
                image_path=self.__imagePath,
                local_translation=self.local_translation,
                vertices=[(25, 25), (325, 25), (325, 325), (25, 325)]))

        # self.pickable_card_base.set_attached_shapes(
        #     self.create_text_field(
        #         text="Unit Card Ability",
        #         local_translation=self.local_translation,
        #         vertices=[(25, 350), (325, 350), (325, 450), (25, 450)]))

        project_root = get_project_root()
        self.pickable_card_base.set_attached_shapes(
            self.create_equipped_mark(
                image_path=os.path.join(project_root, "local_storage", "card_images", "equip_white.jpg"),
                local_translation=self.local_translation,
                vertices=[(390, 30), (430, 30), (430, 70), (390, 70)]))

        circle_radius = 30
        self.pickable_card_base.set_attached_shapes(
            self.create_unit_energy_circle(
                color=(1.0, 0.33, 0.34, 1.0),
                center=(0, 0),
                local_translation=self.local_translation,
                radius=circle_radius))

        self.pickable_card_base.set_attached_shapes(
            self.create_unit_race_circle(
                color=(0.678, 0.847, 0.902, 1.0),
                center=(350, 0),
                local_translation=self.local_translation,
                radius=circle_radius))

        self.pickable_card_base.set_attached_shapes(
            self.create_unit_attack_circle(
                color=(0.988, 0.976, 0.800, 1.0),
                center=(350, 500),
                local_translation=self.local_translation,
                radius=circle_radius))

        self.pickable_card_base.set_attached_shapes(
            self.create_unit_hp_circle(
                color=(0.267, 0.839, 0.475, 1.0),
                center=(0, 500),
                local_translation=self.local_translation,
                radius=circle_radius))

    def redraw_shapes_with_scale(self, scale: float):
        print(f"scale : {scale}")

        self.shapes = []

        # self.scale = scale * self.scale
        self.scale = 3 / (scale + 1)
        rectangle_width = 350 * self.scale
        rectangle_height = 500 * self.scale

        print(f"local_translation = {self.local_translation}")
        self.local_translation = ((self.scale * self.local_translation[0]), 0)

        self.create_attached_tool_card_rectangle(color=(0.6, 0.4, 0.6, 1.0),
                                                 vertices=[(20 * self.scale, 20 * self.scale),
                                                           (20 * self.scale + rectangle_width, 20 * self.scale),
                                                           (20 * self.scale + rectangle_width,
                                                            20 * self.scale + rectangle_height),
                                                           (20 * self.scale, 20 * self.scale + rectangle_height)])

        self.create_card_base_rectangle(color=(0.0, 0.78, 0.34, 1.0),
                                        vertices=[(0, 0), (rectangle_width, 0),
                                                  (rectangle_width, rectangle_height), (0, rectangle_height)])

        self.create_illustration(image_path=self.__imagePath,
                                 vertices=[(25 * self.scale, 25 * self.scale),
                                           (rectangle_width - 25 * self.scale, 25 * self.scale),
                                           (rectangle_width - 25 * self.scale, rectangle_height - 25 * self.scale),
                                           (25 * self.scale, rectangle_height - 25 * self.scale)])

        project_root = get_project_root()
        self.create_equipped_mark(
            image_path=os.path.join(project_root, "local_storage", "card_images", "equip_white.jpg"),
            vertices=[(rectangle_width + 40 * self.scale, 30 * self.scale),
                      (rectangle_width + 80 * self.scale, 30 * self.scale),
                      (rectangle_width + 80 * self.scale, 70 * self.scale),
                      (rectangle_width + 40 * self.scale, 70 * self.scale)])

        circle_radius = 30 * self.scale
        self.create_unit_energy_circle(color=(1.0, 0.33, 0.34, 1.0),
                                       center=(0, 0),
                                       radius=circle_radius)

        self.create_unit_tribe_circle(color=(0.678, 0.847, 0.902, 1.0),
                                      center=(rectangle_width, 0),
                                      radius=circle_radius)

        self.create_unit_attack_circle(color=(0.988, 0.976, 0.800, 1.0),
                                       center=(rectangle_width, rectangle_height),
                                       radius=circle_radius)

        self.create_unit_hp_circle(color=(0.267, 0.839, 0.475, 1.0),
                                   center=(0, rectangle_height),
                                   radius=circle_radius)
