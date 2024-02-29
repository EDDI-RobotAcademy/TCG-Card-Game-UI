from battle_field.infra.your_field_energy_repository import YourFieldEnergyRepository
from image_shape.rectangle_image import RectangleImage
from opengl_shape.rectangle import Rectangle
from pre_drawed_image_manager.pre_drawed_image import PreDrawedImage


class PrevFieldEnergyRace:
    __pre_drawed_image = PreDrawedImage.getInstance()
    __your_field_energy_repository = YourFieldEnergyRepository.getInstance()

    def __init__(self):
        self.prev_field_energy_race_panel = None

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

    def get_prev_field_energy_race_panel(self):
        return self.prev_field_energy_race_panel

    def create_prev_field_energy_race_panel(self):
        # x1 = 0.138
        # x2 = 0.224
        # y1 = 0.767
        # y2 = 0.959

        left_x_point = self.total_width * 0.88
        right_x_point = self.total_width * 0.905
        top_y_point = self.total_height * 0.7275
        bottom_y_point = self.total_height * 0.7775

        self.prev_field_energy_race_panel = Rectangle(
            (0,0,0,0.1),
            [
                (left_x_point, top_y_point),
                (right_x_point, top_y_point),
                (right_x_point, bottom_y_point),
                (left_x_point, bottom_y_point)
            ],
            (0, 0),
            (0, 0))

    def is_point_inside(self, point):

        point_x, point_y = point
        point_y *= -1

        prev_field_energy_race_panel = self.get_prev_field_energy_race_panel()

        translated_vertices = [
            (x * self.width_ratio + prev_field_energy_race_panel.local_translation[0] * self.width_ratio, y *
             self.height_ratio + prev_field_energy_race_panel.local_translation[1] * self.height_ratio)
            for x, y in prev_field_energy_race_panel.get_vertices()
        ]

        if not (translated_vertices[0][0] <= point_x <= translated_vertices[1][0] and
                translated_vertices[0][1] <= point_y <= translated_vertices[2][1]):
            print("your prev field energy race panel result -> False")
            return False

        print("your prev field energy race panel result -> True")
        return True
