import os

from common.utility import get_project_root
from opengl_shape.circle import Circle
from opengl_shape.image_element import ImageElement
from opengl_shape.rectangle import Rectangle


class UnitCard:
    def __init__(self, local_translation=(0, 0)):
        self.shapes = []
        self.local_translation = local_translation

    def get_unit_shapes(self):
        return self.shapes

    def add_shape(self, shape):
        shape.local_translate(self.local_translation)
        self.shapes.append(shape)

    def create_attached_tool_card_rectangle(self, color, vertices):
        attached_tool_card = Rectangle(color=color,
                                       vertices=vertices)
        attached_tool_card.set_draw_gradient(True)
        attached_tool_card.set_visible(False)
        self.add_shape(attached_tool_card)

    def create_card_base_rectangle(self, color, vertices):
        unit_card_base = Rectangle(color=color,
                                   vertices=vertices)
        unit_card_base.set_draw_gradient(True)
        self.add_shape(unit_card_base)

    def create_illustration(self, image_path, vertices):
        unit_illustration = ImageElement(image_path=image_path,
                                         vertices=vertices)
        self.add_shape(unit_illustration)

    def create_equipped_mark(self, image_path, vertices):
        unit_equipped_mark = ImageElement(image_path=image_path,
                                          vertices=vertices)
        unit_equipped_mark.set_visible(False)
        self.add_shape(unit_equipped_mark)

    def create_unit_energy_circle(self, color, center, radius):
        unit_energy_circle = Circle(color=color,
                                    center=center,
                                    radius=radius)
        self.add_shape(unit_energy_circle)

    def create_unit_tribe_circle(self, color, center, radius):
        unit_tribe_circle = Circle(color=color,
                                   center=center,
                                   radius=radius)
        self.add_shape(unit_tribe_circle)

    def create_unit_attack_circle(self, color, center, radius):
        unit_attack_circle = Circle(color=color,
                                    center=center,
                                    radius=radius)
        self.add_shape(unit_attack_circle)

    def create_unit_hp_circle(self, color, center, radius):
        unit_hp_circle = Circle(color=color,
                                center=center,
                                radius=radius)
        self.add_shape(unit_hp_circle)

    def init_shapes(self, image_path):
        self.create_attached_tool_card_rectangle(color=(0.6, 0.4, 0.6, 1.0),
                                                 vertices=[(20, 20), (370, 20), (370, 520), (20, 520)])

        self.create_card_base_rectangle(color=(0.0, 0.78, 0.34, 1.0),
                                        vertices=[(0, 0), (350, 0), (350, 500), (0, 500)])

        self.create_illustration(image_path=image_path,
                                 vertices=[(25, 25), (325, 25), (325, 325), (25, 325)])

        project_root = get_project_root()
        self.create_equipped_mark(image_path=os.path.join(project_root, "local_storage", "card_images", "equip_white.jpeg"),
                                  vertices=[(390, 30), (430, 30), (430, 70), (390, 70)])

        circle_radius = 30
        self.create_unit_energy_circle(color=(1.0, 0.33, 0.34, 1.0),
                                       center=(0, 0),
                                       radius=circle_radius)

        self.create_unit_tribe_circle(color=(0.678, 0.847, 0.902, 1.0),
                                      center=(350, 0),
                                      radius=circle_radius)

        self.create_unit_attack_circle(color=(0.988, 0.976, 0.800, 1.0),
                                       center=(350, 500),
                                       radius=circle_radius)

        self.create_unit_hp_circle(color=(0.267, 0.839, 0.475, 1.0),
                                   center=(0, 500),
                                   radius=circle_radius)


