from battle_field.infra.opponent_hp_repository import OpponentHpRepository
from image_shape.rectangle_image import RectangleImage
from opengl_shape.rectangle import Rectangle
from pre_drawed_image_manager.pre_drawed_image import PreDrawedImage


class BattleFieldTimer:
    __pre_drawed_image = PreDrawedImage.getInstance()

    def __init__(self):
        self.timer_panel = None
        self.timer = 30

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

    def get_timer_panel(self):
        return self.timer_panel

    def set_timer(self, timer):
        self.timer = timer

    def draw_current_opponent_hp_panel(self):


        left_x_point = self.total_width * 0.33
        right_x_point = self.total_width * 0.42
        top_y_point = self.total_height * 0.135
        bottom_y_point = self.total_height * 0.206

        self.timer_panel = RectangleImage(
            image_data=self.__pre_drawed_image.get_pre_draw_character_hp_image(self.timer),
            #image_data=self.__pre_drawed_image.get_pre_draw_number_image(self.current_your_hp_state.get_current_health()),
            vertices=[
                (left_x_point, top_y_point),
                (right_x_point, top_y_point),
                (right_x_point, bottom_y_point),
                (left_x_point, bottom_y_point)
            ])

        #self.opponent_hp_panel.draw()

    def update_current_opponent_hp_panel(self):
        self.timer -= 1
        self.timer_panel.set_image_data(self.__pre_drawed_image.get_pre_draw_character_hp_image(self.timer))

