from opengl_shape.rectangle import Rectangle


class YourTomb:
    def __init__(self):
        self.your_tomb_panel = None
        self.tomb_panel_popup_rectangle = None

        self.popup_width = None
        self.popup_height = None

        self.width_ratio = 1
        self.height_ratio = 1

    def set_total_window_size(self, width, height):
        self.popup_width = width
        self.popup_height = height

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
        self.your_tomb_panel = Rectangle(
            (0.0, 0.0, 0.0, 0.1),
            [(255, 970), (255, 790), (415, 790), (415, 970)],
            (0, 0),
            (0, 0))

    def get_tomb_panel_popup_rectangle(self):
        return self.tomb_panel_popup_rectangle

    def create_tomb_panel_popup_rectangle(self):
        width_left_margin_20 = self.popup_width * 0.2 * self.width_ratio
        width_right_margin_80 = self.popup_width * 0.8 * self.width_ratio
        height_top_margin_20 = self.popup_height * 0.2 * self.height_ratio
        height_bottom_margin_80 = self.popup_height * 0.8 * self.height_ratio

        self.tomb_panel_popup_rectangle = Rectangle(
            (0.0, 0.0, 0.0, 0.8),
            [
                (width_left_margin_20, height_top_margin_20),
                (width_left_margin_20, height_bottom_margin_80),
                (width_right_margin_80, height_bottom_margin_80),
                (width_right_margin_80, height_top_margin_20)
            ],
            (0, 0),
            (0, 0))

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
