from opengl_shape.rectangle import Rectangle
from pre_drawed_image_manager.pre_drawed_image import PreDrawedImage


class Option:
    __pre_drawed_image = PreDrawedImage.getInstance()

    def __init__(self):
        self.option_button = None
        self.option_button_popup = None

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

    def get_option_button(self):
        return self.option_button

    def create_option_button(self):
        # x1 = 0.138
        # x2 = 0.224
        # y1 = 0.767
        # y2 = 0.959

        left_x_point = self.total_width * 0.015
        right_x_point = self.total_width * 0.055
        top_y_point = self.total_height * 0.43
        bottom_y_point = self.total_height * 0.57

        self.option_button = Rectangle(
            (0, 0, 0, 0.1),
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

        option_button = self.get_option_button()

        translated_vertices = [
            (
            x * self.width_ratio + option_button.local_translation[0] * self.width_ratio, y *
            self.height_ratio + option_button.local_translation[1] * self.height_ratio)
            for x, y in option_button.get_vertices()
        ]

        if not (translated_vertices[0][0] <= point_x <= translated_vertices[1][0] and
                translated_vertices[0][1] <= point_y <= translated_vertices[2][1]):
            print("your next field energy race panel result -> False")
            return False

        print("your next field energy race panel result -> True")
        return True

    def get_option_button_popup(self):
        return self.option_button_popup

    def create_option_button_popup(self):
        width_left = self.total_width * 0.065
        width_right = self.total_width * 0.165
        height_top = self.total_height * 0.43
        height_bottom = self.total_height * 0.57

        self.option_button_popup = Rectangle(
            (0.0, 0.0, 0.0, 0.8),
            [
                (width_left, height_top),
                (width_left, height_bottom),
                (width_right, height_bottom),
                (width_right, height_top)
            ],
            (0, 0),
            (0, 0))

        self.option_button_popup.set_draw_border(False)

    def is_point_inside_popup(self, point):
        point_x, point_y = point
        point_y *= -1

        tomb_popup_panel = self.get_option_button_popup()

        translated_vertices = [
            (x * self.width_ratio + tomb_popup_panel.local_translation[0] * self.width_ratio,
             y * self.height_ratio + tomb_popup_panel.local_translation[1] * self.height_ratio)
            for x, y in tomb_popup_panel.get_vertices()
        ]

        if not (translated_vertices[0][0] <= point_x <= translated_vertices[2][0] and
                translated_vertices[0][1] <= point_y <= translated_vertices[1][1]):
            return False

        print("opponent tomb popup panel result -> True")
        return True