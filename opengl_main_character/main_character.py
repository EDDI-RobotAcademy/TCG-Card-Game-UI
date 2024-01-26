import os

from opengl_shape.oval import Oval


class MainCharacter:
    __imagePath = None

    def __init__(self, local_translation=(0, 0), scale=1):
        self.shapes = []
        self.local_translation = local_translation
        self.scale = scale

    def change_main_character_translation(self, _translation):
        self.local_translation = _translation

    def get_main_character_shapes(self):
        return self.shapes

    def add_shape(self, shape):
        shape.local_translate(self.local_translation)
        self.shapes.append(shape)

    def create_main_character_oval(self, color, center, radius_x, radius_y):
        main_character_oval = Oval(color=color, center=center, radius_x=radius_x, radius_y=radius_y)

        self.add_shape(main_character_oval)

    def init_your_main_character_shapes(self):

        radius_x = 100
        radius_y = 50

        self.create_main_character_oval(color=(0, 0, 0, 1.0),
                                       center=(960, 780),
                                       radius_x=radius_x, radius_y=radius_y)

    def init_opponent_main_character_shapes(self):
        radius_x = 100
        radius_y = 50

        self.create_main_character_oval(color=(0, 0, 0, 0),
                                             center=(960, 100),
                                             radius_x=radius_x, radius_y=radius_y)