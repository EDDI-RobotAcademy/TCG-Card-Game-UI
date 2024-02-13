import os

from opengl_shape.circle import Circle

class TokenCard:
    __imagePath = None

    def __init__(self, local_translation=(0, 0), scale=1):
        self.shapes = []
        self.local_translation = local_translation
        self.scale = scale

    def change_local_translation(self, _translation):
        self.local_translation = _translation

    def get_shapes(self):
        return self.shapes

    def add_shape(self, shape):
        shape.local_translate(self.local_translation)
        self.shapes.append(shape)

    def create_token_energy_circle(self, color, center, radius):
        unit_energy_circle = Circle(color=color,
                                    center=center,
                                    radius=radius)
        self.add_shape(unit_energy_circle)

    def create_token_tribe_circle(self, color, center, radius):
        unit_tribe_circle = Circle(color=color,
                                   center=center,
                                   radius=radius)
        self.add_shape(unit_tribe_circle)

    def create_token_attack_circle(self, color, center, radius):
        unit_attack_circle = Circle(color=color,
                                    center=center,
                                    radius=radius)
        self.add_shape(unit_attack_circle)

    def create_token_hp_circle(self, color, center, radius):
        unit_hp_circle = Circle(color=color,
                                center=center,
                                radius=radius)
        self.add_shape(unit_hp_circle)

    def init_shapes(self, circle_radius, card_number):

        self.create_token_energy_circle(color=(1.0, 0.33, 0.34, 1.0),
                                        center=(0, 0),
                                        radius=circle_radius)

        self.create_token_tribe_circle(color=(0.678, 0.847, 0.902, 1.0),
                                       center=(350, 0),
                                       radius=circle_radius)

        self.create_token_attack_circle(color=(0.988, 0.976, 0.800, 1.0),
                                        center=(350, 500),
                                        radius=circle_radius)

        self.create_token_hp_circle(color=(0.267, 0.839, 0.475, 1.0),
                                    center=(0, 500),
                                    radius=circle_radius)