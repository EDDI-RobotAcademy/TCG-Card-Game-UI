from opengl_shape.rectangle import Rectangle
from pre_drawed_image_manager.pre_drawed_image import PreDrawedImage


class TurnEnd:
    __pre_drawed_image = PreDrawedImage.getInstance()

    def __init__(self):
        self.turn_end_button = None

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

    def get_turn_end_button(self):
        return self.turn_end_button

    def create_turn_end_button(self):
        # x1 = 0.138
        # x2 = 0.224
        # y1 = 0.767
        # y2 = 0.959

        left_x_point = self.total_width * 0.892
        right_x_point = self.total_width * 0.99
        top_y_point = self.total_height * 0.42
        bottom_y_point = self.total_height * 0.58
        
        self.turn_end_button = Rectangle(
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

        turn_end_button = self.get_turn_end_button()

        translated_vertices = [
            (
            x * self.width_ratio + turn_end_button.local_translation[0] * self.width_ratio, y *
            self.height_ratio + turn_end_button.local_translation[1] * self.height_ratio)
            for x, y in turn_end_button.get_vertices()
        ]

        if not (translated_vertices[0][0] <= point_x <= translated_vertices[1][0] and
                translated_vertices[0][1] <= point_y <= translated_vertices[2][1]):
            print("your next field energy race panel result -> False")
            return False

        print("your next field energy race panel result -> True")
        return True
