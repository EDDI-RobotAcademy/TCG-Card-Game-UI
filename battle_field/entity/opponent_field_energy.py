from battle_field.infra.opponent_field_energy_repository import OpponentFieldEnergyRepository
from image_shape.non_background_image import NonBackgroundImage
from image_shape.rectangle_image import RectangleImage
from opengl_shape.rectangle import Rectangle
from pre_drawed_image_manager.pre_drawed_image import PreDrawedImage



class OpponentFieldEnergy:
    __pre_drawed_image = PreDrawedImage.getInstance()
    __opponent_field_energy_repository = OpponentFieldEnergyRepository.getInstance()

    def __init__(self):
        self.opponent_field_energy_panel = None

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

    def get_opponent_field_energy_panel(self):
        return self.opponent_field_energy_panel

    def create_opponent_field_energy_panel(self):
        # x1 = 0.138
        # x2 = 0.224
        # y1 = 0.767
        # y2 = 0.959


        left_x_point = self.total_width * 0.027
        right_x_point = self.total_width * 0.11
        top_y_point = self.total_height * 0.032
        bottom_y_point = self.total_height * 0.193

        self.opponent_field_energy_panel = RectangleImage(
            image_data=self.__pre_drawed_image.get_pre_draw_field_energy(self.__opponent_field_energy_repository.get_opponent_field_energy()),
            vertices=[
                (left_x_point, top_y_point),
                (right_x_point, top_y_point),
                (right_x_point, bottom_y_point),
                (left_x_point, bottom_y_point)
            ],
            global_translation=(0, 0),
            local_translation=(0, 0)
        )

        # self.opponent_field_energy_panel.draw()

    def update_current_opponent_field_energy_panel(self):
        self.opponent_field_energy_panel.set_image_data(
            self.__pre_drawed_image.get_pre_draw_field_energy(
                self.__opponent_field_energy_repository.get_opponent_field_energy()))

