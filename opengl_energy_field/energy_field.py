import os

from opengl_shape.circle import Circle

class EnergyField:
    __imagePath = None

    def __init__(self, local_translation=(0, 0), scale=1):
        self.shapes = []
        self.local_translation = local_translation
        self.scale = scale

    def change_energy_field_translation(self, _translation):
        self.local_translation = _translation

    def get_energy_field_shapes(self):
        return self.shapes

    def add_shape(self, shape):
        shape.local_translate(self.local_translation)
        self.shapes.append(shape)

    def create_energy_field_circle(self, color, center, radius):
        energy_field_circle = Circle(color=color,
                                    center=center,
                                    radius=radius)
        self.add_shape(energy_field_circle)
    def init_shapes(self):

        circle_radius = 30
        self.create_energy_field_circle(color=(0.5, 0.33, 0.34, 1.0),
                                       center=(1280, 510),
                                       radius=circle_radius)

        self.create_energy_field_circle(color=(0.1, 0.33, 0.34, 1.0),
                                       center=(640, 570),
                                       radius=circle_radius)