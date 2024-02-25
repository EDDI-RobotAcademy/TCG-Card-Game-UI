from battle_field.infra.battle_field_repository import BattleFieldRepository
from battle_field_muligun.entity.background.battle_field_muligun_background import BattleFieldMuligunBackground
from image_shape.rectangle_image import RectangleImage
from opengl_shape.rectangle import Rectangle
from pre_drawed_image_manager.pre_drawed_image import PreDrawedImage


class YourFieldPanel:
    __pre_drawed_image_instance = PreDrawedImage.getInstance()

    def __init__(self, local_translation=(0, 0), scale=1):
        self.your_field_panel = None
        self.local_translation = local_translation
        self.scale = scale

        self.total_width = None
        self.total_height = None

        self.width_ratio = 1
        self.height_ratio = 1

    def set_total_window_size(self, width, height):
        self.total_width = width
        self.total_height = height

    def set_width_ratio(self, width_ratio):
        self.width_ratio = width_ratio

    def set_height_ratio(self, height_ratio):
        self.height_ratio = height_ratio

    def get_your_field_panel(self):
        return self.your_field_panel

    def change_local_translation(self, _translation):
        self.local_translation = _translation

    def create_your_field_panel(self):
        left_x_point = self.total_width * 0.138
        right_x_point = self.total_width * 0.872
        top_y_point = self.total_height * 0.470
        bottom_y_point = self.total_height * 0.667

        self.your_field_panel = Rectangle(
            (0.0, 0.0, 0.0, 0.1),
            [
                (left_x_point, bottom_y_point),
                (left_x_point, top_y_point),
                (right_x_point, top_y_point),
                (right_x_point, bottom_y_point)
            ],
            (0, 0),
            (0, 0))

        self.your_field_panel.set_draw_border(False)

