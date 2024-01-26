import os

from opengl_shape.circle import Circle

class EnergyCard():
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

    def create_energy_race_circle(self, color, center, radius):
        unit_tribe_circle = Circle(color=color,
                                   center=center,
                                   radius=radius)
        self.add_shape(unit_tribe_circle)

    def create_energy_type_circle(self, color, center, radius):
        unit_attack_circle = Circle(color=color,
                                    center=center,
                                    radius=radius)
        self.add_shape(unit_attack_circle)


    def init_shapes(self):

        circle_radius = 30

        self.create_energy_race_circle(color=(0.678, 0.847, 0.902, 1.0),
                                        center=(350, 0),
                                        radius=circle_radius)

        self.create_energy_type_circle(color=(0.988, 0.976, 0.800, 1.0),
                                        center=(350, 500),
                                        radius=circle_radius)