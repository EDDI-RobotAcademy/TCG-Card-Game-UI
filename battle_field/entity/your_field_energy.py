from battle_field.infra.your_field_energy_repository import YourFieldEnergyRepository
from image_shape.rectangle_image import RectangleImage
from opengl_shape.rectangle import Rectangle
from pre_drawed_image_manager.pre_drawed_image import PreDrawedImage



class YourFieldEnergy:
    __pre_drawed_image = PreDrawedImage.getInstance()
    __your_field_energy_repository = YourFieldEnergyRepository.getInstance()

    def __init__(self):
        self.your_field_energy_panel = None

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

    def get_your_field_energy_panel(self):
        return self.your_field_energy_panel

    def create_your_field_energy_panel(self):
        # x1 = 0.138
        # x2 = 0.224
        # y1 = 0.767
        # y2 = 0.959

        left_x_point = self.total_width * 0.905
        right_x_point = self.total_width * 0.995
        top_y_point = self.total_height * 0.767
        bottom_y_point = self.total_height * 0.959

        self.your_field_energy_panel = RectangleImage(
            self.__pre_drawed_image.get_pre_draw_rectangle_number_image(self.__your_field_energy_repository.get_your_field_energy()),
            [
                (left_x_point, top_y_point),
                (right_x_point, top_y_point),
                (right_x_point, bottom_y_point),
                (left_x_point, bottom_y_point)
            ],
            (0, 0),
            (0, 0))

        # self.your_field_energy_panel.draw()

    def get_your_field_energy_panel_popup_rectangle(self):
        return self.your_field_energy_popup

    def create_your_field_energy_panel_popup_rectangle(self):
        # width_left_margin_20 = self.popup_width * 0.2 * self.width_ratio
        # width_right_margin_80 = self.popup_width * 0.8 * self.width_ratio
        # height_top_margin_20 = self.popup_height * 0.2 * self.height_ratio
        # height_bottom_margin_80 = self.popup_height * 0.8 * self.height_ratio
        width_left_margin_20 = self.total_width * 0.2
        width_right_margin_80 = self.total_width * 0.8
        height_top_margin_20 = self.total_height * 0.2
        height_bottom_margin_80 = self.total_height * 0.8

        self.your_field_energy_popup = Rectangle(
            (0.0, 0.0, 0.0, 0.8),
            [
                (width_left_margin_20, height_top_margin_20),
                (width_left_margin_20, height_bottom_margin_80),
                (width_right_margin_80, height_bottom_margin_80),
                (width_right_margin_80, height_top_margin_20)
            ],
            (0, 0),
            (0, 0))


        # TODO: 가만 보니 border에 문제가 있는 것 같다 (울퉁 불퉁 해지는 경향이 있음)
        self.your_field_energy_popup.set_draw_border(False)

    def is_point_inside_popup_rectangle(self, point):
        point_x, point_y = point
        point_y *= -1

        energy_popup_panel = self.get_your_field_energy_panel_popup_rectangle()

        translated_vertices = [
            (x * self.width_ratio + energy_popup_panel.local_translation[0] * self.width_ratio,
             y * self.height_ratio + energy_popup_panel.local_translation[1] * self.height_ratio)
            for x, y in energy_popup_panel.get_vertices()
        ]

        # print(f"is_point_inside_popup_rectangle -> x: {point_x}, y: {point_y}")
        # print(f"is_point_inside_popup_rectangle -> translated_vertices: {translated_vertices}")

        if not (translated_vertices[0][0] <= point_x <= translated_vertices[1][0] and
                translated_vertices[2][1] <= point_y <= translated_vertices[0][1]):
            return False

        print("your energy popup panel result -> True")
        return True

    def is_point_inside(self, point):

        point_x, point_y = point
        point_y *= -1

        energy_panel = self.get_your_field_energy_panel()

        translated_vertices = [
            (x * self.width_ratio + energy_panel.local_translation[0] * self.width_ratio, y * self.height_ratio + energy_panel.local_translation[1] * self.height_ratio)
            for x, y in energy_panel.get_vertices()
        ]

        if not (translated_vertices[0][0] <= point_x <= translated_vertices[1][0] and
                translated_vertices[0][1] <= point_y <= translated_vertices[2][1]):
            print("your field energy panel result -> False")
            return False

        print("your field energy panel result -> True")
        return True

    def update_curent_field_energy_panel(self):
        self.your_field_energy_panel.set_image_data(
            self.__pre_drawed_image.get_pre_draw_rectangle_number_image(
                self.__your_field_energy_repository.get_your_field_energy()))

    def use_energy_card(self):
        print("use_energy_card")
        #energy_count = self.__your_field_energy_repository.get_to_use_field_energy_count()
        energy_race = self.__your_field_energy_repository.get_current_field_energy_race()

        #.__your_field_energy_repository.decrease_your_field_energy(energy_count)

