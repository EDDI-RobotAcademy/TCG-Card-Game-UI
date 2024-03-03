from opengl_shape.rectangle import Rectangle


class OpponentMainCharacter:
    def __init__(self):
        self.opponent_main_character_panel = None

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

    def get_opponent_main_character_panel(self):
        return self.opponent_main_character_panel

    def create_opponent_main_character_panel(self):
        # 1848, 1016

        left_x_point = self.total_width * 0.4572
        right_x_point = self.total_width * 0.5450
        top_y_point = self.total_height * 0.0442
        bottom_y_point = self.total_height * 0.2131

        self.opponent_main_character_panel = Rectangle(
            (0.0, 0.0, 0.0, 0.1),
            [
                (left_x_point, bottom_y_point),
                (left_x_point, top_y_point),
                (right_x_point, top_y_point),
                (right_x_point, bottom_y_point)
            ],
            (0, 0),
            (0, 0))

    def is_point_inside(self, point):
        point_x, point_y = point
        point_y *= -1

        opponent_main_character_panel = self.get_opponent_main_character_panel()

        translated_vertices = [
            (x * self.width_ratio + opponent_main_character_panel.local_translation[0] * self.width_ratio, y * self.height_ratio + opponent_main_character_panel.local_translation[1] * self.height_ratio)
            for x, y in opponent_main_character_panel.get_vertices()
        ]

        if not (translated_vertices[0][0] <= point_x <= translated_vertices[2][0] and
                translated_vertices[1][1] <= point_y <= translated_vertices[0][1]):
            return False

        print("opponent_main_character_panel result -> True")
        return True
