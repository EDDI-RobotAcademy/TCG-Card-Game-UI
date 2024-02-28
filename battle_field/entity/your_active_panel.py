from card_info_from_csv.repository.card_info_from_csv_repository_impl import CardInfoFromCsvRepositoryImpl
from opengl_shape.rectangle import Rectangle


class YourActivePanel:
    card_info_repository = CardInfoFromCsvRepositoryImpl.getInstance()

    def __init__(self):
        self.your_active_panel = None

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

    def get_your_active_panel(self):
        return self.your_active_panel

    def clear_your_active_panel(self):
        self.your_active_panel = None

    def create_your_active_panel(self, start_point, selected_object):
        card_id = selected_object.get_card_number()
        skill_count = self.card_info_repository.getCardSkillCounterForCardNumber(card_id)

        width_size = 100 * self.width_ratio
        height_size = (62 * self.height_ratio) * (skill_count + 1)

        rectangle_color = (1.0, 1.0, 1.0, 0.6)

        end_point = (start_point[0] + width_size, start_point[1] + height_size)

        self.your_active_panel = Rectangle(
            rectangle_color,
            [
                (start_point[0], start_point[1]),
                (end_point[0], start_point[1]),
                (end_point[0], end_point[1]),
                (start_point[0], end_point[1])
            ],
            (0, 0),
            (0, 0))

    def is_point_inside(self, point):
        point_x, point_y = point
        point_y *= -1

        lost_zone_panel = self.get_your_lost_zone_panel()

        translated_vertices = [
            (x * self.width_ratio + lost_zone_panel.local_translation[0] * self.width_ratio, y * self.height_ratio + lost_zone_panel.local_translation[1] * self.height_ratio)
            for x, y in lost_zone_panel.get_vertices()
        ]

        if not (translated_vertices[0][0] <= point_x <= translated_vertices[2][0] and
                translated_vertices[1][1] <= point_y <= translated_vertices[0][1]):
            print("your lostzone panel result -> False")
            return False

        print("your tomb panel result -> True")
        return True
