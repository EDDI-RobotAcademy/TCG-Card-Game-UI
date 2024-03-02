from battle_field.infra.your_field_energy_repository import YourFieldEnergyRepository
from image_shape.non_background_image import NonBackgroundImage
from image_shape.rectangle_image import RectangleImage
from opengl_shape.rectangle import Rectangle
from pre_drawed_image_manager.pre_drawed_image import PreDrawedImage


class CurrentToUseFieldEnergyCount:
    __pre_drawed_image = PreDrawedImage.getInstance()
    __your_field_energy_repository = YourFieldEnergyRepository.getInstance()

    def __init__(self):
        self.current_to_use_field_energy_count_panel = None

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

    def get_current_to_use_field_energy_count_panel(self):
        return self.current_to_use_field_energy_count_panel

    def create_current_to_use_field_energy_count_panel(self):

        left_x_point = self.total_width * 0.922
        right_x_point = self.total_width * 0.957
        top_y_point = self.total_height * 0.6275
        bottom_y_point = self.total_height * 0.6825

        # self.current_to_use_field_energy_count_panel = Rectangle(
        #     (0,0,0,0.1),
        #     vertices=[
        #         (left_x_point, top_y_point),
        #         (right_x_point, top_y_point),
        #         (right_x_point, bottom_y_point),
        #         (left_x_point, bottom_y_point)
        #     ])

        self.current_to_use_field_energy_count_panel = NonBackgroundImage(
            image_data=self.__pre_drawed_image.get_pre_draw_number_of_energy(
                self.__your_field_energy_repository.get_to_use_field_energy_count()),
            vertices=[
                (left_x_point, top_y_point),
                (right_x_point, top_y_point),
                (right_x_point, bottom_y_point),
                (left_x_point, bottom_y_point)
            ])

        # self.current_to_use_field_energy_count_panel = RectangleImage(
        #     image_data=self.__pre_drawed_image.get_pre_draw_rectangle_number_image(
        #         self.__your_field_energy_repository.get_to_use_field_energy_count()),
        #     vertices=[
        #         (left_x_point, top_y_point),
        #         (right_x_point, top_y_point),
        #         (right_x_point, bottom_y_point),
        #         (left_x_point, bottom_y_point)
        #     ])

    def update_current_to_use_field_energy_count_panel(self):
        self.current_to_use_field_energy_count_panel.set_image_data(
            self.__pre_drawed_image.get_pre_draw_number_of_energy(
                self.__your_field_energy_repository.get_to_use_field_energy_count())
        )