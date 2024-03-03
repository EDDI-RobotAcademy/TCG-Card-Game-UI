from image_shape.rectangle_image import RectangleImage
from opengl_shape.rectangle import Rectangle
from pre_drawed_image_manager.pre_drawed_image import PreDrawedImage


class SurrenderConfirm:
    __pre_drawed_image = PreDrawedImage.getInstance()

    def __init__(self):
        self.surrender_confirm_panel_list = []

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

    def get_surrender_confirm_panel_list(self):
        return self.surrender_confirm_panel_list

    def create_surrender_confirm_panel_list(self):
        self.create_surrender_confirm_panel_ok_button()
        self.create_surrender_confirm_panel_cancel_button()
        self.create_surrender_confirm_panel()


    def create_surrender_confirm_panel(self):
        # x1 = 0.138
        # x2 = 0.224
        # y1 = 0.767
        # y2 = 0.959

        left_x_point = self.total_width * 0.3
        right_x_point = self.total_width * 0.7
        top_y_point = self.total_height * 0.3
        bottom_y_point = self.total_height * 0.7

        surrender_confirm_panel = RectangleImage(
            self.__pre_drawed_image.get_pre_draw_surrender_confirm_panel(),
            [
                (left_x_point, top_y_point),
                (right_x_point, top_y_point),
                (right_x_point, bottom_y_point),
                (left_x_point, bottom_y_point)
            ],
            (0, 0),
            (0, 0))
        #surrender_confirm_panel.set_draw_border(False)
        self.surrender_confirm_panel_list.append(surrender_confirm_panel)

    def create_surrender_confirm_panel_ok_button(self):
        left_x_point = self.total_width * 0.54
        right_x_point = self.total_width * 0.65
        top_y_point = self.total_height * 0.58
        bottom_y_point = self.total_height * 0.645

        ok_button = Rectangle(
            (0, 0, 0, 0.5),
            [
                (left_x_point, top_y_point),
                (right_x_point, top_y_point),
                (right_x_point, bottom_y_point),
                (left_x_point, bottom_y_point)
            ],
            (0, 0),
            (0, 0))
        ok_button.set_draw_border(False)
        self.surrender_confirm_panel_list.append(ok_button)

    def create_surrender_confirm_panel_cancel_button(self):
        left_x_point = self.total_width * 0.35
        right_x_point = self.total_width * 0.46
        top_y_point = self.total_height * 0.58
        bottom_y_point = self.total_height * 0.645

        cancel_button = Rectangle(
            (0, 0, 0, 0.5),
            [
                (left_x_point, top_y_point),
                (right_x_point, top_y_point),
                (right_x_point, bottom_y_point),
                (left_x_point, bottom_y_point)
            ],
            (0, 0),
            (0, 0))
        cancel_button.set_draw_border(False)
        self.surrender_confirm_panel_list.append(cancel_button)

    def is_point_inside_cancel(self, point):
        point_x, point_y = point
        point_y *= -1

        surrender_confirm_panel_cancel_button = self.surrender_confirm_panel_list[1]

        translated_vertices = [
            (
                x * self.width_ratio + surrender_confirm_panel_cancel_button.local_translation[0] * self.width_ratio, y *
                self.height_ratio + surrender_confirm_panel_cancel_button.local_translation[1] * self.height_ratio)
            for x, y in surrender_confirm_panel_cancel_button.get_vertices()
        ]

        if not (translated_vertices[0][0] <= point_x <= translated_vertices[1][0] and
                translated_vertices[0][1] <= point_y <= translated_vertices[2][1]):
            print("your next field energy race panel result -> False")
            return False

        print("your next field energy race panel result -> True")
        return True

    def is_point_inside_ok(self, point):
        point_x, point_y = point
        point_y *= -1

        surrender_confirm_panel_ok_button = self.surrender_confirm_panel_list[0]

        translated_vertices = [
            (
                x * self.width_ratio + surrender_confirm_panel_ok_button.local_translation[0] * self.width_ratio, y *
                self.height_ratio + surrender_confirm_panel_ok_button.local_translation[1] * self.height_ratio)
            for x, y in surrender_confirm_panel_ok_button.get_vertices()
        ]

        if not (translated_vertices[0][0] <= point_x <= translated_vertices[1][0] and
                translated_vertices[0][1] <= point_y <= translated_vertices[2][1]):
            print("your next field energy race panel result -> False")
            return False

        print("your next field energy race panel result -> True")
        return True

