from battle_field.infra.battle_field_repository import BattleFieldRepository
from image_shape.non_background_image import NonBackgroundImage
from image_shape.rectangle_image import RectangleImage
from opengl_shape.rectangle import Rectangle
from pre_drawed_image_manager.pre_drawed_image import PreDrawedImage


class BattleResult:
    __pre_drawed_image = PreDrawedImage.getInstance()
    __battle_field_repository = BattleFieldRepository.getInstance()

    def __init__(self):
        self.battle_result_panel_list = []

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

    def get_battle_result_panel_list(self):
        return self.battle_result_panel_list

    def create_battle_result_panel_list(self):
        self.battle_result_panel_list = []
        self.create_battle_result_text()
        self.create_battle_result_panel()



    def create_battle_result_panel(self):

        left_x_point = self.total_width * 0
        right_x_point = self.total_width * 1
        top_y_point = self.total_height * 0.3
        bottom_y_point = self.total_height * 0.7

        # print(f"게임 끝~~ {self.__battle_field_repository.get_is_game_end()}")
        # print(f"이겼냐 {self.__battle_field_repository.get_is_win()}")

        battle_result_panel = Rectangle(
            (0, 0, 0, 0.5),
            [
                (left_x_point, top_y_point),
                (right_x_point, top_y_point),
                (right_x_point, bottom_y_point),
                (left_x_point, bottom_y_point)
            ],
            (0, 0),
            (0, 0))
        battle_result_panel.set_draw_border(False)

        self.battle_result_panel_list.append(battle_result_panel)

    def create_battle_result_text(self):
        if self.__battle_field_repository.get_is_win().name == 'Winner':
            image_data = self.__pre_drawed_image.get_pre_draw_win_text()
        elif self.__battle_field_repository.get_is_win().name == 'Loser':
            image_data = self.__pre_drawed_image.get_pre_draw_lose_text()
        else:
            #todo : 무승부일 때 이미지가 필요함.
            image_data = self.__pre_drawed_image.get_pre_draw_lose_text()


        left_x_point = self.total_width * 0.35
        right_x_point = self.total_width * 0.65
        top_y_point = self.total_height * 0.35
        bottom_y_point = self.total_height * 0.65

        battle_result_text = NonBackgroundImage(
            image_data,
            [
                (left_x_point, top_y_point),
                (right_x_point, top_y_point),
                (right_x_point, bottom_y_point),
                (left_x_point, bottom_y_point)
            ],
            (0, 0),
            (0, 0))
        # self.battle_result_panel.set_draw_border(False)

        self.battle_result_panel_list.append(battle_result_text)
