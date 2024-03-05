from image_shape.rectangle_image import RectangleImage
from opengl_shape.rectangle import Rectangle
from pre_drawed_image_manager.pre_drawed_image import PreDrawedImage


class Option:
    __pre_drawed_image = PreDrawedImage.getInstance()

    def __init__(self):
        self.option_button = None
        self.option_button_popup_list = []

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

        left_x_point = self.total_width * 0.0
        right_x_point = self.total_width * 0.045
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

    def get_option_button_popup_list(self):
        return self.option_button_popup_list


    def create_option_button_popup_list(self):

        #self.create_option_button_popup_cancel_button()
        self.create_option_button_popup()
        self.create_option_button_popup_surrender_button()

    def create_option_button_popup(self):
        width_left = self.total_width * 0.045
        width_right = self.total_width * 0.13
        height_top = self.total_height * 0.455
        height_bottom = self.total_height * 0.535

        option_button_popup = Rectangle(
            (0.0, 0.0, 0.0, 0.5),
            [
                (width_left, height_top),
                (width_left, height_bottom),
                (width_right, height_bottom),
                (width_right, height_top)
            ],
            (0, 0),
            (0, 0))

        option_button_popup.set_draw_border(False)

        self.option_button_popup_list.append(option_button_popup)

    def create_option_button_popup_surrender_button(self):

        width_left = self.total_width * 0.049
        width_right = self.total_width * 0.125
        height_top = self.total_height * 0.465
        height_bottom = self.total_height * 0.525

        surrender_button = RectangleImage(
            self.__pre_drawed_image.get_pre_draw_surrender_button(),
            [
                (width_left, height_top),
                (width_right, height_top),
                (width_right, height_bottom),
                (width_left, height_bottom)
            ],
            (0, 0),
            (0, 0))

        #surrender_button.set_draw_border(False)

        self.option_button_popup_list.append(surrender_button)

    def create_option_button_popup_cancel_button(self):

        width_left = self.total_width * 0.047
        width_right = self.total_width * 0.127
        height_top = self.total_height * 0.508
        height_bottom = self.total_height * 0.568

        cancel_button = Rectangle(
            (0.0, 1.0, 0.0, 0.5),
            [
                (width_left, height_top),
                (width_left, height_bottom),
                (width_right, height_bottom),
                (width_right, height_top)
            ],
            (0, 0),
            (0, 0))

        cancel_button.set_draw_border(False)

        self.option_button_popup_list.append(cancel_button)


    def is_point_inside_option_close(self, point):
        point_x, point_y = point
        point_y *= -1

        option_close = self.get_option_button_popup_list()[1]

        translated_vertices = [
            (x * self.width_ratio + option_close.local_translation[0] * self.width_ratio,
             y * self.height_ratio + option_close.local_translation[1] * self.height_ratio)
            for x, y in option_close.get_vertices()
        ]

        if not (translated_vertices[0][0] <= point_x <= translated_vertices[1][0] and
                translated_vertices[0][1] <= point_y <= translated_vertices[2][1]):
            return False

        print("opponent tomb popup panel result -> True")
        return True

    def is_point_inside_option_surrender(self, point):
        point_x, point_y = point
        point_y *= -1

        option_surrender = self.get_option_button_popup_list()[1]

        translated_vertices = [
            (x * self.width_ratio + option_surrender.local_translation[0] * self.width_ratio,
             y * self.height_ratio + option_surrender.local_translation[1] * self.height_ratio)
            for x, y in option_surrender.get_vertices()
        ]

        if not (translated_vertices[0][0] <= point_x <= translated_vertices[1][0] and
                translated_vertices[0][1] <= point_y <= translated_vertices[2][1]):
            return False

        print("opponent tomb popup panel result -> True")
        return True