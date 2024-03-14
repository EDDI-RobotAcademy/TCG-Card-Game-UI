import math

from battle_field.infra.round_repository import RoundRepository
from battle_field.infra.your_field_energy_repository import YourFieldEnergyRepository
from image_shape.circle_image import CircleImage
from image_shape.non_background_image import NonBackgroundImage
from image_shape.rectangle_image import RectangleImage
from opengl_shape.rectangle import Rectangle
from pre_drawed_image_manager.pre_drawed_image import PreDrawedImage



class MessageOnTheBattleScreen:
    __pre_drawed_image = PreDrawedImage.getInstance()

    def __init__(self):
        self.current_message_on_the_battle_screen = None

        self.total_width = None
        self.total_height = None

        self.width_ratio = 1
        self.height_ratio = 1

    def set_total_window_size(self, width, height):
        self.total_width = width
        self.total_height = height

    def get_width_ratio(self):
        return self.width_ratio

    def set_width_ratio(self, width_ratio):
        self.width_ratio = width_ratio

    def get_height_ratio(self):
        return self.height_ratio

    def set_height_ratio(self, height_ratio):
        self.height_ratio = height_ratio

    def change_local_translation(self, _translation):
        self.local_translation = _translation

    def get_current_message_on_the_battle_screen(self):
        return self.current_message_on_the_battle_screen

    def clear_current_message_on_the_battle_screen(self):
        self.current_message_on_the_battle_screen = None

    def create_message_on_the_battle_screen(self, number):

        left_x_point = self.total_width * 0
        right_x_point = self.total_width
        top_y_point = self.total_height * 0.61
        bottom_y_point = self.total_height * 0.78

        self.current_message_on_the_battle_screen = NonBackgroundImage(
            image_data=self.__pre_drawed_image.get_pre_draw_message_on_the_battle_screen(number),
            vertices=[
                (left_x_point, top_y_point),
                (right_x_point, top_y_point),
                (right_x_point, bottom_y_point),
                (left_x_point, bottom_y_point)
            ],
            global_translation=(0, 0),
            local_translation=(0, 0)
        )
