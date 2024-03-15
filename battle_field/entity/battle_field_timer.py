from battle_field.infra.opponent_hp_repository import OpponentHpRepository
from image_shape.rectangle_image import RectangleImage
from opengl_shape.rectangle import Rectangle
from pre_drawed_image_manager.pre_drawed_image import PreDrawedImage
from image_shape.non_background_image import NonBackgroundImage
from pyopengltk import OpenGLFrame

class BattleFieldTimer(OpenGLFrame):
    __pre_drawed_image = PreDrawedImage.getInstance()

    def __init__(self):
        super().__init__()
        self.timer_panel = None
        self.timer = 0
        self.timer_id = None

        self.total_width = None
        self.total_height = None

        self.width_ratio = 1
        self.height_ratio = 1

        self.function = None


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

    def set_function(self, function):
        self.function = function

    def draw_current_timer_panel(self):

        left_x_point = self.total_width * 0.05
        right_x_point = self.total_width * 0.12
        top_y_point = self.total_height * 0.60
        bottom_y_point = self.total_height * 0.70

        self.timer_panel = RectangleImage(
            image_data=self.__pre_drawed_image.get_pre_draw_battle_field_timer(self.timer),
            vertices=[
                (left_x_point, top_y_point),
                (right_x_point, top_y_point),
                (right_x_point, bottom_y_point),
                (left_x_point, bottom_y_point)
            ])


    def update_current_timer_panel(self):
        if self.timer >= 0:
            self.timer_panel.set_image_data(self.__pre_drawed_image.get_pre_draw_battle_field_timer(self.timer))

    def start_timer(self):
        if self.timer >= -1:
            self.timer -= 1
            self.timer_id = self.master.after(1000, self.start_timer)
        if self.timer == -1:
            self.function()

    def stop_timer(self):
        if self.timer_id is not None:
            self.master.after_cancel(self.timer_id)
            self.timer_id = None

    def deleteTimer(self):
        self.destroy()
