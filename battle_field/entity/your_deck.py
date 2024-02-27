from opengl_shape.rectangle import Rectangle


class YourDeck:
    def __init__(self):
        self.your_deck_popup_rectangle = None

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

    def get_your_deck_popup_rectangle(self):
        return self.your_deck_popup_rectangle

    def create_your_deck_popup_rectangle(self):
        width_left_margin_20 = self.total_width * 0.2
        width_right_margin_80 = self.total_width * 0.8
        height_top_margin_20 = self.total_height * 0.2
        height_bottom_margin_80 = self.total_height * 0.8

        self.your_deck_popup_rectangle = Rectangle(
            (0.0, 0.0, 0.0, 0.8),
            [
                (width_left_margin_20, height_top_margin_20),
                (width_left_margin_20, height_bottom_margin_80),
                (width_right_margin_80, height_bottom_margin_80),
                (width_right_margin_80, height_top_margin_20)
            ],
            (0, 0),
            (0, 0))

        self.your_deck_popup_rectangle.set_draw_border(False)

    def is_point_inside_popup_rectangle(self, point):
        point_x, point_y = point
        point_y *= -1

        your_deck_popup_rectangle = self.get_your_deck_popup_rectangle()

        translated_vertices = [
            (x * self.width_ratio + your_deck_popup_rectangle.local_translation[0] * self.width_ratio,
             y * self.height_ratio + your_deck_popup_rectangle.local_translation[1] * self.height_ratio)
            for x, y in your_deck_popup_rectangle.get_vertices()
        ]

        if not (translated_vertices[0][0] <= point_x <= translated_vertices[2][0] and
                translated_vertices[0][1] <= point_y <= translated_vertices[1][1]):
            return False

        print("your deck popup result -> True")
        return True

