from opengl_shape.rectangle import Rectangle


class YourMainCharacter:
    def __init__(self):
        self.your_main_character_panel = None

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

    def get_your_main_character_panel(self):
        return self.your_main_character_panel

    def create_your_main_character_panel(self):
        # width: 1848, height: 1016
        # 840, 706 -> 0.45887, 0.69488
        # 1015, 895 -> 0.54924, 0.88090

        left_x_point = self.total_width * 0.45887
        right_x_point = self.total_width * 0.54924
        top_y_point = self.total_height * 0.69488
        bottom_y_point = self.total_height * 0.88091

        self.your_main_character_panel = Rectangle(
            (0.0, 0.0, 0.0, 0.1),
            [
                (left_x_point, top_y_point),
                (right_x_point, top_y_point),
                (right_x_point, bottom_y_point),
                (left_x_point, bottom_y_point),
            ],
            (0, 0),
            (0, 0))

    def is_point_inside(self, point):
        point_x, point_y = point
        point_y *= -1

        your_main_character_panel = self.get_your_main_character_panel()

        translated_vertices = [
            (x * self.width_ratio + your_main_character_panel.local_translation[0] * self.width_ratio,
             y * self.height_ratio + your_main_character_panel.local_translation[1] * self.height_ratio)
            for x, y in your_main_character_panel.get_vertices()
        ]

        print(f"point_x: {point_x}, point_y: {point_y}")
        print(f"translated_vertices: {translated_vertices}")

        if not (translated_vertices[0][0] <= point_x <= translated_vertices[2][0] and
                translated_vertices[0][1] <= point_y <= translated_vertices[2][1]):
            print("opponent_main_character_panel result -> False")
            return False

        print("opponent_main_character_panel result -> True")
        return True

