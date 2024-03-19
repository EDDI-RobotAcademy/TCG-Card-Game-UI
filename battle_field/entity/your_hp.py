from colorama import Style

from battle_field.infra.battle_field_repository import BattleFieldRepository
from battle_field.infra.your_hp_repository import YourHpRepository
from common.survival_type import SurvivalType
from image_shape.rectangle_image import RectangleImage
from opengl_shape.rectangle import Rectangle
from pre_drawed_image_manager.pre_drawed_image import PreDrawedImage
from image_shape.non_background_image import NonBackgroundImage


class YourHp:
    __pre_drawed_image = PreDrawedImage.getInstance()
    __your_hp_repository = YourHpRepository.getInstance()
    __battle_field_repository = BattleFieldRepository().getInstance()

    def __init__(self):
        self.your_hp_panel = None
        self.current_your_hp_state = self.__your_hp_repository.get_current_your_hp_state()

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

    def get_your_hp_panel(self):
        return self.your_hp_panel

    def set_current_your_hp_state(self, current_your_hp_state):
        self.current_your_hp_state = current_your_hp_state

    def draw_current_your_hp_panel(self):
        # 546 / 330 = 1.654545

        # start_x = center[0] - 5 - radius * 1.0
        # end_x = center[0] - 5 + radius * 1.0
        # start_y = center[1] - 12 - radius * 1.618 * 1.0
        # end_y = center[1] - 12 + radius * 1.618 * 1.0

        # vertices = [
        #     (start_x, start_y),
        #     (end_x, start_y),
        #     (end_x, end_y),
        #     (start_x, end_y),
        # ]

        # width: 1848, height: 1016
        # x: 1057, y: -755
        # x: 957, y: -750
        # 1057 / 1848 -> 0.58
        # 957  / 1848  -> 0.51
        # 비율 고려 했을 때 x -> 100, y -> 165.4545
        # UI 배치 상 x: 963, y: -786 좌표가 이쁨
        # 786 / 1016 -> 0.77362
        # 이론 수치상 165를 빼야 하므로 621 / 1016 -> 0.61122
        # 차이 (difference) -> 0.1624
        # 위 기준은 x 값 100

        # 카드 가시성을 헤치므로 80으로 조정
        # 80 / 1848 -> 0.0432
        # 80 * 1.654545 -> 132.3636
        # 132.3636 / 1016 -> 0.13028

        left_x_point = self.total_width * 0.53
        right_x_point = self.total_width * 0.58
        top_y_point = self.total_height * 0.66816
        bottom_y_point = self.total_height * 0.79844

        self.your_hp_panel = NonBackgroundImage(
            image_data=self.__pre_drawed_image.get_pre_draw_character_hp_image(self.current_your_hp_state.get_current_health()),
            #image_data=self.__pre_drawed_image.get_pre_draw_number_image(self.current_your_hp_state.get_current_health()),
            vertices=[
                (left_x_point, top_y_point),
                (right_x_point, top_y_point),
                (right_x_point, bottom_y_point),
                (left_x_point, bottom_y_point)
            ]
        )



       # self.your_hp_panel.draw()

    def update_current_your_hp_panel(self):
        # print(f"update_current_your_hp_panel(): {self.current_your_hp_state.get_current_health()}{Style.RESET_ALL}")
        self.your_hp_panel.set_image_data(self.__pre_drawed_image.get_pre_draw_character_hp_image(self.current_your_hp_state.get_current_health()))

    def check_you_are_survival(self):
        if self.__your_hp_repository.get_your_character_survival_info() == SurvivalType.DEATH:
            self.__battle_field_repository.lose()
