import random

from colorama import Fore, Style
from screeninfo import get_monitors
from shapely import Polygon, Point

from battle_field.components.field_area_inside.field_area_action import FieldAreaAction

from OpenGL.GL import *
from OpenGL.GLU import *
from pyopengltk import OpenGLFrame

from battle_field.components.field_area_inside.field_area_inside_handler import FieldAreaInsideHandler
from battle_field.components.fixed_unit_card_inside.fixed_unit_card_inside_action import FixedUnitCardInsideAction
from battle_field.components.mouse_left_click.left_click_detector import LeftClickDetector
from battle_field.components.opponent_fixed_unit_card_inside.opponent_field_area_action import OpponentFieldAreaAction
from battle_field.components.opponent_fixed_unit_card_inside.opponent_fixed_unit_card_inside_handler import \
    OpponentFixedUnitCardInsideHandler
from battle_field.entity.battle_field_scene import BattleFieldScene
from battle_field.entity.battle_result import BattleResult
from battle_field.entity.current_field_energy_race import CurrentFieldEnergyRace
from battle_field.entity.current_to_use_field_energy_count import CurrentToUseFieldEnergyCount
from battle_field.entity.decrease_to_use_field_energy_count import DecreaseToUseFieldEnergyCount
from battle_field.entity.increase_to_use_field_energy_count import IncreaseToUseFieldEnergyCount
from battle_field.entity.next_field_energy_race import NextFieldEnergyRace
from battle_field.entity.opponent_field_energy import OpponentFieldEnergy
from battle_field.entity.opponent_field_panel import OpponentFieldPanel
from battle_field.entity.opponent_hp import OpponentHp
from battle_field.entity.opponent_main_character import OpponentMainCharacter
from battle_field.entity.option import Option
from battle_field.entity.prev_field_energy_race import PrevFieldEnergyRace
from battle_field.entity.surrender_confirm import SurrenderConfirm
from battle_field.entity.turn_end import TurnEnd
from battle_field.entity.your_active_panel import YourActivePanel
from battle_field.entity.your_deck import YourDeck
from battle_field.entity.your_field_energy import YourFieldEnergy
from battle_field.entity.your_field_panel import YourFieldPanel
from battle_field.entity.opponent_lost_zone import OpponentLostZone
from battle_field.entity.opponent_tomb import OpponentTomb
from battle_field.entity.tomb_type import TombType
from battle_field.entity.your_hand import YourHand
from battle_field.entity.your_hp import YourHp
from battle_field.entity.your_lost_zone import YourLostZone
from battle_field.entity.your_tomb import YourTomb
from battle_field.handler.support_card_handler import SupportCardHandler
from battle_field.infra.battle_field_repository import BattleFieldRepository

from battle_field.infra.opponent_field_energy_repository import OpponentFieldEnergyRepository
from battle_field.infra.opponent_field_unit_repository import OpponentFieldUnitRepository
from battle_field.infra.opponent_hand_repository import OpponentHandRepository
from battle_field.infra.opponent_hp_repository import OpponentHpRepository
from battle_field.infra.opponent_lost_zone_repository import OpponentLostZoneRepository

from battle_field.infra.opponent_tomb_repository import OpponentTombRepository
from battle_field.infra.request.request_attach_field_energy_to_unit import RequestAttachFieldEnergyToUnit
from battle_field.infra.request.request_use_energy_burn_to_unit import RequestUseEnergyBurnToUnit
from battle_field.infra.request.request_use_energy_card_to_unit import RequestUseEnergyCardToUnit

from battle_field.infra.round_repository import RoundRepository
from battle_field.infra.your_deck_repository import YourDeckRepository

from battle_field.infra.your_field_energy_repository import YourFieldEnergyRepository
from battle_field.infra.your_field_unit_action_repository import YourFieldUnitActionRepository
from battle_field.infra.your_field_unit_repository import YourFieldUnitRepository

from battle_field.infra.your_hand_repository import YourHandRepository

from battle_field.infra.your_hp_repository import YourHpRepository
from battle_field.infra.your_lost_zone_repository import YourLostZoneRepository

from battle_field.infra.your_tomb_repository import YourTombRepository

from battle_field.state.FieldUnitActionStatus import FieldUnitActionStatus
from battle_field.state.energy_type import EnergyType
from battle_field_fixed_card.fixed_field_card import FixedFieldCard
from battle_field_function.controller.battle_field_function_controller_impl import BattleFieldFunctionControllerImpl
from battle_field_function.service.request.turn_end_request import TurnEndRequest
from battle_field_muligun.service.request.muligun_request import MuligunRequest

from card_info_from_csv.repository.card_info_from_csv_repository_impl import CardInfoFromCsvRepositoryImpl
from common.card_grade import CardGrade
from common.card_race import CardRace
from common.card_type import CardType
from fake_battle_field.entity.animation_test_image import AnimationTestImage
from fake_battle_field.entity.muligun_reset_button import MuligunResetButton
from fake_battle_field.entity.multi_draw_button import MultiDrawButton
from fake_battle_field.infra.fake_battle_field_frame_repository_impl import FakeBattleFieldFrameRepositoryImpl
from fake_battle_field.infra.fake_opponent_hand_repository import FakeOpponentHandRepositoryImpl
from fake_battle_field.service.request.fake_multi_draw_request import FakeMultiDrawRequest
from fake_battle_field.service.request.fake_opponent_deploy_unit_request import FakeOpponentDeployUnitRequest
from image_shape.circle_image import CircleImage
from image_shape.circle_kinds import CircleKinds
from image_shape.circle_number_image import CircleNumberImage
from image_shape.non_background_number_image import NonBackgroundNumberImage

from notify_reader.repository.notify_reader_repository_impl import NotifyReaderRepositoryImpl
from opengl_battle_field_pickable_card.pickable_card import PickableCard

from opengl_rectangle_lightning_border.lightning_border import LightningBorder
from opengl_shape.circle import Circle
from opengl_shape.rectangle import Rectangle
from pre_drawed_image_manager.pre_drawed_image import PreDrawedImage
from session.repository.session_repository_impl import SessionRepositoryImpl


class FakeBattleFieldFrame(OpenGLFrame):
    battle_field_function_controller = BattleFieldFunctionControllerImpl.getInstance()

    __fake_battle_field_frame_repository = FakeBattleFieldFrameRepositoryImpl.getInstance()
    __fake_opponent_hand_repository = FakeOpponentHandRepositoryImpl.getInstance()
    __session_repository = SessionRepositoryImpl.getInstance()
    __notify_reader_repository = NotifyReaderRepositoryImpl.getInstance()

    def __init__(self, master=None, switchFrameWithMenuName=None, **kwargs):
        super().__init__(master, **kwargs)

        self.init_monitor_specification()

        self.battle_field_background_shape_list = None

        self.your_field_panel = None
        self.opponent_field_panel = None

        self.active_panel_rectangle = None
        self.active_panel_attack_button = None
        self.active_panel_first_skill_button = None
        self.active_panel_second_skill_button = None
        self.active_panel_third_skill_button = None
        self.selected_object = None
        self.prev_selected_object = None
        self.drag_start = None

        self.lightning_border = LightningBorder()

        self.your_hand_repository = YourHandRepository.getInstance()
        self.hand_card_list = None
        self.your_hand = YourHand()
        self.your_hand_next_button = None
        self.your_hand_prev_button = None

        self.your_deck_repository = YourDeckRepository.getInstance()
        self.your_deck_list = None
        self.your_deck = YourDeck()
        self.your_deck_search_panel = None
        self.your_deck_next_button = None
        self.your_deck_prev_button = None
        self.your_deck_ok_button = None

        self.opponent_hand_repository = OpponentHandRepository.getInstance()
        self.opponent_hand_card_list = None

        self.selected_search_unit_id_list = []
        self.selected_search_unit_index_list = []
        self.selected_search_unit_page_number_list = []
        self.selected_search_unit_lightning_border = []

        self.your_field_unit_repository = YourFieldUnitRepository.getInstance()

        self.card_info_repository = CardInfoFromCsvRepositoryImpl.getInstance()

        self.pre_drawed_image_instance = PreDrawedImage.getInstance()

        self.your_field_unit_lightning_border_list = []
        self.boost_selection = False

        self.support_card_handler = SupportCardHandler.getInstance()
        self.current_process_card_id = 0

        self.your_tomb_repository = YourTombRepository.getInstance()
        self.your_tomb_panel = None
        self.your_tomb = YourTomb()
        self.tomb_panel_popup_rectangle = None
        self.tomb_panel_selected = False

        self.opponent_tomb_repository = OpponentTombRepository.getInstance()
        self.opponent_tomb_panel = None
        self.opponent_tomb = OpponentTomb()
        self.opponent_tomb_popup_rectangle_panel = None
        self.opponent_tomb_panel_selected = False

        self.selected_tomb = TombType.Dummy

        self.opponent_field_unit_repository = OpponentFieldUnitRepository.getInstance()
        # self.opponent_fixed_unit_card_inside_handler = OpponentFixedUnitCardInsideHandler.getInstance()
        self.field_area_inside_handler = FieldAreaInsideHandler.getInstance()
        # TODO: Your 카드에 집어넣는 경우도 이것으로 감지하는 것이 더 좋을 것임
        self.your_fixed_unit_card_inside_handler = None
        self.opponent_fixed_unit_card_inside_handler = OpponentFixedUnitCardInsideHandler.getInstance()
        # self.your_tomb_repository = YourTombRepository.getInstance()

        self.left_click_detector = LeftClickDetector.getInstance()

        self.selected_object_for_check_required_energy = []
        self.selected_object_index_for_check_required_energy = []
        self.required_energy_select_lightning_border_list = []

        self.targeting_enemy_select_support_lightning_border_list = []
        self.targeting_ememy_select_using_hand_card_id = -1
        self.targeting_ememy_select_using_hand_card_index = -1
        self.targeting_enemy_select_using_your_field_card_index = -1
        self.targeting_enemy_select_using_your_field_card_id = -1
        self.targeting_enemy_select_count = 0

        self.opponent_you_selected_lightning_border_list = []
        self.opponent_you_selected_object_list = []

        self.your_hp_panel = None
        self.your_hp = YourHp()
        self.your_hp_repository = YourHpRepository.getInstance()

        self.opponent_hp_panel = None
        self.opponent_hp = OpponentHp()
        self.opponent_hp_repository = OpponentHpRepository.getInstance()

        self.your_field_energy_panel = None
        self.your_field_energy = YourFieldEnergy()
        self.your_field_energy_repository = YourFieldEnergyRepository.getInstance()
        self.your_field_energy_panel_selected = False

        self.next_field_energy_race_panel = None
        self.next_field_energy_race = NextFieldEnergyRace()
        self.next_field_energy_race_panel_selected = False

        self.prev_field_energy_race_panel = None
        self.prev_field_energy_race = PrevFieldEnergyRace()
        self.prev_field_energy_race_panel_selected = False

        self.current_field_energy_race_panel = None
        self.current_field_energy_race = CurrentFieldEnergyRace()

        self.current_to_use_field_energy_count_panel = None
        self.current_to_use_field_energy_count = CurrentToUseFieldEnergyCount()

        self.increase_to_use_field_energy_count_panel = None
        self.increase_to_use_field_energy_count = IncreaseToUseFieldEnergyCount()
        self.increase_to_use_field_energy_count_panel_selected = False

        self.decrease_to_use_field_energy_count_panel = None
        self.decrease_to_use_field_energy_count = DecreaseToUseFieldEnergyCount()
        self.decrease_to_use_field_energy_count_panel_selected = False

        self.opponent_field_energy = OpponentFieldEnergy()
        self.opponent_field_energy_panel = None
        self.opponent_field_energy_repository = OpponentFieldEnergyRepository.getInstance()
        # self.opponent_field_energy_repository.increase_opponent_field_energy(3)

        self.your_lost_zone_repository = YourLostZoneRepository.getInstance()
        self.your_lost_zone_panel = None
        self.your_lost_zone = YourLostZone()
        self.your_lost_zone_popup_panel = None
        self.your_lost_zone_panel_selected = False

        self.opponent_lost_zone_repository = OpponentLostZoneRepository.getInstance()
        self.opponent_lost_zone_panel = None
        self.opponent_lost_zone = OpponentLostZone()
        self.opponent_lost_zone_popup_panel = None
        self.opponent_lost_zone_panel_selected = False

        self.opponent_main_character_panel = None
        self.opponent_main_character = OpponentMainCharacter()

        self.round_repository = RoundRepository.getInstance()

        self.turn_end = TurnEnd()
        self.turn_end_button = None
        self.turn_end_button_selected = False

        self.your_field_unit_action_repository = YourFieldUnitActionRepository.getInstance()

        self.option = Option()
        self.option_button = None
        self.option_button_selected = False
        self.option_popup_panel_list = []
        self.option_popup_surrender_button_selected = False
        self.option_popup_close_button_selected = False

        self.surrender_confirm = SurrenderConfirm()
        self.surrender_confirm_panel_list = []
        self.surrender_confirm_ok_button_selected = False
        self.surrender_confirm_close_button_selected = False

        self.multi_draw_button = None
        self.multi_draw_button_clicked = False

        self.muligun_reset_button = None
        self.muligun_reset_button_clicked = False
        self.battle_field_muligun_background_shape_list = None

        self.animation_test_image_panel = None
        self.animation_test_image = AnimationTestImage()
        self.animation_test_image_list = []
        self.animation_test_image_panel_list = []

        self.battle_field_repository = BattleFieldRepository.getInstance()
        self.battle_result = BattleResult()
        self.battle_result_panel_list = []

        self.bind("<Configure>", self.on_resize)
        self.bind("<B1-Motion>", self.on_canvas_drag)
        self.bind("<ButtonRelease-1>", self.on_canvas_release)
        self.bind("<Button-1>", self.on_canvas_left_click)
        self.bind("<Button-3>", self.on_canvas_right_click)

        # TODO: 이 부분은 임시 방편입니다 (상대방 행동 했다 가정하고 키보드 입력 받기 위함)
        self.bind("<Key>", self.on_key_press)

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
        glClearColor(1.0, 1.0, 1.0, 0.0)
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

        self.your_tomb.set_total_window_size(self.width, self.height)
        self.your_tomb.create_your_tomb_panel()
        self.your_tomb_panel = self.your_tomb.get_your_tomb_panel()

        self.opponent_tomb.set_total_window_size(self.width, self.height)
        self.opponent_tomb.create_opponent_tomb_panel()
        self.opponent_tomb_panel = self.opponent_tomb.get_opponent_tomb_panel()

        self.opponent_hand_repository.set_total_window_size(self.width, self.height)
        self.opponent_hand_repository.save_current_opponent_hand_state([30, 8, 2, 33, 35])
        self.opponent_hand_repository.create_opponent_hand_card_list()
        self.opponent_hand_card_list = self.opponent_hand_repository.get_current_opponent_hand_card_list()

        # self.your_hand_repository.set_x_base(550)
        self.your_hand_repository.set_total_window_size(self.width, self.height)
        # self.your_hand_repository.save_current_hand_state([30, 30, 8, 93, 8, 2, 33, 35, 9, 20, 25, 36, 151])
        # self.your_hand_repository.save_current_hand_state(
        #     [30, 8, 93, 27, 27, 27, 32, 30, 8, 93, 8, 2, 33, 35, 9, 20, 25, 36, 151])
        # self.your_hand_repository.save_current_hand_state([151])
        # self.your_hand_repository.create_hand_card_list()
        self.your_hand_repository.build_your_hand_page()
        self.your_hand.set_total_window_size(self.width, self.height)
        self.your_hand.init_next_prev_gold_button_hand()
        self.your_hand_prev_button = self.your_hand.get_prev_gold_button_hand()
        self.your_hand_next_button = self.your_hand.get_next_gold_button_hand()

        self.your_deck_repository.set_total_window_size(self.width, self.height)
        # self.your_deck_repository.save_deck_state([93, 35, 35, 93, 25,
        #                                            25, 33, 93, 93, 32,
        #                                            32, 93, 19, 8, 8,
        #                                            8, 9, 9, 2, 26,
        #                                            2, 27, 27, 151, 20,
        #                                            20, 20, 31, 31, 32,
        #                                            36, 36, 26, 26])
        self.your_deck_repository.build_deck_page()
        # self.your_deck_repository.create_deck_card_list()
        self.your_deck.set_total_window_size(self.width, self.height)
        self.your_deck.create_your_deck_popup_rectangle()
        self.your_deck_search_panel = self.your_deck.get_your_deck_popup_rectangle()
        self.your_deck.init_next_prev_gold_button()
        self.your_deck_prev_button = self.your_deck.get_prev_gold_button()
        self.your_deck_next_button = self.your_deck.get_next_gold_button()
        self.your_deck_ok_button = self.your_deck.get_ok_button()

        self.hand_card_list = self.your_hand_repository.get_current_hand_card_list()

        self.your_lost_zone.set_total_window_size(self.width, self.height)
        self.your_lost_zone.create_your_lost_zone_panel()
        self.your_lost_zone_panel = self.your_lost_zone.get_your_lost_zone_panel()

        self.opponent_lost_zone.set_total_window_size(self.width, self.height)
        self.opponent_lost_zone.create_opponent_lost_zone_panel()
        self.opponent_lost_zone_panel = self.opponent_lost_zone.get_opponent_lost_zone_panel()

        self.your_active_panel = YourActivePanel()
        self.your_active_panel.set_total_window_size(self.width, self.height)

        self.your_hp.set_total_window_size(self.width, self.height)
        self.your_hp_repository.set_first_hp_state()
        self.your_hp.draw_current_your_hp_panel()
        self.your_hp_panel = self.your_hp.get_your_hp_panel()

        self.opponent_hp.set_total_window_size(self.width, self.height)
        self.opponent_hp_repository.set_first_hp_state()
        self.opponent_hp.draw_current_opponent_hp_panel()
        self.opponent_hp_panel = self.opponent_hp.get_opponent_hp_panel()

        self.opponent_main_character.set_total_window_size(self.width, self.height)
        self.opponent_main_character.create_opponent_main_character_panel()
        self.opponent_main_character_panel = self.opponent_main_character.get_opponent_main_character_panel()

        self.your_field_energy.set_total_window_size(self.width, self.height)
        self.your_field_energy_repository.reset_field_energy()
        self.your_field_energy.create_your_field_energy_panel()
        self.your_field_energy_panel = self.your_field_energy.get_your_field_energy_panel()

        self.next_field_energy_race.set_total_window_size(self.width, self.height)
        self.next_field_energy_race.create_next_field_energy_race_panel()
        self.next_field_energy_race_panel = self.next_field_energy_race.get_next_field_energy_race_panel()

        self.prev_field_energy_race.set_total_window_size(self.width, self.height)
        self.prev_field_energy_race.create_prev_field_energy_race_panel()
        self.prev_field_energy_race_panel = self.prev_field_energy_race.get_prev_field_energy_race_panel()

        self.current_field_energy_race.set_total_window_size(self.width, self.height)
        self.current_field_energy_race.create_current_field_energy_race_panel()
        self.current_field_energy_race_panel = self.current_field_energy_race.get_current_field_energy_race_panel()

        self.current_to_use_field_energy_count.set_total_window_size(self.width, self.height)
        self.current_to_use_field_energy_count.create_current_to_use_field_energy_count_panel()
        self.current_to_use_field_energy_count_panel = (
            self.current_to_use_field_energy_count.get_current_to_use_field_energy_count_panel())

        self.increase_to_use_field_energy_count.set_total_window_size(self.width, self.height)
        self.increase_to_use_field_energy_count.create_increase_to_use_field_energy_count_panel()
        self.increase_to_use_field_energy_count_panel = (
            self.increase_to_use_field_energy_count.get_increase_to_use_field_energy_count_panel()
        )

        self.decrease_to_use_field_energy_count.set_total_window_size(self.width, self.height)
        self.decrease_to_use_field_energy_count.create_decrease_to_use_field_energy_count_panel()
        self.decrease_to_use_field_energy_count_panel = (
            self.decrease_to_use_field_energy_count.get_decrease_to_use_field_energy_count_panel()
        )

        self.opponent_field_energy.set_total_window_size(self.width, self.height)
        self.opponent_field_energy.create_opponent_field_energy_panel()
        self.opponent_field_energy_panel = self.opponent_field_energy.get_opponent_field_energy_panel()

        self.turn_end.set_total_window_size(self.width, self.height)
        self.turn_end.create_turn_end_button()
        self.turn_end_button = self.turn_end.get_turn_end_button()

        self.option.set_total_window_size(self.width, self.height)
        self.option.create_option_button()
        self.option_button = self.option.get_option_button()
        self.option.create_option_button_popup_list()
        self.option_popup_panel_list = self.option.get_option_button_popup_list()

        self.surrender_confirm.set_total_window_size(self.width, self.height)
        self.surrender_confirm.create_surrender_confirm_panel_list()
        self.surrender_confirm_panel_list = self.surrender_confirm.get_surrender_confirm_panel_list()

        muligun_reset_button_instance = MuligunResetButton()
        muligun_reset_button_instance.set_total_window_size(self.width, self.height)
        muligun_reset_button_instance.init_muligun_reset_button()
        self.muligun_reset_button = muligun_reset_button_instance.get_muligun_reset_button()

        multi_draw_button_instance = MultiDrawButton()
        multi_draw_button_instance.set_total_window_size(self.width, self.height)
        multi_draw_button_instance.init_multi_draw_button()
        self.multi_draw_button = multi_draw_button_instance.get_multi_draw_button()

        if self.battle_field_repository.get_is_game_end():
            print("게임 끝났어 ")
            self.battle_result.set_total_window_size(self.width, self.height)
            self.battle_result.create_battle_result_panel_list()
            self.battle_result_panel_list = self.battle_result.get_battle_result_panel_list()

        self.focus_set()


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

    def on_key_press(self, event):
        key = event.keysym
        print(f"Key pressed: {key}")

        if key.lower() == 'z':
            print("만약 Opponent Hand에 출격시킬 유닛이 있다면 내보낸다.")

            opponent_hand_list = self.__fake_opponent_hand_repository.get_fake_opponent_hand_list()
            for opponent_hand_index, opponent_hand in enumerate(opponent_hand_list):
                opponent_hand_card_type = self.card_info_repository.getCardTypeForCardNumber(opponent_hand)
                if opponent_hand_card_type == CardType.UNIT.value:
                    print("상대방 유닛 출격")

                    result = self.__fake_opponent_hand_repository.request_deploy_fake_opponent_unit(
                        FakeOpponentDeployUnitRequest(
                            self.__session_repository.get_second_fake_session_info(),
                            opponent_hand))

                    print(f"fake opponent deploy unit result: {result}")
                    is_success_value = result.get('is_success', False)

                    if is_success_value == False:
                        return

                    self.__fake_opponent_hand_repository.remove_card_by_index(opponent_hand_index)

                    break

        if key.lower() == 'x':
            print("Opponent Turn을 종료합니다")

            turn_end_request_result = self.round_repository.request_turn_end(
                TurnEndRequest(
                    self.__session_repository.get_second_fake_session_info()))
            print(f"turn_end_request_result: {turn_end_request_result}")

            self.__notify_reader_repository.set_is_your_turn_for_check_fake_process(True)

        # ` (숫자 1 옆에 있는 것)
        if key.lower() == 'grave':
            print(f"{Fore.RED}상대방 20장 뽑기{Style.RESET_ALL}")

            multi_draw_response = self.__fake_battle_field_frame_repository.request_fake_multi_draw(
                FakeMultiDrawRequest(self.__session_repository.get_second_fake_session_info()))

            print(f"{Fore.RED}opponent multi_draw_response:{Fore.GREEN} {multi_draw_response}{Style.RESET_ALL}")
            opponent_multi_draw_hand_list = multi_draw_response['player_multi_drawn_card_list']['You']

            self.__fake_opponent_hand_repository.save_fake_opponent_hand_list(opponent_multi_draw_hand_list)
            print(f"{Fore.RED}current opponent_multi_draw_hand_list:{Fore.GREEN} {self.__fake_opponent_hand_repository.get_fake_opponent_hand_list()}{Style.RESET_ALL}")

        if key.lower() == '1':
            if self.animation_test_image_panel:
                self.animation_test_image_panel = None

            self.animation_test_image.set_total_window_size(self.width, self.height)
            self.animation_test_image.change_local_translation(
                self.opponent_field_unit_repository.find_opponent_field_unit_by_index(0).get_local_translation()
            )
            self.animation_test_image.draw_animation_panel()
            self.animation_test_image_panel = self.animation_test_image.get_animation_panel()
            print("created animation panel")

        if key.lower() == '2':
            if self.animation_test_image_panel:
                self.animation_test_image_panel = None

            self.animation_test_image.set_total_window_size(self.width, self.height)
            self.animation_test_image.change_local_translation(
                self.opponent_field_unit_repository.find_opponent_field_unit_by_index(1).get_local_translation()
            )
            self.animation_test_image.draw_animation_panel()
            self.animation_test_image_panel = self.animation_test_image.get_animation_panel()
            print("created animation panel")

        if key.lower() == '3':
            if self.animation_test_image_panel:
                self.animation_test_image_panel = None

            self.animation_test_image.set_total_window_size(self.width, self.height)
            self.animation_test_image.change_local_translation(
                self.opponent_field_unit_repository.find_opponent_field_unit_by_index(2).get_local_translation()
            )
            self.animation_test_image.draw_animation_panel()
            self.animation_test_image_panel = self.animation_test_image.get_animation_panel()
            print("created animation panel")

        if key.lower() == 'l':

            def animate():
                self.animation_test_image.update_animation_panel()
                if not self.animation_test_image.is_finished:
                    self.master.after(17, animate)
                else:
                    self.animation_test_image_panel = None

            self.animation_test_image.reset_animation_count()
            self.master.after(0, animate)

        if key.lower() == 'kp_1':
            self.animation_test_image_panel = None
            animation_test_image = AnimationTestImage()

            animation_test_image.set_total_window_size(self.width, self.height)
            animation_test_image.change_local_translation(
                self.opponent_field_unit_repository.find_opponent_field_unit_by_index(0).get_local_translation()
            )
            animation_test_image.draw_animation_panel()
            animation_test_image_panel = animation_test_image.get_animation_panel()

            self.animation_test_image_list.append(animation_test_image)
            self.animation_test_image_panel_list.append(animation_test_image_panel)
            print("첨부 완료~: ", self.animation_test_image_panel_list, self.animation_test_image_list)
            print("체크: ", type(self.animation_test_image_panel_list[0]), type(self.animation_test_image_list[0]))

        if key.lower() == 'kp_2':
            self.animation_test_image_panel = None
            animation_test_image = AnimationTestImage()

            animation_test_image.set_total_window_size(self.width, self.height)
            animation_test_image.change_local_translation(
                self.opponent_field_unit_repository.find_opponent_field_unit_by_index(1).get_local_translation()
            )
            animation_test_image.draw_animation_panel()
            animation_test_image_panel = animation_test_image.get_animation_panel()

            self.animation_test_image_list.append(animation_test_image)
            self.animation_test_image_panel_list.append(animation_test_image_panel)

        if key.lower() == '4':
            opponent_hand_list = self.__fake_opponent_hand_repository.get_fake_opponent_hand_list()
            print(f"opponent hand list : {opponent_hand_list}")
            for opponent_hand_index, opponent_hand in enumerate(opponent_hand_list):
                opponent_hand_card_type = self.card_info_repository.getCardTypeForCardNumber(opponent_hand)
                if opponent_hand_card_type == CardType.ENERGY.value:
                    print("상대방 에너지 부착 ")

                    response = self.your_hand_repository.request_use_energy_card_to_unit(
                        RequestUseEnergyCardToUnit(
                            _sessionInfo=self.__session_repository.get_second_fake_session_info(),
                            _unitIndex=0,
                            _energyCardId=93)
                    )
                    print(f"use energy card response: {response}")
                    is_success_value = response.get('is_success', False)

                    if is_success_value == False:
                        return

                    self.__fake_opponent_hand_repository.remove_card_by_index(opponent_hand_index)

                    break

        if key.lower() == '5':
            opponent_hand_list = self.__fake_opponent_hand_repository.get_fake_opponent_hand_list()
            print(f"opponent hand list : {opponent_hand_list}")
            for opponent_hand_index, opponent_hand in enumerate(opponent_hand_list):
                if opponent_hand == 9:
                    print("상대방 에너지번 사용~ ")

                    response = self.your_hand_repository.request_use_energy_burn_to_unit(
                        RequestUseEnergyBurnToUnit(
                            _sessionInfo=self.__session_repository.get_second_fake_session_info(),
                            _itemCardId = 9,
                            _opponentTargetUnitIndex = 0
                        )

                    )
                    print(f"use energy card response: {response}")
                    is_success_value = response.get('is_success', False)

                    if is_success_value == False:
                        return

                    self.__fake_opponent_hand_repository.remove_card_by_index(opponent_hand_index)

                    break



        if key.lower() == 'kp_enter':
            def animate():
                finish_list = []
                is_all_finished = False
                for _animation_test_image in self.animation_test_image_list:
                    _animation_test_image.update_animation_panel()
                    finish_list.append(_animation_test_image.is_finished)

                for finish in finish_list:
                    if finish == False:
                        is_all_finished = False
                        break
                    else:
                        is_all_finished = True

                if not is_all_finished:
                    self.master.after(17, animate)
                else:
                    self.animation_test_image_list = []
                    self.animation_test_image_panel_list = []
                    print("finish animation")

                # if not self.animation_test_image_list[0].is_finished:
                #     self.master.after(17, animate)
                # else:
                #     self.animation_test_image_panel_list = []
                #     self.animation_test_image_list = []
                #     print("finish animation")

            for animation_test_image in self.animation_test_image_list:
                print(f"animation count: {animation_test_image}")
                animation_test_image.reset_animation_count()

            self.master.after(0, animate)

        if key.lower() == 'a':
            self.opponent_field_unit_repository.create_field_unit_card(26)
            self.opponent_field_unit_repository.replace_opponent_field_unit_card_position()

        if key.lower() == 'q':
            self.opponent_field_unit_repository.create_field_unit_card(31)
            self.opponent_field_unit_repository.replace_opponent_field_unit_card_position()

        if key.lower() == 'n':
            self.opponent_field_unit_repository.create_field_unit_card(19)
            self.opponent_field_unit_repository.replace_opponent_field_unit_card_position()

        if key.lower() == 'b':
            self.your_field_unit_repository.create_field_unit_card(19)
            self.your_field_unit_repository.replace_field_card_position()

            first_passive_skill_type = self.card_info_repository.getCardPassiveFirstForCardNumber(19)
            if first_passive_skill_type == 1:
                print("단일기")
            elif first_passive_skill_type == 2:
                print("광역기")

                damage = self.card_info_repository.getCardPassiveFirstDamageForCardNumber(19)
                print(f"wide area damage: {damage}")

                for index in range(
                        len(self.opponent_field_unit_repository.get_current_field_unit_card_object_list()) - 1,
                        -1,
                        -1):
                    opponent_field_unit = \
                        self.opponent_field_unit_repository.get_current_field_unit_card_object_list()[index]

                    if opponent_field_unit is None:
                        continue

                    remove_from_field = False

                    fixed_card_base = opponent_field_unit.get_fixed_card_base()
                    attached_shape_list = fixed_card_base.get_attached_shapes()

                    for attached_shape in attached_shape_list:
                        if isinstance(attached_shape, NonBackgroundNumberImage):
                            if attached_shape.get_circle_kinds() is CircleKinds.HP:

                                hp_number = attached_shape.get_number()
                                hp_number -= damage

                                if hp_number <= 0:
                                    remove_from_field = True
                                    break

                                print(f"contract_of_doom -> hp_number: {hp_number}")
                                attached_shape.set_number(hp_number)

                                # attached_shape.set_image_data(
                                #     self.pre_drawed_image_instance.get_pre_draw_number_image(hp_number))

                                attached_shape.set_image_data(
                                    self.pre_drawed_image_instance.get_pre_draw_unit_hp(hp_number))

                    if remove_from_field:
                        card_id = opponent_field_unit.get_card_number()

                        self.opponent_field_unit_repository.remove_current_field_unit_card(index)
                        self.opponent_tomb_repository.create_opponent_tomb_card(card_id)

                self.opponent_field_unit_repository.replace_opponent_field_unit_card_position()

            second_passive_skill_type = self.card_info_repository.getCardPassiveSecondForCardNumber(19)
            if second_passive_skill_type == 1:
                print("단일기")

                # TODO: 여기서 본체 공격 할 수 있어야 함
                self.targeting_enemy_select_support_lightning_border_list.append(self.opponent_main_character_panel)

                opponent_field_unit_object_list = self.opponent_field_unit_repository.get_current_field_unit_card_object_list()
                valid_opponent_field_units_object_list = [unit for unit in opponent_field_unit_object_list if
                                                          unit is not None]
                print(f"실제 유효한 상대 필드 유닛 숫자: {len(valid_opponent_field_units_object_list)}")

                # if len(valid_opponent_field_units_object_list) == 0:
                #     return

                for opponent_field_unit_object in opponent_field_unit_object_list:
                    if opponent_field_unit_object is None:
                        continue

                    fixed_opponent_card_base = opponent_field_unit_object.get_fixed_card_base()
                    self.targeting_enemy_select_support_lightning_border_list.append(fixed_opponent_card_base)

                self.targeting_enemy_select_support_lightning_border_list.append(self.opponent_main_character_panel)

                self.opponent_fixed_unit_card_inside_handler.set_opponent_field_area_action(
                    OpponentFieldAreaAction.PASSIVE_SKILL_TARGETING_ENEMY)

                your_field_unit_id = 19

                self.targeting_enemy_select_using_your_field_card_id = your_field_unit_id
            elif second_passive_skill_type == 2:
                print("광역기")

        if key.lower() == 't':
            self.round_repository.increase_current_round_number()

        if key.lower() == 'e':
            result = {
                "hand_use_card_id": 93, "field_unit_index": 0,
                "attach_energy_race_type": 2,
                "attach_race_energy_count": 1,
                "attach_total_energy_count": 1
            }
            self.attach_energy(result)
            #return
            # print("attach undead energy")
            #
            # # TODO: Change it to ENUM Value (Not just integer)
            # card_race = self.card_info_repository.getCardRaceForCardNumber(93)
            # print(f"card_race: {card_race}")
            #
            # attach_energy_count = 1
            # opponent_unit_index = 0
            #
            # # self.opponent_field_unit_repository.attach_race_energy(opponent_unit_index, EnergyType.Undead, attach_energy_count)
            # # opponent_field_unit = self.opponent_field_unit_repository.find_opponent_field_unit_by_index(0)
            # #
            # # opponent_field_unit_attached_undead_energy_count = self.opponent_field_unit_repository.get_opponent_field_unit_race_energy(0, EnergyType.Undead)
            # # print(f"opponent_field_unit_attached_undead_energy_count: {opponent_field_unit_attached_undead_energy_count}")
            #
            # before_attach_energy_count = self.opponent_field_unit_repository.get_opponent_field_unit_race_energy(
            #     0, EnergyType.Undead)
            #
            # self.opponent_field_unit_repository.attach_race_energy(
            #     opponent_unit_index,
            #     EnergyType.Undead,
            #     attach_energy_count)
            # opponent_field_unit = self.opponent_field_unit_repository.find_opponent_field_unit_by_index(0)
            #
            # # after_attach_energy_count = self.opponent_field_unit_repository.get_opponent_field_unit_race_energy(
            # #     0, EnergyType.Undead)
            # total_attached_energy_count = self.opponent_field_unit_repository.get_total_energy_at_index(0)
            # print(
            #     f"opponent_field_unit_attached_undead_energy_count: {total_attached_energy_count}")
            #
            # opponent_fixed_card_base = opponent_field_unit.get_fixed_card_base()
            # opponent_fixed_card_attached_shape_list = opponent_fixed_card_base.get_attached_shapes()
            #
            # for opponent_fixed_card_attached_shape in opponent_fixed_card_attached_shape_list:
            #     if isinstance(opponent_fixed_card_attached_shape, NonBackgroundNumberImage):
            #         if opponent_fixed_card_attached_shape.get_circle_kinds() is CircleKinds.ENERGY:
            #             # opponent_fixed_card_attached_shape.set_image_data(
            #             #     self.pre_drawed_image_instance.get_pre_draw_number_image(
            #             #         total_attached_energy_count))
            #
            #             opponent_fixed_card_attached_shape.set_image_data(
            #                 self.pre_drawed_image_instance.get_pre_draw_unit_energy(
            #                     total_attached_energy_count))
            #
            #             print(f"changed energy: {opponent_fixed_card_attached_shape.get_circle_kinds()}")
            #
            # # after_attach_energy_count
            # # before_attach_energy_count
            #
            # every_energy = self.opponent_field_unit_repository.get_energy_info_at_index(0)
            # print(f"every_energy: {every_energy}")
            #
            # if card_race == CardRace.UNDEAD.value:
            #     card_race_circle = opponent_field_unit.creat_fixed_card_energy_race_circle(
            #         color=(0, 0, 0, 1),
            #         vertices=(0, (total_attached_energy_count * 10) + 20),
            #         local_translation=opponent_fixed_card_base.get_local_translation())
            #     opponent_fixed_card_base.set_attached_shapes(card_race_circle)

        if key.lower() == 'h':
            self.your_field_energy_repository.to_next_field_energy_race()

        if key.lower() == 'u':
            self.your_field_energy_repository.increase_your_field_energy()

        if key.lower() == 'i':
            self.opponent_field_energy_repository.increase_opponent_field_energy()

        if key.lower() == 'y':
            self.opponent_field_energy_repository.decrease_opponent_field_energy()

        if key.lower() == 'd':
            self.your_hp_repository.take_damage()

        if key.lower() == 'o':
            self.opponent_hp_repository.take_damage()

        if key.lower() == 'p':
            self.your_field_unit_repository.create_field_unit_card(17)

        if key.lower() == 'w':
            notify_raw_data = '''{
                       "NOTIFY_UNIT_SPAWN":
                           {"player_spawn_unit_map":
                               {"Opponent" : "26"}
                           }
                   }'''
            NotifyReaderRepositoryImpl.getInstance().getNoWaitIpcChannel().put(notify_raw_data)
            # self.opponent_field_unit_repository.create_field_unit_card(26)

        if key.lower() == 's':
            print("attach undead energy")
            notify_raw_data = '''{
                       "NOTIFY_FIELD_UNIT_ENERGY":
                           {"player_field_unit_energy_map":
                                {"Opponent":
                                     {"0":
                                          {"attached_energy_map":
                                               {"2": 2}, "total_energy_count": 2}}}}}'''
            notify_dict = {"player_field_unit_energy_map":
                               {"Opponent":
                                    {"0":
                                         {"attached_energy_map": {"2": 2}, "total_energy_count": 2}}}}

            NotifyReaderRepositoryImpl.getInstance().getNoWaitIpcChannel().put(notify_raw_data)

    def on_resize(self, event):
        self.reshape(event.width, event.height)

    def draw_base(self):
        for battle_field_background_shape in self.battle_field_background_shape_list:
            battle_field_background_shape.set_width_ratio(self.width_ratio)
            battle_field_background_shape.set_height_ratio(self.height_ratio)
            battle_field_background_shape.draw()

        # TODO: 메인 로직에선 제거해야함 (현재는 개발 편의상 배치)
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

        self.your_field_panel.set_width_ratio(self.width_ratio)
        self.your_field_panel.set_height_ratio(self.height_ratio)
        self.your_field_panel.draw()

        self.opponent_field_panel.set_width_ratio(self.width_ratio)
        self.opponent_field_panel.set_height_ratio(self.height_ratio)
        self.opponent_field_panel.draw()

        # 현재 Tomb 와 Lost Zone은 전부 비율 기반이다.
        # 그러므로 사각형의 width_ratio를 계산할 필요는 없다 (마우스 포인터가 내부에 있나 계산하는 부분 제외)
        self.your_tomb.set_width_ratio(self.width_ratio)
        self.your_tomb.set_height_ratio(self.height_ratio)
        self.your_tomb_panel.set_width_ratio(self.width_ratio)
        self.your_tomb_panel.set_height_ratio(self.height_ratio)
        self.your_tomb_panel.set_draw_border(False)
        self.your_tomb_panel.draw()

        self.opponent_tomb.set_width_ratio(self.width_ratio)
        self.opponent_tomb.set_height_ratio(self.height_ratio)
        self.opponent_tomb_panel.set_width_ratio(self.width_ratio)
        self.opponent_tomb_panel.set_height_ratio(self.height_ratio)
        self.opponent_tomb_panel.set_draw_border(False)
        self.opponent_tomb_panel.draw()

        self.your_lost_zone.set_width_ratio(self.width_ratio)
        self.your_lost_zone.set_height_ratio(self.height_ratio)
        self.your_lost_zone_panel.set_width_ratio(self.width_ratio)
        self.your_lost_zone_panel.set_height_ratio(self.height_ratio)
        self.your_lost_zone_panel.set_draw_border(False)
        self.your_lost_zone_panel.draw()

        self.opponent_lost_zone.set_width_ratio(self.width_ratio)
        self.opponent_lost_zone.set_height_ratio(self.height_ratio)
        self.opponent_lost_zone_panel.set_width_ratio(self.width_ratio)
        self.opponent_lost_zone_panel.set_height_ratio(self.height_ratio)
        self.opponent_lost_zone_panel.set_draw_border(False)
        self.opponent_lost_zone_panel.draw()

        self.opponent_main_character.set_width_ratio(self.width_ratio)
        self.opponent_main_character.set_height_ratio(self.height_ratio)
        self.opponent_main_character_panel.set_width_ratio(self.width_ratio)
        self.opponent_main_character_panel.set_height_ratio(self.height_ratio)
        self.opponent_main_character_panel.set_draw_border(False)
        self.opponent_main_character_panel.draw()

        self.increase_to_use_field_energy_count.set_width_ratio(self.width_ratio)
        self.increase_to_use_field_energy_count.set_height_ratio(self.height_ratio)
        self.increase_to_use_field_energy_count_panel.set_draw_border(False)
        self.increase_to_use_field_energy_count_panel.set_width_ratio(self.width_ratio)
        self.increase_to_use_field_energy_count_panel.set_height_ratio(self.height_ratio)
        self.increase_to_use_field_energy_count_panel.draw()

        self.decrease_to_use_field_energy_count.set_width_ratio(self.width_ratio)
        self.decrease_to_use_field_energy_count.set_height_ratio(self.height_ratio)
        self.decrease_to_use_field_energy_count_panel.set_draw_border(False)
        self.decrease_to_use_field_energy_count_panel.set_width_ratio(self.width_ratio)
        self.decrease_to_use_field_energy_count_panel.set_height_ratio(self.height_ratio)
        self.decrease_to_use_field_energy_count_panel.draw()

        self.next_field_energy_race.set_width_ratio(self.width_ratio)
        self.next_field_energy_race.set_height_ratio(self.width_ratio)
        self.next_field_energy_race_panel.set_draw_border(False)
        self.next_field_energy_race_panel.set_width_ratio(self.width_ratio)
        self.next_field_energy_race_panel.set_height_ratio(self.height_ratio)
        self.next_field_energy_race_panel.draw()

        self.prev_field_energy_race.set_width_ratio(self.width_ratio)
        self.prev_field_energy_race.set_height_ratio(self.height_ratio)
        self.prev_field_energy_race_panel.set_draw_border(False)
        self.prev_field_energy_race_panel.set_width_ratio(self.width_ratio)
        self.prev_field_energy_race_panel.set_height_ratio(self.height_ratio)
        self.prev_field_energy_race_panel.draw()

        self.turn_end.set_width_ratio(self.width_ratio)
        self.turn_end.set_height_ratio(self.height_ratio)
        self.turn_end_button.set_draw_border(False)
        self.turn_end_button.set_width_ratio(self.width_ratio)
        self.turn_end_button.set_height_ratio(self.height_ratio)
        self.turn_end_button.draw()

        self.your_hp.set_width_ratio(self.width_ratio)
        self.your_hp.set_height_ratio(self.height_ratio)
        self.your_hp.update_current_your_hp_panel()
        self.your_hp_panel.set_width_ratio(self.width_ratio)
        self.your_hp_panel.set_height_ratio(self.height_ratio)
        self.your_hp_panel.draw()

        self.opponent_hp.set_width_ratio(self.width_ratio)
        self.opponent_hp.set_height_ratio(self.height_ratio)
        self.opponent_hp.update_current_opponent_hp_panel()
        self.opponent_hp_panel.set_width_ratio(self.width_ratio)
        self.opponent_hp_panel.set_height_ratio(self.height_ratio)
        self.opponent_hp_panel.draw()

        self.option.set_width_ratio(self.width_ratio)
        self.option.set_height_ratio(self.height_ratio)
        self.option_button.set_draw_border(False)
        self.option_button.draw()
        if self.option_button_selected:
            for option_popup_panel in self.option_popup_panel_list:
                option_popup_panel.draw()

        self.surrender_confirm.set_width_ratio(self.width_ratio)
        self.surrender_confirm.set_height_ratio(self.height_ratio)
        if self.option_popup_surrender_button_selected:
            for surrender_confirm_panel in self.surrender_confirm_panel_list:
                surrender_confirm_panel.draw()

        glDisable(GL_BLEND)

    def post_draw(self):
        # glEnable(GL_BLEND)
        # glBlendFunc(GL_ONE_MINUS_SRC_ALPHA, GL_SRC_ALPHA)

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

        self.muligun_reset_button.set_width_ratio(self.width_ratio)
        self.muligun_reset_button.set_height_ratio(self.height_ratio)
        self.muligun_reset_button.draw()

        self.multi_draw_button.set_width_ratio(self.width_ratio)
        self.multi_draw_button.set_height_ratio(self.height_ratio)
        self.multi_draw_button.draw()

        if self.animation_test_image_panel is not None:
            self.animation_test_image.set_width_ratio(self.width_ratio)
            self.animation_test_image.set_height_ratio(self.height_ratio)
            self.animation_test_image_panel.draw()

        if self.animation_test_image_list is not [] and self.animation_test_image_panel_list is not []:
            for animation_test_image, animation_test_image_panel in zip(self.animation_test_image_list,
                                                                        self.animation_test_image_panel_list):
                if animation_test_image.is_finished:
                    continue
                animation_test_image.set_width_ratio(self.width_ratio)
                animation_test_image.set_height_ratio(self.height_ratio)
                animation_test_image_panel.draw()

        # glDisable(GL_BLEND)

    def redraw(self):
        if self.is_reshape_not_complete:
            return

        self.tkMakeCurrent()
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        glDisable(GL_DEPTH_TEST)

        self.draw_base()

        for opponent_field_unit in self.opponent_field_unit_repository.get_current_field_unit_card_object_list():
            if opponent_field_unit is None:
                continue

            attached_tool_card = opponent_field_unit.get_tool_card()
            if attached_tool_card is not None:
                attached_tool_card.set_width_ratio(self.width_ratio)
                attached_tool_card.set_height_ratio(self.height_ratio)
                attached_tool_card.draw()

            fixed_card_base = opponent_field_unit.get_fixed_card_base()
            fixed_card_base.set_width_ratio(self.width_ratio)
            fixed_card_base.set_height_ratio(self.height_ratio)
            fixed_card_base.draw()

            attached_shape_list = fixed_card_base.get_attached_shapes()

            for attached_shape in attached_shape_list:
                attached_shape.set_width_ratio(self.width_ratio)
                attached_shape.set_height_ratio(self.height_ratio)
                attached_shape.draw()

        for field_unit in self.your_field_unit_repository.get_current_field_unit_list():
            if field_unit is None:
                continue

            attached_tool_card = field_unit.get_tool_card()
            if attached_tool_card is not None:
                attached_tool_card.set_width_ratio(self.width_ratio)
                attached_tool_card.set_height_ratio(self.height_ratio)
                attached_tool_card.draw()

            fixed_card_base = field_unit.get_fixed_card_base()
            fixed_card_base.set_width_ratio(self.width_ratio)
            fixed_card_base.set_height_ratio(self.height_ratio)
            fixed_card_base.draw()

            attached_shape_list = fixed_card_base.get_attached_shapes()

            for attached_shape in attached_shape_list:
                attached_shape.set_width_ratio(self.width_ratio)
                attached_shape.set_height_ratio(self.height_ratio)
                attached_shape.draw()

        if self.battle_field_repository.get_is_game_end():
        # if len(self.battle_result_panel_list) != 0:
            glEnable(GL_BLEND)
            glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

            self.battle_result.set_width_ratio(self.width_ratio)
            self.battle_result.set_height_ratio(self.height_ratio)
            self.battle_result_panel_list[1].draw()

            # for battle_result_panel in self.battle_result_panel_list:
            #     battle_result_panel.draw()

            glDisable(GL_BLEND)

        # for hand_card in self.hand_card_list:
        #     attached_tool_card = hand_card.get_tool_card()
        #     if attached_tool_card is not None:
        #         attached_tool_card.set_width_ratio(self.width_ratio)
        #         attached_tool_card.set_height_ratio(self.height_ratio)
        #         attached_tool_card.draw()
        #
        #     pickable_card_base = hand_card.get_pickable_card_base()
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

        for opponent_hand_card in self.opponent_hand_card_list:
            opponent_hand_card_base = opponent_hand_card.get_fixed_card_base()
            opponent_hand_card_base.draw()

            attached_shape_list = opponent_hand_card_base.get_attached_shapes()

            for attached_shape in attached_shape_list:
                attached_shape.set_width_ratio(self.width_ratio)
                attached_shape.set_height_ratio(self.height_ratio)
                attached_shape.draw()

        current_page_your_hand_list = self.your_hand_repository.get_current_page_your_hand_list()
        if current_page_your_hand_list is not None:
            for get_current_page_hand_card in current_page_your_hand_list:

                pickable_card_base = get_current_page_hand_card.get_pickable_card_base()
                pickable_card_base.set_width_ratio(self.width_ratio)
                pickable_card_base.set_height_ratio(self.height_ratio)
                pickable_card_base.draw()

                attached_shape_list = pickable_card_base.get_attached_shapes()

                for attached_shape in attached_shape_list:
                    attached_shape.set_width_ratio(self.width_ratio)
                    attached_shape.set_height_ratio(self.height_ratio)
                    attached_shape.draw()

                # for selected_search_unit in self.selected_search_unit_lightning_border:
                #     if selected_search_unit == fixed_card_base:
                #         selected_search_unit.set_width_ratio(self.width_ratio)
                #         selected_search_unit.set_height_ratio(self.height_ratio)
                #
                #         self.lightning_border.set_padding(20)
                #         self.lightning_border.update_shape(selected_search_unit)
                #         self.lightning_border.draw_lightning_border()

        self.your_hand_prev_button.draw()
        self.your_hand_next_button.draw()

        self.post_draw()

        if self.selected_object:
            card_base = None

            if isinstance(self.selected_object, FixedFieldCard):
                card_base = self.selected_object.get_fixed_card_base()
            elif isinstance(self.selected_object, PickableCard):
                card_base = self.selected_object.get_pickable_card_base()

            self.lightning_border.set_width_ratio(self.width_ratio)
            self.lightning_border.set_height_ratio(self.height_ratio)

            self.lightning_border.set_padding(50)
            self.lightning_border.update_shape(card_base)
            self.lightning_border.draw_lightning_border()

        if self.active_panel_rectangle:
            # self.active_panel_rectangle.set_width_ratio(self.width_ratio)
            # self.active_panel_rectangle.set_height_ratio(self.height_ratio)
            glEnable(GL_BLEND)
            glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

            self.active_panel_rectangle.draw()

            glDisable(GL_BLEND)

            self.active_panel_attack_button.draw()

            if self.active_panel_first_skill_button is not None:
                self.active_panel_first_skill_button.draw()

            if self.active_panel_second_skill_button is not None:
                self.active_panel_second_skill_button.draw()

            self.active_panel_third_skill_button = None

            if self.active_panel_details_button is not None:
                self.active_panel_details_button.draw()

        for your_lightning_border in self.field_area_inside_handler.get_lightning_border_list():
            self.lightning_border.set_padding(20)
            self.lightning_border.update_shape(your_lightning_border)
            self.lightning_border.draw_lightning_border()

        for your_field_unit_lightning_border in self.your_field_unit_lightning_border_list:
            your_field_unit_lightning_border.set_width_ratio(self.width_ratio)
            your_field_unit_lightning_border.set_height_ratio(self.height_ratio)

            self.lightning_border.set_padding(20)
            self.lightning_border.update_shape(your_field_unit_lightning_border)
            self.lightning_border.draw_lightning_border()

        for your_hand_lightning_border in self.opponent_fixed_unit_card_inside_handler.get_lightning_border_list():
            self.lightning_border.set_padding(20)
            self.lightning_border.update_shape(your_hand_lightning_border)
            self.lightning_border.draw_lightning_border()

        for required_energy_selection_border in self.required_energy_select_lightning_border_list:
            required_energy_selection_border.set_width_ratio(self.width_ratio)
            required_energy_selection_border.set_height_ratio(self.height_ratio)

            self.lightning_border.set_padding(20)
            self.lightning_border.update_shape(required_energy_selection_border)
            self.lightning_border.draw_lightning_border()

        for targeting_enemy_select_support_lightning_border in self.targeting_enemy_select_support_lightning_border_list:
            targeting_enemy_select_support_lightning_border.set_width_ratio(self.width_ratio)
            targeting_enemy_select_support_lightning_border.set_height_ratio(self.height_ratio)

            self.lightning_border.set_padding(20)
            self.lightning_border.update_shape(targeting_enemy_select_support_lightning_border)
            self.lightning_border.draw_lightning_border()

        for opponent_you_selected in self.opponent_you_selected_lightning_border_list:
            opponent_you_selected.set_width_ratio(self.width_ratio)
            opponent_you_selected.set_height_ratio(self.height_ratio)

            self.lightning_border.set_padding(20)
            self.lightning_border.update_shape(opponent_you_selected)
            self.lightning_border.draw_lightning_border()

        if self.field_area_inside_handler.get_field_area_action() is FieldAreaAction.SEARCH_UNIT_CARD:
            # print(f"검색하기 위한 덱 화면 띄우기")

            glEnable(GL_BLEND)
            glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

            self.your_deck_search_panel.set_width_ratio(self.width_ratio)
            self.your_deck_search_panel.set_height_ratio(self.height_ratio)
            self.your_deck_search_panel.draw()

            for get_current_page_deck_card in self.your_deck_repository.get_current_page_deck_list():
                fixed_card_base = get_current_page_deck_card.get_fixed_card_base()
                fixed_card_base.set_width_ratio(self.width_ratio)
                fixed_card_base.set_height_ratio(self.height_ratio)
                fixed_card_base.draw()

                attached_shape_list = fixed_card_base.get_attached_shapes()

                for attached_shape in attached_shape_list:
                    attached_shape.set_width_ratio(self.width_ratio)
                    attached_shape.set_height_ratio(self.height_ratio)
                    attached_shape.draw()

                for selected_search_unit in self.selected_search_unit_lightning_border:
                    if selected_search_unit == fixed_card_base:
                        selected_search_unit.set_width_ratio(self.width_ratio)
                        selected_search_unit.set_height_ratio(self.height_ratio)

                        self.lightning_border.set_padding(20)
                        self.lightning_border.update_shape(selected_search_unit)
                        self.lightning_border.draw_lightning_border()

            self.your_deck_prev_button.draw()
            self.your_deck_ok_button.draw()
            self.your_deck_next_button.draw()

            glDisable(GL_BLEND)

        if self.tomb_panel_selected:
            # if self.selected_tomb is TombType.Your:
            glEnable(GL_BLEND)
            glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

            self.tomb_panel_popup_rectangle.set_width_ratio(self.width_ratio)
            self.tomb_panel_popup_rectangle.set_height_ratio(self.height_ratio)
            self.tomb_panel_popup_rectangle.draw()

            for tomb_unit in self.your_tomb_repository.get_current_tomb_unit_list():
                # print(f"tomb_unit: {tomb_unit}")
                attached_tool_card = tomb_unit.get_tool_card()
                if attached_tool_card is not None:
                    attached_tool_card.set_width_ratio(self.width_ratio)
                    attached_tool_card.set_height_ratio(self.height_ratio)
                    attached_tool_card.draw()

                fixed_card_base = tomb_unit.get_fixed_card_base()
                fixed_card_base.set_width_ratio(self.width_ratio)
                fixed_card_base.set_height_ratio(self.height_ratio)
                fixed_card_base.draw()

                attached_shape_list = fixed_card_base.get_attached_shapes()

                for attached_shape in attached_shape_list:
                    attached_shape.set_width_ratio(self.width_ratio)
                    attached_shape.set_height_ratio(self.height_ratio)
                    attached_shape.draw()

            # left_x_point = self.width * 0.89
            # right_x_point = self.width * 0.973
            # top_y_point = self.height * 0.807
            # bottom_y_point = self.height * 0.968
            #
            # temp_rect = Rectangle(
            #     color=(1.0, 1.0, 1.0, 1.0),
            #     vertices=[
            #         (left_x_point, top_y_point),
            #         (right_x_point, top_y_point),
            #         (right_x_point, bottom_y_point),
            #         (left_x_point, bottom_y_point)
            #     ],
            #     global_translation=(0, 0),
            #     local_translation=(0, 0)
            # )
            #
            # temp_rect.draw()

            glDisable(GL_BLEND)

        if self.opponent_tomb_panel_selected:
            # elif self.selected_tomb is TombType.Opponent:
            glEnable(GL_BLEND)
            glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

            self.opponent_tomb_popup_rectangle_panel.set_width_ratio(self.width_ratio)
            self.opponent_tomb_popup_rectangle_panel.set_height_ratio(self.height_ratio)
            self.opponent_tomb_popup_rectangle_panel.draw()

            for opponent_tomb_unit in self.opponent_tomb_repository.get_opponent_tomb_unit_list():
                # print(f"tomb_unit: {opponent_tomb_unit}")
                attached_tool_card = opponent_tomb_unit.get_tool_card()
                if attached_tool_card is not None:
                    attached_tool_card.set_width_ratio(self.width_ratio)
                    attached_tool_card.set_height_ratio(self.height_ratio)
                    attached_tool_card.draw()

                fixed_card_base = opponent_tomb_unit.get_fixed_card_base()
                fixed_card_base.set_width_ratio(self.width_ratio)
                fixed_card_base.set_height_ratio(self.height_ratio)
                fixed_card_base.draw()

                attached_shape_list = fixed_card_base.get_attached_shapes()

                for attached_shape in attached_shape_list:
                    attached_shape.set_width_ratio(self.width_ratio)
                    attached_shape.set_height_ratio(self.height_ratio)
                    attached_shape.draw()

            glDisable(GL_BLEND)

        if self.your_lost_zone_panel_selected:
            glEnable(GL_BLEND)
            glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

            self.your_lost_zone_popup_panel.set_width_ratio(self.width_ratio)
            self.your_lost_zone_popup_panel.set_height_ratio(self.height_ratio)
            self.your_lost_zone_popup_panel.draw()

            for your_lost_zone_unit in self.your_lost_zone_repository.get_your_lost_zone_card_list():
                attached_tool_card = your_lost_zone_unit.get_tool_card()
                if attached_tool_card is not None:
                    attached_tool_card.set_width_ratio(self.width_ratio)
                    attached_tool_card.set_height_ratio(self.height_ratio)
                    attached_tool_card.draw()

                fixed_card_base = your_lost_zone_unit.get_fixed_card_base()
                fixed_card_base.set_width_ratio(self.width_ratio)
                fixed_card_base.set_height_ratio(self.height_ratio)
                fixed_card_base.draw()

                attached_shape_list = fixed_card_base.get_attached_shapes()

                for attached_shape in attached_shape_list:
                    attached_shape.set_width_ratio(self.width_ratio)
                    attached_shape.set_height_ratio(self.height_ratio)
                    attached_shape.draw()

            glDisable(GL_BLEND)

        if self.opponent_lost_zone_panel_selected:
            glEnable(GL_BLEND)
            glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

            self.opponent_lost_zone_popup_panel.set_width_ratio(self.width_ratio)
            self.opponent_lost_zone_popup_panel.set_height_ratio(self.height_ratio)
            self.opponent_lost_zone_popup_panel.draw()

            for opponent_lost_zone_unit in self.opponent_lost_zone_repository.get_opponent_lost_zone_card_list():
                attached_tool_card = opponent_lost_zone_unit.get_tool_card()
                if attached_tool_card is not None:
                    attached_tool_card.set_width_ratio(self.width_ratio)
                    attached_tool_card.set_height_ratio(self.height_ratio)
                    attached_tool_card.draw()

                fixed_card_base = opponent_lost_zone_unit.get_fixed_card_base()
                fixed_card_base.set_width_ratio(self.width_ratio)
                fixed_card_base.set_height_ratio(self.height_ratio)
                fixed_card_base.draw()

                attached_shape_list = fixed_card_base.get_attached_shapes()

                for attached_shape in attached_shape_list:
                    attached_shape.set_width_ratio(self.width_ratio)
                    attached_shape.set_height_ratio(self.height_ratio)
                    attached_shape.draw()

            glDisable(GL_BLEND)

        # self.post_draw()
        if self.battle_field_repository.get_is_game_end():
        # if len(self.battle_result_panel_list) != 0:
            self.battle_result.set_width_ratio(self.width_ratio)
            self.battle_result.set_height_ratio(self.height_ratio)
            self.battle_result_panel_list[0].draw()

        glEnable(GL_DEPTH_TEST)

        self.tkSwapBuffers()

    def on_canvas_drag(self, event):
        x, y = event.x, event.y
        y = self.winfo_reqheight() - y
        # print(f"on_canvas_drag -> x: {x}, y: {y}")

        if self.selected_object and self.drag_start:
            if not isinstance(self.selected_object, PickableCard):
                return

            pickable_card = self.selected_object.get_pickable_card_base()

            dx = x - self.drag_start[0]
            dy = y - self.drag_start[1]
            dx /= self.width_ratio
            dy /= self.height_ratio
            dy *= -1

            new_vertices = [
                (vx + dx, vy + dy) for vx, vy in pickable_card.vertices
            ]
            pickable_card.update_vertices(new_vertices)

            tool_card = self.selected_object.get_tool_card()
            if tool_card is not None:
                new_tool_card_vertices = [
                    (vx + dx, vy + dy) for vx, vy in tool_card.vertices
                ]
                tool_card.update_vertices(new_tool_card_vertices)
                # print(f"Rectangle -> update_vertices dx: {dx}, dy: {dy}")

            for attached_shape in pickable_card.get_attached_shapes():
                if isinstance(attached_shape, CircleImage):
                    # print(f"CircleImage -> before update_center() attached_shape.center: {attached_shape.center}, dx: {dx}, dy: {dy}")
                    new_attached_shape_center = (attached_shape.vertices[0][0] + dx, attached_shape.vertices[0][1] + dy)
                    # print("CircleImage -> update_center()")
                    attached_shape.update_circle_vertices(new_attached_shape_center)
                    continue

                if isinstance(attached_shape, CircleNumberImage):
                    new_attached_shape_center = (attached_shape.vertices[0][0] + dx, attached_shape.vertices[0][1] + dy)
                    # print("CircleNumberImage -> update_center()")
                    attached_shape.update_circle_vertices(new_attached_shape_center)
                    continue

                if isinstance(attached_shape, Circle):
                    new_attached_shape_center = (attached_shape.vertices[0][0] + dx, attached_shape.vertices[0][1] + dy)
                    # print("Circle -> update_center()")
                    attached_shape.update_center(new_attached_shape_center)
                    continue

                new_attached_shape_vertices = [
                    (vx + dx, vy + dy) for vx, vy in attached_shape.vertices
                ]
                attached_shape.update_vertices(new_attached_shape_vertices)

            self.drag_start = (x, y)

    # TODO: 임시 방편
    def is_point_inside_opponent_field_area(self, point, opponent_battle_field_area):
        x, y = point
        y *= -1

        opponent_battle_field_area_vertices = opponent_battle_field_area.get_vertices()

        ratio_applied_valid_your_field = [(x * self.width_ratio, y * self.height_ratio) for x, y in
                                          opponent_battle_field_area_vertices]
        print(f"ratio_applied_valid_your_field: {ratio_applied_valid_your_field}")
        print(f"x: {x * self.width_ratio}, y: {y * self.height_ratio}")

        poly = Polygon(ratio_applied_valid_your_field)
        point = Point(x, y)

        return point.within(poly)

    def on_canvas_release(self, event):
        x, y = event.x, event.y
        y = self.winfo_reqheight() - y

        if isinstance(self.selected_object, PickableCard):
            # Opponent Field Area 시작
            # is_pickable_card_inside_opponent_field =

            if self.is_point_inside_opponent_field_area((x, y), self.opponent_field_panel):

                your_card_id = self.selected_object.get_card_number()
                card_type = self.card_info_repository.getCardTypeForCardNumber(your_card_id)
                print(f"opponent field area -> card_type: {card_type}")

                if card_type in [CardType.ITEM.value]:
                    if your_card_id == 25:

                        # TODO: 추후 변경이 필요함
                        # if opponent_field_area_vertices.is_point_inside((x, y)):
                        if self.is_point_inside_opponent_field_area((x, y), self.opponent_field_panel):
                            print("파멸의 계약 사용")
                            self.__required_energy = 0

                            damage = 15

                            # TODO: 즉발이므로 대기 액션이 필요없음 (서버와의 통신을 위해 대기가 발생 할 수 있긴함) 그 때 가서 추가
                            for index in range(
                                    len(self.opponent_field_unit_repository.get_current_field_unit_card_object_list()) - 1,
                                    -1,
                                    -1):
                                opponent_field_unit = \
                                    self.opponent_field_unit_repository.get_current_field_unit_card_object_list()[index]

                                if opponent_field_unit is None:
                                    continue

                                remove_from_field = False

                                fixed_card_base = opponent_field_unit.get_fixed_card_base()
                                attached_shape_list = fixed_card_base.get_attached_shapes()

                                # TODO: 가만 보면 이 부분이 은근히 많이 사용되고 있음 (중복 많이 발생함)
                                for attached_shape in attached_shape_list:
                                    if isinstance(attached_shape, NonBackgroundNumberImage):
                                        if attached_shape.get_circle_kinds() is CircleKinds.HP:

                                            hp_number = attached_shape.get_number()
                                            hp_number -= damage

                                            # TODO: n 턴간 불사 특성을 검사해야하므로 사실 이것도 summary 방식으로 빼는 것이 맞으나 우선은 진행한다.
                                            # (지금 당장 불사가 존재하지 않음)
                                            if hp_number <= 0:
                                                remove_from_field = True
                                                break

                                            print(f"contract_of_doom -> hp_number: {hp_number}")
                                            attached_shape.set_number(hp_number)

                                            # attached_shape.set_image_data(
                                            #     # TODO: 실제로 여기서 서버로부터 계산 받은 값을 적용해야함
                                            #     self.pre_drawed_image_instance.get_pre_draw_number_image(hp_number))

                                            attached_shape.set_image_data(
                                                self.pre_drawed_image_instance.get_pre_draw_unit_hp(hp_number))

                                if remove_from_field:
                                    card_id = opponent_field_unit.get_card_number()

                                    self.opponent_field_unit_repository.remove_current_field_unit_card(index)
                                    self.opponent_tomb_repository.create_opponent_tomb_card(card_id)

                            # your_card_index = self.your_hand_repository.find_index_by_selected_object(self.selected_object)
                            # self.your_hand_repository.remove_card_by_index(your_card_index)
                            your_card_index = self.your_hand_repository.find_index_by_selected_object_with_page(
                                self.selected_object)
                            self.your_hand_repository.remove_card_by_index_with_page(your_card_index)

                            self.your_tomb_repository.create_tomb_card(your_card_id)

                            # self.your_hand_repository.replace_hand_card_position()
                            self.your_hand_repository.update_your_hand()
                            self.opponent_field_unit_repository.replace_opponent_field_unit_card_position()

                            # 실제 날리는 데이터의 경우 서버로부터 응답 받은 정보를 로스트 존으로 배치
                            self.opponent_lost_zone_repository.create_opponent_lost_zone_card(32)

                            self.selected_object = None
                            return

                    # if your_card_id == 9:
                    #     target_unit_data = self.opponent_fixed_unit_card_inside_handler.handle_pickable_card_inside_unit(
                    #         self.selected_object, x, y)
                    #
                    #     target_unit = target_unit_data[0]
                    #     target_unit_index = target_unit_data[1]
                    #
                    #     if target_unit:
                    #         print("에너지 번 사용")
                    #
                    #         card_id = target_unit.get_card_number()
                    #
                    #
                    #         damage_to_unit = False
                    #
                    #         fixed_card_base = target_unit.get_fixed_card_base()
                    #         attached_shape_list = fixed_card_base.get_attached_shapes()
                    #
                    #         # TODO: 가만 보면 이 부분이 은근히 많이 사용되고 있음 (중복 많이 발생함)
                    #         for attached_shape in attached_shape_list:
                    #             if isinstance(attached_shape, NonBackgroundNumberImage):
                    #                 if attached_shape.get_circle_kinds() is CircleKinds.ENERGY:
                    #
                    #                     energy_number = attached_shape.get_number()
                    #
                    #                     if energy_number <= 0:
                    #                         damage_to_unit = True
                    #                         break
                    #
                    #                     energy_number -= 1
                    #
                    #                     print(f"energy burn -> energy_number: {energy_number}")
                    #                     attached_shape.set_number(energy_number)
                    #
                    #                     attached_shape.set_image_data(
                    #                         self.pre_drawed_image_instance.get_pre_draw_unit_energy(energy_number))
                    #
                    #         if damage_to_unit:
                    #             damage = 10
                    #
                    #             fixed_card_base = target_unit.get_fixed_card_base()
                    #             attached_shape_list = fixed_card_base.get_attached_shapes()
                    #
                    #             remove_from_field = False
                    #
                    #             # TODO: 가만 보면 이 부분이 은근히 많이 사용되고 있음 (중복 많이 발생함)
                    #             for attached_shape in attached_shape_list:
                    #                 if isinstance(attached_shape, NonBackgroundNumberImage):
                    #                     if attached_shape.get_circle_kinds() is CircleKinds.HP:
                    #
                    #                         hp_number = attached_shape.get_number()
                    #                         hp_number -= damage
                    #
                    #                         # TODO: n 턴간 불사 특성을 검사해야하므로 사실 이것도 summary 방식으로 빼는 것이 맞으나 우선은 진행한다.
                    #                         # (지금 당장 불사가 존재하지 않음)
                    #                         if hp_number <= 0:
                    #                             remove_from_field = True
                    #                             break
                    #
                    #                         print(f"contract_of_doom -> hp_number: {hp_number}")
                    #                         attached_shape.set_number(hp_number)
                    #
                    #                         # attached_shape.set_image_data(
                    #                         #     # TODO: 실제로 여기서 서버로부터 계산 받은 값을 적용해야함
                    #                         #     self.pre_drawed_image_instance.get_pre_draw_number_image(hp_number))
                    #
                    #                         attached_shape.set_image_data(
                    #                             self.pre_drawed_image_instance.get_pre_draw_unit_hp(hp_number))
                    #
                    #             if remove_from_field:
                    #                 card_id = target_unit.get_card_number()
                    #
                    #                 self.opponent_field_unit_repository.remove_current_field_unit_card(target_unit_index)
                    #                 self.opponent_tomb_repository.create_opponent_tomb_card(card_id)
                    #
                    #     #     fixed_card_base = opponent_field_unit.get_fixed_card_base()
                    #     #     self.targeting_enemy_select_support_lightning_border_list.append(fixed_card_base)
                    #     #
                    #     # self.fixed_unit_card_inside_action = FixedUnitCardInsideAction.ENERGY_BURN
                    #     # self.targeting_ememy_select_using_hand_card_id = your_card_id
                    #     #
                    #     # your_card_index = self.your_hand_repository.find_index_by_selected_object(self.selected_object)
                    #     # self.targeting_ememy_select_using_hand_card_index = your_card_index
                    #     # self.targeting_enemy_select_count = 1
                    #
                    #     self.selected_object = None
                    #     return

                if card_type in [CardType.SUPPORT.value]:
                    if your_card_id != 36:
                        self.return_to_initial_location()
                        return

                    # if your_card_id == 2:
                    #     self.return_to_initial_location()
                    #     return

                    if self.is_point_inside_opponent_field_area((x, y), self.opponent_field_panel):
                        print("죽음의 대지 사용")

                        opponent_field_energy = self.opponent_field_energy_repository.get_opponent_field_energy()
                        print(f"before land of death -> opponent_field_energy: {opponent_field_energy}")

                        self.opponent_field_energy_repository.decrease_opponent_field_energy(2)

                        print(
                            f"after land of death -> opponent_field_energy: {self.opponent_field_energy_repository.get_opponent_field_energy()}")

                        self.your_tomb_repository.create_tomb_card(your_card_id)

                        # your_card_index = self.your_hand_repository.find_index_by_selected_object(self.selected_object)
                        # self.your_hand_repository.remove_card_by_index(your_card_index)
                        your_card_index = self.your_hand_repository.find_index_by_selected_object_with_page(
                            self.selected_object)
                        self.your_hand_repository.remove_card_by_index_with_page(your_card_index)

                        # self.your_hand_repository.replace_hand_card_position()
                        self.your_hand_repository.update_your_hand()

                        self.selected_object = None
                        return

            # Opponent Field Area 끝

            current_opponent_field_unit_list = self.opponent_field_unit_repository.get_current_field_unit_card_object_list()
            current_opponent_field_unit_list_length = len(current_opponent_field_unit_list)
            print(f"current_opponent_field_unit_list_length: {current_opponent_field_unit_list_length}")

            valid_opponent_field_unit_list = [unit for unit in current_opponent_field_unit_list if unit is not None]
            valid_opponent_field_unit_list_length = len(valid_opponent_field_unit_list)
            print(f"valid_opponent_field_unit_list_length: {valid_opponent_field_unit_list_length}")

            if valid_opponent_field_unit_list_length > 0:
                # if self.selected_object.get_card_number() != 8:
                #     self.return_to_initial_location()

                is_pickable_card_inside_unit = self.opponent_fixed_unit_card_inside_handler.handle_pickable_card_inside_unit(
                    self.selected_object, x, y)

                if is_pickable_card_inside_unit:
                    self.selected_object = None
                    # self.return_to_initial_location()
                    return
                else:
                    self.return_to_initial_location()

            # current_field_unit_list = self.your_field_unit_repository.get_current_field_unit_list()
            # current_field_unit_list_length = len(current_field_unit_list)

            current_field_unit_list = self.your_field_unit_repository.get_current_field_unit_list()
            filtered_field_unit_list = [unit for unit in current_field_unit_list if unit is not None]
            current_field_unit_list_length = len(filtered_field_unit_list)

            # TODO: 이 부분이 YourFixedFieldUnitCardInsideHandler
            # 현재 Your Field Unit에게 에너지 부착 및 도구 부착
            if current_field_unit_list_length > 0:
                for unit_index, current_field_unit in enumerate(current_field_unit_list):
                    if current_field_unit is None:
                        continue

                    fixed_card_base = current_field_unit.get_fixed_card_base()
                    if fixed_card_base.is_point_inside((x, y)):
                        print("fixed field unit detect something comes inside!")

                        placed_card_id = self.selected_object.get_card_number()
                        card_type = self.card_info_repository.getCardTypeForCardNumber(placed_card_id)
                        # placed_index = self.your_hand_repository.find_index_by_selected_object(self.selected_object)
                        # placed_index = self.your_hand_repository.find_index_by_selected_object_with_page(self.selected_object)
                        placed_index = self.your_hand_repository.find_index_by_selected_object_with_page(
                            self.selected_object)

                        if card_type == CardType.TOOL.value:
                            # TODO: 배포덱에서는 도구를 사용하지 않음
                            print("도구를 붙입니다!")
                            self.your_hand_repository.remove_card_by_id(placed_card_id)
                            self.your_hand_repository.replace_hand_card_position()

                            self.selected_object = None
                            return

                        # TODO: Ugly -> Need to Refactor: Item Action Summary
                        elif card_type == CardType.ITEM.value:
                            print("아군에게 아이템 사용")

                            if self.selected_object.get_card_number() == 8:
                                return self.return_to_initial_location()

                            if placed_card_id == 35:
                                print(f"사기 전환(35) -> placed_card_id: {placed_card_id}")
                                card_id = current_field_unit.get_card_number()
                                fixed_field_unit_hp = self.card_info_repository.getCardHpForCardNumber(card_id)
                                acquire_energy = round(fixed_field_unit_hp / 5)
                                print(f"acquire_energy: {acquire_energy}")

                                self.your_field_energy_repository.increase_your_field_energy(acquire_energy)
                                # self.your_hand_repository.remove_card_by_index(placed_index)
                                self.your_hand_repository.remove_card_by_index_with_page(placed_index)
                                self.your_field_unit_repository.remove_card_by_index(unit_index)

                                # self.your_hand_repository.replace_hand_card_position()
                                self.your_hand_repository.update_your_hand()
                                self.your_field_unit_repository.replace_field_card_position()

                                self.your_tomb_repository.create_tomb_card(card_id)
                                self.your_tomb_repository.create_tomb_card(placed_card_id)

                                print(
                                    f"사기 전환 이후 필드 에너지 수량: {self.your_field_energy_repository.get_your_field_energy()}")

                            if placed_card_id == 33:
                                print(f"시체 폭발(33) -> placed_card_id: {placed_card_id}")
                                card_id = current_field_unit.get_card_number()

                                opponent_field_unit_object_list = self.opponent_field_unit_repository.get_current_field_unit_card_object_list()
                                for opponent_field_unit_object in opponent_field_unit_object_list:
                                    if opponent_field_unit_object is None:
                                        continue

                                    fixed_opponent_card_base = opponent_field_unit_object.get_fixed_card_base()
                                    self.targeting_enemy_select_support_lightning_border_list.append(
                                        fixed_opponent_card_base)

                                self.fixed_unit_card_inside_action = FixedUnitCardInsideAction.TARGETING_TWO_ENEMY_AS_POSSIBLE
                                # self.targeting_enemy_select_support_lightning_border_list = []
                                self.targeting_ememy_select_using_hand_card_id = placed_card_id
                                self.targeting_ememy_select_using_hand_card_index = placed_index
                                print(
                                    f"explosion targeting_ememy_select_using_hand_card_index: {self.targeting_ememy_select_using_hand_card_index}")
                                self.targeting_enemy_select_using_your_field_card_index = unit_index
                                print(
                                    f"explosion targeting_enemy_select_using_your_field_card_index: {self.targeting_enemy_select_using_your_field_card_index}")
                                self.targeting_enemy_for_sacrifice_unit_id = card_id
                                print(
                                    f"explosion targeting_enemy_for_sacrifice_unit_id: {self.targeting_enemy_for_sacrifice_unit_id}")
                                self.targeting_enemy_select_count = 2

                                # self.your_hand_repository.replace_hand_card_position()
                                #
                                # self.your_tomb_repository.create_tomb_card(card_id)
                                # self.your_tomb_repository.create_tomb_card(placed_card_id)

                            self.selected_object = None
                            return


                        elif card_type == CardType.ENERGY.value:
                            print("에너지를 붙입니다!")

                            response = self.your_hand_repository.request_use_energy_card_to_unit(
                                RequestUseEnergyCardToUnit(
                                    _sessionInfo=self.__session_repository.get_first_fake_session_info(),
                                    _unitIndex=unit_index,
                                    _energyCardId=self.selected_object.get_card_number())
                            )

                            print(f"response: {response}")
                            is_success_value = response.get('is_success', False)

                            if is_success_value == False:
                                return

                            # self.selected_object = None
                            self.your_hand_repository.remove_card_by_index_with_page(placed_index)
                            # self.your_field_unit_repository.get_attached_energy_info().add_energy_at_index(unit_index, 1)

                            # TODO: 에너지 enum으로 처리해야함
                            race = None
                            card_race = self.card_info_repository.getCardRaceForCardNumber(placed_card_id)
                            print(f"card_race: {card_race}")
                            if card_race == 2:
                                race = EnergyType.Undead

                            self.your_field_unit_repository.attach_race_energy(
                                unit_index,
                                race,
                                1)

                            every_list = self.your_field_unit_repository.get_current_field_unit_list()
                            print(f"every_list: {every_list}")

                            your_fixed_field_unit = self.your_field_unit_repository.find_field_unit_by_index(unit_index)
                            print(f"energy_attach -> your_fixed_field_unit: {your_fixed_field_unit}")
                            fixed_card_base = your_fixed_field_unit.get_fixed_card_base()
                            fixed_card_attached_shape_list = fixed_card_base.get_attached_shapes()
                            placed_card_id = self.selected_object.get_card_number()
                            print(f"placed_card_id : {placed_card_id}")
                            print(f"card grade : {self.card_info_repository.getCardGradeForCardNumber(placed_card_id)}")

                            # attached_energy_count = self.your_field_unit_repository.get_attached_energy_info().get_energy_at_index(unit_index)
                            total_attached_energy_count = self.your_field_unit_repository.get_total_energy_at_index(
                                unit_index)
                            print(f"total_attached_energy_count: {total_attached_energy_count}")
                            # undead_attach_energy_count = self.your_field_unit_repository.get_your_field_unit_race_energy(
                            #     unit_index, race)

                            # card_id = current_field_unit.get_card_number()
                            # self.your_tomb_repository.create_tomb_card(card_id)
                            self.your_tomb_repository.create_tomb_card(placed_card_id)
                            # TODO: attached_energy 값 UI에 표현 (이미지 작업 미완료)

                            # TODO: 특수 에너지 붙인 것을 어떻게 표현 할 것인가 ? (아직 미정)
                            for fixed_card_attached_shape in fixed_card_attached_shape_list:
                                if isinstance(fixed_card_attached_shape, NonBackgroundNumberImage):
                                    if fixed_card_attached_shape.get_circle_kinds() is CircleKinds.ENERGY:
                                        # fixed_card_attached_shape.set_image_data(
                                        #     self.pre_drawed_image_instance.get_pre_draw_number_image(
                                        #         total_attached_energy_count))

                                        fixed_card_attached_shape.set_image_data(
                                            self.pre_drawed_image_instance.get_pre_draw_unit_energy(
                                                total_attached_energy_count))

                                        print(f"changed energy: {fixed_card_attached_shape.get_circle_kinds()}")

                            card_race = self.card_info_repository.getCardRaceForCardNumber(placed_card_id)
                            # if card_race == CardRace.UNDEAD.value:
                            #     card_race_circle = your_fixed_field_unit.creat_fixed_card_energy_race_circle(
                            #         color=(0, 0, 0, 1),
                            #         vertices=(0, (total_attached_energy_count * 10) + 20),
                            #         local_translation=fixed_card_base.get_local_translation())
                            #     fixed_card_base.set_attached_shapes(card_race_circle)

                            self.selected_object = None

                            current_hand_list = self.your_hand_repository.get_current_hand_state()
                            print(f"get_current_hand_state: {current_hand_list}")
                            # self.your_hand_repository.replace_hand_card_position()
                            # self.your_hand_repository.save_current_hand_state(current_hand_list)
                            # self.your_hand_repository.update_your_hand(current_hand_list)
                            self.your_hand_repository.update_your_hand()

                            return
                        else:
                            self.return_to_initial_location()
                            return

            y *= -1

            # 당신(Your) Field에 던진 카드
            self.field_area_inside_handler.set_width_ratio(self.width_ratio)
            self.field_area_inside_handler.set_height_ratio(self.height_ratio)

            drop_action_result = self.field_area_inside_handler.handle_card_drop(x, y, self.selected_object,
                                                                                 self.your_field_panel)
            if drop_action_result is None or drop_action_result is FieldAreaAction.Dummy:
                print("self.field_area_inside_handler.get_field_area_action() = None")
                self.return_to_initial_location()
            elif drop_action_result is FieldAreaAction.ENERGY_BOOST:
                print("self.field_area_inside_handler.get_field_area_action() = EnergyBoost")
                self.selected_object = None
            else:
                print("self.field_area_inside_handler.get_field_area_action() = Some Action")
                self.selected_object = None

        # if self.your_tomb_panel.

    def return_to_initial_location(self):
        pickable_card_base = self.selected_object.get_pickable_card_base()
        # print(f"pickable_card_base: {pickable_card_base.vertices}")

        intiial_vertices = pickable_card_base.get_initial_vertices()
        # print(f"revert position -> initial_position: {intiial_vertices}")

        pickable_card_base.update_vertices(intiial_vertices)

        tool_card = self.selected_object.get_tool_card()
        if tool_card is not None:
            tool_intiial_vertices = tool_card.get_initial_vertices()
            tool_card.update_vertices(tool_intiial_vertices)

        for attached_shape in pickable_card_base.get_attached_shapes():
            if isinstance(attached_shape, CircleImage):
                attached_shape_intiial_center = attached_shape.get_initial_center()
                # print(f"attached_shape_intiial_center: {attached_shape_intiial_center}")
                # print(f"attached_shape_intiial_center[0]: {attached_shape_intiial_center[0]}")
                attached_shape.update_circle_vertices(attached_shape_intiial_center[0])
                continue

            if isinstance(attached_shape, CircleNumberImage):
                attached_shape_intiial_center = attached_shape.get_initial_center()
                attached_shape.update_circle_vertices(attached_shape_intiial_center[0])
                continue

            # if isinstance(attached_shape, Circle):
            #     attached_shape_intiial_center = attached_shape.get_initial_center()
            #     attached_shape.update_circle_vertices(attached_shape_intiial_center[0])
            #     continue

            attached_shape_intiial_vertices = attached_shape.get_initial_vertices()
            attached_shape.update_vertices(attached_shape_intiial_vertices)

        self.drag_start = None

    def is_drop_location_valid_battle_field_panel(self, x, y):
        print(f"is_drop_location_valid_battle_field_panel -> x: {x}, y: {y}")
        valid_area_vertices = self.your_field_panel.get_vertices()
        return self.point_inside_polygon(x, y, valid_area_vertices)

    def is_point_to_left_of_intersection(self, x, y, p1x, p1y, p2x, p2y):
        return p1y != p2y and (x <= (y - p1y) * (p2x - p1x) / (p2y - p1y) + p1x or p1x == p2x)

    def point_inside_polygon(self, x, y, poly):
        n = len(poly)
        inside = False

        for i in range(n):
            p1x, p1y = poly[i]
            p2x, p2y = poly[(i + 1) % n]

            p1x *= self.width_ratio
            p2x *= self.width_ratio

            p1y *= self.height_ratio
            p2y *= self.height_ratio

            # Point의 y 좌표가 현재 도형 테두리(가장자리) y 범위 내에 있는지 확인
            y_range_condition = (y > min(p1y, p2y)) and (y <= max(p1y, p2y))

            # Point의 x 좌표가 교점의 왼쪽에 있는지 확인
            x_condition = x <= max(p1x, p2x)

            if y_range_condition and x_condition and self.is_point_to_left_of_intersection(x, y, p1x, p1y, p2x, p2y):
                inside = not inside

        return inside

    def on_canvas_left_click(self, event):
        try:
            x, y = event.x, event.y
            y = self.winfo_reqheight() - y
            print(f"x: {x}, y: {y}")

            # if len(self.battle_result_panel_list) != 0:
            if self.battle_field_repository.get_is_game_end():
                # print(self.battle_result_panel_list)

                self.battle_field_function_controller.callGameEndReward()
                self.battle_result_panel_list = []
                return

            if self.your_active_panel.get_your_active_panel_attack_button() is not None:
                if self.your_active_panel.is_point_inside_attack_button((x, y)):
                    your_field_unit_index = self.selected_object.get_index()
                    your_selected_unit_action_count = self.your_field_unit_action_repository.get_current_field_unit_action_count(
                        your_field_unit_index)

                    if your_selected_unit_action_count <= 0:
                        print("행동을 마친 유닛은 더 이상 공격 할 수 없습니다")
                        return

                    your_selected_unit_action_status = self.your_field_unit_action_repository.get_current_field_unit_action_status(
                        your_field_unit_index)

                    if your_selected_unit_action_status == FieldUnitActionStatus.WAIT:
                        print(f"처음 필드에 출격한 유닛은 공격 할 수 없습니다")
                        return

                    elif your_selected_unit_action_status == FieldUnitActionStatus.Dummy:
                        print(f"Dummy 상태입니다")
                        return

                    print("일반 공격 클릭")

                    opponent_field_unit_object_list = self.opponent_field_unit_repository.get_current_field_unit_card_object_list()
                    for opponent_field_unit_object in opponent_field_unit_object_list:
                        if opponent_field_unit_object is None:
                            continue

                        fixed_opponent_card_base = opponent_field_unit_object.get_fixed_card_base()
                        self.targeting_enemy_select_support_lightning_border_list.append(fixed_opponent_card_base)

                    self.targeting_enemy_select_support_lightning_border_list.append(self.opponent_main_character_panel)

                    self.opponent_fixed_unit_card_inside_handler.set_opponent_field_area_action(
                        OpponentFieldAreaAction.GENERAL_ATTACK_TO_TARGETING_ENEMY)

                    your_field_unit_id = self.selected_object.get_card_number()
                    your_field_unit_index = self.selected_object.get_index()

                    # self.targeting_ememy_select_using_hand_card_id

                    self.targeting_enemy_select_using_your_field_card_index = your_field_unit_index
                    self.targeting_enemy_select_using_your_field_card_id = your_field_unit_id

                    return

            if self.your_active_panel.get_your_active_panel_first_skill_button() is not None:
                if self.your_active_panel.is_point_inside_first_skill_button((x, y)):
                    your_field_unit_index = self.selected_object.get_index()
                    your_selected_unit_action_count = self.your_field_unit_action_repository.get_current_field_unit_action_count(
                        your_field_unit_index)

                    if your_selected_unit_action_count <= 0:
                        print("행동을 마친 유닛은 더 이상 공격 할 수 없습니다")
                        return

                    your_selected_unit_action_status = self.your_field_unit_action_repository.get_current_field_unit_action_status(
                        your_field_unit_index)

                    if your_selected_unit_action_status == FieldUnitActionStatus.WAIT:
                        print(f"처음 필드에 출격한 유닛은 공격 할 수 없습니다")
                        return

                    elif your_selected_unit_action_status == FieldUnitActionStatus.Dummy:
                        print(f"Dummy 상태입니다")
                        return

                    print("첫 번째 스킬 클릭")

                    your_field_unit_id = self.selected_object.get_card_number()
                    your_field_unit_index = self.selected_object.get_index()
                    your_field_unit_attached_energy = self.your_field_unit_repository.get_attached_energy_info()

                    your_field_unit_total_energy = your_field_unit_attached_energy.get_total_energy_at_index(
                        your_field_unit_index)
                    print(f"your_field_unit_total_energy: {your_field_unit_total_energy}")

                    your_field_unit_attached_energy_info = your_field_unit_attached_energy.get_energy_info_at_index(
                        your_field_unit_index)
                    print(f"your_field_unit_attached_energy_info: {your_field_unit_attached_energy_info}")

                    your_field_unit_attached_undead_energy = your_field_unit_attached_energy.get_race_energy_at_index(
                        your_field_unit_index, EnergyType.Undead)
                    # print(f"your_field_unit_attached_undead_energy: {your_field_unit_attached_undead_energy}")

                    your_field_unit_attached_human_energy = your_field_unit_attached_energy.get_race_energy_at_index(
                        your_field_unit_index, EnergyType.Human)
                    # print(f"your_field_unit_attached_human_energy: {your_field_unit_attached_human_energy}")

                    your_field_unit_attached_trent_energy = your_field_unit_attached_energy.get_race_energy_at_index(
                        your_field_unit_index, EnergyType.Trent)
                    # print(f"your_field_unit_attached_trent_energy: {your_field_unit_attached_trent_energy}")

                    your_field_unit_required_undead_energy = self.card_info_repository.getCardSkillFirstUndeadEnergyRequiredForCardNumber(
                        your_field_unit_id)
                    your_field_unit_required_human_energy = self.card_info_repository.getCardSkillFirstHumanEnergyRequiredForCardNumber(
                        your_field_unit_id)
                    your_field_unit_required_trent_energy = self.card_info_repository.getCardSkillFirstTrentEnergyRequiredForCardNumber(
                        your_field_unit_id)
                    # print(f"your_field_unit_required_undead_energy: {your_field_unit_required_undead_energy}")
                    # print(f"your_field_unit_required_human_energy: {your_field_unit_required_human_energy}")
                    # print(f"your_field_unit_required_trent_energy: {your_field_unit_required_trent_energy}")

                    if your_field_unit_required_undead_energy > your_field_unit_attached_undead_energy:
                        return

                    if your_field_unit_required_human_energy > your_field_unit_attached_human_energy:
                        return

                    if your_field_unit_required_trent_energy > your_field_unit_attached_trent_energy:
                        return

                    skill_type = self.card_info_repository.getCardSkillFirstForCardNumber(your_field_unit_id)
                    print(f"skill_type: {skill_type}")

                    # 단일기
                    if skill_type == 1:
                        opponent_field_unit_object_list = self.opponent_field_unit_repository.get_current_field_unit_card_object_list()
                        for opponent_field_unit_object in opponent_field_unit_object_list:
                            if opponent_field_unit_object is None:
                                continue

                            fixed_opponent_card_base = opponent_field_unit_object.get_fixed_card_base()
                            self.targeting_enemy_select_support_lightning_border_list.append(fixed_opponent_card_base)

                        self.targeting_enemy_select_support_lightning_border_list.append(
                            self.opponent_main_character_panel)

                        self.opponent_fixed_unit_card_inside_handler.set_opponent_field_area_action(
                            OpponentFieldAreaAction.SKILL_TARGETING_ENEMY)

                        your_field_unit_id = self.selected_object.get_card_number()
                        your_field_unit_index = self.selected_object.get_index()

                        self.targeting_enemy_select_using_your_field_card_index = your_field_unit_index
                        self.targeting_enemy_select_using_your_field_card_id = your_field_unit_id

                    # 광역기
                    elif skill_type == 2:
                        pass

                    return

            if self.your_active_panel.get_your_active_panel_second_skill_button() is not None:
                if self.your_active_panel.is_point_inside_second_skill_button((x, y)):
                    your_field_unit_index = self.selected_object.get_index()
                    print(f"광역기 -> your_field_unit_index: {your_field_unit_index}")
                    print(
                        f"every_field_unit_action_count: {self.your_field_unit_action_repository.get_every_field_unit_action_count()}")
                    your_selected_unit_action_count = self.your_field_unit_action_repository.get_current_field_unit_action_count(
                        your_field_unit_index)

                    if your_selected_unit_action_count <= 0:
                        print("행동을 마친 유닛은 더 이상 공격 할 수 없습니다")
                        return

                    your_selected_unit_action_status = self.your_field_unit_action_repository.get_current_field_unit_action_status(
                        your_field_unit_index)

                    if your_selected_unit_action_status == FieldUnitActionStatus.WAIT:
                        print(f"처음 필드에 출격한 유닛은 공격 할 수 없습니다")
                        return

                    elif your_selected_unit_action_status == FieldUnitActionStatus.Dummy:
                        print(f"Dummy 상태입니다")
                        return

                    print("두 번째 스킬 클릭")

                    # your_field_card_index = self.targeting_enemy_select_using_your_field_card_index
                    # print(f"스킬 사용 확정 -> your_field_card_index: {your_field_card_index}")
                    self.your_field_unit_action_repository.use_field_unit_action_count_by_index(your_field_unit_index)

                    your_field_unit_id = self.selected_object.get_card_number()
                    print(f"your_field_unit_id: {your_field_unit_id}")

                    your_field_unit_index = self.selected_object.get_index()
                    your_field_unit_attached_energy = self.your_field_unit_repository.get_attached_energy_info()

                    your_field_unit_total_energy = your_field_unit_attached_energy.get_total_energy_at_index(
                        your_field_unit_index)
                    print(f"your_field_unit_total_energy: {your_field_unit_total_energy}")

                    your_field_unit_attached_energy_info = your_field_unit_attached_energy.get_energy_info_at_index(
                        your_field_unit_index)
                    print(f"your_field_unit_attached_energy_info: {your_field_unit_attached_energy_info}")

                    your_field_unit_attached_undead_energy = your_field_unit_attached_energy.get_race_energy_at_index(
                        your_field_unit_index, EnergyType.Undead)
                    print(f"your_field_unit_attached_undead_energy: {your_field_unit_attached_undead_energy}")
                    your_field_unit_attached_human_energy = your_field_unit_attached_energy.get_race_energy_at_index(
                        your_field_unit_index, EnergyType.Human)
                    print(f"your_field_unit_attached_human_energy: {your_field_unit_attached_human_energy}")
                    your_field_unit_attached_trent_energy = your_field_unit_attached_energy.get_race_energy_at_index(
                        your_field_unit_index, EnergyType.Trent)
                    print(f"your_field_unit_attached_trent_energy: {your_field_unit_attached_trent_energy}")

                    your_field_unit_required_undead_energy = self.card_info_repository.getCardSkillFirstUndeadEnergyRequiredForCardNumber(
                        your_field_unit_id)
                    your_field_unit_required_human_energy = self.card_info_repository.getCardSkillFirstHumanEnergyRequiredForCardNumber(
                        your_field_unit_id)
                    your_field_unit_required_trent_energy = self.card_info_repository.getCardSkillFirstTrentEnergyRequiredForCardNumber(
                        your_field_unit_id)

                    if your_field_unit_required_undead_energy > your_field_unit_attached_undead_energy:
                        return

                    if your_field_unit_required_human_energy > your_field_unit_attached_human_energy:
                        return

                    if your_field_unit_required_trent_energy > your_field_unit_attached_trent_energy:
                        return

                    skill_type = self.card_info_repository.getCardSkillSecondForCardNumber(your_field_unit_id)
                    print(f"skill_type: {skill_type}")

                    # 단일기
                    if skill_type == 1:
                        pass

                    # 광역기
                    elif skill_type == 2:
                        damage = self.card_info_repository.getCardSkillSecondDamageForCardNumber(your_field_unit_id)
                        print(f"wide area damage: {damage}")

                        # TODO: 즉발이므로 대기 액션이 필요없음 (서버와의 통신을 위해 대기가 발생 할 수 있긴함) 그 때 가서 추가
                        for index in range(
                                len(self.opponent_field_unit_repository.get_current_field_unit_card_object_list()) - 1,
                                -1,
                                -1):
                            opponent_field_unit = \
                                self.opponent_field_unit_repository.get_current_field_unit_card_object_list()[index]

                            if opponent_field_unit is None:
                                continue

                            remove_from_field = False

                            fixed_card_base = opponent_field_unit.get_fixed_card_base()
                            attached_shape_list = fixed_card_base.get_attached_shapes()

                            # TODO: 가만 보면 이 부분이 은근히 많이 사용되고 있음 (중복 많이 발생함)
                            for attached_shape in attached_shape_list:
                                if isinstance(attached_shape, NonBackgroundNumberImage):
                                    if attached_shape.get_circle_kinds() is CircleKinds.HP:

                                        hp_number = attached_shape.get_number()
                                        hp_number -= damage

                                        # TODO: n 턴간 불사 특성을 검사해야하므로 사실 이것도 summary 방식으로 빼는 것이 맞으나 우선은 진행한다.
                                        # (지금 당장 불사가 존재하지 않음)
                                        if hp_number <= 0:
                                            remove_from_field = True
                                            break

                                        print(f"contract_of_doom -> hp_number: {hp_number}")
                                        attached_shape.set_number(hp_number)

                                        # attached_shape.set_image_data(
                                        #     # TODO: 실제로 여기서 서버로부터 계산 받은 값을 적용해야함
                                        #     self.pre_drawed_image_instance.get_pre_draw_number_image(hp_number))

                                        attached_shape.set_image_data(
                                            self.pre_drawed_image_instance.get_pre_draw_unit_hp(hp_number))

                            if remove_from_field:
                                card_id = opponent_field_unit.get_card_number()

                                self.opponent_field_unit_repository.remove_current_field_unit_card(index)
                                self.opponent_tomb_repository.create_opponent_tomb_card(card_id)

                        self.opponent_field_unit_repository.replace_opponent_field_unit_card_position()

                        self.selected_object = None
                        return

                    return

            # if self.your_active_panel.get_your_active_panel_third_skill_button() is not None:
            #     if self.your_active_panel.is_point_inside_third_skill_button((x, y)):
            #         print("세 번째 스킬 클릭")
            #         return

            if self.your_active_panel.get_your_active_panel_details_button() is not None:
                if self.your_active_panel.is_point_inside_details_button((x, y)):
                    print("상세 보기 클릭")

                    # your_field_unit_id = self.selected_object.get_card_number()
                    # skill_type = self.card_info_repository.getCardSkillSecondForCardNumber(your_field_unit_id)
                    # print(f"skill_type: {skill_type}")

                    return

            if self.tomb_panel_selected:
                if self.your_tomb.is_point_inside_popup_rectangle((x, y)):
                    return

            if self.opponent_tomb_panel_selected:
                if self.opponent_tomb.is_point_inside_popup_rectangle((x, y)):
                    return

            if self.your_lost_zone_panel_selected:
                if self.your_lost_zone.is_point_inside_popup_rectangle((x, y)):
                    return

            if self.opponent_lost_zone_panel_selected:
                if self.opponent_lost_zone.is_point_inside_popup_rectangle((x, y)):
                    return

            if self.option_button_selected or self.option_popup_surrender_button_selected:
                if self.option_popup_surrender_button_selected:
                    print(f"on click invoke!! : option_popup_surrender_selected")

                    self.surrender_confirm_ok_button_selected = (
                        self.left_click_detector.which_one_select_is_in_ok_surrender_confirm_area(
                            (x, y),
                            self.surrender_confirm,
                            self.winfo_reqheight()
                        ))

                    if self.surrender_confirm_ok_button_selected:
                        print(f"행복해용~~~")
                        self.battle_field_function_controller.callSurrender()
                        #self.call_surrender()

                    self.surrender_confirm_close_button_selected = (
                        self.left_click_detector.which_one_select_is_in_close_surrender_confirm_area(
                            (x, y),
                            self.surrender_confirm,
                            self.winfo_reqheight()
                        ))

                    if self.surrender_confirm_close_button_selected:
                        print("취소해용~~~")
                        self.option_popup_surrender_button_selected = False

                self.option_popup_surrender_button_selected = (
                    self.left_click_detector.which_one_select_is_in_option_surrender_area(
                        (x, y),
                        self.option,
                        self.winfo_reqheight()
                    ))

            self.option_button_selected = self.left_click_detector.which_one_select_is_in_option_area(
                (x, y),
                self.option,
                self.winfo_reqheight()
            )

            print(f"option button selected : {self.option_button_selected}")
            print(f"option_popup_surrender_button_selected : {self.option_popup_surrender_button_selected}")

            self.tomb_panel_selected = False
            self.opponent_tomb_panel_selected = False
            self.your_lost_zone_panel_selected = False
            self.opponent_lost_zone_panel_selected = False
            self.muligun_reset_button_clicked = False
            self.multi_draw_button_clicked = False

            # TODO: Your Hand List in Page
            print(f"Your Hand List in Page")
            # for hand_card in self.hand_card_list:
            current_page_your_hand_list = self.your_hand_repository.get_current_page_your_hand_list()
            if current_page_your_hand_list is not None:
                for get_current_page_hand_card in current_page_your_hand_list:
                    if isinstance(get_current_page_hand_card, PickableCard):
                        get_current_page_hand_card.selected = False

            self.selected_object = None

            # TODO: Your Hand List in Page
            if current_page_your_hand_list is not None:
                for hand_card in reversed(current_page_your_hand_list):
                    print(f"hand_card: {hand_card}")
                    # for hand_card in reversed(self.your_hand_repository.get_current_page_your_hand_list()):
                    pickable_card_base = hand_card.get_pickable_card_base()
                    pickable_card_base.set_width_ratio(self.width_ratio)
                    pickable_card_base.set_height_ratio(self.height_ratio)

                    if pickable_card_base.is_point_inside((x, y)):
                        print("카드 선택!")
                        hand_card.selected = not hand_card.selected
                        self.selected_object = hand_card
                        self.drag_start = (x, y)

                        if self.selected_object != self.prev_selected_object:
                            self.your_active_panel.clear_your_active_panel_details_button()
                            self.your_active_panel.clear_your_active_panel_second_skill_button()
                            self.your_active_panel.clear_your_active_panel_first_skill_button()
                            self.your_active_panel.clear_your_active_panel_attack_button()
                            self.your_active_panel.clear_your_active_panel()
                            self.active_panel_rectangle = None

                            self.prev_selected_object = self.selected_object

                        break

            if self.your_field_energy_panel_selected:
                current_field_unit_list = self.your_field_unit_repository.get_current_field_unit_list()
                print(f"field_energy_panel_selected -> current_field_unit_list: {current_field_unit_list}")

                for unit_index, current_field_unit in enumerate(current_field_unit_list):
                    if current_field_unit is None:
                        continue

                    fixed_card_base = current_field_unit.get_fixed_card_base()
                    if fixed_card_base.is_point_inside((x, y)):
                        print("필드 에너지를 붙입니다!")

                        # TODO: 통신해야함

                        self.selected_object = current_field_unit
                        energy_race = self.your_field_energy_repository.get_current_field_energy_race()
                        print(f"energy_race: {energy_race}")
                        energy_count = self.your_field_energy_repository.get_to_use_field_energy_count()
                        before_energy_count = self.your_field_unit_repository.get_total_energy_at_index(unit_index)

                        response = self.your_field_energy_repository.request_to_attach_energy_to_unit(
                            RequestAttachFieldEnergyToUnit(
                                _sessionInfo=self.__session_repository.get_first_fake_session_info(),
                                _unitIndex=unit_index,
                                _energyRace=energy_race,
                                _energyCount=energy_count
                            )
                        )
                        print(f"after energy attach server communication: {response}")

                        # response = self.__field_energy_application.send_request_to_attach_field_energy_to_unit(
                        #     unitIndex=unit_index, energyRace = energy_race, energyCount=energy_count
                        # )
                        # if not response:
                        #     self.selected_object = None
                        #     self.your_field_energy_panel_selected = False
                        #     return

                        # self.your_field_unit_repository.attach_race_energy(
                        #     unit_index,
                        #     energy_race,
                        #     energy_count)

                        for _ in range(energy_count):
                            self.your_field_unit_repository.attach_race_energy(
                                unit_index,
                                energy_race,
                                1)

                        your_fixed_field_unit = self.your_field_unit_repository.find_field_unit_by_index(unit_index)
                        print(f"unit index = {unit_index} , {your_fixed_field_unit}")
                        fixed_card_base = your_fixed_field_unit.get_fixed_card_base()
                        fixed_card_attached_shape_list = fixed_card_base.get_attached_shapes()
                        placed_card_id = self.selected_object.get_card_number()
                        print(f"placed_card_id : {placed_card_id}")
                        print(f"card grade : {self.card_info_repository.getCardGradeForCardNumber(placed_card_id)}")
                        total_attached_energy_count = self.your_field_unit_repository.get_total_energy_at_index(
                            unit_index)
                        print(f"total_attached_energy_count: {total_attached_energy_count}")

                        for fixed_card_attached_shape in fixed_card_attached_shape_list:
                            if isinstance(fixed_card_attached_shape, NonBackgroundNumberImage):
                                if fixed_card_attached_shape.get_circle_kinds() is CircleKinds.ENERGY:
                                    # fixed_card_attached_shape.set_image_data(
                                    #     self.pre_drawed_image_instance.get_pre_draw_number_image(
                                    #         total_attached_energy_count))

                                    fixed_card_attached_shape.set_image_data(
                                        self.pre_drawed_image_instance.get_pre_draw_unit_energy(
                                            total_attached_energy_count))

                                    print(f"changed energy: {fixed_card_attached_shape.get_circle_kinds()}")

                        card_race = self.card_info_repository.getCardRaceForCardNumber(placed_card_id)
                        # if card_race == CardRace.UNDEAD.value:
                        #     for count in range(before_energy_count + 1, total_attached_energy_count + 1):
                        #         card_race_circle = your_fixed_field_unit.creat_fixed_card_energy_race_circle(
                        #             color=(0, 0, 0, 1),
                        #             vertices=(0, (count * 10) + 20),
                        #             local_translation=fixed_card_base.get_local_translation())
                        #         fixed_card_base.set_attached_shapes(card_race_circle)

                        self.selected_object = None
                        self.your_field_energy_panel_selected = False
                        self.your_field_energy_repository.decrease_your_field_energy(
                            self.your_field_energy_repository.get_to_use_field_energy_count()
                        )
                        self.your_field_energy_repository.reset_to_use_field_energy_count()
                        return
                    else:
                        self.your_field_energy_panel_selected = False

            # if self.opponent_fixed_unit_card_inside_handler.get_opponent_field_area_action() is OpponentFieldAreaAction.REQUIRE_ENERGY_TO_USAGE:
            #     print("카드를 사용하기 위해 에너지가 필요합니다!")
            #
            #     selected_card_id = self.selected_object.get_card_number()
            #
            #     if self.card_info_repository.getCardTypeForCardNumber(selected_card_id) is not CardType.ENERGY.value:
            #         return
            #
            #     required_energy_race = self.opponent_fixed_unit_card_inside_handler.get_required_energy_race()
            #     if self.card_info_repository.getCardRaceForCardNumber(
            #             selected_card_id) is not required_energy_race.value:
            #         return
            #
            #     self.selected_object_for_check_required_energy.append(self.selected_object)
            #     self.selected_object_index_for_check_required_energy.append(
            #         self.your_hand_repository.find_index_by_selected_object(
            #             self.selected_object))
            #
            #     card_base = self.selected_object.get_pickable_card_base()
            #     self.required_energy_select_lightning_border_list.append(card_base)
            #
            #     self.opponent_fixed_unit_card_inside_handler.decrease_required_energy()
            #     required_energy_count = self.opponent_fixed_unit_card_inside_handler.get_required_energy()
            #
            #     if required_energy_count == 0:
            #         print(f"required_energy_count: {required_energy_count}")
            #         usage_card_index = self.opponent_fixed_unit_card_inside_handler.get_action_set_card_index()
            #
            #         selected_energy_index_list = []
            #         selected_energy_index_list.append(self.selected_object_index_for_check_required_energy[0])
            #         selected_energy_index_list.append(self.selected_object_index_for_check_required_energy[1])
            #
            #         selected_energy_id_list = []
            #         selected_energy_id_list.append(self.selected_object_for_check_required_energy[0].get_card_number())
            #         selected_energy_id_list.append(self.selected_object_for_check_required_energy[1].get_card_number())
            #         # print(f"self.selected_object_for_check_required_energy[0]: {self.selected_object_for_check_required_energy[0]}")
            #         # print(f"self.selected_object_for_check_required_energy[1]: {self.selected_object_for_check_required_energy[1]}")
            #
            #         self.your_hand_repository.remove_card_by_multiple_index(
            #             [
            #                 usage_card_index,
            #                 selected_energy_index_list[0],
            #                 selected_energy_index_list[1]
            #             ])
            #
            #         opponent_unit_card_index = self.opponent_fixed_unit_card_inside_handler.get_opponent_unit_index()
            #
            #         self.opponent_field_unit_repository.remove_current_field_unit_card(
            #             opponent_unit_card_index)
            #
            #         # print("isn't it operate ? (Death Sice)")
            #         self.your_tomb_repository.create_tomb_card(selected_energy_id_list[0])
            #         self.your_tomb_repository.create_tomb_card(selected_energy_id_list[1])
            #         self.your_tomb_repository.create_tomb_card(
            #             self.opponent_fixed_unit_card_inside_handler.get_your_hand_card_id())
            #         # TODO: 상대편은 상대 무덤으로 이동해야함
            #         self.opponent_tomb_repository.create_opponent_tomb_card(
            #             self.opponent_fixed_unit_card_inside_handler.get_opponent_unit_id())
            #
            #         self.your_hand_repository.replace_hand_card_position()
            #
            #         self.selected_object_for_check_required_energy = []
            #         self.selected_object_index_for_check_required_energy = []
            #         self.required_energy_select_lightning_border_list = []
            #
            #         self.opponent_fixed_unit_card_inside_handler.clear_opponent_unit_index()
            #         self.opponent_fixed_unit_card_inside_handler.clear_action_set_card_index()
            #         self.opponent_fixed_unit_card_inside_handler.clear_opponent_field_area_action()
            #         self.opponent_fixed_unit_card_inside_handler.clear_required_energy_race()
            #         self.opponent_fixed_unit_card_inside_handler.clear_required_energy()
            #         self.opponent_fixed_unit_card_inside_handler.clear_lightning_border_list()
            #         self.opponent_fixed_unit_card_inside_handler.clear_opponent_unit_id()
            #         self.opponent_fixed_unit_card_inside_handler.clear_your_hand_card_id()
            #
            #         self.opponent_field_unit_repository.replace_opponent_field_unit_card_position()
            #
            #         self.selected_object = None
            #         return

            # TODO: 메인 캐릭터 공격할 때도 이쪽 루틴을 타고 있어 Refactoring이 필요함
            if self.opponent_fixed_unit_card_inside_handler.get_opponent_field_area_action() is OpponentFieldAreaAction.GENERAL_ATTACK_TO_TARGETING_ENEMY:
                print("일반 공격 진행")

                if self.opponent_main_character.is_point_inside((x, y)):
                    print("메인 캐릭터 공격")

                    your_field_card_index = self.targeting_enemy_select_using_your_field_card_index
                    self.your_field_unit_action_repository.use_field_unit_action_count_by_index(your_field_card_index)

                    your_field_card_id = self.targeting_enemy_select_using_your_field_card_id
                    print(f"your_field_card_id: {your_field_card_id}")

                    your_damage = self.card_info_repository.getCardAttackForCardNumber(your_field_card_id)
                    print(f"your_damage: {your_damage}")

                    self.opponent_hp_repository.take_damage(your_damage)

                    self.opponent_fixed_unit_card_inside_handler.clear_opponent_field_area_action()
                    self.targeting_enemy_select_using_your_field_card_index = None
                    self.targeting_enemy_select_using_your_field_card_id = None
                    self.targeting_enemy_select_support_lightning_border_list = []
                    self.opponent_you_selected_lightning_border_list = []

                    self.selected_object = None
                    self.active_panel_rectangle = None

                    return

                # self.targeting_ememy_select_using_hand_card_id = placed_card_id
                # self.targeting_ememy_select_using_hand_card_index = placed_index

                opponent_field_unit_object_list = self.opponent_field_unit_repository.get_current_field_unit_card_object_list()
                for opponent_field_unit_object in opponent_field_unit_object_list:
                    if opponent_field_unit_object:
                        continue

                    if isinstance(opponent_field_unit_object, FixedFieldCard):
                        opponent_field_unit_object.selected = False

                print("지정한 상대 유닛 찾기")
                for opponent_field_unit_object in opponent_field_unit_object_list:
                    if opponent_field_unit_object is None:
                        continue

                    opponent_fixed_card_base = opponent_field_unit_object.get_fixed_card_base()
                    print("지정한 상대 유닛 베이스 찾기")

                    if opponent_fixed_card_base.is_point_inside((x, y)):
                        your_field_card_index = self.targeting_enemy_select_using_your_field_card_index
                        self.your_field_unit_action_repository.use_field_unit_action_count_by_index(
                            your_field_card_index)

                        self.opponent_you_selected_lightning_border_list.append(opponent_fixed_card_base)

                        opponent_fixed_card_attached_shape_list = opponent_fixed_card_base.get_attached_shapes()

                        are_opponent_field_unit_death = False
                        opponent_field_card_index = None
                        opponent_field_card_id = None

                        for opponent_fixed_card_attached_shape in opponent_fixed_card_attached_shape_list:
                            if isinstance(opponent_fixed_card_attached_shape, NonBackgroundNumberImage):
                                if opponent_fixed_card_attached_shape.get_circle_kinds() is CircleKinds.HP:
                                    print("지정한 상대방 유닛 HP Circle 찾기")

                                    # self.targeting_enemy_select_using_your_field_card_index = your_field_unit_index
                                    # self.targeting_enemy_select_using_your_field_card_id

                                    # your_field_card_id = self.targeting_ememy_select_using_hand_card_id
                                    # print(f"your_field_card_id: {your_field_card_id}")
                                    # your_field_card_index = self.targeting_ememy_select_using_hand_card_index
                                    # print(f"your_field_card_index: {your_field_card_index}")

                                    your_field_card_id = self.targeting_enemy_select_using_your_field_card_id
                                    print(f"your_field_card_id: {your_field_card_id}")
                                    your_field_card_index = self.targeting_enemy_select_using_your_field_card_index
                                    print(f"your_field_card_index: {your_field_card_index}")
                                    your_damage = self.card_info_repository.getCardAttackForCardNumber(
                                        your_field_card_id)
                                    print(f"your_damage: {your_damage}")

                                    your_field_unit = self.your_field_unit_repository.find_field_unit_by_index(
                                        your_field_card_index)
                                    your_fixed_card_base = your_field_unit.get_fixed_card_base()
                                    your_fixed_card_attached_shape_list = your_fixed_card_base.get_attached_shapes()

                                    opponent_field_card_id = opponent_field_unit_object.get_card_number()
                                    opponent_field_card_index = opponent_field_unit_object.get_index()
                                    opponent_damage = self.card_info_repository.getCardAttackForCardNumber(
                                        opponent_field_card_id)

                                    print(f"opponent_damage: {opponent_damage}")

                                    are_your_field_unit_death = False
                                    for your_fixed_card_attached_shape in your_fixed_card_attached_shape_list:
                                        if isinstance(your_fixed_card_attached_shape, NonBackgroundNumberImage):
                                            if your_fixed_card_attached_shape.get_circle_kinds() is CircleKinds.HP:
                                                your_hp_number = your_fixed_card_attached_shape.get_number()
                                                your_hp_number -= opponent_damage
                                                print(f"your 유닛 hp number: {your_hp_number}")

                                                if your_hp_number <= 0:
                                                    are_your_field_unit_death = True

                                                    break

                                                print(f"공격 후 your unit 체력 -> hp_number: {your_hp_number}")
                                                your_fixed_card_attached_shape.set_number(your_hp_number)

                                                # your_fixed_card_attached_shape.set_image_data(
                                                #     # TODO: 실제로 여기서 서버로부터 계산 받은 값을 적용해야함
                                                #     self.pre_drawed_image_instance.get_pre_draw_number_image(
                                                #         your_hp_number))

                                                your_fixed_card_attached_shape.set_image_data(
                                                    self.pre_drawed_image_instance.get_pre_draw_unit_hp(
                                                        your_hp_number))

                                    if are_your_field_unit_death is True:
                                        self.your_field_unit_repository.remove_card_by_index(
                                            your_field_card_index)
                                        self.your_tomb_repository.create_tomb_card(
                                            your_field_card_id)

                                        self.your_field_unit_repository.replace_field_card_position()

                                    print("your 유닛 hp 갱신")

                                    opponent_hp_number = opponent_fixed_card_attached_shape.get_number()
                                    opponent_hp_number -= your_damage

                                    print(f"opponent_hp_number: {opponent_hp_number}")

                                    # TODO: n 턴간 불사 특성을 검사해야하므로 사실 이것도 summary 방식으로 빼는 것이 맞으나 우선은 진행한다.
                                    # (지금 당장 불사가 존재하지 않음)
                                    if opponent_hp_number <= 0:
                                        are_opponent_field_unit_death = True

                                        break

                                    print(f"공격 후 opponent unit 체력 -> hp_number: {opponent_hp_number}")
                                    opponent_fixed_card_attached_shape.set_number(opponent_hp_number)

                                    # opponent_fixed_card_attached_shape.set_image_data(
                                    #     # TODO: 실제로 여기서 서버로부터 계산 받은 값을 적용해야함
                                    #     self.pre_drawed_image_instance.get_pre_draw_number_image(opponent_hp_number))

                                    opponent_fixed_card_attached_shape.set_image_data(
                                        self.pre_drawed_image_instance.get_pre_draw_unit_hp(opponent_hp_number))

                        # opponent_field_card_index = None
                        # opponent_field_card_id = None

                        print(f"opponent_field_card_index: {opponent_field_card_index}")

                        if are_opponent_field_unit_death is True:
                            self.opponent_field_unit_repository.remove_card_by_multiple_index(
                                [opponent_field_card_index])
                            self.opponent_tomb_repository.create_opponent_tomb_card(
                                opponent_field_card_id)

                            self.opponent_field_unit_repository.replace_opponent_field_unit_card_position()

                        self.opponent_fixed_unit_card_inside_handler.clear_opponent_field_area_action()
                        self.targeting_enemy_select_using_your_field_card_index = None
                        self.targeting_enemy_select_using_your_field_card_id = None
                        self.targeting_enemy_select_support_lightning_border_list = []
                        self.opponent_you_selected_lightning_border_list = []

                        self.selected_object = None
                        self.active_panel_rectangle = None

                        return

            if self.opponent_fixed_unit_card_inside_handler.get_opponent_field_area_action() is OpponentFieldAreaAction.PASSIVE_SKILL_TARGETING_ENEMY:
                print("단일기 사용")

                if self.opponent_main_character.is_point_inside((x, y)):
                    print("메인 캐릭터 공격")

                    # your_field_card_index = self.targeting_enemy_select_using_your_field_card_index
                    # self.your_field_unit_action_repository.use_field_unit_action_count_by_index(your_field_card_index)

                    your_field_card_id = self.targeting_enemy_select_using_your_field_card_id
                    print(f"your_field_card_id: {your_field_card_id}")

                    your_damage = self.card_info_repository.getCardPassiveSecondDamageForCardNumber(your_field_card_id)
                    print(f"your_damage: {your_damage}")

                    self.opponent_hp_repository.take_damage(your_damage)

                    self.opponent_fixed_unit_card_inside_handler.clear_opponent_field_area_action()
                    self.targeting_enemy_select_using_your_field_card_index = None
                    self.targeting_enemy_select_using_your_field_card_id = None
                    self.targeting_enemy_select_support_lightning_border_list = []
                    self.opponent_you_selected_lightning_border_list = []

                    self.selected_object = None
                    self.active_panel_rectangle = None

                    return

                opponent_field_unit_object_list = self.opponent_field_unit_repository.get_current_field_unit_card_object_list()
                for opponent_field_unit_object in opponent_field_unit_object_list:
                    if opponent_field_unit_object:
                        continue

                    if isinstance(opponent_field_unit_object, FixedFieldCard):
                        opponent_field_unit_object.selected = False

                print("지정한 상대 유닛 찾기")
                for opponent_field_unit_object in opponent_field_unit_object_list:
                    if opponent_field_unit_object is None:
                        continue

                    opponent_fixed_card_base = opponent_field_unit_object.get_fixed_card_base()
                    print("지정한 상대 유닛 베이스 찾기")

                    if opponent_fixed_card_base.is_point_inside((x, y)):
                        # TODO: 패시브도 버그에 대응하기 위해 패시브 카운트도 계산하고 있어야함
                        # your_field_card_index = self.targeting_enemy_select_using_your_field_card_index
                        # self.your_field_unit_action_repository.use_field_unit_action_count_by_index(
                        #     your_field_card_index)
                        # print("문제 포인트 찾기")

                        self.opponent_you_selected_lightning_border_list.append(opponent_fixed_card_base)

                        opponent_fixed_card_attached_shape_list = opponent_fixed_card_base.get_attached_shapes()

                        are_opponent_field_unit_death = False
                        opponent_field_card_index = None
                        opponent_field_card_id = None

                        print("지정한 상대 유닛 모양 찾기")

                        for opponent_fixed_card_attached_shape in opponent_fixed_card_attached_shape_list:
                            if isinstance(opponent_fixed_card_attached_shape, NonBackgroundNumberImage):
                                if opponent_fixed_card_attached_shape.get_circle_kinds() is CircleKinds.HP:
                                    print("지정한 상대방 유닛 HP Circle 찾기")

                                    your_field_card_id = self.targeting_enemy_select_using_your_field_card_id
                                    print(f"your_field_card_id: {your_field_card_id}")

                                    your_second_passive_skill_damage = self.card_info_repository.getCardPassiveSecondDamageForCardNumber(
                                        your_field_card_id)
                                    print(f"your_skill_damage: {your_second_passive_skill_damage}")

                                    opponent_field_card_id = opponent_field_unit_object.get_card_number()
                                    opponent_field_card_index = opponent_field_unit_object.get_index()

                                    opponent_hp_number = opponent_fixed_card_attached_shape.get_number()
                                    opponent_hp_number -= your_second_passive_skill_damage

                                    print(f"opponent_hp_number: {opponent_hp_number}")

                                    # TODO: n 턴간 불사 특성을 검사해야하므로 사실 이것도 summary 방식으로 빼는 것이 맞으나 우선은 진행한다.
                                    # (지금 당장 불사가 존재하지 않음)
                                    if opponent_hp_number <= 0:
                                        are_opponent_field_unit_death = True

                                        break

                                    print(f"공격 후 opponent unit 체력 -> hp_number: {opponent_hp_number}")
                                    opponent_fixed_card_attached_shape.set_number(opponent_hp_number)

                                    # opponent_fixed_card_attached_shape.set_image_data(
                                    #     # TODO: 실제로 여기서 서버로부터 계산 받은 값을 적용해야함
                                    #     self.pre_drawed_image_instance.get_pre_draw_number_image(opponent_hp_number))

                                    opponent_fixed_card_attached_shape.set_image_data(
                                        self.pre_drawed_image_instance.get_pre_draw_unit_hp(opponent_hp_number))

                        print(f"opponent_field_card_index: {opponent_field_card_index}")

                        if are_opponent_field_unit_death is True:
                            self.opponent_field_unit_repository.remove_card_by_multiple_index(
                                [opponent_field_card_index])
                            self.opponent_tomb_repository.create_opponent_tomb_card(
                                opponent_field_card_id)

                            self.opponent_field_unit_repository.replace_opponent_field_unit_card_position()

                        self.opponent_fixed_unit_card_inside_handler.clear_opponent_field_area_action()
                        self.targeting_enemy_select_using_your_field_card_index = None
                        self.targeting_enemy_select_using_your_field_card_id = None
                        self.targeting_enemy_select_support_lightning_border_list = []
                        self.opponent_you_selected_lightning_border_list = []

                        self.selected_object = None
                        self.active_panel_rectangle = None

                        return

            if self.opponent_fixed_unit_card_inside_handler.get_opponent_field_area_action() is OpponentFieldAreaAction.SKILL_TARGETING_ENEMY:
                print("단일기 사용")

                # self.targeting_ememy_select_using_hand_card_id = placed_card_id
                # self.targeting_ememy_select_using_hand_card_index = placed_index

                if self.opponent_main_character.is_point_inside((x, y)):
                    print("메인 캐릭터 공격")

                    your_field_card_index = self.targeting_enemy_select_using_your_field_card_index
                    self.your_field_unit_action_repository.use_field_unit_action_count_by_index(your_field_card_index)

                    your_field_card_id = self.targeting_enemy_select_using_your_field_card_id
                    print(f"your_field_card_id: {your_field_card_id}")

                    your_damage = self.card_info_repository.getCardSkillFirstDamageForCardNumber(your_field_card_id)
                    print(f"your_damage: {your_damage}")

                    self.opponent_hp_repository.take_damage(your_damage)

                    self.opponent_fixed_unit_card_inside_handler.clear_opponent_field_area_action()
                    self.targeting_enemy_select_using_your_field_card_index = None
                    self.targeting_enemy_select_using_your_field_card_id = None
                    self.targeting_enemy_select_support_lightning_border_list = []
                    self.opponent_you_selected_lightning_border_list = []

                    self.selected_object = None
                    self.active_panel_rectangle = None

                    return

                opponent_field_unit_object_list = self.opponent_field_unit_repository.get_current_field_unit_card_object_list()
                for opponent_field_unit_object in opponent_field_unit_object_list:
                    if opponent_field_unit_object:
                        continue

                    if isinstance(opponent_field_unit_object, FixedFieldCard):
                        opponent_field_unit_object.selected = False

                print("지정한 상대 유닛 찾기")
                for opponent_field_unit_object in opponent_field_unit_object_list:
                    if opponent_field_unit_object is None:
                        continue

                    opponent_fixed_card_base = opponent_field_unit_object.get_fixed_card_base()

                    if opponent_fixed_card_base.is_point_inside((x, y)):
                        your_field_card_index = self.targeting_enemy_select_using_your_field_card_index
                        self.your_field_unit_action_repository.use_field_unit_action_count_by_index(
                            your_field_card_index)

                        self.opponent_you_selected_lightning_border_list.append(opponent_fixed_card_base)

                        opponent_fixed_card_attached_shape_list = opponent_fixed_card_base.get_attached_shapes()

                        are_opponent_field_unit_death = False
                        opponent_field_card_index = None
                        opponent_field_card_id = None

                        for opponent_fixed_card_attached_shape in opponent_fixed_card_attached_shape_list:
                            if isinstance(opponent_fixed_card_attached_shape, NonBackgroundNumberImage):
                                if opponent_fixed_card_attached_shape.get_circle_kinds() is CircleKinds.HP:
                                    print("지정한 상대방 유닛 HP Circle 찾기")

                                    your_field_card_id = self.targeting_enemy_select_using_your_field_card_id
                                    print(f"your_field_card_id: {your_field_card_id}")
                                    your_field_card_index = self.targeting_enemy_select_using_your_field_card_index
                                    print(f"your_field_card_index: {your_field_card_index}")
                                    # your_skill_damage = self.card_info_repository.getCardAttackForCardNumber(your_field_card_id)
                                    # your_skill_damage = self.card_info_repository.getCardAttackForCardNumber(your_field_card_id)
                                    # your_skill_damage = 20
                                    your_skill_damage = self.card_info_repository.getCardSkillFirstDamageForCardNumber(
                                        your_field_card_id)
                                    print(f"your_skill_damage: {your_skill_damage}")

                                    opponent_field_card_id = opponent_field_unit_object.get_card_number()
                                    opponent_field_card_index = opponent_field_unit_object.get_index()

                                    opponent_hp_number = opponent_fixed_card_attached_shape.get_number()
                                    opponent_hp_number -= your_skill_damage

                                    print(f"opponent_hp_number: {opponent_hp_number}")

                                    # TODO: n 턴간 불사 특성을 검사해야하므로 사실 이것도 summary 방식으로 빼는 것이 맞으나 우선은 진행한다.
                                    # (지금 당장 불사가 존재하지 않음)
                                    if opponent_hp_number <= 0:
                                        are_opponent_field_unit_death = True

                                        break

                                    print(f"공격 후 opponent unit 체력 -> hp_number: {opponent_hp_number}")
                                    opponent_fixed_card_attached_shape.set_number(opponent_hp_number)

                                    # opponent_fixed_card_attached_shape.set_image_data(
                                    #     # TODO: 실제로 여기서 서버로부터 계산 받은 값을 적용해야함
                                    #     self.pre_drawed_image_instance.get_pre_draw_number_image(opponent_hp_number))

                                    opponent_fixed_card_attached_shape.set_image_data(
                                        self.pre_drawed_image_instance.get_pre_draw_unit_hp(opponent_hp_number))

                        print(f"opponent_field_card_index: {opponent_field_card_index}")

                        if are_opponent_field_unit_death is True:
                            self.opponent_field_unit_repository.remove_card_by_multiple_index(
                                [opponent_field_card_index])
                            self.opponent_tomb_repository.create_opponent_tomb_card(
                                opponent_field_card_id)

                            self.opponent_field_unit_repository.replace_opponent_field_unit_card_position()

                        self.opponent_fixed_unit_card_inside_handler.clear_opponent_field_area_action()
                        self.targeting_enemy_select_using_your_field_card_index = None
                        self.targeting_enemy_select_using_your_field_card_id = None
                        self.targeting_enemy_select_support_lightning_border_list = []
                        self.opponent_you_selected_lightning_border_list = []

                        self.selected_object = None
                        self.active_panel_rectangle = None

                        return

            your_field_unit_list = self.your_field_unit_repository.get_current_field_unit_list()
            for your_field_unit in your_field_unit_list:
                if your_field_unit is None:
                    continue

                if isinstance(your_field_unit, FixedFieldCard):
                    your_field_unit.selected = False

            for your_field_unit in self.your_field_unit_repository.get_current_field_unit_list():
                if your_field_unit is None:
                    continue

                # if self.selected_object.get_card_number() == 9:
                #     self.return_to_initial_location()

                print(f"your field unit (field_unit) = {type(your_field_unit)}")
                fixed_card_base = your_field_unit.get_fixed_card_base()
                print(f"your field unit type (fixed_card_base) = {type(fixed_card_base)}")

                if fixed_card_base.is_point_inside((x, y)):
                    # if self.your_field_unit_action_repository.get_current_field_unit_action_status(your_field_unit.get_index()) == FieldUnitActionStatus.WAIT:
                    #     print(f"처음 필드에 출격한 유닛은 공격 할 수 없습니다")

                    if self.field_area_inside_handler.get_field_area_action() is FieldAreaAction.ENERGY_BOOST:
                        self.field_area_inside_handler.clear_lightning_border_list()
                        self.field_area_inside_handler.clear_field_area_action()
                        self.your_field_unit_lightning_border_list = []
                        print("덱에서 에너지 검색해서 부스팅 진행")

                        current_process_card_id = self.field_area_inside_handler.get_action_set_card_id()
                        proper_handler = self.support_card_handler.getSupportCardHandler(current_process_card_id)
                        # proper_handler(your_field_unit.get_index())

                        your_field_unit_index = your_field_unit.get_index()
                        print(f"your_field_unit index: {your_field_unit_index}")

                        # real_field_unit_index = self.your_field_unit_repository.find_field_unit_by_index(your_field_unit.get_index())
                        # print(f"real_field_unit_index: {real_field_unit_index}")

                        proper_handler(your_field_unit_index)

                        self.your_tomb_repository.create_tomb_card(current_process_card_id)
                        self.your_hand_repository.update_your_hand()

                        # self.boost_selection = False
                        break

                    # if self.field_area_inside_handler.get_field_area_action() is FieldAreaAction.TARGETING_TWO_ENEMY_AS_POSSIBLE:
                    #     print("적 유닛 2체까지 선택 가능")
                    #
                    #     break

                    your_field_unit.selected = not your_field_unit.selected
                    self.selected_object = your_field_unit
                    self.drag_start = (x, y)

                    if self.selected_object != self.prev_selected_object:
                        self.active_panel_rectangle = None
                        self.your_active_panel.clear_your_active_panel_details_button()
                        self.your_active_panel.clear_your_active_panel_second_skill_button()
                        self.your_active_panel.clear_your_active_panel_first_skill_button()
                        self.your_active_panel.clear_your_active_panel_attack_button()
                        self.your_active_panel.clear_your_active_panel()

                        self.prev_selected_object = self.selected_object

                    break

            if self.field_area_inside_handler.get_field_area_action() is FieldAreaAction.SEARCH_UNIT_CARD:
                print("레오닉의 부름: 유닛 2체 검색")

                if self.your_deck.is_point_inside_next_button((x, y)):
                    print("다음 버튼 클릭")

                    self.your_deck_repository.next_deck_page()

                if self.your_deck.is_point_inside_prev_button((x, y)):
                    print("이전 버튼 클릭")

                    self.your_deck_repository.prev_deck_page()

                if self.your_deck.is_point_inside_ok_button((x, y)):
                    print("OK 버튼 클릭")

                    # will_remove_index_from_deck = []
                    # processing_length = len(self.selected_search_unit_index_list)
                    # for index in range(processing_length):
                    #     will_remove_index_from_deck.append(
                    #         self.selected_search_unit_index_list[index] + 12 * self.selected_search_unit_page_number_list[index])
                    #
                    # print(f"will_remove_index_from_deck: {will_remove_index_from_deck}")
                    # self.your_deck_repository

                    # 실제로 지울 때 몇 개 지우는지만 알면 된다.
                    # 어차피 셔플 받아서 이미지만 갈아 끼워넣을 것이기 때문
                    processing_length = len(self.selected_search_unit_index_list)
                    self.your_deck_repository.remove_card_object_list_with_count(processing_length)

                    # self.your_hand_repository.create_additional_hand_card_list(self.selected_search_unit_id_list)
                    self.your_hand_repository.save_current_hand_state(self.selected_search_unit_id_list)
                    self.your_hand_repository.update_your_hand()
                    # self.selected_search_unit_page_number_list
                    self.selected_search_unit_lightning_border = []

                    self.field_area_inside_handler.clear_field_area_action()

                    # 셔플 받았다 가정
                    current_deck_list = self.your_deck_repository.get_current_deck_state()

                    will_remove_index_from_deck = []
                    processing_length = len(self.selected_search_unit_index_list)
                    for index in range(processing_length):
                        will_remove_index_from_deck.append(
                            self.selected_search_unit_index_list[index] + 12 *
                            self.selected_search_unit_page_number_list[index])

                    print(f"will_remove_index_from_deck: {will_remove_index_from_deck}")

                    remaining_shuffled_deck_list = [card for i, card in enumerate(current_deck_list) if
                                                    i not in will_remove_index_from_deck]

                    # 셔플
                    random.shuffle(remaining_shuffled_deck_list)
                    print(f"Shuffled deck (excluding removed indices): {remaining_shuffled_deck_list}")

                    self.your_deck_repository.update_deck(remaining_shuffled_deck_list)

                    self.selected_search_unit_index_list = []
                    self.selected_search_unit_id_list = []
                    self.selected_search_unit_page_number_list = []

                # TODO: 개수 제한 필요
                for current_page_deck_card_object in self.your_deck_repository.get_current_page_deck_list():
                    card_id = current_page_deck_card_object.get_card_number()
                    card_grade = self.card_info_repository.getCardGradeForCardNumber(card_id)
                    # print(f"card_id: {card_id}, card_grade: {card_grade}")
                    if card_grade > CardGrade.HERO.value:
                        # print("영웅 등급 이하의 유닛만 검색하여 가져 올 수 있습니다")
                        continue

                    card_type = self.card_info_repository.getCardTypeForCardNumber(card_id)
                    # print(f"card_id: {card_id}, card_type: {card_type}")
                    if card_type != CardType.UNIT.value:
                        # print("유닛 카드만 가져 올 수 있습니다")
                        continue

                    # current_page_deck_list = self.your_deck_repository.get_current_page_deck_list()
                    deck_fixed_card_base = current_page_deck_card_object.get_fixed_card_base()

                    # print(f"레오닉의 부름 -> x: {x}, y: {y}")

                    existing_index = None

                    if deck_fixed_card_base.is_point_inside((x, y)):
                        print("덱에서 검색하여 유닛 선택!")
                        current_page_deck_card_index = current_page_deck_card_object.get_index()
                        current_page_number = self.your_deck_repository.get_current_deck_page()
                        try:
                            existing_index = self.selected_search_unit_index_list.index(current_page_deck_card_index)
                            print(f"current_page_number: {current_page_number}, existing_index: {existing_index}")
                            print(
                                f"selected_search_unit_page_number_list[existing_index]: {self.selected_search_unit_page_number_list[existing_index]}")
                            print(
                                f"selected_search_unit_index_list[existing_index]: {self.selected_search_unit_index_list[existing_index]}")

                            if (current_page_number == self.selected_search_unit_page_number_list[existing_index]) and \
                                    (current_page_deck_card_index == self.selected_search_unit_index_list[
                                        existing_index]):
                                del self.selected_search_unit_index_list[existing_index]
                                del self.selected_search_unit_id_list[existing_index]
                                del self.selected_search_unit_page_number_list[existing_index]
                                del self.selected_search_unit_lightning_border[existing_index]
                                return

                        except ValueError:
                            pass

                        if len(self.selected_search_unit_index_list) == 2:
                            return

                        else:
                            self.selected_search_unit_index_list.append(current_page_deck_card_index)

                            self.selected_search_unit_id_list.append(current_page_deck_card_object.get_card_number())
                            self.selected_search_unit_page_number_list.append(
                                self.your_deck_repository.get_current_deck_page())

                            self.selected_search_unit_lightning_border.append(deck_fixed_card_base)

                return

            if self.fixed_unit_card_inside_action is FixedUnitCardInsideAction.TARGETING_TWO_ENEMY_AS_POSSIBLE:
                print("적 유닛 2체까지 선택 가능")

                opponent_field_unit_object_list = self.opponent_field_unit_repository.get_current_field_unit_card_object_list()
                for opponent_field_unit_object in opponent_field_unit_object_list:
                    if opponent_field_unit_object is None:
                        continue

                    if isinstance(opponent_field_unit_object, FixedFieldCard):
                        opponent_field_unit_object.selected = False

                for opponent_field_unit_object in opponent_field_unit_object_list:
                    if opponent_field_unit_object is None:
                        continue

                    opponent_fixed_card_base = opponent_field_unit_object.get_fixed_card_base()

                    # TODO: 1체라도 선택하면 확인 버튼이 나와야 합니다.
                    if opponent_fixed_card_base.is_point_inside((x, y)):
                        self.opponent_you_selected_lightning_border_list.append(opponent_fixed_card_base)

                        # opponent_you_select_unit_index = opponent_field_unit_object.get_index()
                        self.opponent_you_selected_object_list.append(opponent_field_unit_object)

                        self.targeting_enemy_select_count -= 1
                        print(f"selected_opponent_unit index: {opponent_field_unit_object.get_index()}")

                        if self.targeting_enemy_select_count == 0:
                            remove_from_field_index_list = []
                            remove_from_field_id_list = []

                            for opponent_you_selected_object in self.opponent_you_selected_object_list:
                                opponent_fixed_card_base = opponent_you_selected_object.get_fixed_card_base()

                                opponent_fixed_card_attached_shape_list = opponent_fixed_card_base.get_attached_shapes()
                                # remove_from_field = False

                                for opponent_fixed_card_attached_shape in opponent_fixed_card_attached_shape_list:
                                    if isinstance(opponent_fixed_card_attached_shape, NonBackgroundNumberImage):
                                        if opponent_fixed_card_attached_shape.get_circle_kinds() is CircleKinds.HP:

                                            hp_number = opponent_fixed_card_attached_shape.get_number()
                                            hp_number -= 10

                                            # TODO: n 턴간 불사 특성을 검사해야하므로 사실 이것도 summary 방식으로 빼는 것이 맞으나 우선은 진행한다.
                                            # (지금 당장 불사가 존재하지 않음)
                                            if hp_number <= 0:
                                                # remove_from_field = True
                                                remove_from_field_index_list.append(
                                                    opponent_you_selected_object.get_index())
                                                remove_from_field_id_list.append(
                                                    opponent_you_selected_object.get_card_number())

                                                break

                                            print(f"corpse explosion -> hp_number: {hp_number}")
                                            opponent_fixed_card_attached_shape.set_number(hp_number)

                                            # opponent_fixed_card_attached_shape.set_image_data(
                                            #     # TODO: 실제로 여기서 서버로부터 계산 받은 값을 적용해야함
                                            #     self.pre_drawed_image_instance.get_pre_draw_number_image(hp_number))

                                            opponent_fixed_card_attached_shape.set_image_data(
                                                self.pre_drawed_image_instance.get_pre_draw_unit_hp(hp_number))

                                # if remove_from_field:
                                #     card_id = opponent_you_selected_object.get_card_number()
                                #
                                #     self.opponent_field_unit_repository.remove_current_field_unit_card(opponent_you_selected_object.get_index())
                                #     self.opponent_tomb_repository.create_opponent_tomb_card(card_id)

                            # for remove_from_field in remove_from_field_list:

                            print(
                                f"corpse explosion your hand index: {self.targeting_ememy_select_using_hand_card_index}")
                            # self.your_hand_repository.remove_card_by_index(
                            #     self.targeting_ememy_select_using_hand_card_index)
                            self.your_hand_repository.remove_card_by_index_with_page(
                                self.targeting_ememy_select_using_hand_card_index)
                            self.your_tomb_repository.create_tomb_card(
                                self.targeting_ememy_select_using_hand_card_id)

                            self.opponent_field_unit_repository.remove_card_by_multiple_index(
                                remove_from_field_index_list)

                            for remove_from_field_id in remove_from_field_id_list:
                                self.opponent_tomb_repository.create_opponent_tomb_card(
                                    remove_from_field_id)

                            print(
                                f"corpse explosion your field index: {self.targeting_enemy_select_using_your_field_card_index}")
                            self.your_field_unit_repository.remove_card_by_index(
                                self.targeting_enemy_select_using_your_field_card_index)
                            self.your_tomb_repository.create_tomb_card(self.targeting_enemy_for_sacrifice_unit_id)

                            # self.your_hand_repository.replace_hand_card_position()
                            self.your_hand_repository.update_your_hand()
                            self.opponent_field_unit_repository.replace_opponent_field_unit_card_position()
                            self.your_field_unit_repository.replace_field_card_position()

                            self.fixed_unit_card_inside_action = FixedUnitCardInsideAction.Dummy

                            self.targeting_ememy_select_using_hand_card_id = -1
                            self.targeting_ememy_select_using_hand_card_index = -1
                            self.targeting_enemy_select_using_your_field_card_index = -1
                            self.targeting_enemy_for_sacrifice_unit_id = -1

                            self.targeting_enemy_select_support_lightning_border_list = []
                            self.opponent_you_selected_lightning_border_list = []
                            self.opponent_you_selected_object_list = []

                            self.selected_object = None
                            return

            your_hand_next_button_clicked = self.your_hand.is_point_inside_next_button_hand((x, y))
            if your_hand_next_button_clicked:
                print("Your Hand Next Button Clicked!")

                self.your_hand_repository.next_your_hand_page()

            your_hand_prev_button_clicked = self.your_hand.is_point_inside_prev_button_hand((x, y))
            if your_hand_prev_button_clicked:
                print("Your Hand Prev Button Clicked!")

                self.your_hand_repository.prev_your_hand_page()

            self.tomb_panel_selected = self.left_click_detector.which_one_select_is_in_your_tomb_area(
                (x, y),
                self.your_tomb,
                self.winfo_reqheight())

            if self.tomb_panel_selected:
                print(
                    f"on_canvas_left_click() -> current_tomb_unit_list: {self.your_tomb_repository.get_current_tomb_state()}")
                self.your_tomb.create_tomb_panel_popup_rectangle()
                self.tomb_panel_popup_rectangle = self.your_tomb.get_tomb_panel_popup_rectangle()

                self.opponent_tomb_panel_selected = False
                self.your_lost_zone_panel_selected = False
                self.opponent_lost_zone_panel_selected = False
                self.muligun_reset_button_clicked = False
                self.multi_draw_button_clicked = False
                return

            self.opponent_tomb_panel_selected = self.left_click_detector.which_one_select_is_in_opponent_tomb_area(
                (x, y),
                self.opponent_tomb,
                self.winfo_reqheight())

            if self.opponent_tomb_panel_selected:
                print(
                    f"on_canvas_left_click() -> current_tomb_unit_list: {self.opponent_tomb_repository.get_opponent_tomb_state()}")
                self.opponent_tomb.create_opponent_tomb_panel_popup_rectangle()
                self.opponent_tomb_popup_rectangle_panel = self.opponent_tomb.get_opponent_tomb_panel_popup_rectangle()

                self.tomb_panel_selected = False
                self.your_lost_zone_panel_selected = False
                self.opponent_lost_zone_panel_selected = False
                self.muligun_reset_button_clicked = False
                self.multi_draw_button_clicked = False
                return

            self.your_lost_zone_panel_selected = self.left_click_detector.which_one_select_is_in_your_lost_zone_area(
                (x, y),
                self.your_lost_zone,
                self.winfo_reqheight())

            if self.your_lost_zone_panel_selected:
                print(
                    f"on_canvas_left_click() -> current_lost_zone_card_list: {self.your_lost_zone_repository.get_your_lost_zone_card_list()}")
                self.your_lost_zone.create_your_lost_zone_popup_panel()
                self.your_lost_zone_popup_panel = self.your_lost_zone.get_your_lost_zone_popup_panel()

                self.tomb_panel_selected = False
                self.opponent_tomb_panel_selected = False
                self.opponent_lost_zone_panel_selected = False
                self.muligun_reset_button_clicked = False
                self.multi_draw_button_clicked = False
                return

            self.opponent_lost_zone_panel_selected = self.left_click_detector.which_one_select_is_in_opponent_lost_zone_area(
                (x, y),
                self.opponent_lost_zone,
                self.winfo_reqheight())

            if self.opponent_lost_zone_panel_selected:
                print(
                    f"on_canvas_left_click() -> current_lost_zone_card_list: {self.opponent_lost_zone_repository.get_opponent_lost_zone_card_list()}")
                self.opponent_lost_zone.create_opponent_lost_zone_popup_panel()
                self.opponent_lost_zone_popup_panel = self.opponent_lost_zone.get_opponent_lost_zone_popup_panel()

                self.tomb_panel_selected = False
                self.opponent_tomb_panel_selected = False
                self.your_lost_zone_panel_selected = False
                self.muligun_reset_button_clicked = False
                self.multi_draw_button_clicked = False
                return

            self.muligun_reset_button_clicked = self.is_point_inside_muligun_reset_button(
                (x, y),
                self.muligun_reset_button,
                self.winfo_reqheight())

            if self.muligun_reset_button_clicked:
                print(f"muligun_reset_button_clicked()")

                self.tomb_panel_selected = False
                self.opponent_tomb_panel_selected = False
                self.your_lost_zone_panel_selected = False
                self.opponent_lost_zone_panel_selected = False
                self.multi_draw_button_clicked = False

                current_hand_card_list = self.your_hand_repository.get_current_hand_state()
                current_hand_card_list_str = list(map(str, current_hand_card_list))

                muligunResponseData = self.your_hand_repository.request_fake_muligun(
                    MuligunRequest(self.__session_repository.get_first_fake_session_info(),
                                   current_hand_card_list_str))

                # self.your_hand_repository.remove_card_by_index_with_page([0, 1, 2, 3, 4, 5])

                print(f"muligun responseData: {muligunResponseData}")
                redrawn_hand_card_list = muligunResponseData['redrawn_hand_card_list']
                print(f"{Fore.RED}redrawn_hand_card_list:{Fore.GREEN} {redrawn_hand_card_list}{Style.RESET_ALL}")
                # redrawn_hand_card_list_str = list(map(str, redrawn_hand_card_list))
                self.your_hand_repository.clear_your_hand_state()
                self.your_hand_repository.save_current_hand_state(redrawn_hand_card_list)
                self.your_hand_repository.update_your_hand()

                deck_card_list = muligunResponseData['updated_deck_card_list']

                return

            self.multi_draw_button_clicked = self.is_point_inside_multi_draw_button(
                (x, y),
                self.multi_draw_button,
                self.winfo_reqheight())

            if self.multi_draw_button_clicked:
                print(f"multi_draw_button_clicked()")

                self.tomb_panel_selected = False
                self.opponent_tomb_panel_selected = False
                self.your_lost_zone_panel_selected = False
                self.opponent_lost_zone_panel_selected = False
                self.muligun_reset_button_clicked = False

                multi_draw_response = self.__fake_battle_field_frame_repository.request_fake_multi_draw(
                    FakeMultiDrawRequest(self.__session_repository.get_first_fake_session_info()))

                print(f"{Fore.RED}multi_draw_response:{Fore.GREEN} {multi_draw_response}{Style.RESET_ALL}")
                multi_draw_hand_list = multi_draw_response['player_multi_drawn_card_list']['You']

                self.your_hand_repository.save_current_hand_state(multi_draw_hand_list)
                self.your_hand_repository.update_your_hand()

                before_current_deck_list = self.your_deck_repository.get_current_deck_state_object().get_current_deck()
                print(f"{Fore.RED}before multi draw -> before_current_deck_list:{Fore.GREEN} {before_current_deck_list}{Style.RESET_ALL}")

                for _ in range(20):
                    self.your_deck_repository.get_current_deck_state_object().draw_card()

                after_current_deck_list = self.your_deck_repository.get_current_deck_state_object().get_current_deck()
                print(f"{Fore.RED}after multi draw -> after_current_deck_list:{Fore.GREEN} {after_current_deck_list}{Style.RESET_ALL}")

            self.turn_end_button_selected = self.left_click_detector.which_one_select_is_in_turn_end_area(
                (x, y),
                self.turn_end,
                self.winfo_reqheight()
            )

            if self.turn_end_button_selected:
                self.call_turn_end()

            self.your_field_energy_panel_selected = False

            self.your_field_energy_panel_selected = self.left_click_detector.which_one_select_is_in_your_field_energy_area(
                (x, y),
                self.your_field_energy,
                self.winfo_reqheight()
            )

            self.next_field_energy_race_panel_selected = self.left_click_detector.which_one_select_is_in_next_field_energy_race_area(
                (x, y),
                self.next_field_energy_race,
                self.winfo_reqheight()
            )

            if self.next_field_energy_race_panel_selected:
                self.your_field_energy_repository.to_next_field_energy_race()
                print(
                    f"on_canvas_left_click() -> to_next_field_energy_race: {self.your_field_energy_repository.get_current_field_energy_race()}")

            self.prev_field_energy_race_panel_selected = self.left_click_detector.which_one_select_is_in_prev_field_energy_race_area(
                (x, y),
                self.prev_field_energy_race,
                self.winfo_reqheight()
            )

            if self.prev_field_energy_race_panel_selected:
                self.your_field_energy_repository.to_prev_field_energy_race()
                print(
                    f"on_canvas_left_click() -> to_prev_field_energy_race: {self.your_field_energy_repository.get_current_field_energy_race()}")

            self.increase_to_use_field_energy_count_panel_selected = (
                self.left_click_detector.which_one_select_is_in_increase_to_use_field_energy_count_area(
                    (x, y),
                    self.increase_to_use_field_energy_count,
                    self.winfo_reqheight()
                )
            )

            if self.increase_to_use_field_energy_count_panel_selected:
                print(f"on_canvas_left_click() -> increase_to_use_field_energy_count(): "
                      f"{self.your_field_energy_repository.get_to_use_field_energy_count()}")
                self.your_field_energy_repository.increase_to_use_field_energy_count()

            self.decrease_to_use_field_energy_count_panel_selected = (
                self.left_click_detector.which_one_select_is_in_decrease_to_use_field_energy_count_area(
                    (x, y),
                    self.decrease_to_use_field_energy_count,
                    self.winfo_reqheight()
                )
            )

            if self.decrease_to_use_field_energy_count_panel_selected:
                print(f"on_canvas_left_click() -> decrease_to_use_field_energy_count(): "
                      f"{self.your_field_energy_repository.get_to_use_field_energy_count()}")
                self.your_field_energy_repository.decrease_to_use_field_energy_count()

            self.tomb_panel_selected = False
            self.opponent_tomb_panel_selected = False
            self.your_lost_zone_panel_selected = False
            self.opponent_lost_zone_panel_selected = False
            self.muligun_reset_button_clicked = False

        except Exception as e:
            print(f"Exception in on_canvas_click: {e}")

    def is_point_inside_multi_draw_button(self, click_point, multi_draw_button, canvas_height):
        x, y = click_point
        y = canvas_height - y

        translated_vertices = [
            (x * self.width_ratio, y * self.height_ratio)
            for x, y in multi_draw_button.get_vertices()
        ]
        print(f"translated_vertices: {translated_vertices}")

        if not (translated_vertices[0][0] <= x <= translated_vertices[2][0] and
                translated_vertices[1][1] <= y <= translated_vertices[2][1]):
            print("multi_draw_button result -> False")
            return False

        print("multi_draw_button result -> True")
        return True

    def is_point_inside_muligun_reset_button(self, click_point, muligun_reset_button, canvas_height):
        x, y = click_point
        y = canvas_height - y

        translated_vertices = [
            (x * self.width_ratio, y * self.height_ratio)
            for x, y in muligun_reset_button.get_vertices()
        ]
        print(f"translated_vertices: {translated_vertices}")

        if not (translated_vertices[0][0] <= x <= translated_vertices[2][0] and
                translated_vertices[1][1] <= y <= translated_vertices[2][1]):
            print("muligun_reset_button result -> False")
            return False

        print("muligun_reset_button result -> True")
        return True

    def call_turn_end(self):
        turn_end_request_result = self.round_repository.request_turn_end(
            TurnEndRequest(
                self.__session_repository.get_session_info()))
        print(f"turn_end_request_result: {turn_end_request_result}")

        self.__notify_reader_repository.set_is_your_turn_for_check_fake_process(False)
        whose_turn = self.__notify_reader_repository.get_is_your_turn_for_check_fake_process()
        print(f"{Fore.RED}call_turn_end() -> whose_turn True(Your) or False(Opponent):{Fore.GREEN} {whose_turn}{Style.RESET_ALL}")

        self.round_repository.increase_current_round_number()
        round = self.round_repository.get_current_round_number()
        print(f"current round: {round}")

        # before_turn_end_field_energy_count = self.your_field_energy_repository.get_your_field_energy()
        # print(f"before_turn_end_field_energy_count: {before_turn_end_field_energy_count}")
        #
        # self.your_field_energy_repository.increase_your_field_energy(1)
        #
        # after_turn_end_field_energy_count = self.your_field_energy_repository.get_your_field_energy()
        # print(f"after_turn_end_field_energy_count: {after_turn_end_field_energy_count}")

        current_your_field_unit_list = self.your_field_unit_repository.get_current_field_unit_list()
        for current_your_field_unit in current_your_field_unit_list:
            if current_your_field_unit is None:
                continue

            current_your_field_unit_index = current_your_field_unit.get_index()
            print(f"call_turn_end() -> current_your_field_unit_index: {current_your_field_unit_index}")
            self.your_field_unit_action_repository.set_current_field_unit_action_ready(current_your_field_unit_index)
            self.your_field_unit_action_repository.set_current_field_unit_action_count(current_your_field_unit_index, 1)

    def call_surrender(self):
        print("항복 요청!")

    def on_canvas_right_click(self, event):
        x, y = event.x, event.y

        if self.selected_object and isinstance(self.selected_object, FixedFieldCard):
            convert_y = self.winfo_reqheight() - y
            fixed_card_base = self.selected_object.get_fixed_card_base()
            if fixed_card_base.is_point_inside((x, convert_y)):
                # new_rectangle = self.create_opengl_rectangle((x, y))
                self.your_active_panel.create_your_active_panel((x, y), self.selected_object)

                new_rectangle = self.your_active_panel.get_your_active_panel()
                self.active_panel_rectangle = new_rectangle

                self.active_panel_attack_button = self.your_active_panel.get_your_active_panel_attack_button()
                self.active_panel_first_skill_button = self.your_active_panel.get_your_active_panel_first_skill_button()
                self.active_panel_second_skill_button = self.your_active_panel.get_your_active_panel_second_skill_button()
                self.active_panel_third_skill_button = None
                self.active_panel_details_button = self.your_active_panel.get_your_active_panel_details_button()

    def create_opengl_rectangle(self, start_point):
        card_id = self.selected_object.get_card_number()
        print(f"card id: {card_id}")
        print(f"skill info: {self.card_info_repository.getCardSkillForCardNumber(card_id)}")
        print(f"skill counter: {self.card_info_repository.getCardSkillCounterForCardNumber(card_id)}")
        print(f"skill first: {self.card_info_repository.getCardSkillFirstForCardNumber(card_id)}")
        print(f"skill second: {self.card_info_repository.getCardSkillSecondForCardNumber(card_id)}")
        print(f"passive info: {self.card_info_repository.getCardPassiveForCardNumber(card_id)}")
        print(f"passive first: {self.card_info_repository.getCardPassiveFirstForCardNumber(card_id)}")
        print(f"passive second: {self.card_info_repository.getCardPassiveSecondForCardNumber(card_id)}")

        rectangle_size = 50 * self.width_ratio
        rectangle_color = (1.0, 0.0, 0.0, 1.0)

        end_point = (start_point[0] + rectangle_size, start_point[1] + rectangle_size)

        new_rectangle = Rectangle(rectangle_color, [
            (start_point[0], start_point[1]),
            (end_point[0], start_point[1]),
            (end_point[0], end_point[1]),
            (start_point[0], end_point[1])
        ])
        new_rectangle.created_by_right_click = True
        return new_rectangle

    def battle_finish(self):
        self.battle_result.set_total_window_size(self.width, self.height)
        self.battle_result.create_battle_result_panel_list()
        self.battle_result_panel_list = self.battle_result.get_battle_result_panel_list()

    def attach_energy_to_opponent_unit(self, attach_energy_data):
        print("attach undead energy")

        # TODO: Change it to ENUM Value (Not just integer)
        card_race = attach_energy_data['attach_energy_race_type']
        print(f"card_race: {card_race}")

        attach_energy_count = attach_energy_data['attach_race_energy_count']
        opponent_unit_index = attach_energy_data['field_unit_index']

        # self.opponent_field_unit_repository.attach_race_energy(opponent_unit_index, EnergyType.Undead, attach_energy_count)
        # opponent_field_unit = self.opponent_field_unit_repository.find_opponent_field_unit_by_index(0)
        #
        # opponent_field_unit_attached_undead_energy_count = self.opponent_field_unit_repository.get_opponent_field_unit_race_energy(0, EnergyType.Undead)
        # print(f"opponent_field_unit_attached_undead_energy_count: {opponent_field_unit_attached_undead_energy_count}")

        before_attach_energy_count = self.opponent_field_unit_repository.get_opponent_field_unit_race_energy(
            opponent_unit_index, EnergyType.Undead)

        difference_energy_count = attach_energy_count - before_attach_energy_count

        self.opponent_field_unit_repository.attach_race_energy(
            opponent_unit_index,
            EnergyType.Undead,
            difference_energy_count)
        opponent_field_unit = self.opponent_field_unit_repository.find_opponent_field_unit_by_index(opponent_unit_index)

        # after_attach_energy_count = self.opponent_field_unit_repository.get_opponent_field_unit_race_energy(
        #     0, EnergyType.Undead)
        total_attached_energy_count = self.opponent_field_unit_repository.get_total_energy_at_index(opponent_unit_index)
        print(
            f"opponent_field_unit_attached_undead_energy_count: {total_attached_energy_count}")

        opponent_fixed_card_base = opponent_field_unit.get_fixed_card_base()
        opponent_fixed_card_attached_shape_list = opponent_fixed_card_base.get_attached_shapes()

        for opponent_fixed_card_attached_shape in opponent_fixed_card_attached_shape_list:
            if isinstance(opponent_fixed_card_attached_shape, NonBackgroundNumberImage):
                if opponent_fixed_card_attached_shape.get_circle_kinds() is CircleKinds.ENERGY:
                    # opponent_fixed_card_attached_shape.set_image_data(
                    #     self.pre_drawed_image_instance.get_pre_draw_number_image(
                    #         total_attached_energy_count))

                    opponent_fixed_card_attached_shape.set_image_data(
                        self.pre_drawed_image_instance.get_pre_draw_unit_energy(
                            total_attached_energy_count))

                    print(f"changed energy: {opponent_fixed_card_attached_shape.get_circle_kinds()}")

        every_energy = self.opponent_field_unit_repository.get_energy_info_at_index(0)
        print(f"every_energy: {every_energy}")

    def detach_energy_to_your_unit(self, attach_energy_data):
        print("detach undead energy")

        # TODO: Change it to ENUM Value (Not just integer)
        card_race = attach_energy_data['attach_energy_race_type']
        print(f"card_race: {card_race}")

        attach_energy_count = attach_energy_data['attach_race_energy_count']
        your_unit_index = attach_energy_data['field_unit_index']

        before_attach_energy_count = self.your_field_unit_repository.get_your_field_unit_race_energy(
            your_unit_index, EnergyType.Undead)

        difference_energy_count = before_attach_energy_count - attach_energy_count

        self.your_field_unit_repository.detach_race_energy(
            your_unit_index,
            EnergyType.Undead,
            difference_energy_count)
        your_field_unit = self.your_field_unit_repository.find_field_unit_by_index(your_unit_index)

        # after_attach_energy_count = self.opponent_field_unit_repository.get_opponent_field_unit_race_energy(
        #     0, EnergyType.Undead)
        total_attached_energy_count = self.your_field_unit_repository.get_total_energy_at_index(your_unit_index)
        print(
            f"your_field_unit_attached_undead_energy_count: {total_attached_energy_count}")

        your_fixed_card_base = your_field_unit.get_fixed_card_base()
        your_fixed_card_attached_shape_list = your_fixed_card_base.get_attached_shapes()

        for your_fixed_card_attached_shape in your_fixed_card_attached_shape_list:
            if isinstance(your_fixed_card_attached_shape, NonBackgroundNumberImage):
                if your_fixed_card_attached_shape.get_circle_kinds() is CircleKinds.ENERGY:
                    # opponent_fixed_card_attached_shape.set_image_data(
                    #     self.pre_drawed_image_instance.get_pre_draw_number_image(
                    #         total_attached_energy_count))

                    your_fixed_card_attached_shape.set_image_data(
                        self.pre_drawed_image_instance.get_pre_draw_unit_energy(
                            total_attached_energy_count))

                    print(f"changed energy: {your_fixed_card_attached_shape.get_circle_kinds()}")

        every_energy = self.opponent_field_unit_repository.get_energy_info_at_index(your_unit_index)
        print(f"every_energy: {every_energy}")

    # if card_race == CardRace.UNDEAD.value:
    #     card_race_circle = opponent_field_unit.creat_fixed_card_energy_race_circle(
    #         color=(0, 0, 0, 1),
    #         vertices=(0, (total_attached_energy_count * 10) + 20),
    #         local_translation=opponent_fixed_card_base.get_local_translation())
    #     opponent_fixed_card_base.set_attached_shapes(card_race_circle)

