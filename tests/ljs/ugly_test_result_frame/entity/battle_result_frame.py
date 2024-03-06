from OpenGL.raw.GLU import gluOrtho2D
from screeninfo import get_monitors
from OpenGL.GL import *
from pyopengltk import OpenGLFrame
from battle_field.components.fixed_unit_card_inside.fixed_unit_card_inside_action import FixedUnitCardInsideAction
from battle_field.entity.battle_field_scene import BattleFieldScene
from battle_field.entity.battle_result import BattleResult
from battle_field.entity.current_field_energy_race import CurrentFieldEnergyRace
from battle_field.entity.current_to_use_field_energy_count import CurrentToUseFieldEnergyCount
from battle_field.entity.opponent_field_energy import OpponentFieldEnergy
from battle_field.entity.opponent_field_panel import OpponentFieldPanel
from battle_field.entity.your_field_energy import YourFieldEnergy
from battle_field.entity.your_field_panel import YourFieldPanel
from battle_field.entity.your_hand import YourHand
from battle_field.infra.battle_field_repository import BattleFieldRepository
from battle_field.infra.opponent_field_energy_repository import OpponentFieldEnergyRepository
from battle_field.infra.opponent_field_unit_repository import OpponentFieldUnitRepository
from battle_field.infra.round_repository import RoundRepository
from battle_field.infra.your_field_energy_repository import YourFieldEnergyRepository
from battle_field.infra.your_field_unit_repository import YourFieldUnitRepository
from battle_field.infra.your_hand_repository import YourHandRepository
from battle_field_function.controller.battle_field_function_controller_impl import BattleFieldFunctionControllerImpl

from card_info_from_csv.repository.card_info_from_csv_repository_impl import CardInfoFromCsvRepositoryImpl

from opengl_rectangle_lightning_border.lightning_border import LightningBorder

from pre_drawed_image_manager.pre_drawed_image import PreDrawedImage

class BattleResultFrame(OpenGLFrame):

    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)

        self.init_monitor_specification()

        self.battle_field_background_shape_list = None
        self.is_reshape_not_complete = True

        self.your_field_panel = None
        self.opponent_field_panel = None

        self.lightning_border = LightningBorder()

        self.your_hand_repository = YourHandRepository.getInstance()
        self.hand_card_list = None
        self.your_hand = YourHand()
        self.your_hand_next_button = None
        self.your_hand_prev_button = None

        self.your_field_unit_repository = YourFieldUnitRepository.getInstance()

        self.card_info_repository = CardInfoFromCsvRepositoryImpl.getInstance()

        self.pre_drawed_image_instance = PreDrawedImage.getInstance()

        self.opponent_field_unit_repository = OpponentFieldUnitRepository.getInstance()

        self.your_field_energy_panel = None
        self.your_field_energy = YourFieldEnergy()
        self.your_field_energy_repository = YourFieldEnergyRepository.getInstance()
        self.your_field_energy_panel_selected = False

        self.current_field_energy_race_panel = None
        self.current_field_energy_race = CurrentFieldEnergyRace()

        self.current_to_use_field_energy_count_panel = None
        self.current_to_use_field_energy_count = CurrentToUseFieldEnergyCount()

        self.opponent_field_energy = OpponentFieldEnergy()
        self.opponent_field_energy_panel = None
        self.opponent_field_energy_repository = OpponentFieldEnergyRepository.getInstance()
        # self.opponent_field_energy_repository.increase_opponent_field_energy(3)

        self.round_repository = RoundRepository.getInstance()

        self.battle_result = BattleResult()
        self.battle_result_panel_list = []

        self.battle_field_repository = BattleFieldRepository.getInstance()

        self.bind("<Button-1>", self.on_canvas_left_click)

        # TODO: 이 부분은 임시 방편입니다 (상대방 행동 했다 가정하고 키보드 입력 받기 위함)
        self.focus_set()

        print("init finished!!!!@@@@")

        self.init_first_window(self.width, self.height)
        self.redraw()

    def reshape(self, width, height):
        print(f"Reshaping window to width={width}, height={height}")

        if self.is_reshape_not_complete:
            self.init_first_window(width, height)

        self.current_width = width
        self.current_height = height

        self.width_ratio = self.current_width / self.prev_width
        self.height_ratio = self.current_height / self.prev_height

        self.width_ratio = min(self.width_ratio, 1.0)
        self.height_ratio = min(self.height_ratio, 1.0)

        self.prev_width = self.current_width
        self.prev_height = self.current_height

        glViewport(0, 0, width, height)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluOrtho2D(0, width, height, 0)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()


    def init_monitor_specification(self):
        monitors = get_monitors()
        target_monitor = monitors[2] if len(monitors) > 2 else monitors[0]

        self.width = target_monitor.width
        self.height = target_monitor.height

        self.is_reshape_not_complete = True

        self.current_width = self.width
        self.current_height = self.height

        self.prev_width = self.width
        self.prev_height = self.height

        self.width_ratio = 1.0
        self.height_ratio = 1.0

    def initgl(self):
        glClearColor(0.0, 1.0, 1.0, 0.0)
        glOrtho(0, self.width, self.height, 0, -1, 1)

        self.tkMakeCurrent()

    def init_first_window(self, width, height):
        print(f"Operate Only Once -> width: {width}, height: {height}")
        self.width = width
        self.height = height

        self.current_width = self.width
        self.current_height = self.height

        self.prev_width = self.width
        self.prev_height = self.height
        self.is_reshape_not_complete = False

        battle_field_scene = BattleFieldScene()
        battle_field_scene.create_battle_field_cene(self.width, self.height)
        self.battle_field_background_shape_list = battle_field_scene.get_battle_field_background()

        your_field_panel_instance = YourFieldPanel()
        your_field_panel_instance.set_total_window_size(self.width, self.height)
        your_field_panel_instance.create_your_field_panel()
        self.your_field_panel = your_field_panel_instance.get_your_field_panel()

        self.fixed_unit_card_inside_action = FixedUnitCardInsideAction.Dummy

        opponent_field_panel_instance = OpponentFieldPanel()
        opponent_field_panel_instance.set_total_window_size(self.width, self.height)
        opponent_field_panel_instance.create_opponent_field_panel()
        self.opponent_field_panel = opponent_field_panel_instance.get_opponent_field_panel()

        # self.your_hand_repository.set_x_base(550)
        self.your_hand_repository.set_total_window_size(self.width, self.height)
        self.your_hand.set_total_window_size(self.width, self.height)
        self.your_hand.init_next_prev_gold_button_hand()
        self.your_hand_prev_button = self.your_hand.get_prev_gold_button_hand()
        self.your_hand_next_button = self.your_hand.get_next_gold_button_hand()

        self.hand_card_list = self.your_hand_repository.get_current_hand_card_list()

        self.your_field_energy.set_total_window_size(self.width, self.height)
        self.your_field_energy_repository.reset_field_energy()
        self.your_field_energy.create_your_field_energy_panel()
        self.your_field_energy_panel = self.your_field_energy.get_your_field_energy_panel()

        self.current_field_energy_race.set_total_window_size(self.width, self.height)
        self.current_field_energy_race.create_current_field_energy_race_panel()
        self.current_field_energy_race_panel = self.current_field_energy_race.get_current_field_energy_race_panel()

        self.current_to_use_field_energy_count.set_total_window_size(self.width, self.height)
        self.current_to_use_field_energy_count.create_current_to_use_field_energy_count_panel()
        self.current_to_use_field_energy_count_panel = (
            self.current_to_use_field_energy_count.get_current_to_use_field_energy_count_panel())

        self.opponent_field_energy.set_total_window_size(self.width, self.height)
        self.opponent_field_energy.create_opponent_field_energy_panel()
        self.opponent_field_energy_panel = self.opponent_field_energy.get_opponent_field_energy_panel()

        self.battle_result.set_total_window_size(self.width, self.height)
        self.battle_result.create_battle_result_panel_list()
        self.battle_result_panel_list = self.battle_result.get_battle_result_panel_list()

    def on_canvas_left_click(self, event):
        try:
            x, y = event.x, event.y
            y = self.winfo_reqheight() - y
            print(f"x: {x}, y: {y}")

            print("결과확인끝")
            BattleFieldFunctionControllerImpl.getInstance().callGameEndReward()

        except Exception as e:
            print(f"battle result frame left click error : {e}")

    def draw_base(self):
        print(self.battle_field_background_shape_list)
        # for battle_field_background_shape in self.battle_field_background_shape_list:
        #     print(battle_field_background_shape)
        #     battle_field_background_shape.set_width_ratio(self.width_ratio)
        #     battle_field_background_shape.set_height_ratio(self.height_ratio)
        #     battle_field_background_shape.draw()

        # # TODO: 메인 로직에선 제거해야함 (현재는 개발 편의상 배치)
        # glEnable(GL_BLEND)
        # glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        #
        # self.your_field_panel.set_width_ratio(self.width_ratio)
        # self.your_field_panel.set_height_ratio(self.height_ratio)
        # self.your_field_panel.draw()
        #
        # self.opponent_field_panel.set_width_ratio(self.width_ratio)
        # self.opponent_field_panel.set_height_ratio(self.height_ratio)
        # self.opponent_field_panel.draw()
        #
        # glDisable(GL_BLEND)

    def post_draw(self):

        self.your_field_energy.set_width_ratio(self.width_ratio)
        self.your_field_energy.set_height_ratio(self.height_ratio)
        self.your_field_energy.update_current_field_energy_panel()
        self.your_field_energy_panel.set_width_ratio(self.width_ratio)
        self.your_field_energy_panel.set_height_ratio(self.height_ratio)
        self.your_field_energy_panel.draw()

        self.opponent_field_energy.set_width_ratio(self.width_ratio)
        self.opponent_field_energy.set_height_ratio(self.height_ratio)
        self.opponent_field_energy.update_current_opponent_field_energy_panel()
        self.opponent_field_energy_panel.set_width_ratio(self.width_ratio)
        self.opponent_field_energy_panel.set_height_ratio(self.height_ratio)
        self.opponent_field_energy_panel.draw()

        self.current_field_energy_race.set_width_ratio(self.width_ratio)
        self.current_field_energy_race.set_height_ratio(self.height_ratio)
        self.current_field_energy_race.update_current_field_energy_race_panel()
        self.current_field_energy_race_panel.set_width_ratio(self.width_ratio)
        self.current_field_energy_race_panel.set_height_ratio(self.height_ratio)
        self.current_field_energy_race_panel.draw()

        self.current_to_use_field_energy_count.set_width_ratio(self.width_ratio)
        self.current_to_use_field_energy_count.set_height_ratio(self.height_ratio)
        self.current_to_use_field_energy_count.update_current_to_use_field_energy_count_panel()
        self.current_to_use_field_energy_count_panel.set_width_ratio(self.width_ratio)
        self.current_to_use_field_energy_count_panel.set_height_ratio(self.height_ratio)
        self.current_to_use_field_energy_count_panel.draw()

    def redraw(self):

        if self.is_reshape_not_complete:
            return
        print('리드로우중~~~')
        self.tkMakeCurrent()
        # glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        #
        # glDisable(GL_DEPTH_TEST)

        self.draw_base()

        # for opponent_field_unit in self.opponent_field_unit_repository.get_current_field_unit_card_object_list():
        #     if opponent_field_unit is None:
        #         continue
        #
        #     attached_tool_card = opponent_field_unit.get_tool_card()
        #     if attached_tool_card is not None:
        #         attached_tool_card.set_width_ratio(self.width_ratio)
        #         attached_tool_card.set_height_ratio(self.height_ratio)
        #         attached_tool_card.draw()
        #
        #     fixed_card_base = opponent_field_unit.get_fixed_card_base()
        #     fixed_card_base.set_width_ratio(self.width_ratio)
        #     fixed_card_base.set_height_ratio(self.height_ratio)
        #     fixed_card_base.draw()
        #
        #     attached_shape_list = fixed_card_base.get_attached_shapes()
        #
        #     for attached_shape in attached_shape_list:
        #         attached_shape.set_width_ratio(self.width_ratio)
        #         attached_shape.set_height_ratio(self.height_ratio)
        #         attached_shape.draw()
        #
        # for field_unit in self.your_field_unit_repository.get_current_field_unit_list():
        #     if field_unit is None:
        #         continue
        #
        #     attached_tool_card = field_unit.get_tool_card()
        #     if attached_tool_card is not None:
        #         attached_tool_card.set_width_ratio(self.width_ratio)
        #         attached_tool_card.set_height_ratio(self.height_ratio)
        #         attached_tool_card.draw()
        #
        #     fixed_card_base = field_unit.get_fixed_card_base()
        #     fixed_card_base.set_width_ratio(self.width_ratio)
        #     fixed_card_base.set_height_ratio(self.height_ratio)
        #     fixed_card_base.draw()
        #
        #     attached_shape_list = fixed_card_base.get_attached_shapes()
        #
        #     for attached_shape in attached_shape_list:
        #         attached_shape.set_width_ratio(self.width_ratio)
        #         attached_shape.set_height_ratio(self.height_ratio)
        #         attached_shape.draw()

        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

        self.battle_result.set_width_ratio(self.width_ratio)
        self.battle_result.set_height_ratio(self.height_ratio)
        self.battle_result_panel_list[1].draw()

        # for battle_result_panel in self.battle_result_panel_list:
        #     battle_result_panel.draw()

        glDisable(GL_BLEND)

        # for get_current_page_hand_card in self.hand_card_list:
        #     pickable_card_base = get_current_page_hand_card.get_pickable_card_base()
        #     pickable_card_base.set_width_ratio(self.width_ratio)
        #     pickable_card_base.set_height_ratio(self.height_ratio)
        #     pickable_card_base.draw()
        #
        #     attached_shape_list = pickable_card_base.get_attached_shapes()
        #
        #     for attached_shape in attached_shape_list:
        #         attached_shape.set_width_ratio(self.width_ratio)
        #         attached_shape.set_height_ratio(self.height_ratio)
        #         attached_shape.draw()
        #
        # self.your_hand_prev_button.draw()
        # self.your_hand_next_button.draw()
        #
        # self.post_draw()

        self.battle_result.set_width_ratio(self.width_ratio)
        self.battle_result.set_height_ratio(self.height_ratio)
        self.battle_result_panel_list[0].draw()

        # self.post_draw()

        # glEnable(GL_DEPTH_TEST)

        self.tkSwapBuffers()