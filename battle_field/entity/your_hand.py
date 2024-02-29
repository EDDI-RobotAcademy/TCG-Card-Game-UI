from image_shape.non_background_image import NonBackgroundImage
from pre_drawed_image_manager.pre_drawed_image import PreDrawedImage

class YourHand:
    __pre_drawed_image_instance = PreDrawedImage.getInstance()

    def __init__(self):

        self.total_width = None
        self.total_height = None

        self.width_ratio = 1
        self.height_ratio = 1

        self.next_gold_button_hand = None
        self.prev_gold_button_hand = None

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


    def create_next_gold_button_hand(self, vertices):
        next_gold_button_image_data = self.__pre_drawed_image_instance.get_pre_draw_next_gold_button()
        self.next_gold_button_hand = NonBackgroundImage(image_data=next_gold_button_image_data,
                                                   vertices=vertices)

    def create_prev_gold_button_hand(self, vertices):
        prev_gold_button_image_data = self.__pre_drawed_image_instance.get_pre_draw_prev_gold_button()
        self.prev_gold_button_hand = NonBackgroundImage(image_data=prev_gold_button_image_data,
                                                   vertices=vertices)

    def init_next_prev_gold_button_hand(self):
        prev_left_x_point = self.total_width * 0.259
        prev_right_x_point = self.total_width * 0.291
        prev_top_y_point = self.total_height * 0.910
        prev_bottom_y_point = self.total_height * 0.946

        self.create_prev_gold_button_hand(
            vertices=[
                (prev_left_x_point, prev_top_y_point),
                (prev_right_x_point, prev_top_y_point),
                (prev_right_x_point, prev_bottom_y_point),
                (prev_left_x_point, prev_bottom_y_point)
            ])

        next_left_x_point = self.total_width * 0.706
        next_right_x_point = self.total_width * 0.738
        next_top_y_point = self.total_height * 0.910
        next_bottom_y_point = self.total_height * 0.946

        self.create_next_gold_button_hand(
            vertices=[
                (next_left_x_point, next_top_y_point),
                (next_right_x_point, next_top_y_point),
                (next_right_x_point, next_bottom_y_point),
                (next_left_x_point, next_bottom_y_point)
            ])

    def get_prev_gold_button_hand(self):
        return self.prev_gold_button_hand

    def get_next_gold_button_hand(self):
        return self.next_gold_button_hand

    def is_point_inside_prev_button_hand(self, point):
        point_x, point_y = point
        point_y *= -1
        # point_x = self.total_width - point_x

        prev_gold_button_hand = self.get_prev_gold_button_hand()
        # print(f"prev_gold_button: {prev_gold_button.get_vertices()}")
        # print(f"point -> x: {point_x}, y: {point_y}")

        translated_vertices = [
            (x * self.width_ratio + prev_gold_button_hand.local_translation[0] * self.width_ratio,
             y * self.height_ratio + prev_gold_button_hand.local_translation[1] * self.height_ratio)
            for x, y in prev_gold_button_hand.get_vertices()
        ]

        if not (translated_vertices[0][0] <= point_x <= translated_vertices[2][0] and
                translated_vertices[0][1] <= point_y <= translated_vertices[2][1]):
            return False

        print("prev button clicked!")
        return True

    def is_point_inside_next_button_hand(self, point):
        point_x, point_y = point
        point_y *= -1

        next_gold_button_hand = self.get_next_gold_button_hand()
        # print(f"next_gold_button: {next_gold_button.get_vertices()}")
        # print(f"point: {point}")

        translated_vertices = [
            (x * self.width_ratio + next_gold_button_hand.local_translation[0] * self.width_ratio,
             y * self.height_ratio + next_gold_button_hand.local_translation[1] * self.height_ratio)
            for x, y in next_gold_button_hand.get_vertices()
        ]

        if not (translated_vertices[0][0] <= point_x <= translated_vertices[2][0] and
                translated_vertices[0][1] <= point_y <= translated_vertices[2][1]):
            return False

        print("next button clicked!")
        return True