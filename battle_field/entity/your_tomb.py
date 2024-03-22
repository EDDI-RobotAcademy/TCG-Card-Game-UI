from image_shape.non_background_image import NonBackgroundImage
from opengl_shape.rectangle import Rectangle
from pre_drawed_image_manager.pre_drawed_image import PreDrawedImage


class YourTomb:
    def __init__(self):
        self.your_tomb_panel = None
        self.tomb_panel_popup_rectangle = None
        self.pre_draw_image = PreDrawedImage.getInstance()
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

    def get_your_tomb_panel(self):
        return self.your_tomb_panel

    def create_your_tomb_panel(self):
        # x1 = 0.138
        # x2 = 0.224
        # y1 = 0.767
        # y2 = 0.959

        left_x_point = self.total_width * 0.138
        right_x_point = self.total_width * 0.224
        top_y_point = self.total_height * 0.767
        bottom_y_point = self.total_height * 0.959

        self.your_tomb_panel = Rectangle(
            (0.0, 0.0, 0.0, 0.1),
            [
                (left_x_point, bottom_y_point),
                (left_x_point, top_y_point),
                (right_x_point, top_y_point),
                (right_x_point, bottom_y_point)
            ],
            (0, 0),
            (0, 0))

    def get_tomb_panel_popup_rectangle(self):
        return self.tomb_panel_popup_rectangle

    def create_tomb_panel_popup_rectangle(self):
        # width_left_margin_20 = self.popup_width * 0.2 * self.width_ratio
        # width_right_margin_80 = self.popup_width * 0.8 * self.width_ratio
        # height_top_margin_20 = self.popup_height * 0.2 * self.height_ratio
        # height_bottom_margin_80 = self.popup_height * 0.8 * self.height_ratio
        width_left_margin_20 = self.total_width * 0.2
        width_right_margin_80 = self.total_width * 0.8
        height_top_margin_20 = self.total_height * 0.2
        height_bottom_margin_80 = self.total_height * 0.8

        self.tomb_panel_popup_rectangle = NonBackgroundImage(
            self.pre_draw_image.get_pre_draw_popup_panel(),
            [
                (width_left_margin_20, height_top_margin_20),
                (width_left_margin_20, height_bottom_margin_80),
                (width_right_margin_80, height_bottom_margin_80),
                (width_right_margin_80, height_top_margin_20)
            ],
            (0, 0),
            (0, 0))
        # TODO: 가만 보니 border에 문제가 있는 것 같다 (울퉁 불퉁 해지는 경향이 있음)
        # self.tomb_panel_popup_rectangle.set_draw_border(False)

    def is_point_inside_popup_rectangle(self, point):
        point_x, point_y = point
        point_y *= -1

        tomb_popup_panel = self.get_tomb_panel_popup_rectangle()

        translated_vertices = [
            (x * self.width_ratio + tomb_popup_panel.local_translation[0] * self.width_ratio,
             y * self.height_ratio + tomb_popup_panel.local_translation[1] * self.height_ratio)
            for x, y in tomb_popup_panel.get_vertices()
        ]

        # print(f"is_point_inside_popup_rectangle -> x: {point_x}, y: {point_y}")
        # print(f"is_point_inside_popup_rectangle -> translated_vertices: {translated_vertices}")

        if not (translated_vertices[0][0] <= point_x <= translated_vertices[2][0] and
                translated_vertices[0][1] <= point_y <= translated_vertices[1][1]):
            return False

        print("your tomb popup panel result -> True")
        return True

    def is_point_inside(self, point):
        point_x, point_y = point
        point_y *= -1

        # print(f"your_tomb is_point_inside -> x: {point_x}, y: {point_y}")

        tomb_panel = self.get_your_tomb_panel()

        # translated_vertices = [
        #     (x * self.width_ratio + self.global_translation[0] + self.local_translation[0] * self.width_ratio,
        #      y * self.height_ratio + self.global_translation[1] + self.local_translation[1] * self.height_ratio)
        #     for x, y in tomb_panel.get_vertices()
        # ]

        # translated_vertices = [
        #     (x * self.width_ratio + self.local_translation[0] * self.width_ratio,
        #      y * self.height_ratio + self.local_translation[1] * self.height_ratio)
        #     for x, y in tomb_panel.get_vertices()
        # ]

        # print(f"tomb_panel.get_vertices(): {tomb_panel.get_vertices()}")

        translated_vertices = [
            (x * self.width_ratio + tomb_panel.local_translation[0] * self.width_ratio, y * self.height_ratio + tomb_panel.local_translation[1] * self.height_ratio)
            for x, y in tomb_panel.get_vertices()
        ]

        # print(f"your tomb translated_vertices: {translated_vertices}")
        # print(f"your tomb translated_vertices[0]: {translated_vertices[0]}")
        # print(f"your tomb translated_vertices[1]: {translated_vertices[1]}")
        # print(f"your tomb translated_vertices[2]: {translated_vertices[2]}")
        # print(f"your tomb translated_vertices[3]: {translated_vertices[3]}")
        #
        # print(f"translated_vertices[0][0] <= point_x <= translated_vertices[2][0] result: {translated_vertices[0][0] <= point_x <= translated_vertices[2][0]}")
        # print(f"translated_vertices[0][1] <= point_y <= translated_vertices[1][1] result: {translated_vertices[0][1] <= point_y <= translated_vertices[1][1]}")

        if not (translated_vertices[0][0] <= point_x <= translated_vertices[2][0] and
                translated_vertices[1][1] <= point_y <= translated_vertices[0][1]):
            print("your tomb panel result -> False")
            return False

        print("your tomb panel result -> True")
        return True
