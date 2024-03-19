from card_info_from_csv.repository.card_info_from_csv_repository_impl import CardInfoFromCsvRepositoryImpl
from image_shape.non_background_image import NonBackgroundImage
from image_shape.rectangle_image import RectangleImage
from opengl_shape.rectangle import Rectangle
from pre_drawed_image_manager.pre_drawed_image import PreDrawedImage


class YourHandDetailsPanel:
    card_info_repository = CardInfoFromCsvRepositoryImpl.getInstance()
    pre_drawed_image_instance = PreDrawedImage.getInstance()

    def __init__(self):
        self.your_hand_details_panel = None
        self.your_hand_details_panel_button = None

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

    def get_your_hand_details_panel(self):
        return self.your_hand_details_panel

    def clear_all_your_hand_details_panel(self):
        self.clear_your_hand_details_panel_button()
        self.clear_your_hand_details_panel()

    def clear_your_hand_details_panel(self):
        del self.your_hand_details_panel
        self.your_hand_details_panel = None

    def get_your_hand_details_panel_button(self):
        return self.your_hand_details_panel_button

    def clear_your_hand_details_panel_button(self):
        del self.your_hand_details_panel_button
        self.your_hand_details_panel_button = None

    def create_details_button(self, image_data, vertices):
        details_button = RectangleImage(image_data=image_data,
                                        vertices=vertices)

        details_button.set_initial_vertices(vertices)
        return details_button

    def create_your_hand_details_panel(self, start_point, right_clicked_object):
        card_id = right_clicked_object.get_card_number()
        skill_count = self.card_info_repository.getCardSkillCounterForCardNumber(card_id)

        width_size = 120 * self.width_ratio
        base_height_size = 74.2 * self.height_ratio
        height_size = (74.2 * self.height_ratio) * (1)

        rectangle_color = (1.0, 1.0, 1.0, 0.6)

        end_point = (start_point[0] + width_size, start_point[1] + height_size)

        self.your_hand_details_panel = Rectangle(
            rectangle_color,
            [
                (start_point[0], start_point[1]),
                (end_point[0], start_point[1]),
                (end_point[0], end_point[1]),
                (start_point[0], end_point[1])
            ],
            (0, 0),
            (0, 0))

        print(f"your_hand_details_panel -> start_point: {start_point}, end_point: {end_point}")

        button_width_size = 100 * self.width_ratio
        button_height_size = 62 * self.height_ratio

        height_margin = (base_height_size - button_height_size)

        button_end_point = (start_point[0] + button_width_size, start_point[1] + button_height_size)

        self.your_hand_details_panel_button = self.create_details_button(
            image_data=self.pre_drawed_image_instance.get_pre_draw_view_detail_button(),
            vertices=[
                (start_point[0] + 10, start_point[1] + height_margin),
                (button_end_point[0] + 10, start_point[1] + height_margin),
                (button_end_point[0] + 10, button_end_point[1]),
                (start_point[0] + 10, button_end_point[1])])

    def is_point_inside_details_button(self, point):
        point_x, point_y = point
        point_y *= -1

        details_button = self.get_your_hand_details_panel_button()

        translated_vertices = [
            (x * self.width_ratio + details_button.local_translation[0] * self.width_ratio,
             y * self.height_ratio + details_button.local_translation[1] * self.height_ratio)
            for x, y in details_button.get_vertices()
        ]

        if not (translated_vertices[0][0] <= point_x <= translated_vertices[2][0] and
                translated_vertices[1][1] <= point_y <= translated_vertices[2][1]):
            print("your attack_button result -> False")
            return False

        print("your attack_button -> True")
        return True

