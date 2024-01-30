import os

from opengl_battle_field.entity.battle_field import BattleField
from opengl_shape.image_rectangle_element import ImageRectangleElement
from opengl_shape.rectangle import Rectangle


class HandDeck:
    __imagePath = None

    def __init__(self, local_translation=(0, 0), scale=1):
        self.shapes = []
        self.local_translation = local_translation
        self.scale = scale
        self.battle_field = BattleField()

    def get_hand_deck_shapes(self):
        return self.shapes
    def change_local_translation(self, _translation):
        self.local_translation = _translation

    def add_shape(self, shape):
        shape.local_translate(self.local_translation)
        self.shapes.append(shape)
    def create_hand_deck_rectangle(self, color, vertices):
        tomb_base = Rectangle(color=color,
                                       vertices=vertices)
        tomb_base.set_visible(True)
        self.add_shape(tomb_base)

    def create_illustration(self, image_path, vertices):
        unit_illustration = ImageRectangleElement(image_path=image_path,
                                         vertices=vertices)
        self.add_shape(unit_illustration)

    def init_shapes(self, imagePath):

        self.__imagePath = imagePath
        self.create_hand_deck_rectangle(color=(0, 0, 0, 1.0),
                                   vertices=[(600, 860), (750, 860), (750, 1055), (600, 1055)])

        self.create_illustration(image_path=self.__imagePath,
                                 vertices=[(600, 860), (750, 860), (750, 1055), (600, 1055)])

    def redraw_shapes_with_scale(self, scale: float):
        print(f"scale : {scale}")

        self.shapes = []

        # self.scale = scale * self.scale
        self.scale = 3 / (scale + 1)
        rectangle_width = 350 * self.scale
        rectangle_height = 500 * self.scale

        print(f"local_translation = {self.local_translation}")
        self.local_translation = ((self.scale * self.local_translation[0]), 0)
        #
        # self.create_attached_tool_card_rectangle(color=(0.6, 0.4, 0.6, 1.0),
        #                                          vertices=[(20 * self.scale, 20 * self.scale),
        #                                                    (20 * self.scale + rectangle_width, 20 * self.scale),
        #                                                    (20 * self.scale + rectangle_width,
        #                                                     20 * self.scale + rectangle_height),
        #                                                    (20 * self.scale, 20 * self.scale + rectangle_height)])
        #
        # self.create_card_base_rectangle(color=(0.0, 0.78, 0.34, 1.0),
        #                                 vertices=[(0, 0), (rectangle_width, 0),
        #                                           (rectangle_width, rectangle_height), (0, rectangle_height)])

        self.create_illustration(image_path=self.__imagePath,
                                 vertices=[(25 * self.scale, 25 * self.scale),
                                           (rectangle_width - 25 * self.scale, 25 * self.scale),
                                           (rectangle_width - 25 * self.scale, rectangle_height - 25 * self.scale),
                                           (25 * self.scale, rectangle_height - 25 * self.scale)])

        # project_root = get_project_root()
        # self.create_equipped_mark(
        #     image_path=os.path.join(project_root, "local_storage", "card_images", "equip_white.jpg"),
        #     vertices=[(rectangle_width + 40 * self.scale, 30 * self.scale),
        #               (rectangle_width + 80 * self.scale, 30 * self.scale),
        #               (rectangle_width + 80 * self.scale, 70 * self.scale),
        #               (rectangle_width + 40 * self.scale, 70 * self.scale)])
        #
        # circle_radius = 30 * self.scale
        # self.create_unit_energy_circle(color=(1.0, 0.33, 0.34, 1.0),
        #                                center=(0, 0),
        #                                radius=circle_radius)
        #
        # self.create_unit_tribe_circle(color=(0.678, 0.847, 0.902, 1.0),
        #                               center=(rectangle_width, 0),
        #                               radius=circle_radius)
        #
        # self.create_unit_attack_circle(color=(0.988, 0.976, 0.800, 1.0),
        #                                center=(rectangle_width, rectangle_height),
        #                                radius=circle_radius)
        #
        # self.create_unit_hp_circle(color=(0.267, 0.839, 0.475, 1.0),
        #                            center=(0, rectangle_height),
        #                            radius=circle_radius)
