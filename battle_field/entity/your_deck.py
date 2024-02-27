from image_shape.non_background_image import NonBackgroundImage
from opengl_shape.rectangle import Rectangle
from pre_drawed_image_manager.pre_drawed_image import PreDrawedImage


class YourDeck:
    __pre_drawed_image_instance = PreDrawedImage.getInstance()

    def __init__(self):
        self.your_deck_popup_rectangle = None

        self.total_width = None
        self.total_height = None

        self.width_ratio = 1
        self.height_ratio = 1

        self.next_gold_button = None
        self.prev_gold_button = None

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

    def create_next_gold_button(self, vertices):
        next_gold_button_image_data = self.__pre_drawed_image_instance.get_pre_draw_next_gold_button()
        self.next_gold_button = NonBackgroundImage(image_data=next_gold_button_image_data,
                                                   vertices=vertices)

    def create_prev_gold_button(self, vertices):
        prev_gold_button_image_data = self.__pre_drawed_image_instance.get_pre_draw_prev_gold_button()
        self.prev_gold_button = NonBackgroundImage(image_data=prev_gold_button_image_data,
                                                   vertices=vertices)

    def init_next_prev_gold_button(self):
        prev_left_x_point = self.total_width * 0.222
        prev_right_x_point = self.total_width * 0.278
        prev_top_y_point = self.total_height * 0.463
        prev_bottom_y_point = self.total_height * 0.533

        next_left_x_point = self.total_width * 0.722
        next_right_x_point = self.total_width * 0.778
        next_top_y_point = self.total_height * 0.463
        next_bottom_y_point = self.total_height * 0.533

        self.create_prev_gold_button(
            vertices=[
                (prev_left_x_point, prev_top_y_point),
                (prev_right_x_point, prev_top_y_point),
                (prev_right_x_point, prev_bottom_y_point),
                (prev_left_x_point, prev_bottom_y_point)
            ])

        self.create_next_gold_button(
            vertices=[
                (next_left_x_point, next_top_y_point),
                (next_right_x_point, next_top_y_point),
                (next_right_x_point, next_bottom_y_point),
                (next_left_x_point, next_bottom_y_point)
            ])

    def get_prev_gold_button(self):
        return self.prev_gold_button

    def get_next_gold_button(self):
        return self.next_gold_button

    def is_point_inside_prev_button(self, point):
        point_x, point_y = point
        point_y *= -1
        # point_x = self.total_width - point_x

        prev_gold_button = self.get_prev_gold_button()
        # print(f"prev_gold_button: {prev_gold_button.get_vertices()}")
        # print(f"point -> x: {point_x}, y: {point_y}")

        translated_vertices = [
            (x * self.width_ratio + prev_gold_button.local_translation[0] * self.width_ratio,
             y * self.height_ratio + prev_gold_button.local_translation[1] * self.height_ratio)
            for x, y in prev_gold_button.get_vertices()
        ]

        if not (translated_vertices[0][0] <= point_x <= translated_vertices[2][0] and
                translated_vertices[0][1] <= point_y <= translated_vertices[2][1]):
            return False

        print("prev button clicked!")
        return True

    def is_point_inside_next_button(self, point):
        point_x, point_y = point
        point_y *= -1

        next_gold_button = self.get_next_gold_button()
        # print(f"next_gold_button: {next_gold_button.get_vertices()}")
        # print(f"point: {point}")

        translated_vertices = [
            (x * self.width_ratio + next_gold_button.local_translation[0] * self.width_ratio,
             y * self.height_ratio + next_gold_button.local_translation[1] * self.height_ratio)
            for x, y in next_gold_button.get_vertices()
        ]

        if not (translated_vertices[0][0] <= point_x <= translated_vertices[2][0] and
                translated_vertices[0][1] <= point_y <= translated_vertices[2][1]):
            return False

        print("next button clicked!")
        return True

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

