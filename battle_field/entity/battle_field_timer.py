from battle_field.infra.battle_field_timer_repository import BattleFieldTimerRepository
from pre_drawed_image_manager.pre_drawed_image import PreDrawedImage
from image_shape.non_background_image import NonBackgroundImage
from pyopengltk import OpenGLFrame

class BattleFieldTimer(OpenGLFrame):
    __pre_drawed_image = PreDrawedImage.getInstance()
    __battle_field_timer_repository = BattleFieldTimerRepository.getInstance()

    def __init__(self):
        super().__init__()
        self.timer_panel = None
        self.timer_id = None
        self.unit_timer_id = None

        self.total_width = None
        self.total_height = None

        self.width_ratio = 1
        self.height_ratio = 1

        self.function = self.__battle_field_timer_repository.get_function()
        self.timer = self.__battle_field_timer_repository.get_timer()
        self.unit_timeout_function = self.__battle_field_timer_repository.get_unit_timeout_function()

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

    def draw_current_timer_panel(self):

        left_x_point = self.total_width * 0.865
        right_x_point = self.total_width
        top_y_point = self.total_height * 0.245
        bottom_y_point = self.total_height * 0.351

        self.timer_panel = NonBackgroundImage(
            image_data=self.__pre_drawed_image.get_pre_draw_battle_field_timer(self.timer),
            vertices=[
                (left_x_point, top_y_point),
                (right_x_point, top_y_point),
                (right_x_point, bottom_y_point),
                (left_x_point, bottom_y_point)
            ],
            global_translation=(0, 0),
            local_translation=(0, 0)

        )

    def update_current_timer_panel(self):
        if self.timer >= 0:
            self.timer_panel.set_image_data(self.__pre_drawed_image.get_pre_draw_battle_field_timer(self.timer))

    def get_timer(self):
        self.timer = self.__battle_field_timer_repository.get_timer()
        self.function = self.__battle_field_timer_repository.get_function()
        self.unit_timeout_function = self.__battle_field_timer_repository.get_unit_timeout_function()

    def start_timer(self):
        if self.timer >= -1:
            self.timer -= 1
            self.timer_id = self.master.after(1000, self.start_timer)
        if self.timer == -1:
            self.unit_timeout_function()
            self.function()


    def stop_timer(self):
        if self.timer_id is not None:
            self.master.after_cancel(self.timer_id)
            self.timer_id = None

    def deleteTimer(self):
        self.destroy()


