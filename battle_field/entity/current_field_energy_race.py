from battle_field.infra.your_field_energy_repository import YourFieldEnergyRepository
from image_shape.rectangle_image import RectangleImage
from opengl_shape.rectangle import Rectangle
from pre_drawed_image_manager.pre_drawed_image import PreDrawedImage



class CurrentFieldEnergyRace:
    __pre_drawed_image = PreDrawedImage.getInstance()
    __your_field_energy_repository = YourFieldEnergyRepository.getInstance()

    def __init__(self):
        self.current_field_energy_race_panel = None

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

    def get_current_field_energy_race_panel(self):
        return self.current_field_energy_race_panel

    def create_current_field_energy_race_panel(self):

        left_x_point = self.total_width * 0.93
        right_x_point = self.total_width * 0.97
        top_y_point = self.total_height * 0.717
        bottom_y_point = self.total_height * 0.757

        self.current_field_energy_race_panel = RectangleImage(
            image_data=self.__pre_drawed_image.get_pre_draw_energy_race_with_race_number(
                self.__your_field_energy_repository.get_current_field_energy_race().value),
            vertices=[
                (left_x_point, top_y_point),
                (right_x_point, top_y_point),
                (right_x_point, bottom_y_point),
                (left_x_point, bottom_y_point)
            ])

    def update_current_field_energy_race_panel(self):
        self.current_field_energy_race_panel.set_image_data(
            self.__pre_drawed_image.get_pre_draw_energy_race_with_race_number(
                self.__your_field_energy_repository.get_current_field_energy_race().value)
        )