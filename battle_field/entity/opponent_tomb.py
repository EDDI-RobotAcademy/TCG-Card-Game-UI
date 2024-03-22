from image_shape.non_background_image import NonBackgroundImage
from opengl_shape.rectangle import Rectangle
from pre_drawed_image_manager.pre_drawed_image import PreDrawedImage


class OpponentTomb:
    def __init__(self):
        self.opponent_tomb_panel = None
        self.opponent_tomb_panel_popup_rectangle = None
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

    def get_opponent_tomb_panel(self):
        return self.opponent_tomb_panel

    def create_opponent_tomb_panel(self):
        # x1 = 0.781
        # x2 = 0.867
        # y1 = 0.024
        # y2 = 0.215

        left_x_point = self.total_width * 0.781
        right_x_point = self.total_width * 0.867
        top_y_point = self.total_height * 0.024
        bottom_y_point = self.total_height * 0.215

        self.opponent_tomb_panel = Rectangle(
            (0.0, 0.0, 0.0, 0.1),
            [
                (left_x_point, bottom_y_point),
                (left_x_point, top_y_point),
                (right_x_point, top_y_point),
                (right_x_point, bottom_y_point)
            ],
            (0, 0),
            (0, 0))

    def get_opponent_tomb_panel_popup_rectangle(self):
        return self.opponent_tomb_panel_popup_rectangle

    def create_opponent_tomb_panel_popup_rectangle(self):
        width_left_margin_20 = self.total_width * 0.2
        width_right_margin_80 = self.total_width * 0.8
        height_top_margin_20 = self.total_height * 0.2
        height_bottom_margin_80 = self.total_height * 0.8

        # self.opponent_tomb_panel_popup_rectangle = Rectangle(
        #     (0.0, 0.0, 0.0, 0.8),
        #     [
        #         (width_left_margin_20, height_top_margin_20),
        #         (width_left_margin_20, height_bottom_margin_80),
        #         (width_right_margin_80, height_bottom_margin_80),
        #         (width_right_margin_80, height_top_margin_20)
        #     ],
        #     (0, 0),
        #     (0, 0))
        #
        # self.opponent_tomb_panel_popup_rectangle.set_draw_border(False)



        self.opponent_tomb_panel_popup_rectangle = NonBackgroundImage(
            self.pre_draw_image.get_pre_draw_popup_panel(),
            [
                (width_left_margin_20, height_top_margin_20),
                (width_left_margin_20, height_bottom_margin_80),
                (width_right_margin_80, height_bottom_margin_80),
                (width_right_margin_80, height_top_margin_20)
            ],
            (0, 0),
            (0, 0))

        # self.opponent_tomb_panel_popup_rectangle.set_draw_border(False)

    def is_point_inside_popup_rectangle(self, point):
        point_x, point_y = point
        point_y *= -1

        tomb_popup_panel = self.get_opponent_tomb_panel_popup_rectangle()

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

    def is_point_inside(self, point):
        point_x, point_y = point
        point_y *= -1

        tomb_panel = self.get_opponent_tomb_panel()

        translated_vertices = [
            (x * self.width_ratio + tomb_panel.local_translation[0] * self.width_ratio, y * self.height_ratio + tomb_panel.local_translation[1] * self.height_ratio)
            for x, y in tomb_panel.get_vertices()
        ]

        if not (translated_vertices[0][0] <= point_x <= translated_vertices[2][0] and
                translated_vertices[1][1] <= point_y <= translated_vertices[0][1]):
            return False

        print("opponent tomb panel result -> True")
        return True
