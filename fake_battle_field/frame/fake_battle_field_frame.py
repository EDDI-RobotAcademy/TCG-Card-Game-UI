import math
import random

from colorama import Fore, Style
from screeninfo import get_monitors
from shapely import Polygon, Point

from battle_field.animation_support.animation_action import AnimationAction
from battle_field.components.field_area_inside.field_area_action import FieldAreaAction

from OpenGL.GL import *
from OpenGL.GLU import *
from pyopengltk import OpenGLFrame

from battle_field.components.field_area_inside.field_area_inside_handler import FieldAreaInsideHandler
from battle_field.components.field_area_inside.turn_start_action import TurnStartAction
from battle_field.components.field_area_inside.unit_action import UnitAction
from battle_field.components.fixed_unit_card_inside.fixed_unit_card_inside_action import FixedUnitCardInsideAction
from battle_field.components.mouse_left_click.left_click_detector import LeftClickDetector
from battle_field.components.opponent_field_area_inside.opponent_field_area_action_process import \
    OpponentFieldAreaActionProcess
from battle_field.components.opponent_field_area_inside.opponent_field_area_inside_handler import \
    OpponentFieldAreaInsideHandler
from battle_field.components.opponent_field_area_inside.opponent_unit_action import OpponentUnitAction
from battle_field.components.opponent_fixed_unit_card_inside.ActionToApplyOpponent import ActionToApplyOpponent
from battle_field.components.opponent_fixed_unit_card_inside.opponent_field_area_action import OpponentFieldAreaAction
from battle_field.components.opponent_fixed_unit_card_inside.opponent_fixed_unit_card_inside_handler import \
    OpponentFixedUnitCardInsideHandler
from battle_field.entity.battle_field_scene import BattleFieldScene
from battle_field.entity.battle_result import BattleResult
from battle_field.entity.current_field_energy_race import CurrentFieldEnergyRace
from battle_field.entity.current_to_use_field_energy_count import CurrentToUseFieldEnergyCount
from battle_field.entity.decrease_to_use_field_energy_count import DecreaseToUseFieldEnergyCount
from battle_field.entity.effect_animation import EffectAnimation
from battle_field.entity.increase_to_use_field_energy_count import IncreaseToUseFieldEnergyCount
from battle_field.entity.opponent_active_panel import OpponentActivePanel
from battle_field.entity.skill_focus_panel import SkillFocusPanel
from battle_field.entity.your_hand_details_panel import YourHandDetailsPanel
from battle_field.entity.your_main_character import YourMainCharacter
from battle_field.entity.message_on_the_battle_screen import MessageOnTheBattleScreen
from battle_field.entity.next_field_energy_race import NextFieldEnergyRace
from battle_field.entity.opponent_field_energy import OpponentFieldEnergy
from battle_field.entity.opponent_field_panel import OpponentFieldPanel
from battle_field.entity.opponent_hp import OpponentHp
from battle_field.entity.opponent_main_character import OpponentMainCharacter
from battle_field.entity.option import Option
from battle_field.entity.prev_field_energy_race import PrevFieldEnergyRace
from battle_field.entity.surrender_confirm import SurrenderConfirm
from battle_field.entity.turn_end import TurnEnd
from battle_field.entity.turn_number import CurrentFieldTurnNumber
from battle_field.entity.your_active_panel import YourActivePanel
from battle_field.entity.opponent_details_panel import OpponentDetailsPanel
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
from battle_field.entity.battle_field_timer import BattleFieldTimer
from battle_field.handler.support_card_handler import SupportCardHandler
from battle_field.infra.battle_field_repository import BattleFieldRepository
from battle_field.infra.effect_animation_repository import EffectAnimationRepository

from battle_field.infra.opponent_field_energy_repository import OpponentFieldEnergyRepository
from battle_field.infra.opponent_field_unit_repository import OpponentFieldUnitRepository
from battle_field.infra.opponent_hand_repository import OpponentHandRepository
from battle_field.infra.opponent_hp_repository import OpponentHpRepository
from battle_field.infra.opponent_lost_zone_repository import OpponentLostZoneRepository

from battle_field.infra.opponent_tomb_repository import OpponentTombRepository
from battle_field.infra.request.drawCardByUseSupportCardRequest import DrawCardByUseSupportCardRequest
from battle_field.infra.request.request_attach_field_energy_to_unit import RequestAttachFieldEnergyToUnit
from battle_field.infra.request.request_attack_main_character_with_active_skill import \
    RequestAttackMainCharacterWithActiveSkill
from battle_field.infra.request.request_attack_opponent_unit import RequestAttackOpponentUnit
from battle_field.infra.request.request_attack_to_opponent_field_unit_with_active_skill import \
    RequestAttackToOpponentFieldUnitWithActiveSkill
from battle_field.infra.request.request_attack_to_your_field_unit_with_active_skill import \
    RequestAttackToYourFieldUnitWithActiveSkill
from battle_field.infra.request.request_attack_with_non_targeting_active_skill import \
    RequestAttackWithNonTargetingActiveSkill
from battle_field.infra.request.request_use_add_field_energy_by_sacrificing_field_unit_support_card import \
    RequestUseAddFieldEnergyBySacrificingFieldUnitSupportCard
from battle_field.infra.request.request_use_corpse_explosion import RequestUseCorpseExplosion
from battle_field.infra.request.request_use_death_sice_to_unit import RequestUseDeathSiceToUnit
from battle_field.infra.request.request_use_energy_burn_to_unit import RequestUseEnergyBurnToUnit
from battle_field.infra.request.request_use_energy_card_to_unit import RequestUseEnergyCardToUnit
from battle_field.infra.request.request_use_field_of_death import RequestUseFieldOfDeath
from battle_field.infra.request.request_use_morale_conversion import RequestUseMoraleConversion
from battle_field.infra.request.request_use_overflow_of_energy import RequestUseOverflowOfEnergy
from battle_field.infra.request.target_passive_skill_to_main_character_from_deploy_request import \
    TargetingPassiveSkillToMainCharacterFromDeployRequest
from battle_field.infra.request.targeting_passive_skill_to_opponent_field_unit_from_deploy_request import \
    TargetingPassiveSkillToOpponentFieldUnitFromDeployRequest
from battle_field.infra.request.targeting_passive_skill_to_your_field_unit_from_deploy_request import \
    TargetingPassiveSkillToYourFieldUnitFromDeployRequest
from battle_field.infra.request.turn_start_first_passive_skill_request import TurnStartFirstPassiveSkillRequest
from battle_field.infra.request.turn_start_second_passive_skill_to_main_character_request import \
    TurnStartSecondPassiveSkillToMainCharacterRequest
from battle_field.infra.request.turn_start_second_passive_skill_to_your_field_unit_request import \
    TurnStartSecondPassiveSkillToYourFieldUnitRequest

from battle_field.infra.request.wide_area_passive_skill_from_deploy_request import WideAreaPassiveSkillFromDeployRequest
from battle_field.infra.request.request_use_special_energy_card_to_unit import RequestUseSpecialEnergyCardToUnit

from battle_field.infra.round_repository import RoundRepository
from battle_field.infra.window_size_repository import WindowSizeRepository
from battle_field.infra.your_deck_repository import YourDeckRepository

from battle_field.infra.your_field_energy_repository import YourFieldEnergyRepository
from battle_field.infra.your_field_unit_action_repository import YourFieldUnitActionRepository
from battle_field.infra.your_field_unit_repository import YourFieldUnitRepository

from battle_field.infra.your_hand_repository import YourHandRepository

from battle_field.infra.your_hp_repository import YourHpRepository
from battle_field.infra.your_lost_zone_repository import YourLostZoneRepository

from battle_field.infra.your_tomb_repository import YourTombRepository
from battle_field.infra.battle_field_timer_repository import BattleFieldTimerRepository

from battle_field.state.FieldUnitActionStatus import FieldUnitActionStatus
from battle_field.state.energy_type import EnergyType
from battle_field_fixed_card.fixed_details_card import FixedDetailsCard
from battle_field_fixed_card.fixed_field_card import FixedFieldCard
from battle_field_function.controller.battle_field_function_controller_impl import BattleFieldFunctionControllerImpl
from battle_field_function.service.request.turn_end_request import TurnEndRequest
# from battle_field_muligun.infra.muligun_your_hand_repository import MuligunYourHandRepository
from battle_field_muligun.service.request.muligun_request import MuligunRequest

from card_info_from_csv.repository.card_info_from_csv_repository_impl import CardInfoFromCsvRepositoryImpl
from common.attack_type import AttackType
from common.battle_finish_position import BattleFinishPosition
from common.card_grade import CardGrade
from common.card_race import CardRace
from common.card_type import CardType
from common.message_number import MessageNumber
from common.survival_type import SurvivalType
from common.target_type import TargetType
from fake_battle_field.entity.animation_test_image import AnimationTestImage
from fake_battle_field.entity.muligun_reset_button import MuligunResetButton
from fake_battle_field.entity.multi_draw_button import MultiDrawButton
from fake_battle_field.infra.fake_battle_field_frame_repository_impl import FakeBattleFieldFrameRepositoryImpl
from fake_battle_field.infra.fake_opponent_hand_repository import FakeOpponentHandRepositoryImpl
from fake_battle_field.service.request.attack_main_character_request import RequestAttackMainCharacter
from fake_battle_field.service.request.call_of_leonic_request import RequestUseCallOfLeonic
from fake_battle_field.service.request.fake_multi_draw_request import FakeMultiDrawRequest
from fake_battle_field.service.request.fake_opponent_deploy_unit_request import FakeOpponentDeployUnitRequest
from fake_battle_field.service.request.request_use_contract_of_doom import RequestUseContractOfDoom
from fake_notify_reader.repository.fake_notify_reader_repository_impl import FakeNotifyReaderRepositoryImpl
from image_shape.circle_image import CircleImage
from image_shape.circle_kinds import CircleKinds
from image_shape.circle_number_image import CircleNumberImage
from image_shape.non_background_number_image import NonBackgroundNumberImage
from image_shape.rectangle_kinds import RectangleKinds
from music_player.repository.music_player_repository_impl import MusicPlayerRepositoryImpl

# from notify_reader.repository.notify_reader_repository_impl import NotifyReaderRepositoryImpl
from opengl_battle_field_pickable_card.pickable_card import PickableCard

from opengl_rectangle_lightning_border.lightning_border import LightningBorder
from opengl_shape.circle import Circle
from opengl_shape.rectangle import Rectangle
from pre_drawed_image_manager.pre_drawed_image import PreDrawedImage
from session.repository.session_repository_impl import SessionRepositoryImpl
from battle_field.animation_support.attack_animation import AttackAnimation


class FakeBattleFieldFrame(OpenGLFrame):
    battle_field_function_controller = BattleFieldFunctionControllerImpl.getInstance()

    __fake_battle_field_frame_repository = FakeBattleFieldFrameRepositoryImpl.getInstance()
    __fake_opponent_hand_repository = FakeOpponentHandRepositoryImpl.getInstance()
    __session_repository = SessionRepositoryImpl.getInstance()
    __notify_reader_repository = FakeNotifyReaderRepositoryImpl.getInstance()
    __music_player_repository = MusicPlayerRepositoryImpl.getInstance()
    window_size_repository = WindowSizeRepository.getInstance()

    is_playing_action_animation = False

    attack_animation_object = AttackAnimation.getInstance()

    animation_step_count = 0

    def __init__(self, master=None, switchFrameWithMenuName=None, **kwargs):
        super().__init__(master, **kwargs)
        self.is_loading_finished = False

        self.play_loading_effect_animation()

        self.init_monitor_specification()

        self.battle_field_background_shape_list = None

        self.current_fixed_details_card = None

        self.your_field_panel = None
        self.opponent_field_panel = None

        self.opponent_details_panel_rectangle = None
        self.your_hand_details_panel_rectangle = None

        self.active_panel_rectangle = None
        self.active_panel_attack_button = None
        self.active_panel_first_skill_button = None
        self.active_panel_second_skill_button = None
        self.active_panel_third_skill_button = None
        self.selected_object = None
        self.opponent_selected_object = None
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

        # self.mulligan_repository = MuligunYourHandRepository()

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
        self.opponent_field_area_inside_handler = OpponentFieldAreaInsideHandler.getInstance()
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

        self.your_hp = None
        self.opponent_hp = None

        self.your_hp_panel = None
        self.your_hp_repository = YourHpRepository.getInstance()

        self.opponent_hp_panel = None
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

        self.your_main_character_panel = None
        self.your_main_character = YourMainCharacter()

        self.round_repository = RoundRepository.getInstance()

        self.turn_end = TurnEnd()
        self.turn_end_button = None
        self.turn_end_button_selected = False

        self.current_field_turn_number_panel = None
        self.turn_number = CurrentFieldTurnNumber()

        self.current_field_message_on_the_battle_screen_panel = None
        self.message_on_the_screen = MessageOnTheBattleScreen()

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

        self.timer_panel = None
        self.timer = None
        self.timer_repository = BattleFieldTimerRepository.getInstance()
        self.unit_timer = None

        self.animation_test_image_panel = None
        self.animation_test_image = AnimationTestImage()
        self.animation_test_image_list = []
        self.animation_test_image_panel_list = []

        self.skill_focus_background_panel = None
        self.skill_focus_panel = None

        self.effect_animation_panel = None
        self.effect_animation = EffectAnimation()
        self.effect_animation_repository = EffectAnimationRepository.getInstance()
        self.effect_animation_list = []
        self.effect_animation_panel_list = []
        self.is_effect_animation_playing = False

        self.battle_field_repository = BattleFieldRepository.getInstance()
        self.battle_result = BattleResult()
        self.battle_result_panel_list = []

        self.game_end_sound_call = False

        self.notice_card = FixedFieldCard(local_translation=(self.width / 2 - 150, self.height / 2 - (150 * 1.618)))


        self.bind("<Configure>", self.on_resize)
        self.bind("<B1-Motion>", self.on_canvas_drag)
        self.bind("<ButtonRelease-1>", self.on_canvas_release)
        self.bind("<Button-1>", self.on_canvas_left_click)
        self.bind("<Button-3>", self.on_canvas_right_click)

        # TODO: 이 부분은 임시 방편입니다 (상대방 행동 했다 가정하고 키보드 입력 받기 위함)
        self.bind("<Key>", self.on_key_press)

        self.is_loading_finished = True

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

        self.attack_animation_object.set_total_window_size(self.width, self.height)

        self.pre_drawed_image_instance.pre_draw_full_screen_nether_blade_skill(width, height)
        self.pre_drawed_image_instance.pre_draw_full_screen_sea_of_wraith(width, height)
        self.pre_drawed_image_instance.pre_draw_full_screen_nether_blade_targeting_skill(width, height)

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
        # TODO: Fake 용으로 뒷면을 그리기 위해 살려둠
        self.opponent_hand_repository.save_current_opponent_hand_state([-1, -1, -1, -1, -1])
        self.opponent_hand_repository.create_opponent_hand_card_list()
        self.opponent_hand_card_list = self.opponent_hand_repository.get_current_opponent_hand_card_list()

        # self.your_hand_repository.set_x_base(550)
        self.your_hand_repository.set_total_window_size(self.width, self.height)
        # self.your_hand_card_state = self.mulligan_repository.get_current_hand_state()
        # self.your_hand_repository.save_current_hand_state(self.your_hand_card_state)
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

        self.window_size_repository.set_is_it_re_entrance(True)
        self.window_size_repository.set_total_window_size(self.width, self.height)
        self.window_size_repository.set_master_opengl_frame(self)

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

        self.message_on_the_screen.set_total_window_size(self.width, self.height)
        self.current_field_message_on_the_battle_screen_panel = (
            self.message_on_the_screen.get_current_message_on_the_battle_screen()
        )


        self.your_active_panel = YourActivePanel()
        self.your_active_panel.set_total_window_size(self.width, self.height)

        self.opponent_details_panel = OpponentDetailsPanel()
        self.opponent_details_panel.set_total_window_size(self.width, self.height)

        self.your_hand_details_panel = YourHandDetailsPanel()
        self.your_hand_details_panel.set_total_window_size(self.width, self.height)

        self.opponent_active_panel = OpponentActivePanel()
        self.opponent_active_panel.set_total_window_size(self.width, self.height)

        self.your_hp = YourHp()
        self.opponent_hp = OpponentHp()

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

        self.your_main_character.set_total_window_size(self.width, self.height)
        self.your_main_character.create_your_main_character_panel()
        self.your_main_character_panel = self.your_main_character.get_your_main_character_panel()

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

        self.turn_number.set_total_window_size(self.width, self.height)
        self.turn_number.create_current_field_turn_number_panel()
        self.current_field_turn_number_panel = (
            self.turn_number.get_current_field_turn_number_panel()
        )

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

        self.timer = BattleFieldTimer()
        self.unit_timer = BattleFieldTimer()

        self.timer.set_total_window_size(self.width, self.height)
        self.timer.draw_current_timer_panel()
        self.timer_panel = self.timer.get_timer_panel()

        self.start_first_turn()

        skill_focus_panel_instance = SkillFocusPanel()
        skill_focus_panel_instance.set_total_window_size(self.width, self.height)
        skill_focus_panel_instance.create_skill_background_panel()
        skill_focus_panel_instance.create_skill_focus_panel()
        self.skill_focus_background_panel = skill_focus_panel_instance.get_skill_background_panel()
        self.skill_focus_panel = skill_focus_panel_instance.get_skill_focus_panel()

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
        if key == "Alt_L":
            # ALT_L이 눌렸을 때는 아무 작업도 하지 않음
            # 탭 전환
            return
        
        print(f"Key pressed: {key}")
        print(f"Key pressed lower(): {key.lower()}")
        print(f"Key pressed type: {type(key)}")


        if key.lower() == 'kp_add':
            opponent_hand_list = self.__fake_opponent_hand_repository.get_fake_opponent_hand_list()
            for opponent_hand_index, opponent_hand in enumerate(opponent_hand_list):
                if opponent_hand == 36:
                    print("죽음의 대지 사용!! ")

                    result = self.__fake_opponent_hand_repository.request_use_energy_card_to_unit(
                        RequestUseFieldOfDeath(
                            _sessionInfo=self.__session_repository.get_second_fake_session_info(),
                            _itemCardId=36
                        )
                    )

                    print(f"fake death scythe result: {result}")
                    is_success_value = result.get('is_success', False)

                    if is_success_value == False:
                        return

                    self.__fake_opponent_hand_repository.remove_card_by_index(opponent_hand_index)

                    break


        # if key.lower() == 'w':
        #     opponent_hand_list = self.__fake_opponent_hand_repository.get_fake_opponent_hand_list()
        #     your_field_unit_list = self.your_field_unit_repository.get_current_field_unit_list()
        #     first_non_none_index = (
        #         next((index for index, item in enumerate(your_field_unit_list) if item is not None), None))
        #     for opponent_hand_index, opponent_hand in enumerate(opponent_hand_list):
        #         if opponent_hand == 9:
        #             print("상대방 에너지번 사용!! ")
        #
        #             result = self.__fake_opponent_hand_repository.request_use_energy_card_to_unit(
        #                 RequestUseDeathSiceToUnit(
        #                     _sessionInfo=self.__session_repository.get_second_fake_session_info(),
        #                     _itemCardId=9,
        #                     _opponentTargetUnitIndex=first_non_none_index
        #                 ))
        #
        #             print(f"fake death scythe result: {result}")
        #             is_success_value = result.get('is_success', False)
        #
        #             if is_success_value == False:
        #                 return
        #
        #             self.__fake_opponent_hand_repository.remove_card_by_index(opponent_hand_index)
        #
        #             break

        # if key.lower() == 'w':
        #     opponent_hand_list = self.__fake_opponent_hand_repository.get_fake_opponent_hand_list()
        #     for opponent_hand_index, opponent_hand in enumerate(opponent_hand_list):
        #         if opponent_hand == 9:
        #             print("에너지번 사용!! ")
        # 
        #             result = self.__fake_opponent_hand_repository.request_use_energy_card_to_unit(
        #                 RequestUseDeathSiceToUnit(
        #                     _sessionInfo=self.__session_repository.get_second_fake_session_info(),
        #                     _itemCardId=8,
        #                     _opponentTargetUnitIndex=0
        #                 ))
        # 
        #             print(f"fake death scythe result: {result}")
        #             is_success_value = result.get('is_success', False)
        # 
        #             if is_success_value == False:
        #                 return
        # 
        #             self.__fake_opponent_hand_repository.remove_card_by_index(opponent_hand_index)
        # 
        #             return
        # 
        #     return


        if key.lower() == 'kp_prior':
            opponent_hand_list = self.__fake_opponent_hand_repository.get_fake_opponent_hand_list()
            for opponent_hand_index, opponent_hand in enumerate(opponent_hand_list):
                if opponent_hand == 35:
                    print("상대방 사기 전환 사용!!")
                    opponent_field_list = self.opponent_field_unit_repository.get_current_field_unit_card_object_list()
                    for opponent_field_unit_index, opponent_field_unit in enumerate(opponent_field_list):
                        if opponent_field_unit == None:
                            continue

                        result = self.__fake_opponent_hand_repository.request_use_energy_card_to_unit(
                            RequestUseAddFieldEnergyBySacrificingFieldUnitSupportCard(
                                _sessionInfo=self.__session_repository.get_second_fake_session_info(),
                                _itemCardId = 35,
                                _unitIndex=opponent_field_unit_index
                            )
                        )

                        print(f"fake death scythe result: {result}")
                        is_success_value = result.get('is_success', False)

                        if is_success_value == False:
                            return

                        self.__fake_opponent_hand_repository.remove_card_by_index(opponent_hand_index)

                        break

                    break

        if key.lower() == 's':
            opponent_hand_list = self.__fake_opponent_hand_repository.get_fake_opponent_hand_list()
            your_field_unit_list = self.your_field_unit_repository.get_current_field_unit_list()
            first_non_none_index = (
                next((index for index, item in enumerate(your_field_unit_list) if item is not None), None))
            # your_field_unit = self.your_field_unit_repository.find_field_unit_by_index(first_non_none_index)
            # self.attack_animation_object.set_your_field_unit(your_field_unit)
            for opponent_hand_index, opponent_hand in enumerate(opponent_hand_list):
                if opponent_hand == 8:
                    print("상대방이 내 필드 첫 번째 생존 유닛에 죽음의 낫 사용!!")

                    result = self.__fake_opponent_hand_repository.request_use_energy_card_to_unit(
                        RequestUseDeathSiceToUnit(
                            _sessionInfo=self.__session_repository.get_second_fake_session_info(),
                            _itemCardId=8,
                            _opponentTargetUnitIndex=first_non_none_index
                            ))

                    print(f"fake death scythe result: {result}")
                    is_success_value = result.get('is_success', False)

                    if is_success_value == False:
                        return

                    self.__fake_opponent_hand_repository.remove_card_by_index(opponent_hand_index)

                    return

            return

        # if key.lower() == 'kp_0':
        #     opponent_field_unit_list = self.opponent_field_unit_repository.get_current_field_unit_card_object_list()
        #     for opponent_unit_index, opponent_unit in enumerate(opponent_field_unit_list):
        #         if opponent_unit == None:
        #             continue
        #
        #         if opponent_unit.get_card_number() == 27:
        #             self.your_field_energy_repository.request_to_attach_energy_to_unit(
        #                 RequestAttachFieldEnergyToUnit(
        #                     _sessionInfo=self.__session_repository.get_second_fake_session_info(),
        #                     _unitIndex=opponent_unit.get_index(),
        #                     _energyRace=CardRace.UNDEAD,
        #                     _energyCount=2
        #                 )
        #             )
        #
        #             response = self.__fake_battle_field_frame_repository.request_attack_main_character_with_active_skill(
        #                 RequestAttackMainCharacterWithActiveSkill(
        #                     _sessionInfo=self.__session_repository.get_second_fake_session_info(),
        #                     _unitCardIndex=opponent_unit.get_index(),
        #                     _targetGameMainCharacterIndex="0"
        #                 )
        #             )
        #
        #             print("test dark ball : ", response)
        #             return

        # if key.lower() == 'kp_decimal':
        if key.lower() == 'period':
            your_field_unit_list = self.your_field_unit_repository.get_current_field_unit_list()
            first_non_none_index = next((index for index, item in enumerate(your_field_unit_list) if item is not None), None)
            your_field_unit = self.your_field_unit_repository.find_field_unit_by_index(first_non_none_index)
            self.attack_animation_object.set_your_field_unit(your_field_unit)

            opponent_field_unit_list = self.opponent_field_unit_repository.get_current_field_unit_card_object_list()
            for opponent_unit_index, opponent_unit in enumerate(opponent_field_unit_list):
                if opponent_unit == None:
                    continue

                if opponent_unit.get_card_number() == 27:

                    # self.your_field_energy_repository.request_to_attach_energy_to_unit(
                    #     RequestAttachFieldEnergyToUnit(
                    #         _sessionInfo=self.__session_repository.get_second_fake_session_info(),
                    #         _unitIndex=opponent_unit.get_index(),
                    #         _energyRace=CardRace.UNDEAD,
                    #         _energyCount=2
                    #     )
                    # )

                    response = self.__fake_battle_field_frame_repository.request_attack_your_unit_with_active_skill(
                        RequestAttackToYourFieldUnitWithActiveSkill(
                            _sessionInfo=self.__session_repository.get_second_fake_session_info(),
                            _unitCardIndex=opponent_unit.get_index(),
                            _opponentTargetCardIndex=your_field_unit.get_index(),
                        )
                    )

                    print("test 쉐도우 볼 to unit: ", response)
                    return


        if key.lower() == 'equal':
            opponent_field_unit_list = self.opponent_field_unit_repository.get_current_field_unit_card_object_list()
            for opponent_unit_index, opponent_unit in enumerate(opponent_field_unit_list):
                if opponent_unit == None:
                    continue

                if opponent_unit.get_card_number() == 27:
                    # self.your_field_energy_repository.request_to_attach_energy_to_unit(
                    #     RequestAttachFieldEnergyToUnit(
                    #         _sessionInfo=self.__session_repository.get_second_fake_session_info(),
                    #         _unitIndex=opponent_unit.get_index(),
                    #         _energyRace=CardRace.UNDEAD,
                    #         _energyCount=3
                    #     )
                    # )

                    response = self.__fake_battle_field_frame_repository.request_attack_with_non_targeting_active_skill(
                        RequestAttackWithNonTargetingActiveSkill(
                            _sessionInfo=self.__session_repository.get_second_fake_session_info(),
                            _unitCardIndex=opponent_unit.get_index()
                        )
                    )

                    print("test 망령의 바다: ", response)
                    return

        if key.lower() == 'comma':
            opponent_field_unit_list = self.opponent_field_unit_repository.get_current_field_unit_card_object_list()
            for opponent_unit_index, opponent_unit in enumerate(opponent_field_unit_list):
                if opponent_unit == None:
                    continue

                if opponent_unit.get_card_number() == 27:
                    response = self.__fake_battle_field_frame_repository.request_attack_main_character_with_active_skill(
                        RequestAttackMainCharacterWithActiveSkill(
                            _sessionInfo=self.__session_repository.get_second_fake_session_info(),
                            _unitCardIndex=opponent_unit.get_index(),
                            _targetGameMainCharacterIndex="0"
                        )
                    )
                    
                    print("Opponent 쉐도우 볼 to 메인 캐릭터: ", response)
                    return


        if key.lower() == 'slash':
            # RequestAttackWithNonTargetingActiveSkill(protocolNumber=1002, unitCardIndex=3, usageSkillIndex=2, sessionInfo)
            # 수신된 정보: {"NOTIFY_NON_TARGETING_ACTIVE_SKILL": {"player_field_unit_attack_map": {"Opponent": {
            #     "field_unit_attack_map": {
            #         "3": {"target_player_index": "You", "target_unit_index": -1, "active_skill_index": 2,
            #               "passive_skill_index": -1}}}}, "player_field_unit_health_point_map": {"You": {
            #     "field_unit_health_point_map": {"9": 0, "8": 0, "4": 0, "2": 0, "10": 5, "0": 25, "3": 0, "7": 0}}},
            #                                            "player_field_unit_harmful_effect_map": {"You": {
            #                                                "field_unit_harmful_status_map": {
            #                                                    "7": {"harmful_status_list": []},
            #                                                    "9": {"harmful_status_list": []},
            #                                                    "3": {"harmful_status_list": []},
            #                                                    "2": {"harmful_status_list": []},
            #                                                    "0": {"harmful_status_list": []},
            #                                                    "8": {"harmful_status_list": []},
            #                                                    "10": {"harmful_status_list": []},
            #                                                    "4": {"harmful_status_list": []}}}},
            #                                            "player_field_unit_death_map": {
            #                                                "You": {"dead_field_unit_index_list": [2, 3, 4, 7, 8, 9]}}}}

            opponent_field_unit_list = self.opponent_field_unit_repository.get_current_field_unit_card_object_list()
            for opponent_unit_index, opponent_unit in enumerate(opponent_field_unit_list):
                if opponent_unit == None:
                    continue

                if opponent_unit.get_card_number() == 27:
                    response = self.__fake_battle_field_frame_repository.request_attack_opponent_unit(
                        RequestAttackWithNonTargetingActiveSkill(
                            _sessionInfo=self.__session_repository.get_second_fake_session_info(),
                            _unitCardIndex=opponent_unit_index
                        )
                    )

                    print("Opponent 망령의 바다: ", response)
                    return

        if key.lower() == 'kp_home':
            print("구울 및 스켈레톤 소환.")

            opponent_hand_list = self.__fake_opponent_hand_repository.get_fake_opponent_hand_list()
            for opponent_hand_index, opponent_hand in enumerate(opponent_hand_list):
                if opponent_hand == 31 or opponent_hand == 32 :
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

        if key.lower() == 'z':
            print("만약 Opponent Hand에 출격시킬 유닛이 있다면 내보낸다.")

            opponent_hand_list = self.__fake_opponent_hand_repository.get_fake_opponent_hand_list()
            for opponent_hand_index, opponent_hand in enumerate(opponent_hand_list):
                opponent_hand_card_type = self.card_info_repository.getCardTypeForCardNumber(opponent_hand)
                if opponent_hand_card_type == CardType.UNIT.value and opponent_hand != 19:
                    print("네더를 제외한 상대방 유닛 출격")

                    result = self.__fake_opponent_hand_repository.request_deploy_fake_opponent_unit(
                        FakeOpponentDeployUnitRequest(
                            self.__session_repository.get_second_fake_session_info(),
                            opponent_hand))

                    print(f"fake opponent deploy unit result: {result}")
                    is_success_value = result.get('is_success', False)

                    if is_success_value == False:
                        return

                    self.__fake_opponent_hand_repository.remove_card_by_index(opponent_hand_index)

                    return

            return

        if key.lower() == 'n':
            print("만약 Opponent Hand에 네더가 있다면 내보낸다.")

            opponent_hand_list = self.__fake_opponent_hand_repository.get_fake_opponent_hand_list()
            for opponent_hand_index, opponent_hand in enumerate(opponent_hand_list):
                opponent_hand_card_type = self.card_info_repository.getCardTypeForCardNumber(opponent_hand)
                if opponent_hand_card_type == CardType.UNIT.value and opponent_hand == 19:
                    print("네더를 제외한 상대방 유닛 출격")

                    result = self.__fake_opponent_hand_repository.request_deploy_fake_opponent_unit(
                        FakeOpponentDeployUnitRequest(
                            self.__session_repository.get_second_fake_session_info(),
                            opponent_hand))

                    print(f"fake opponent deploy unit result: {result}")
                    is_success_value = result.get('is_success', False)

                    if is_success_value == False:
                        return

                    self.__fake_opponent_hand_repository.remove_card_by_index(opponent_hand_index)

                    return

            return

        if key.lower() == 'r':
            print("상대방이 네더 출격 이후 광역기 사용 요청")

            recently_added_card_index = self.opponent_field_unit_repository.get_field_unit_max_index()

            opponent_animation_actor = self.opponent_field_unit_repository.find_opponent_field_unit_by_index(recently_added_card_index)
            self.attack_animation_object.set_opponent_animation_actor(opponent_animation_actor)
            # self.__opponent_field_area_inside_handler.set_field_area_action(OpponentFieldAreaActionProcess.PLAY_ANIMATION)
            # self.__opponent_field_area_inside_handler.set_field_area_action(OpponentFieldAreaActionProcess.REQUIRED_FIRST_PASSIVE_SKILL_PROCESS)

            damage = self.card_info_repository.getCardPassiveFirstDamageForCardNumber(opponent_animation_actor.get_card_number())
            self.attack_animation_object.set_opponent_animation_actor_damage(damage)

            self.opponent_field_area_inside_handler.set_unit_action(OpponentUnitAction.NETHER_BLADE_FIRST_WIDE_AREA_PASSIVE_SKILL)

            extra_ability = self.opponent_field_unit_repository.get_opponent_unit_extra_ability_at_index(recently_added_card_index)
            self.attack_animation_object.set_extra_ability(extra_ability)

            self.opponent_field_area_inside_handler.set_active_field_area_action(OpponentFieldAreaActionProcess.PLAY_ANIMATION)

            process_first_passive_skill_response = self.__fake_battle_field_frame_repository.request_to_process_first_passive_skill(
                WideAreaPassiveSkillFromDeployRequest(
                    _sessionInfo=self.__session_repository.get_second_fake_session_info(),
                    _unitCardIndex=str(recently_added_card_index),
                    _usageSkillIndex="1"))

            is_success = process_first_passive_skill_response['is_success']
            if is_success is False:
                return FieldAreaAction.Dummy

            return

        if key.lower() == 'y':
            print("상대방이 네더 출격 이후 본체 타겟팅 사용 요청")

            # your_field_card_id = self.targeting_enemy_select_using_your_field_card_id
            # print(f"your_field_card_id: {your_field_card_id}")
            #
            # your_damage = self.card_info_repository.getCardPassiveSecondDamageForCardNumber(your_field_card_id)
            # print(f"your_damage: {your_damage}")
            #
            # self.attack_animation_object.set_animation_actor_damage(your_damage)
            # self.attack_animation_object.set_opponent_main_character(self.opponent_main_character_panel)
            # # self.opponent_hp_repository.take_damage(your_damage)
            #
            # self.opponent_fixed_unit_card_inside_handler.set_action_to_apply_opponent(ActionToApplyOpponent.Dummy)
            # self.targeting_enemy_select_using_your_field_card_index = None
            # self.targeting_enemy_select_using_your_field_card_id = None
            # self.targeting_enemy_select_support_lightning_border_list = []
            # self.opponent_you_selected_lightning_border_list = []
            #
            # self.selected_object = None
            # self.active_panel_rectangle = None
            # self.current_fixed_details_card = None
            # self.your_active_panel.clear_all_your_active_panel()
            #
            # self.master.after(0, self.start_nether_blade_second_passive_targeting_motion_animation)

            recently_added_card_index = self.opponent_field_unit_repository.get_field_unit_max_index()
            opponent_animation_actor = self.opponent_field_unit_repository.find_opponent_field_unit_by_index(recently_added_card_index)
            self.attack_animation_object.set_opponent_animation_actor(opponent_animation_actor)

            damage = self.card_info_repository.getCardPassiveSecondDamageForCardNumber(opponent_animation_actor.get_card_number())
            self.attack_animation_object.set_opponent_animation_actor_damage(damage)

            self.opponent_field_area_inside_handler.set_unit_action(OpponentUnitAction.NETHER_BLADE_SECOND_TARGETING_PASSIVE_SKILL)

            extra_ability = self.opponent_field_unit_repository.get_opponent_unit_extra_ability_at_index(recently_added_card_index)
            self.attack_animation_object.set_extra_ability(extra_ability)

            self.opponent_field_area_inside_handler.set_active_field_area_action(OpponentFieldAreaActionProcess.PLAY_ANIMATION)

            # {"protocolNumber":2001, "unitCardIndex": "0", "targetGameMainCharacterIndex": "0", "usageSkillIndex": "2", "sessionInfo":""}
            process_second_passive_skill_response = self.__fake_battle_field_frame_repository.request_to_process_second_passive_skill_to_main_character(
                TargetingPassiveSkillToMainCharacterFromDeployRequest(
                    _sessionInfo=self.__session_repository.get_second_fake_session_info(),
                    _unitCardIndex=str(recently_added_card_index),
                    _targetGameMainCharacterIndex="0",
                    _usageSkillIndex="2"))

            print(f"{Fore.RED}opponent process_second_passive_skill_response:{Fore.GREEN} {process_second_passive_skill_response}{Style.RESET_ALL}")

            is_success = process_second_passive_skill_response['is_success']
            if is_success is False:
                return FieldAreaAction.Dummy

            return

        if key.lower() == 't':
            print("상대방이 네더 출격 이후 Your 유닛에 타겟팅 사용 요청")

            recently_added_card_index = self.opponent_field_unit_repository.get_field_unit_max_index()
            opponent_animation_actor = self.opponent_field_unit_repository.find_opponent_field_unit_by_index(
                recently_added_card_index)
            self.attack_animation_object.set_opponent_animation_actor(opponent_animation_actor)

            damage = self.card_info_repository.getCardPassiveSecondDamageForCardNumber(
                opponent_animation_actor.get_card_number())
            self.attack_animation_object.set_opponent_animation_actor_damage(damage)

            self.opponent_field_area_inside_handler.set_unit_action(
                OpponentUnitAction.NETHER_BLADE_SECOND_TARGETING_PASSIVE_SKILL)

            extra_ability = self.opponent_field_unit_repository.get_opponent_unit_extra_ability_at_index(
                recently_added_card_index)
            self.attack_animation_object.set_extra_ability(extra_ability)

            self.opponent_field_area_inside_handler.set_active_field_area_action(
                OpponentFieldAreaActionProcess.PLAY_ANIMATION)

            your_field_unit_list = self.your_field_unit_repository.get_current_field_unit_list()
            # first_non_none_value = next((item for item in your_field_unit_list if item is not None), None)
            first_non_none_index = next((index for index, item in enumerate(your_field_unit_list) if item is not None), None)
            your_field_unit = self.your_field_unit_repository.find_field_unit_by_index(first_non_none_index)
            self.attack_animation_object.set_your_field_unit(your_field_unit)

            print(f"{Fore.RED}first_non_none_value:{Fore.GREEN} {first_non_none_index}{Style.RESET_ALL}")

            # {"protocolNumber":2000, "unitCardIndex": "0", "opponentTargetCardIndex": "0", "usageSkillIndex": "2", "sessionInfo":""}
            process_second_passive_skill_response = self.__fake_battle_field_frame_repository.request_to_process_second_passive_skill_to_your_field_unit(
                TargetingPassiveSkillToYourFieldUnitFromDeployRequest(
                    _sessionInfo=self.__session_repository.get_second_fake_session_info(),
                    _unitCardIndex=str(recently_added_card_index),
                    _opponentTargetCardIndex=str(first_non_none_index),
                    _usageSkillIndex="2"))

            print(f"{Fore.RED}opponent process_second_passive_skill_response:{Fore.GREEN} {process_second_passive_skill_response}{Style.RESET_ALL}")

            is_success = process_second_passive_skill_response['is_success']
            if is_success is False:
                return FieldAreaAction.Dummy

            return

        if key.lower() == 'f':
            print(f"{Fore.RED}상대방 네더 블레이드 매 턴 시작 시 광역기 발동!{Style.RESET_ALL}")

            need_to_process_opponent_unit_map = self.opponent_field_area_inside_handler.get_required_to_process_opponent_passive_skill_multiple_unit_map()
            print(f"{Fore.RED}need_to_process_opponent_unit_map: {Fore.GREEN}{need_to_process_opponent_unit_map}{Style.RESET_ALL}")

            if len(need_to_process_opponent_unit_map) == 0:
                self.opponent_field_area_inside_handler.set_field_turn_start_action(TurnStartAction.Dummy)
                return

            passive_opponent_unit_index = None
            skill_indexes = []

            for key, value in need_to_process_opponent_unit_map.items():
                if 1 in value:
                    passive_opponent_unit_index = key
                    value.remove(1)
                    skill_indexes = value
                    break

            if passive_opponent_unit_index is not None:
                # skill_indexes가 비어 있는지 확인하고, 비어 있으면 해당 유닛 인덱스 제거
                if not skill_indexes:
                    del need_to_process_opponent_unit_map[passive_opponent_unit_index]
                else:
                    need_to_process_opponent_unit_map[passive_opponent_unit_index] = skill_indexes

            self.opponent_field_area_inside_handler.set_field_turn_start_action(TurnStartAction.Dummy)

            opponent_field_unit = self.opponent_field_unit_repository.find_opponent_field_unit_by_index(int(passive_opponent_unit_index))
            self.opponent_field_area_inside_handler.set_field_area_action(OpponentFieldAreaActionProcess.REQUIRED_FIRST_PASSIVE_SKILL_PROCESS)
            self.attack_animation_object.set_opponent_animation_actor(opponent_field_unit)

            #### add
            damage = self.card_info_repository.getCardPassiveFirstDamageForCardNumber(opponent_field_unit.get_card_number())
            self.attack_animation_object.set_opponent_animation_actor_damage(damage)

            self.opponent_field_area_inside_handler.set_unit_action(OpponentUnitAction.NETHER_BLADE_FIRST_WIDE_AREA_PASSIVE_SKILL)

            extra_ability = self.opponent_field_unit_repository.get_opponent_unit_extra_ability_at_index(passive_opponent_unit_index)
            self.attack_animation_object.set_extra_ability(extra_ability)

            self.opponent_field_area_inside_handler.set_active_field_area_action(
                OpponentFieldAreaActionProcess.PLAY_ANIMATION)

            #### add finish

            # {"protocolNumber":2012, "unitCardIndex": "0", "usageSkillIndex": "1", "sessionInfo":""}
            turn_start_first_passive_skill_response = self.__fake_battle_field_frame_repository.request_to_process_turn_start_first_passive_skill_to_your_field_unit(
                TurnStartFirstPassiveSkillRequest(
                    _sessionInfo=self.__session_repository.get_second_fake_session_info(),
                    _unitCardIndex=str(passive_opponent_unit_index),
                    _usageSkillIndex="1"))

            print(f"{Fore.RED}opponent turn_start_first_passive_skill_response:{Fore.GREEN} {turn_start_first_passive_skill_response}{Style.RESET_ALL}")
            return

        if key.lower() == 'h':
            print(f"{Fore.RED}상대방 네더 블레이드 매 턴 시작 시 타겟팅으로 본체 때리기!{Style.RESET_ALL}")

            need_to_process_opponent_unit_map = self.opponent_field_area_inside_handler.get_required_to_process_opponent_passive_skill_multiple_unit_map()
            print(f"{Fore.RED}need_to_process_opponent_unit_map: {Fore.GREEN}{need_to_process_opponent_unit_map}{Style.RESET_ALL}")

            need_to_process_opponent_unit_map = self.opponent_field_area_inside_handler.get_required_to_process_opponent_passive_skill_multiple_unit_map()
            print(
                f"{Fore.RED}need_to_process_opponent_unit_map: {Fore.GREEN}{need_to_process_opponent_unit_map}{Style.RESET_ALL}")

            if len(need_to_process_opponent_unit_map) == 0:
                self.opponent_field_area_inside_handler.set_field_turn_start_action(TurnStartAction.Dummy)
                return

            passive_opponent_unit_index = None
            skill_indexes = []

            for key, value in need_to_process_opponent_unit_map.items():
                if 2 in value:
                    passive_opponent_unit_index = key
                    value.remove(2)
                    skill_indexes = value
                    break

            if passive_opponent_unit_index is not None:
                # skill_indexes가 비어 있는지 확인하고, 비어 있으면 해당 유닛 인덱스 제거
                if not skill_indexes:
                    del need_to_process_opponent_unit_map[passive_opponent_unit_index]
                else:
                    need_to_process_opponent_unit_map[passive_opponent_unit_index] = skill_indexes

            self.opponent_field_area_inside_handler.set_field_turn_start_action(TurnStartAction.Dummy)

            opponent_field_unit_index = int(passive_opponent_unit_index)
            opponent_field_unit = self.opponent_field_unit_repository.find_opponent_field_unit_by_index(opponent_field_unit_index)
            self.opponent_field_area_inside_handler.set_unit_action(
                OpponentUnitAction.NETHER_BLADE_SECOND_TARGETING_PASSIVE_SKILL)
            self.attack_animation_object.set_opponent_animation_actor(opponent_field_unit)

            #### add
            damage = self.card_info_repository.getCardPassiveSecondDamageForCardNumber(opponent_field_unit.get_card_number())
            self.attack_animation_object.set_opponent_animation_actor_damage(damage)

            self.opponent_field_area_inside_handler.set_unit_action(
                OpponentUnitAction.NETHER_BLADE_SECOND_TARGETING_PASSIVE_SKILL)

            extra_ability = self.opponent_field_unit_repository.get_opponent_unit_extra_ability_at_index(opponent_field_unit_index)
            self.attack_animation_object.set_extra_ability(extra_ability)

            self.opponent_field_area_inside_handler.set_active_field_area_action(
                OpponentFieldAreaActionProcess.PLAY_ANIMATION)

            # {"protocolNumber":2011, "unitCardIndex": "0", "targetGameMainCharacterIndex": "0", "usageSkillIndex": "2", "sessionInfo":""}
            turn_start_second_passive_skill_to_main_character_response = self.__fake_battle_field_frame_repository.request_to_process_turn_start_second_passive_skill_to_main_character(
                TurnStartSecondPassiveSkillToMainCharacterRequest(
                    _sessionInfo=self.__session_repository.get_second_fake_session_info(),
                    _unitCardIndex=str(opponent_field_unit_index),
                    _targetGameMainCharacterIndex="0",
                    _usageSkillIndex="2"))

            print(f"{Fore.RED}opponent turn_start_second_passive_skill_to_main_character_response:{Fore.GREEN} {turn_start_second_passive_skill_to_main_character_response}{Style.RESET_ALL}")
            return

        if key.lower() == 'g':
            print(f"{Fore.RED}상대방 네더 블레이드 매 턴 시작 시 타겟팅으로 유닛 때리기!{Style.RESET_ALL}")

            # passive_usage_card_index = self.opponent_field_unit_repository.get_field_unit_max_index()
            # opponent_animation_actor = self.opponent_field_unit_repository.find_opponent_field_unit_by_index(passive_usage_card_index)
            # self.attack_animation_object.set_opponent_animation_actor(opponent_animation_actor)

            need_to_process_opponent_unit_map = self.opponent_field_area_inside_handler.get_required_to_process_opponent_passive_skill_multiple_unit_map()
            print(f"{Fore.RED}need_to_process_opponent_unit_map: {Fore.GREEN}{need_to_process_opponent_unit_map}{Style.RESET_ALL}")

            if len(need_to_process_opponent_unit_map) == 0:
                self.opponent_field_area_inside_handler.set_field_turn_start_action(TurnStartAction.Dummy)
                return

            passive_opponent_unit_index = None
            skill_indexes = []

            for key, value in need_to_process_opponent_unit_map.items():
                if 2 in value:
                    passive_opponent_unit_index = key
                    value.remove(2)
                    skill_indexes = value
                    break

            if passive_opponent_unit_index is not None:
                # skill_indexes가 비어 있는지 확인하고, 비어 있으면 해당 유닛 인덱스 제거
                if not skill_indexes:
                    del need_to_process_opponent_unit_map[passive_opponent_unit_index]
                else:
                    need_to_process_opponent_unit_map[passive_opponent_unit_index] = skill_indexes

            self.opponent_field_area_inside_handler.set_field_turn_start_action(TurnStartAction.Dummy)

            opponent_field_unit = self.opponent_field_unit_repository.find_opponent_field_unit_by_index(int(passive_opponent_unit_index))
            self.opponent_field_area_inside_handler.set_unit_action(OpponentUnitAction.NETHER_BLADE_SECOND_TARGETING_PASSIVE_SKILL)
            self.attack_animation_object.set_opponent_animation_actor(opponent_field_unit)

            # opponent_animation_actor = self.attack_animation_object.get_opponent_animation_actor()
            # opponent_animation_actor_index = opponent_animation_actor.get_index()

            damage = self.card_info_repository.getCardPassiveSecondDamageForCardNumber(opponent_field_unit.get_card_number())
            self.attack_animation_object.set_opponent_animation_actor_damage(damage)

            self.opponent_field_area_inside_handler.set_unit_action(
                OpponentUnitAction.NETHER_BLADE_SECOND_TARGETING_PASSIVE_SKILL)

            extra_ability = self.opponent_field_unit_repository.get_opponent_unit_extra_ability_at_index(passive_opponent_unit_index)
            self.attack_animation_object.set_extra_ability(extra_ability)

            self.opponent_field_area_inside_handler.set_active_field_area_action(
                OpponentFieldAreaActionProcess.PLAY_ANIMATION)

            your_field_unit_list = self.your_field_unit_repository.get_current_field_unit_list()
            first_non_none_index = next((index for index, item in enumerate(your_field_unit_list) if item is not None), None)
            your_field_unit = self.your_field_unit_repository.find_field_unit_by_index(first_non_none_index)
            self.attack_animation_object.set_your_field_unit(your_field_unit)

            print(f"{Fore.RED}first_non_none_value:{Fore.GREEN} {first_non_none_index}{Style.RESET_ALL}")

            # {"protocolNumber":2010, "unitCardIndex": "0", "opponentTargetCardIndex": "0", "usageSkillIndex": "2", "sessionInfo":""}
            turn_start_second_passive_skill_to_main_character_response = self.__fake_battle_field_frame_repository.request_to_process_turn_start_second_passive_skill_to_your_field_unit(
                TurnStartSecondPassiveSkillToYourFieldUnitRequest(
                    _sessionInfo=self.__session_repository.get_second_fake_session_info(),
                    _unitCardIndex=str(passive_opponent_unit_index),
                    _opponentTargetCardIndex=str(first_non_none_index),
                    _usageSkillIndex="2"))

            print(f"{Fore.RED}opponent turn_start_second_passive_skill_to_main_character_response:{Fore.GREEN} {turn_start_second_passive_skill_to_main_character_response}{Style.RESET_ALL}")
            return

        if key.lower() == 'x':
            print("Opponent Turn을 종료합니다")

            turn_end_request_result = self.round_repository.request_turn_end(
                TurnEndRequest(
                    self.__session_repository.get_second_fake_session_info()))
            print(f"turn_end_request_result: {turn_end_request_result}")

            if turn_end_request_result.get('player_main_character_survival_map', {}).get('Opponent', None) == 'Death':
                print(f"{Fore.RED}Fake Opponent win!{Style.RESET_ALL}")
                # self.your_hp_repository.your_character_die()
                # self.battle_field_repository.lose()
                self.timer.stop_timer()
                return

            self.__notify_reader_repository.set_is_your_turn_for_check_fake_process(True)

            self.timer.stop_timer()
            self.timer_repository.set_timer(60)
            self.timer_repository.set_function(self.call_turn_end)
            self.timer.get_timer()
            self.timer.start_timer()

            self.your_deck_repository.draw_deck()
            self.your_deck_repository.update_deck(self.your_deck_repository.get_current_deck_state())
            self.message_on_the_screen.create_message_on_the_battle_screen(MessageNumber.YOUR_TURN.value)
            self.reset_every_selected_action()

            return


        # ` (숫자 1 옆에 있는 것)
        if key.lower() == 'grave':
            print(f"{Fore.RED}상대방 20장 뽑기{Style.RESET_ALL}")

            multi_draw_response = self.__fake_battle_field_frame_repository.request_fake_multi_draw(
                FakeMultiDrawRequest(self.__session_repository.get_second_fake_session_info()))

            print(f"{Fore.RED}opponent multi_draw_response:{Fore.GREEN} {multi_draw_response}{Style.RESET_ALL}")
            opponent_multi_draw_hand_list = multi_draw_response['player_multi_drawn_card_list']['You']

            self.__fake_opponent_hand_repository.save_fake_opponent_hand_list(opponent_multi_draw_hand_list)
            print(f"{Fore.RED}current opponent_multi_draw_hand_list:{Fore.GREEN} {self.__fake_opponent_hand_repository.get_fake_opponent_hand_list()}{Style.RESET_ALL}")

            return

        if key.lower() == 'kp_1':

            if self.animation_test_image_panel:
                self.animation_test_image_panel = None

            self.animation_test_image.set_total_window_size(self.width, self.height)
            self.animation_test_image.change_local_translation(
                self.opponent_field_unit_repository.find_opponent_field_unit_by_index(0).get_local_translation()
            )
            self.animation_test_image.draw_animation_panel()
            self.animation_test_image_panel = self.animation_test_image.get_animation_panel()
            print("created animation panel")

        if key.lower() == 'kp_2':
            if self.animation_test_image_panel:
                self.animation_test_image_panel = None

            self.animation_test_image.set_total_window_size(self.width, self.height)
            self.animation_test_image.change_local_translation(
                self.opponent_field_unit_repository.find_opponent_field_unit_by_index(1).get_local_translation()
            )
            self.animation_test_image.draw_animation_panel()
            self.animation_test_image_panel = self.animation_test_image.get_animation_panel()
            print("created animation panel")

        if key.lower() == 'kp_3':
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

        if key.lower() == 'kp_end':
            self.effect_animation_panel = None
            effect_animation = EffectAnimation()
            effect_animation.set_animation_name('sword_attack')
            effect_animation.set_total_window_size(self.width, self.height)
            effect_animation.change_local_translation(
                self.opponent_field_unit_repository.find_opponent_field_unit_by_index(0).get_local_translation()
            )
            effect_animation.draw_animation_panel()
            effect_animation_panel = effect_animation.get_animation_panel()

            self.effect_animation_list.append(effect_animation)
            self.effect_animation_panel_list.append(effect_animation_panel)

        if key.lower() == 'kp_down':
            self.effect_animation_panel = None
            effect_animation = EffectAnimation()
            effect_animation.set_animation_name('magic_attack')
            effect_animation.set_total_window_size(self.width, self.height)
            effect_animation.change_local_translation(
                self.opponent_field_unit_repository.find_opponent_field_unit_by_index(1).get_local_translation()
            )
            effect_animation.draw_animation_panel()
            effect_animation_panel = effect_animation.get_animation_panel()

            self.effect_animation_list.append(effect_animation)
            self.effect_animation_panel_list.append(effect_animation_panel)

        if key.lower() == 'kp_next':
            self.effect_animation_panel = None
            effect_animation = EffectAnimation()
            effect_animation.set_animation_name('dark_blast')
            effect_animation.set_total_window_size(self.width, self.height)
            effect_animation.change_local_translation(
                self.opponent_field_unit_repository.find_opponent_field_unit_by_index(2).get_local_translation()
            )
            effect_animation.draw_animation_panel()
            effect_animation_panel = effect_animation.get_animation_panel()

            self.effect_animation_list.append(effect_animation)
            self.effect_animation_panel_list.append(effect_animation_panel)

        if key.lower() == 'kp_left':
            self.effect_animation_panel = None
            effect_animation = EffectAnimation()
            effect_animation.set_animation_name('death_scythe')
            effect_animation.set_total_window_size(self.width, self.height)
            effect_animation.change_local_translation(
                self.opponent_field_unit_repository.find_opponent_field_unit_by_index(3).get_local_translation()
            )
            effect_animation.draw_animation_panel()
            effect_animation_panel = effect_animation.get_animation_panel()

            self.effect_animation_list.append(effect_animation)
            self.effect_animation_panel_list.append(effect_animation_panel)

        if key.lower() == 'kp_begin':
            self.effect_animation_panel = None
            effect_animation = EffectAnimation()
            effect_animation.set_animation_name('burst_shadow_ball')
            effect_animation.set_total_window_size(self.width, self.height)
            effect_animation.change_local_translation(
                self.opponent_field_unit_repository.find_opponent_field_unit_by_index(4).get_local_translation()
            )
            effect_animation.draw_animation_panel()
            effect_animation_panel = effect_animation.get_animation_panel()

            self.effect_animation_list.append(effect_animation)
            self.effect_animation_panel_list.append(effect_animation_panel)

        if key.lower() == 'kp_right':
            self.effect_animation_panel = None
            effect_animation = EffectAnimation()
            effect_animation.set_animation_name('moving_shadow_ball')
            effect_animation.set_total_window_size(self.width, self.height)
            effect_animation.change_local_translation(
                self.opponent_field_unit_repository.find_opponent_field_unit_by_index(5).get_local_translation()
            )
            effect_animation.draw_animation_panel()
            effect_animation_panel = effect_animation.get_animation_panel()

            self.effect_animation_list.append(effect_animation)
            self.effect_animation_panel_list.append(effect_animation_panel)

        if key.lower() == 'kp_insert':
            if self.is_effect_animation_playing:
                return
            def animate():
                self.is_effect_animation_playing = True
                finish_list = []
                is_all_finished = False
                for effect_animation in self.effect_animation_list:
                    effect_animation.update_effect_animation_panel()
                    finish_list.append(effect_animation.is_finished)

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
                    self.is_effect_animation_playing = False
                    print("finish animation")


            for effect_animation in self.effect_animation_list:
                print(f"animation count: {effect_animation}")
                effect_animation.reset_animation_count()

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

        if key.lower() == '2':
            opponent_hand_list = self.__fake_opponent_hand_repository.get_fake_opponent_hand_list()
            for opponent_hand_index, opponent_hand in enumerate(opponent_hand_list):
                if opponent_hand == 20:
                    print('상대 망자의 늪 사용')

                    response = self.__fake_opponent_hand_repository.request_use_draw_support(
                        DrawCardByUseSupportCardRequest(
                            _sessionInfo=self.__session_repository.get_second_fake_session_info(),
                            _cardId="20")
                    )

                    if not response.get('is_success'):
                        return

                    opponent_drawn_card_list = response.get('player_drawn_card_list_map', {}).get('You', [])
                    self.__fake_opponent_hand_repository.save_fake_opponent_hand_list(opponent_drawn_card_list)
                    fake_opponent_hand_list = self.__fake_opponent_hand_repository.get_fake_opponent_hand_list()
                    print(
                        f"{Fore.RED}fake opponent hand list after support card use:{Fore.GREEN} {fake_opponent_hand_list}{Style.RESET_ALL}")

                    self.__fake_opponent_hand_repository.remove_card_by_index(opponent_hand_index)

                    return



        if key.lower() == '3':
            print("밸른 필드 에너지 부착")
            opponent_field_unit_list = self.opponent_field_unit_repository.get_current_field_unit_card_object_list()
            opponent_field_energy_count = self.opponent_field_energy_repository.get_opponent_field_energy()
            if opponent_field_energy_count > 3:
                opponent_field_energy_count = 3
            for opponent_unit_index, opponent_unit in enumerate(opponent_field_unit_list):
                if opponent_unit == None:
                    continue

                if opponent_unit.get_card_number() == 27:
                    response = self.your_field_energy_repository.request_to_attach_energy_to_unit(
                        RequestAttachFieldEnergyToUnit(
                            _sessionInfo=self.__session_repository.get_second_fake_session_info(),
                            _unitIndex=opponent_unit.get_index(),
                            _energyRace=CardRace.UNDEAD,
                            _energyCount=opponent_field_energy_count
                        )
                    )



                    return

        if key == '4':
            opponent_hand_list = self.__fake_opponent_hand_repository.get_fake_opponent_hand_list()
            opponent_field_unit_list = self.opponent_field_unit_repository.get_current_field_unit_card_object_list()
            first_non_none_index = (
                next((index for index, item in enumerate(opponent_field_unit_list) if item is not None), None))
            print(f"opponent hand list : {opponent_hand_list}")
            for opponent_hand_index, opponent_hand in enumerate(opponent_hand_list):
                opponent_hand_card_type = self.card_info_repository.getCardTypeForCardNumber(opponent_hand)
                if opponent_hand_card_type == CardType.ENERGY.value:
                    print("상대방 에너지 카드 부착 ")

                    response = self.__fake_opponent_hand_repository.request_use_energy_card_to_unit(
                        RequestUseEnergyCardToUnit(
                            _sessionInfo=self.__session_repository.get_second_fake_session_info(),
                            _unitIndex=first_non_none_index,
                            _energyCardId=93)
                    )
                    print(f"{Fore.RED}fake_opponent_attach_energy -> response:{Fore.GREEN} {response}{Style.RESET_ALL}")
                    is_success_value = response.get('is_success', False)

                    if is_success_value == False:
                        return

                    self.__fake_opponent_hand_repository.remove_card_by_index(opponent_hand_index)

                    return

        if key.lower() == '5':
            your_field_unit_list = self.your_field_unit_repository.get_current_field_unit_list()
            first_non_none_index = next((index for index, item in enumerate(your_field_unit_list) if item is not None), None)
            your_field_unit = self.your_field_unit_repository.find_field_unit_by_index(first_non_none_index)
            self.attack_animation_object.set_your_field_unit(your_field_unit)

            opponent_hand_list = self.__fake_opponent_hand_repository.get_fake_opponent_hand_list()
            print(f"opponent hand list : {opponent_hand_list}")
            for opponent_hand_index, opponent_hand in enumerate(opponent_hand_list):
                if opponent_hand == 9:
                    print("상대방 에너지번 사용~ ")

                    response = self.your_hand_repository.request_use_energy_burn_to_unit(
                        RequestUseEnergyBurnToUnit(
                            _sessionInfo=self.__session_repository.get_second_fake_session_info(),
                            _itemCardId=9,
                            _opponentTargetUnitIndex=first_non_none_index
                        )

                    )
                    print(f"use energy card response: {response}")
                    is_success_value = response.get('is_success', False)

                    if is_success_value == False:
                        return

                    self.__fake_opponent_hand_repository.remove_card_by_index(opponent_hand_index)

                    break

        if key.lower() == '6':
            opponent_hand_list = self.__fake_opponent_hand_repository.get_fake_opponent_hand_list()
            your_field_unit_list = self.your_field_unit_repository.get_current_field_unit_list()

            # first_non_none_index = (
            #     next((index for index, item in enumerate(your_field_unit_list) if item is not None), None))
            # second_non_none_index = first_non_none_index
            #
            # if first_non_none_index is not None:
            your_field_unit_index_list = []
            for index, item in enumerate(your_field_unit_list):
                if item is not None:
                    your_field_unit_index_list.append(index)
                if len(your_field_unit_index_list) == 2:
                    break

            if len(your_field_unit_index_list) == 1:
                first_non_none_index = your_field_unit_index_list[0]
                your_field_unit_index_list.append(first_non_none_index)

            print(f"opponent hand list : {opponent_hand_list}")
            for opponent_hand_index, opponent_hand in enumerate(opponent_hand_list):
                if opponent_hand == 33:
                    opponent_field_unit_list = self.opponent_field_unit_repository.get_current_field_unit_card_object_list()
                    for opponent_unit_index, opponent_unit in enumerate(opponent_field_unit_list):
                        if opponent_unit == None:
                            continue
                        opponent_field_unit_id = opponent_unit.get_card_number()
                        if opponent_field_unit_id == 31 or opponent_field_unit_id == 32:

                            print("상대방 시폭 사용~ ")

                            response = self.your_hand_repository.request_use_corpse_explosion(
                                RequestUseCorpseExplosion(
                                    _sessionInfo=self.__session_repository.get_second_fake_session_info(),
                                    _itemCardId = 33,
                                    _opponentTargetUnitIndexList = [str(your_field_unit_index_list[0]), str(your_field_unit_index_list[1])],
                                    _unitIndex = str(opponent_unit_index)
                                )
                            )
                            print(f"use corpse explosion response: {response}")
                            is_success_value = response.get('is_success', False)

                            if is_success_value == False:
                                continue

                            self.__fake_opponent_hand_repository.remove_card_by_index(opponent_hand_index)

                            break


                        print('희생 불가능한 유닛')

                    break

        if key.lower() == '7':
            print('에너지를 부착하지 않은 Opponent 유닛에 필드 에너지 1개 부착')

            opponent_field_unit_list = self.opponent_field_unit_repository.get_current_field_unit_card_object_list()
            for opponent_unit_index, opponent_unit in enumerate(opponent_field_unit_list):
                if opponent_unit == None:
                    continue

                total_energy = self.opponent_field_unit_repository.get_total_energy_at_index(opponent_unit_index)
                print(f"total_energy: {total_energy}")

                if total_energy > 0:
                    continue

                self.__fake_battle_field_frame_repository.request_to_attach_energy_to_unit(
                    RequestAttachFieldEnergyToUnit(
                        _sessionInfo=self.__session_repository.get_second_fake_session_info(),
                        _unitIndex=opponent_unit_index,
                        _energyRace=CardRace.UNDEAD,
                        _energyCount=1
                    )
                )

                return

        if key.lower() == '8':
            opponent_hand_list = self.__fake_opponent_hand_repository.get_fake_opponent_hand_list()
            opponent_field_unit_list = self.opponent_field_unit_repository.get_current_field_unit_card_object_list()
            first_non_none_index = (
                next((index for index, item in enumerate(opponent_field_unit_list) if item is not None), None))
            print(f"opponent hand list : {opponent_hand_list}")
            for opponent_hand_index, opponent_hand in enumerate(opponent_hand_list):
                if opponent_hand == 2:
                    print("상대방 넘쳐흐르는 사기 사용!! ")

                    response = self.your_hand_repository.request_use_overflow_of_energy(
                        RequestUseOverflowOfEnergy(
                            _sessionInfo=self.__session_repository.get_second_fake_session_info(),
                            _unitIndex=first_non_none_index,
                            _supportCardId="2")
                    )

                    is_success_value = response.get('is_success', False)

                    if is_success_value == False:
                        # self.selected_object = None
                        self.reset_every_selected_action()
                        return

        if key.lower() == 'kp_7':
            opponent_hand_list = self.__fake_opponent_hand_repository.get_fake_opponent_hand_list()
            opponent_field_unit_list = self.opponent_field_unit_repository.get_current_field_unit_card_object_list()
            first_non_none_index = (
                next((index for index, item in enumerate(opponent_field_unit_list) if item is not None), None))
            print(f"opponent hand list : {opponent_hand_list}")
            for opponent_hand_index, opponent_hand in enumerate(opponent_hand_list):

                if opponent_hand == 151:
                    print("상대방 특수 에너지 부착 ")

                    response = self.__fake_opponent_hand_repository.request_use_energy_card_to_unit(
                        RequestUseSpecialEnergyCardToUnit(
                            _sessionInfo=self.__session_repository.get_second_fake_session_info(),
                            _unitIndex=first_non_none_index,
                            _energyCardId=opponent_hand)
                    )
                    print(f"{Fore.RED}fake_opponent_attach_energy -> response:{Fore.GREEN} {response}{Style.RESET_ALL}")
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

        # if key.lower() == 'a':
        #     self.opponent_field_unit_repository.create_field_unit_card(26)
        #     self.opponent_field_unit_repository.replace_opponent_field_unit_card_position()
        #
        # if key.lower() == 'q':
        #     self.opponent_field_unit_repository.create_field_unit_card(31)
        #     self.opponent_field_unit_repository.replace_opponent_field_unit_card_position()

        # if key.lower() == 'n':
        #     self.opponent_field_unit_repository.create_field_unit_card(19)
        #     self.opponent_field_unit_repository.replace_opponent_field_unit_card_position()

        # if key.lower() == 'b':
        #     self.your_field_unit_repository.create_field_unit_card(19)
        #     self.your_field_unit_repository.replace_field_card_position()
        #
        #     first_passive_skill_type = self.card_info_repository.getCardPassiveFirstForCardNumber(19)
        #     if first_passive_skill_type == 1:
        #         print("단일기")
        #     elif first_passive_skill_type == 2:
        #         print("광역기")
        #
        #         damage = self.card_info_repository.getCardPassiveFirstDamageForCardNumber(19)
        #         print(f"wide area damage: {damage}")
        #
        #         for index in range(
        #                 len(self.opponent_field_unit_repository.get_current_field_unit_card_object_list()) - 1,
        #                 -1,
        #                 -1):
        #             opponent_field_unit = \
        #                 self.opponent_field_unit_repository.get_current_field_unit_card_object_list()[index]
        #
        #             if opponent_field_unit is None:
        #                 continue
        #
        #             remove_from_field = False
        #
        #             fixed_card_base = opponent_field_unit.get_fixed_card_base()
        #             attached_shape_list = fixed_card_base.get_attached_shapes()
        #
        #             for attached_shape in attached_shape_list:
        #                 if isinstance(attached_shape, NonBackgroundNumberImage):
        #                     if attached_shape.get_circle_kinds() is CircleKinds.HP:
        #
        #                         hp_number = attached_shape.get_number()
        #                         hp_number -= damage
        #
        #                         if hp_number <= 0:
        #                             remove_from_field = True
        #                             break
        #
        #                         print(f"contract_of_doom -> hp_number: {hp_number}")
        #                         attached_shape.set_number(hp_number)
        #
        #                         # attached_shape.set_image_data(
        #                         #     self.pre_drawed_image_instance.get_pre_draw_number_image(hp_number))
        #
        #                         attached_shape.set_image_data(
        #                             self.pre_drawed_image_instance.get_pre_draw_unit_hp(hp_number))
        #
        #             if remove_from_field:
        #                 card_id = opponent_field_unit.get_card_number()
        #
        #                 effect_animation = EffectAnimation()
        #                 effect_animation.set_animation_name('death')
        #                 effect_animation.set_total_window_size(self.width, self.height)
        #                 effect_animation.change_local_translation(self.opponent_field_unit_repository.find_opponent_field_unit_by_index(
        #                     index).get_fixed_card_base().get_local_translation())
        #                 effect_animation.draw_animation_panel()
        #                 effect_animation_panel = effect_animation.get_animation_panel()
        #
        #                 animation_index = self.effect_animation_repository.save_effect_animation_at_dictionary_without_index_and_return_index(
        #                     effect_animation)
        #
        #                 self.effect_animation_repository.save_effect_animation_panel_at_dictionary_with_index(
        #                     animation_index, effect_animation_panel)
        #
        #                 def remove_opponent_unit(_index):
        #
        #                     self.opponent_field_unit_repository.remove_current_field_unit_card(_index)
        #                     self.opponent_tomb_repository.create_opponent_tomb_card(card_id)
        #                     self.opponent_field_unit_repository.replace_opponent_field_unit_card_position()
        #                     self.opponent_field_unit_repository.remove_harmful_status_by_index(_index)
        #
        #                 self.play_effect_animation_by_index_and_call_function_with_param(
        #                     animation_index, remove_opponent_unit, index)
        #
        #     second_passive_skill_type = self.card_info_repository.getCardPassiveSecondForCardNumber(19)
        #     if second_passive_skill_type == 1:
        #         print("단일기")
        #
        #         # TODO: 여기서 본체 공격 할 수 있어야 함
        #         self.targeting_enemy_select_support_lightning_border_list.append(self.opponent_main_character_panel)
        #
        #         opponent_field_unit_object_list = self.opponent_field_unit_repository.get_current_field_unit_card_object_list()
        #         valid_opponent_field_units_object_list = [unit for unit in opponent_field_unit_object_list if
        #                                                   unit is not None]
        #         print(f"실제 유효한 상대 필드 유닛 숫자: {len(valid_opponent_field_units_object_list)}")
        #
        #         # if len(valid_opponent_field_units_object_list) == 0:
        #         #     return
        #
        #         for opponent_field_unit_object in opponent_field_unit_object_list:
        #             if opponent_field_unit_object is None:
        #                 continue
        #
        #             fixed_opponent_card_base = opponent_field_unit_object.get_fixed_card_base()
        #             self.targeting_enemy_select_support_lightning_border_list.append(fixed_opponent_card_base)
        #
        #         self.targeting_enemy_select_support_lightning_border_list.append(self.opponent_main_character_panel)
        #
        #         self.opponent_fixed_unit_card_inside_handler.set_opponent_field_area_action(
        #             OpponentFieldAreaAction.PASSIVE_SKILL_TARGETING_ENEMY)
        #
        #         your_field_unit_id = 19
        #
        #         self.targeting_enemy_select_using_your_field_card_id = your_field_unit_id
        #     elif second_passive_skill_type == 2:
        #         print("광역기")

        # if key.lower() == 't':
        #     self.round_repository.increase_current_round_number()

        # if key.lower() == 'e':
        #     # result = {
        #     #     "hand_use_card_id": 93, "field_unit_index": 0,
        #     #     "attach_energy_race_type": 2,
        #     #     "attach_race_energy_count": 1,
        #     #     "attach_total_energy_count": 1
        #     # }
        #     # self.attach_energy(result)
        #     # return
        #     print("attach undead energy")
        #
        #     # TODO: Change it to ENUM Value (Not just integer)
        #     card_race = self.card_info_repository.getCardRaceForCardNumber(93)
        #     print(f"card_race: {card_race}")
        #
        #     attach_energy_count = 1
        #     opponent_unit_index = 0
        #
        #     self.opponent_field_unit_repository.attach_race_energy(opponent_unit_index, EnergyType.Undead, attach_energy_count)
        #     opponent_field_unit = self.opponent_field_unit_repository.find_opponent_field_unit_by_index(0)
        #
        #     opponent_field_unit_attached_undead_energy_count = self.opponent_field_unit_repository.get_opponent_field_unit_race_energy(0, EnergyType.Undead)
        #     print(f"opponent_field_unit_attached_undead_energy_count: {opponent_field_unit_attached_undead_energy_count}")
        #
        #     before_attach_energy_count = self.opponent_field_unit_repository.get_opponent_field_unit_race_energy(
        #         0, EnergyType.Undead)
        #
        #     self.opponent_field_unit_repository.attach_race_energy(
        #         opponent_unit_index,
        #         EnergyType.Undead,
        #         attach_energy_count)
        #     opponent_field_unit = self.opponent_field_unit_repository.find_opponent_field_unit_by_index(0)
        #
        #     after_attach_energy_count = self.opponent_field_unit_repository.get_opponent_field_unit_race_energy(
        #         0, EnergyType.Undead)
        #     total_attached_energy_count = self.opponent_field_unit_repository.get_total_energy_at_index(0)
        #     print(
        #         f"opponent_field_unit_attached_undead_energy_count: {total_attached_energy_count}")
        #
        #     opponent_fixed_card_base = opponent_field_unit.get_fixed_card_base()
        #     opponent_fixed_card_attached_shape_list = opponent_fixed_card_base.get_attached_shapes()
        #
        #     for opponent_fixed_card_attached_shape in opponent_fixed_card_attached_shape_list:
        #         if isinstance(opponent_fixed_card_attached_shape, NonBackgroundNumberImage):
        #             if opponent_fixed_card_attached_shape.get_circle_kinds() is CircleKinds.ENERGY:
        #                 # opponent_fixed_card_attached_shape.set_image_data(
        #                 #     self.pre_drawed_image_instance.get_pre_draw_number_image(
        #                 #         total_attached_energy_count))
        #
        #                 opponent_fixed_card_attached_shape.set_image_data(
        #                     self.pre_drawed_image_instance.get_pre_draw_unit_energy(
        #                         total_attached_energy_count))
        #
        #                 print(f"changed energy: {opponent_fixed_card_attached_shape.get_circle_kinds()}")

            # after_attach_energy_count
            # before_attach_energy_count

            # every_energy = self.opponent_field_unit_repository.get_energy_info_at_index(0)
            # print(f"every_energy: {every_energy}")
            #
            # if card_race == CardRace.UNDEAD.value:
            #     card_race_circle = opponent_field_unit.creat_fixed_card_energy_race_circle(
            #         color=(0, 0, 0, 1),
            #         vertices=(0, (total_attached_energy_count * 10) + 20),
            #         local_translation=opponent_fixed_card_base.get_local_translation())
            #     opponent_fixed_card_base.set_attached_shapes(card_race_circle)



        if key.lower() == 'd':
            print("상대방 메인 캐릭터 일반 공격")

            opponent_field_unit_list = self.opponent_field_unit_repository.get_current_field_unit_card_object_list()
            print(f"opponent_field_unit_list : {opponent_field_unit_list}")
            for opponent_field_index, opponent_unit in enumerate(opponent_field_unit_list):
                if opponent_unit == None:
                    continue

                total_energy = self.opponent_field_unit_repository.get_total_energy_at_index(opponent_field_index)
                print(total_energy)
                race_energy = self.opponent_field_unit_repository.get_energy_info_at_index(opponent_field_index)
                print(race_energy)

                if total_energy >= 1:
                    response = self.__fake_battle_field_frame_repository.request_attack_main_character(
                        RequestAttackMainCharacter(
                            _sessionInfo=self.__session_repository.get_second_fake_session_info(),
                            _attacker_unit_index=opponent_field_index,
                            _target_game_main_character_index="0")
                    )
                    print(f"{Fore.RED}attack main character -> response:{Fore.GREEN} {response}{Style.RESET_ALL}")
                    is_success_value = response.get('is_success', False)

                    if is_success_value == False:
                        continue

                    return

            return

        if key.lower() == 'o':
            your_field_unit_list = self.your_field_unit_repository.get_current_field_unit_list()
            first_non_none_index = (
                next((index for index, item in enumerate(your_field_unit_list) if item is not None), None))
            # your_field_unit = self.your_field_unit_repository.find_field_unit_by_index(first_non_none_index)
            # self.attack_animation_object.set_your_field_unit(your_field_unit)

            opponent_field_unit_list = self.opponent_field_unit_repository.get_current_field_unit_card_object_list()
            print(f"opponent_field_unit_list : {opponent_field_unit_list}")
            for opponent_field_index, opponent_unit in enumerate(opponent_field_unit_list):
                if opponent_unit is None:
                    continue

                total_energy = self.opponent_field_unit_repository.get_total_energy_at_index(opponent_field_index)
                required_energy = self.card_info_repository.getCardEnergyForCardNumber(opponent_unit.get_card_number())
                print(total_energy)
                # race_energy = self.opponent_field_unit_repository.get_energy_info_at_index(opponent_field_index)
                # print(race_energy)

                if total_energy >= int(required_energy):
                    print("상대방 평타공격 to unit~ ")

                    response = self.__fake_battle_field_frame_repository.request_attack_opponent_unit(
                        RequestAttackOpponentUnit(
                            _sessionInfo=self.__session_repository.get_second_fake_session_info(),
                            _attackerUnitIndex=opponent_field_index,
                            _targetUnitIndex=first_non_none_index
                        )
                    )

                    print(f"{Fore.RED}attack main character -> response:{Fore.GREEN} {response}{Style.RESET_ALL}")
                    is_success_value = response.get('is_success', False)

                    if is_success_value == False:
                        continue

                    return

        if key.lower() == 'c':
            print("파멸의 계약 사용!")

            response = self.__fake_battle_field_frame_repository.request_use_contract_of_doom(
                RequestUseContractOfDoom(
                    _sessionInfo=self.__session_repository.get_second_fake_session_info(),
                    _itemCardId="25"
                )
            )
            print(f"{Fore.RED}파멸의 계약 -> response:{Fore.GREEN} {response}{Style.RESET_ALL}")
            is_success_value = response.get('is_success', False)

            if is_success_value == False:
                return
            
            return





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

        self.your_main_character.set_width_ratio(self.width_ratio)
        self.your_main_character.set_height_ratio(self.height_ratio)
        self.your_main_character_panel.set_width_ratio(self.width_ratio)
        self.your_main_character_panel.set_height_ratio(self.height_ratio)
        self.your_main_character_panel.set_draw_border(False)
        self.your_main_character_panel.draw()

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




        self.option.set_width_ratio(self.width_ratio)
        self.option.set_height_ratio(self.height_ratio)
        self.option_button.set_draw_border(False)
        self.option_button.draw()
        if self.option_button_selected:
            for option_popup_panel in self.option_popup_panel_list:
                option_popup_panel.draw()

        self.surrender_confirm.set_width_ratio(self.width_ratio)
        self.surrender_confirm.set_height_ratio(self.height_ratio)


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

        self.turn_number.set_width_ratio(self.width_ratio)
        self.turn_number.set_height_ratio(self.height_ratio)
        self.turn_number.update_current_field_turn_number_panel()
        self.current_field_turn_number_panel.set_width_ratio(self.width_ratio)
        self.current_field_turn_number_panel.set_height_ratio(self.height_ratio)
        self.current_field_turn_number_panel.draw()

        self.timer.set_width_ratio(self.width_ratio)
        self.timer.set_height_ratio(self.height_ratio)
        self.timer.update_current_timer_panel()
        self.timer_panel.set_width_ratio(self.width_ratio)
        self.timer_panel.set_height_ratio(self.height_ratio)
        self.timer_panel.draw()

        self.your_hp.set_width_ratio(self.width_ratio)
        self.your_hp.set_height_ratio(self.height_ratio)
        self.your_hp.update_current_your_hp_panel()
        self.your_hp.check_you_are_survival()
        self.your_hp_panel.set_width_ratio(self.width_ratio)
        self.your_hp_panel.set_height_ratio(self.height_ratio)
        self.your_hp_panel.draw()
       
        self.muligun_reset_button.set_width_ratio(self.width_ratio)
        self.muligun_reset_button.set_height_ratio(self.height_ratio)
        self.muligun_reset_button.draw()

        self.multi_draw_button.set_width_ratio(self.width_ratio)
        self.multi_draw_button.set_height_ratio(self.height_ratio)
        self.multi_draw_button.draw()

       

        self.opponent_hp.set_width_ratio(self.width_ratio)
        self.opponent_hp.set_height_ratio(self.height_ratio)
        self.opponent_hp.update_current_opponent_hp_panel()
        self.opponent_hp.check_opponent_is_survival()
        self.opponent_hp_panel.set_width_ratio(self.width_ratio)
        self.opponent_hp_panel.set_height_ratio(self.height_ratio)
        self.opponent_hp_panel.draw()

        # if self.message_on_the_screen.get_current_message_on_the_battle_screen():
        #     self.message_on_the_screen.set_width_ratio(self.width_ratio)
        #     self.message_on_the_screen.set_height_ratio(self.height_ratio)
        #     self.current_field_message_on_the_battle_screen_panel = (
        #         self.message_on_the_screen.get_current_message_on_the_battle_screen()
        #     )
        #     self.current_field_message_on_the_battle_screen_panel.draw()

        # if self.skill_focus_background_panel:
        #     glEnable(GL_BLEND)
        #     glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        #     # glBlendFunc(GL_ONE_MINUS_SRC_ALPHA, GL_SRC_ALPHA)
        #
        #     self.skill_focus_background_panel.draw()
        #     # self.skill_focus_panel.draw()
        #
        #     glDisable(GL_BLEND)

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

        if self.effect_animation_list is not [] and self.effect_animation_panel_list is not []:
            for effect_animation, effect_animation_panel in zip(self.effect_animation_list,
                                                                        self.effect_animation_panel_list):
                if effect_animation.is_finished:
                    continue
                effect_animation.set_width_ratio(self.width_ratio)
                effect_animation.set_height_ratio(self.height_ratio)
                effect_animation_panel.draw()

        if self.effect_animation_repository.get_effect_animation_list() is not [] and self.effect_animation_repository.get_effect_animation_panel_list() is not []:
            for effect_animation, effect_animation_panel in zip(self.effect_animation_repository.get_effect_animation_list(),
                                                                self.effect_animation_repository.get_effect_animation_panel_list()):
                if effect_animation.is_finished:
                    continue
                effect_animation.set_width_ratio(self.width_ratio)
                effect_animation.set_height_ratio(self.height_ratio)
                effect_animation_panel.draw()




        # if self.skill_focus_background_panel:
        #     glEnable(GL_BLEND)
        #     # glBlendFunc(GL_DST_ALPHA, GL_ONE_MINUS_DST_ALPHA)
        #     # glBlendFunc(GL_ONE_MINUS_SRC_ALPHA, GL_SRC_ALPHA)
        #     glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        #
        #     self.skill_focus_background_panel.draw()
        #     # self.skill_focus_panel.draw()
        #
        #     glDisable(GL_BLEND)

        if self.battle_field_repository.get_is_game_end():
            self.battle_finish()


        if len(self.__notify_reader_repository.get_notify_effect_animation_request_list()) != 0:
            for _ in range(0,len(self.__notify_reader_repository.get_notify_effect_animation_request_list())):
                effect_animation_request = self.__notify_reader_repository.get_notify_effect_animation_request_list().pop()
                print(f"effect animation request : {effect_animation_request}")
                effect_animation = effect_animation_request.get_effect_animation()
                effect_animation.set_total_window_size(self.width, self.height)


                if effect_animation_request.get_target_type() == TargetType.AREA:
                    vertices = []
                    if effect_animation_request.get_target_player() == 'You':
                        field_vertices = self.your_field_panel.get_vertices()
                        main_character_vertices = self.your_main_character_panel.get_vertices()
                        #  vertices = [field_vertices[1], field_vertices[2], field_vertices[3], field_vertices[0]]
                        vertices = [field_vertices[1], field_vertices[2],
                                    (field_vertices[3][0], main_character_vertices[2][1]),
                                    (field_vertices[0][0], main_character_vertices[3][1])]
                    elif effect_animation_request.get_target_player() == 'Opponent':
                        field_vertices = self.opponent_field_panel.get_vertices()
                        main_character_vertices = self.opponent_main_character_panel.get_vertices()

                        vertices = [(field_vertices[0][0], main_character_vertices[0][1]),
                                    (field_vertices[2][0], main_character_vertices[1][1]),
                                    field_vertices[3], field_vertices[0]]
                    else:
                        print('unknown target player!!')

                    effect_animation.draw_animation_panel_with_vertices(vertices)
                    effect_animation_panel = effect_animation.get_animation_panel()
                    animation_index = self.effect_animation_repository.save_effect_animation_at_dictionary_without_index_and_return_index(
                        effect_animation)
                    self.effect_animation_repository.save_effect_animation_panel_at_dictionary_with_index(
                        animation_index, effect_animation_panel)


                    if effect_animation_request.get_function_need_param():
                        print('파라미터가 필요한 광역기 실행중')
                        self.play_effect_animation_by_index_and_call_function_with_param(
                            animation_index, effect_animation_request.get_call_function(), effect_animation_request.get_param(),effect_animation_request.get_need_delay())
                    else:
                        print('광역 공격 실행중')
                        self.play_effect_animation_by_index_and_call_function(animation_index,
                                                                              effect_animation_request.get_call_function())

                elif effect_animation_request.get_target_type() == TargetType.UNIT:
                    effect_animation.draw_animation_panel()
                    print(effect_animation_request.get_target_index())

                    effect_animation_panel = effect_animation.get_animation_panel()
                    animation_index = self.effect_animation_repository.save_effect_animation_at_dictionary_without_index_and_return_index(
                        effect_animation)
                    self.effect_animation_repository.save_effect_animation_panel_at_dictionary_with_index(
                        animation_index, effect_animation_panel)

                    if effect_animation_request.get_function_need_param():
                        self.play_effect_animation_by_index_and_call_function_with_param(animation_index, effect_animation_request.get_call_function(
                            ),effect_animation_request.get_param(),effect_animation_request.get_need_delay())
                    else:
                        self.play_effect_animation_by_index_and_call_function(animation_index,
                                                                              effect_animation_request.get_call_function())
                    # self.play_effect_animation_by_index_and_call_function(animation_index,
                    #                                                            effect_animation_request.get_call_function())

           # self.play_effect_animation()

        # glDisable(GL_BLEND)

    def redraw(self):
        if self.is_reshape_not_complete:
            return


        # print("나",self.field_area_inside_handler.get_field_area_action())
        # print("상대",self.opponent_field_area_inside_handler.get_field_area_action())

        self.tkMakeCurrent()
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        glDisable(GL_DEPTH_TEST)

        self.draw_base()

        if self.opponent_field_area_inside_handler.get_field_area_action() is OpponentFieldAreaActionProcess.NEED_TO_FINISH_GAME:
            print(f"{Fore.RED}게임이 종료되었습니다!{Style.RESET_ALL}")
            self.timer.stop_timer()

            self.opponent_field_area_inside_handler.set_field_area_action(OpponentFieldAreaActionProcess.Dummy)

        # if self.opponent_field_area_inside_handler.get_active_field_area_action() is not OpponentFieldAreaActionProcess.PLAY_ANIMATION:
        #     opponent_animation_actor = self.attack_animation_object.get_opponent_animation_actor()
        #     if opponent_animation_actor:
        #         opponent_animation_actor_index = opponent_animation_actor.get_index()
        #     else:
        #         opponent_animation_actor_index = -1
        #
        #     for index, opponent_field_unit in enumerate(
        #             self.opponent_field_unit_repository.get_current_field_unit_card_object_list()):
        #         if opponent_field_unit is None:
        #             continue
        #
        #         if opponent_animation_actor_index == index:
        #             continue
        #
        #         attached_tool_card = opponent_field_unit.get_tool_card()
        #         if attached_tool_card is not None:
        #             attached_tool_card.set_width_ratio(self.width_ratio)
        #             attached_tool_card.set_height_ratio(self.height_ratio)
        #             attached_tool_card.draw()
        #
        #         fixed_card_base = opponent_field_unit.get_fixed_card_base()
        #         fixed_card_base.set_width_ratio(self.width_ratio)
        #         fixed_card_base.set_height_ratio(self.height_ratio)
        #         fixed_card_base.draw()
        #
        #         attached_shape_list = fixed_card_base.get_attached_shapes()
        #
        #         for attached_shape in attached_shape_list:
        #             attached_shape.set_width_ratio(self.width_ratio)
        #             attached_shape.set_height_ratio(self.height_ratio)
        #             attached_shape.draw()

        opponent_animation_actor = self.attack_animation_object.get_opponent_animation_actor()
        if opponent_animation_actor:
            opponent_animation_actor_index = opponent_animation_actor.get_index()
        else:
            opponent_animation_actor_index = -1

        for index, opponent_field_unit in enumerate(
                self.opponent_field_unit_repository.get_current_field_unit_card_object_list()):
            if opponent_field_unit is None:
                continue

            if opponent_animation_actor_index == index:
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

            if self.opponent_field_unit_repository.get_is_index_in_harmful_status(index) == True:
                if 'Freeze' in self.opponent_field_unit_repository.get_harmful_status_by_index(index):
                    fixed_card_effect_animation = opponent_field_unit.get_fixed_card_freeze_effect_animation()
                    if fixed_card_effect_animation is not None:

                        fixed_card_effect_animation.set_total_window_size(self.width, self.height)
                        fixed_card_effect_animation.set_width_ratio(self.width_ratio)
                        fixed_card_effect_animation.set_height_ratio(self.height_ratio)
                        if fixed_card_effect_animation.get_animation_panel() == None:
                            vertices = [(0, 0), (105, 0), (105, 170), (0, 170)]
                            fixed_card_effect_animation.draw_animation_panel_with_vertices(vertices)
                            self.play_harmful_effect_animation(self.opponent_field_unit_repository, index, fixed_card_effect_animation)
                            print('create harmful effect animation')
                        else:
                            fixed_card_effect_animation.get_animation_panel().draw()
                    else:
                        opponent_field_unit.create_fixed_card_freeze_effect_animation()

                if 'DarkFire' in self.opponent_field_unit_repository.get_harmful_status_by_index(index):
                    fixed_card_effect_animation = opponent_field_unit.get_fixed_card_dark_flame_effect_animation()
                    if fixed_card_effect_animation is not None:

                        fixed_card_effect_animation.set_total_window_size(self.width, self.height)
                        fixed_card_effect_animation.set_width_ratio(self.width_ratio)
                        fixed_card_effect_animation.set_height_ratio(self.height_ratio)
                        if fixed_card_effect_animation.get_animation_panel() == None:
                            vertices = [(0, 0), (105, 0), (105, 170), (0, 170)]
                            fixed_card_effect_animation.draw_animation_panel_with_vertices(vertices)
                            self.play_harmful_effect_animation(self.opponent_field_unit_repository, index, fixed_card_effect_animation)
                            print('create harmful effect animation')
                        else:
                            fixed_card_effect_animation.get_animation_panel().draw()
                    else:
                        opponent_field_unit.create_fixed_card_dark_flame_effect_animation()



        if self.battle_field_repository.get_current_use_card_id():
            self.message_on_the_screen.clear_current_message_on_the_battle_screen()
            card_id = self.battle_field_repository.get_current_use_card_id()
            self.notice_card.init_card_view_larger(card_id)
            self.master.after(2000, lambda: self.notice_card.reset_fixed_card_base(card_id))
            self.battle_field_repository.reset_current_use_card_id()

        if self.attack_animation_object.get_animation_action() is AnimationAction.CONTRACT_OF_DOOM:
            print(f"{Fore.RED}파멸의 계약 animation 재생{Style.RESET_ALL}")

            self.master.after(2000, self.ready_to_use_contract_of_doom_attack_animation)

            #self.master.after(2000, self.your_contract_of_doom_attack_animation)
            self.attack_animation_object.set_animation_action(AnimationAction.DUMMY)

        if self.attack_animation_object.get_animation_action() is AnimationAction.DEATH_SCYTHE:
            print(f"{Fore.RED}죽음의 낫 animation 재생{Style.RESET_ALL}")

            self.master.after(0, self.death_scythe_animation)

            # self.master.after(2000, self.your_contract_of_doom_attack_animation)
            self.attack_animation_object.set_animation_action(AnimationAction.DUMMY)

        if self.attack_animation_object.get_animation_action() is AnimationAction.ENERGY_BURN:
            print(f"{Fore.RED}에너지번 animation 재생{Style.RESET_ALL}")

            self.master.after(0, self.energy_burn_animation)

            # self.master.after(2000, self.your_contract_of_doom_attack_animation)
            self.attack_animation_object.set_animation_action(AnimationAction.DUMMY)

        if self.attack_animation_object.get_animation_action() is AnimationAction.CORPSE_EXPLOSION:
            print(f"{Fore.RED}시폭 animation 재생{Style.RESET_ALL}")

            self.master.after(2000, self.corpse_explosion_animation)

            # self.master.after(2000, self.your_contract_of_doom_attack_animation)
            self.attack_animation_object.set_animation_action(AnimationAction.DUMMY)

        if self.field_area_inside_handler.get_field_area_action() is not FieldAreaAction.PLAY_ANIMATION:
            for index, field_unit in enumerate(self.your_field_unit_repository.get_current_field_unit_list()):
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

                if self.your_field_unit_repository.get_is_index_in_harmful_status(index) == True:
                    if 'Freeze' in self.your_field_unit_repository.get_harmful_status_by_index(index):
                        fixed_card_effect_animation = field_unit.get_fixed_card_freeze_effect_animation()
                        if fixed_card_effect_animation is not None:
                            fixed_card_effect_animation.set_total_window_size(self.width, self.height)
                            fixed_card_effect_animation.set_width_ratio(self.width_ratio)
                            fixed_card_effect_animation.set_height_ratio(self.height_ratio)
                            if fixed_card_effect_animation.get_animation_panel() == None:
                                vertices = [(0, 0), (105, 0), (105, 170), (0, 170)]
                                fixed_card_effect_animation.draw_animation_panel_with_vertices(vertices)
                                self.play_harmful_effect_animation(self.your_field_unit_repository, index,
                                                                   fixed_card_effect_animation)
                                print('create harmful effect animation')
                            else:
                                fixed_card_effect_animation.get_animation_panel().draw()
                        else:
                            field_unit.create_fixed_card_freeze_effect_animation()

                    if 'DarkFire' in self.your_field_unit_repository.get_harmful_status_by_index(index):
                        fixed_card_effect_animation = field_unit.get_fixed_card_dark_flame_effect_animation()
                        if fixed_card_effect_animation is not None:
                            fixed_card_effect_animation.set_total_window_size(self.width, self.height)
                            fixed_card_effect_animation.set_width_ratio(self.width_ratio)
                            fixed_card_effect_animation.set_height_ratio(self.height_ratio)
                            if fixed_card_effect_animation.get_animation_panel() == None:
                                vertices = [(0, 0), (105, 0), (105, 170), (0, 170)]
                                fixed_card_effect_animation.draw_animation_panel_with_vertices(vertices)
                                self.play_harmful_effect_animation(self.your_field_unit_repository, index,
                                                                   fixed_card_effect_animation)
                                print('create harmful effect animation')
                            else:
                                fixed_card_effect_animation.get_animation_panel().draw()
                        else:
                            field_unit.create_fixed_card_dark_flame_effect_animation()
        

        # if len(self.battle_result_panel_list) == 2:

        # if len(self.battle_result_panel_list) != 0:
        #     if self.is_playing_action_animation == False and self.field_area_inside_handler.get_field_area_action() == None:
        #         glEnable(GL_BLEND)
        #         glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        #         glEnable(GL_DEPTH_TEST)
        #         glDepthFunc(GL_ALWAYS)
        #
        #         self.battle_result.set_width_ratio(self.width_ratio)
        #         self.battle_result.set_height_ratio(self.height_ratio)
        #         self.battle_result_panel_list[1].draw()
        #
        #         glDisable(GL_BLEND)




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


        # if len(self.battle_result_panel_list) != 0:
        #     if self.is_playing_action_animation == False and self.field_area_inside_handler.get_field_area_action() == None:
        #     # if len(self.battle_result_panel_list) != 0:
        #         self.battle_result.set_width_ratio(self.width_ratio)
        #         self.battle_result.set_height_ratio(self.height_ratio)
        #         self.battle_result_panel_list[1].draw()

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

                for selected_search_unit in self.selected_search_unit_lightning_border:
                    if selected_search_unit == pickable_card_base:
                        selected_search_unit.set_width_ratio(self.width_ratio)
                        selected_search_unit.set_height_ratio(self.height_ratio)

                        self.lightning_border.set_padding(20)
                        self.lightning_border.update_shape(selected_search_unit)
                        self.lightning_border.draw_lightning_border()

        self.your_hand_prev_button.draw()
        self.your_hand_next_button.draw()

        self.post_draw()

        if self.field_area_inside_handler.get_field_area_action() is FieldAreaAction.PLAY_ANIMATION:
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

        if self.opponent_field_area_inside_handler.get_active_field_area_action() is OpponentFieldAreaActionProcess.PLAY_ANIMATION:
            opponent_animation_actor = self.attack_animation_object.get_opponent_animation_actor()
            opponent_animation_actor_index = opponent_animation_actor.get_index()

            for index, opponent_field_unit in enumerate(
                    self.opponent_field_unit_repository.get_current_field_unit_card_object_list()):
                if opponent_field_unit is None:
                    continue

                if opponent_animation_actor_index != index:
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

        if self.effect_animation_repository.get_effect_animation_dictionary() is not {} and self.effect_animation_repository.get_effect_animation_panel_dictionary() is not {}:

            for effect_animation, effect_animation_panel in zip(self.effect_animation_repository.get_effect_animation_dictionary().values(),
                                                                self.effect_animation_repository.get_effect_animation_panel_dictionary().values()):
                if effect_animation.is_finished:
                    continue
                effect_animation.set_width_ratio(self.width_ratio)
                effect_animation.set_height_ratio(self.height_ratio)
                effect_animation_panel.draw()

        if self.opponent_fixed_unit_card_inside_handler.get_opponent_field_area_action() == OpponentFieldAreaAction.ENERGY_BURN:

            print('create energy burn animation')
            target_index = self.opponent_fixed_unit_card_inside_handler.get_target_index_to_action()
            effect_animation = EffectAnimation()
            effect_animation.set_animation_name('dark_blast')
            effect_animation.set_total_window_size(self.width, self.height)
            effect_animation.change_local_translation(
                self.opponent_field_unit_repository.find_opponent_field_unit_by_index(
                    target_index).get_fixed_card_base().get_local_translation()
            )
            effect_animation.draw_animation_panel()
            effect_animation_panel = effect_animation.get_animation_panel()
            print(effect_animation_panel)
            animation_index = self.effect_animation_repository.save_effect_animation_at_dictionary_without_index_and_return_index(
                effect_animation)
            self.effect_animation_repository.save_effect_animation_panel_at_dictionary_with_index(
                animation_index, effect_animation_panel)

            self.opponent_fixed_unit_card_inside_handler.clear_opponent_field_area_action()
            self.opponent_fixed_unit_card_inside_handler.clear_target_index_to_action()

            def calculate_energy_burn(_target_index):
                unit_index = _target_index
                print('target_index : ', _target_index)
                opponent_field_unit = self.opponent_field_unit_repository.find_opponent_field_unit_by_index(
                    unit_index)
                print(f"opponent_field_unit: {opponent_field_unit}")
                card_id = opponent_field_unit.get_card_number()
                detach_count = 2
                total_attached_energy_count = self.opponent_field_unit_repository.get_total_energy_at_index(
                    unit_index)
                print(f"opponent_field_unit_attached_undead_energy_count: {total_attached_energy_count}")

                # attached_energy = self.__opponent_field_unit_repository.attached_energy_info.get(unit_index, [])

                if total_attached_energy_count == 0:
                    print("데미지를 입힙니다.")
                    remove_from_field = False
                    opponent_fixed_card_base = opponent_field_unit.get_fixed_card_base()
                    opponent_fixed_card_attached_shape_list = opponent_fixed_card_base.get_attached_shapes()
                    for opponent_fixed_card_attached_shape in opponent_fixed_card_attached_shape_list:
                        if isinstance(opponent_fixed_card_attached_shape, NonBackgroundNumberImage):
                            if opponent_fixed_card_attached_shape.get_circle_kinds() is CircleKinds.HP:
                                hp = opponent_fixed_card_attached_shape.get_number()
                                hp -= 10
                                print(f"hp : {hp}")

                                if hp <= 0:
                                    remove_from_field = True
                                    break

                                opponent_fixed_card_attached_shape.set_number(hp)

                                opponent_fixed_card_attached_shape.set_image_data(
                                    self.pre_drawed_image_instance.get_pre_draw_unit_hp(hp))

                    if remove_from_field:
                        def remove_field_unit(index):
                            unit_card_id = self.opponent_field_unit_repository.get_opponent_card_id_by_index(index)
                            self.opponent_field_unit_repository.remove_current_field_unit_card(index)
                            self.opponent_tomb_repository.create_opponent_tomb_card(unit_card_id)
                            self.opponent_field_unit_repository.remove_harmful_status_by_index(index)
                            self.opponent_field_unit_repository.replace_opponent_field_unit_card_position()

                        self.create_effect_animation_to_opponent_unit_and_play_animation_and_call_function_with_param(
                            'death', unit_index, remove_field_unit, unit_index)

                else:
                    print("에너지를 태웁니다.")
                    # if total_attached_energy_count == 1:
                    #     detach_count = 1

                    attached_energy_after_energy_burn = total_attached_energy_count - detach_count
                    if attached_energy_after_energy_burn < 0:
                        attached_energy_after_energy_burn = 0

                    opponent_fixed_card_base = opponent_field_unit.get_fixed_card_base()
                    opponent_fixed_card_attached_shape_list = opponent_fixed_card_base.get_attached_shapes()
                    self.opponent_field_unit_repository.detach_race_energy(opponent_field_unit.get_index(),
                                                                           EnergyType.Undead,
                                                                           detach_count)

                    # energy_circle_list = []
                    # energy_circle_index_list = []
                    # count = 0

                    for opponent_fixed_card_attached_shape in opponent_fixed_card_attached_shape_list:
                        if isinstance(opponent_fixed_card_attached_shape, NonBackgroundNumberImage):
                            if opponent_fixed_card_attached_shape.get_circle_kinds() is CircleKinds.ENERGY:
                                opponent_fixed_card_attached_shape.set_number(attached_energy_after_energy_burn)
                                opponent_fixed_card_attached_shape.set_image_data(
                                    self.pre_drawed_image_instance.get_pre_draw_unit_energy(
                                        attached_energy_after_energy_burn))

                    #     if isinstance(opponent_fixed_card_attached_shape, Circle):
                    #         energy_circle_index_list.append(count)
                    #         print(
                    #             f"Energy burn opponent unit vertices: {opponent_fixed_card_attached_shape.get_vertices()}")
                    #         energy_circle_list.append(opponent_fixed_card_attached_shape)
                    #
                    #         del opponent_fixed_card_attached_shape
                    #
                    #     count += 1
                    #
                    # energy_circle_index_list.reverse()
                    # for index in energy_circle_index_list:
                    #     if 0 <= index < len(opponent_fixed_card_attached_shape_list):
                    #         if detach_count == 0:
                    #             break
                    #
                    #         del opponent_fixed_card_attached_shape_list[index]
                    #         detach_count -= 1

            def vibration_energy_burn(target_index):
                steps = 30

                field_unit_object = self.opponent_field_unit_repository.find_opponent_field_unit_by_index(target_index)
                fixed_card_base = field_unit_object.get_fixed_card_base()
                tool_card = field_unit_object.get_tool_card()
                attached_shape_list = fixed_card_base.get_attached_shapes()

                def vibration(step_count):
                    if step_count % 2 == 1:
                        vibration_factor = 10
                        random_translation = (random.uniform(-vibration_factor, vibration_factor),
                                              random.uniform(-vibration_factor, vibration_factor))

                        new_fixed_card_base_vertices = [
                            (vx + random_translation[0], vy + random_translation[1]) for vx, vy in
                            fixed_card_base.get_vertices()
                        ]
                        fixed_card_base.update_vertices(new_fixed_card_base_vertices)

                        if tool_card is not None:
                            new_tool_card_vertices = [
                                (vx + random_translation[0], vy + random_translation[1]) for vx, vy in
                                tool_card.get_vertices()
                            ]
                            tool_card.update_vertices(new_tool_card_vertices)

                        for attached_shape in attached_shape_list:
                            new_attached_shape_vertices = [
                                (vx + random_translation[0], vy + random_translation[1]) for vx, vy in
                                attached_shape.get_vertices()
                            ]
                            attached_shape.update_vertices(new_attached_shape_vertices)

                    else:
                        fixed_card_base.update_vertices(fixed_card_base.get_initial_vertices())
                        if tool_card is not None:
                            tool_card.update_vertices(tool_card.get_initial_vertices())
                        for attached_shape in attached_shape_list:
                            attached_shape.update_vertices(attached_shape.get_initial_vertices())

                    if step_count < steps:
                        self.master.after(20, vibration, step_count + 1)
                    else:
                        calculate_energy_burn(target_index)

                vibration(1)

            self.__music_player_repository.play_sound_effect_of_card_execution('energy_burn')

            self.play_effect_animation_by_index_and_call_function_with_param(animation_index, vibration_energy_burn, target_index)

        if self.opponent_fixed_unit_card_inside_handler.get_opponent_field_area_action() == OpponentFieldAreaAction.DEATH_SCYTHE:
            print('create death scythe animation')

            target_index = self.opponent_fixed_unit_card_inside_handler.get_target_index_to_action()
            effect_animation = EffectAnimation()
            effect_animation.set_animation_name('death_scythe')
            effect_animation.set_total_window_size(self.width, self.height)
            effect_animation.change_local_translation(
                self.opponent_field_unit_repository.find_opponent_field_unit_by_index(
                    target_index).get_fixed_card_base().get_local_translation()
            )
            effect_animation.draw_animation_panel()
            effect_animation_panel = effect_animation.get_animation_panel()
            print(effect_animation_panel)
            animation_index = self.effect_animation_repository.save_effect_animation_at_dictionary_without_index_and_return_index(
                effect_animation)
            self.effect_animation_repository.save_effect_animation_panel_at_dictionary_with_index(
                animation_index, effect_animation_panel)

            self.opponent_fixed_unit_card_inside_handler.clear_opponent_field_area_action()
            self.opponent_fixed_unit_card_inside_handler.clear_target_index_to_action()

            def calculate_death_scythe():
                DEATH_SCYTHE_FIXED_DAMAGE = 30
                unit_index = target_index
                opponent_unit = self.opponent_field_unit_repository.find_opponent_field_unit_by_index(unit_index)
                opponent_unit_card_id = opponent_unit.get_card_number()

                is_opponent_unit_death = True
                opponent_unit_hp = 0

                opponent_fixed_card_base = None
                opponent_attached_shape_list = None

                if self.card_info_repository.getCardGradeForCardNumber(
                        opponent_unit_card_id) > CardGrade.LEGEND.value:
                    # opponent_unit_hp = self.__card_info_repository.getCardHpForCardNumber(opponent_unit_card_id)
                    opponent_fixed_card_base = opponent_unit.get_fixed_card_base()
                    opponent_attached_shape_list = opponent_fixed_card_base.get_attached_shapes()

                    for opponent_attached_shape in opponent_attached_shape_list:
                        if isinstance(opponent_attached_shape, NonBackgroundNumberImage):
                            if opponent_attached_shape.get_circle_kinds() is CircleKinds.HP:
                                opponent_unit_hp = opponent_attached_shape.get_number()
                                opponent_unit_hp -= DEATH_SCYTHE_FIXED_DAMAGE
                                opponent_attached_shape.set_number(opponent_unit_hp)

                                if opponent_unit_hp <= 0:
                                    break

                                # opponent_attached_shape.set_image_data(
                                #     self.__pre_drawed_image_instance.get_pre_draw_number_image(
                                #         opponent_unit_hp))

                                opponent_attached_shape.set_image_data(
                                    self.pre_drawed_image_instance.get_pre_draw_unit_hp(
                                        opponent_unit_hp))
                                is_opponent_unit_death = False

                                print(f"opponent_unit_hp: {opponent_unit_hp}")
                    # if opponent_unit_hp > 0:
                    #     is_opponent_unit_death = False
                else:
                    pass
                    # self.__opponent_tomb_repository.create_opponent_tomb_card(opponent_unit_card_id)

                # self.__your_hand_repository.replace_hand_card_position()

                if is_opponent_unit_death:
                    print(f"is it death ? {opponent_unit_hp}")
                    def remove_opponent_field_unit(index):
                        card_id = self.opponent_field_unit_repository.get_opponent_card_id_by_index(index)
                        self.opponent_field_unit_repository.remove_current_field_unit_card(index)
                        self.opponent_field_unit_repository.replace_opponent_field_unit_card_position()
                        self.opponent_field_unit_repository.remove_harmful_status_by_index(index)
                        self.opponent_tomb_repository.create_opponent_tomb_card(opponent_unit_card_id)

                    self.create_effect_animation_to_opponent_unit_and_play_animation_and_call_function_with_param(
                        'death', unit_index, remove_opponent_field_unit, unit_index)

            def vibration_death_scythe():
                steps = 30
                unit_index = target_index
                field_unit_object = self.opponent_field_unit_repository.find_opponent_field_unit_by_index(unit_index)
                fixed_card_base = field_unit_object.get_fixed_card_base()
                tool_card = field_unit_object.get_tool_card()
                attached_shape_list = fixed_card_base.get_attached_shapes()

                def vibration(step_count):
                    if step_count % 2 == 1:
                        vibration_factor = 10
                        random_translation = (random.uniform(-vibration_factor, vibration_factor),
                                              random.uniform(-vibration_factor, vibration_factor))

                        new_fixed_card_base_vertices = [
                            (vx + random_translation[0], vy + random_translation[1]) for vx, vy in
                            fixed_card_base.get_vertices()
                        ]
                        fixed_card_base.update_vertices(new_fixed_card_base_vertices)

                        if tool_card is not None:
                            new_tool_card_vertices = [
                                (vx + random_translation[0], vy + random_translation[1]) for vx, vy in
                                tool_card.get_vertices()
                            ]
                            tool_card.update_vertices(new_tool_card_vertices)

                        for attached_shape in attached_shape_list:
                            new_attached_shape_vertices = [
                                (vx + random_translation[0], vy + random_translation[1]) for vx, vy in
                                attached_shape.get_vertices()
                            ]
                            attached_shape.update_vertices(new_attached_shape_vertices)

                    else:
                        fixed_card_base.update_vertices(fixed_card_base.get_initial_vertices())
                        if tool_card is not None:
                            tool_card.update_vertices(tool_card.get_initial_vertices())
                        for attached_shape in attached_shape_list:
                            attached_shape.update_vertices(attached_shape.get_initial_vertices())

                    if step_count < steps:
                        self.master.after(20, vibration, step_count + 1)
                    else:
                        calculate_death_scythe()

                vibration(1)

            self.__music_player_repository.play_sound_effect_of_card_execution('death_scythe')

            self.play_effect_animation_by_index_and_call_function(animation_index, vibration_death_scythe)

        if self.field_area_inside_handler.get_required_to_process_passive_skill_multiple_unit_list():
            self.field_area_inside_handler.set_field_turn_start_action(TurnStartAction.CHECK_MULTIPLE_UNIT_REQUIRED_FIRST_PASSIVE_SKILL_PROCESS)

        if self.field_area_inside_handler.get_field_turn_start_action() is TurnStartAction.CHECK_MULTIPLE_UNIT_REQUIRED_FIRST_PASSIVE_SKILL_PROCESS:
            required_to_process_passive_skill_multiple_unit_list = self.field_area_inside_handler.get_required_to_process_passive_skill_multiple_unit_list()
            print(f"{Fore.RED}required_to_process_passive_skill_multiple_unit_list: {Fore.GREEN}{required_to_process_passive_skill_multiple_unit_list}{Style.RESET_ALL}")

            if len(required_to_process_passive_skill_multiple_unit_list) == 0:
                self.field_area_inside_handler.set_field_turn_start_action(TurnStartAction.Dummy)
                return

            passive_unit_index = int(required_to_process_passive_skill_multiple_unit_list.pop(0))
            self.field_area_inside_handler.set_field_turn_start_action(TurnStartAction.Dummy)

            # TODO: 네더 블레이드 턴 시작 시 발동하는 타겟팅 처리 진행해야함
            your_field_unit = self.your_field_unit_repository.find_field_unit_by_index(passive_unit_index)
            self.attack_animation_object.set_animation_actor(your_field_unit)
            self.field_area_inside_handler.set_field_area_action(FieldAreaAction.TURN_START_FIRST_PASSIVE_SKILL_PROCESS)

            # TODO: 임시 방편으로 recently_added에 강제 배치 아래의 패시브를 구동하기 위함
            self.field_area_inside_handler.set_recently_added_card_index(passive_unit_index)

        if self.field_area_inside_handler.get_field_area_action() is FieldAreaAction.TURN_START_FIRST_PASSIVE_SKILL_PROCESS:
            print(f"{Fore.RED}턴 시작 시 패시브 처리가 진행됩니다!{Style.RESET_ALL}")

            your_field_unit = self.attack_animation_object.get_animation_actor()
            your_field_unit_index = your_field_unit.get_index()

            # process_turn_start_first_passive_skill_response = self.__fake_battle_field_frame_repository.request_to_process_first_passive_skill(
            #     WideAreaPassiveSkillFromDeployRequest(
            #         _sessionInfo=self.__session_repository.get_session_info(),
            #         _unitCardIndex=str(your_field_unit_index),
            #         _usageSkillIndex="1"))

            turn_start_first_passive_skill_response = self.__fake_battle_field_frame_repository.request_to_process_turn_start_first_passive_skill_to_your_field_unit(
                TurnStartFirstPassiveSkillRequest(
                    _sessionInfo=self.__session_repository.get_first_fake_session_info(),
                    _unitCardIndex=str(your_field_unit_index),
                    _usageSkillIndex="1"))

            print(f"{Fore.RED}turn_start_first_passive_skill_response:{Fore.GREEN} {turn_start_first_passive_skill_response}{Style.RESET_ALL}")

            is_success = turn_start_first_passive_skill_response['is_success']
            if is_success is False:
                return FieldAreaAction.Dummy

            # {'is_success': True, 'player_field_unit_health_point_map': {'Opponent': {
            #     'field_unit_health_point_map': {'0': 0, '10': 0, '8': 10, '2': 0, '9': 5, '4': 0, '3': 20}}},
            #  'player_field_unit_harmful_effect_map': {'Opponent': {
            #      'field_unit_harmful_status_map': {'9': {'harmful_status_list': []}, '2': {'harmful_status_list': []},
            #                                        '0': {'harmful_status_list': []}, '4': {'harmful_status_list': []},
            #                                        '8': {'harmful_status_list': []}, '10': {'harmful_status_list': []},
            #                                        '3': {'harmful_status_list': []}}}},
            #  'player_field_unit_death_map': {'Opponent': {'dead_field_unit_index_list': [0, 2, 4, 10]}},
            #  'index_list_of_passive_skill_to_handle': [2]}
            self.attack_animation_object.set_response_data(turn_start_first_passive_skill_response)

            self.field_area_inside_handler.set_field_area_action(FieldAreaAction.PLAY_ANIMATION)

            damage = self.card_info_repository.getCardPassiveFirstDamageForCardNumber(your_field_unit.get_card_number())
            self.attack_animation_object.set_animation_actor_damage(damage)

            extra_ability = self.your_field_unit_repository.get_your_unit_extra_ability_at_index(your_field_unit_index)
            self.attack_animation_object.set_extra_ability(extra_ability)

            self.master.after(0, self.nether_blade_turn_start_first_passive_skill_animation)

            self.attack_animation_object.set_animation_action(AnimationAction.DUMMY)

        if self.field_area_inside_handler.get_field_area_action() is FieldAreaAction.REQUIRED_FIRST_PASSIVE_SKILL_PROCESS:
            print(f"{Fore.RED}패시브 처리가 필요합니다!{Style.RESET_ALL}")

            # {"protocolNumber":2002, "unitCardIndex": "0", "usageSkillIndex": "1", "sessionInfo":""}
            # session = self.__session_repository.get_session_info()
            recently_added_card_index = self.field_area_inside_handler.get_recently_added_card_index()
            process_first_passive_skill_response = self.__fake_battle_field_frame_repository.request_to_process_first_passive_skill(
                WideAreaPassiveSkillFromDeployRequest(
                    _sessionInfo=self.__session_repository.get_session_info(),
                    _unitCardIndex=str(recently_added_card_index),
                    _usageSkillIndex="1"))

            # {"is_success":true,
            # "player_field_unit_health_point_map":{"Opponent":{"field_unit_health_point_map":{"1":10,"0":10}}},
            # "player_field_unit_harmful_effect_map":{"Opponent":{"field_unit_harmful_status_map":{"0":{"harmful_status_list":[]},"1":{"harmful_status_list":[]}}}},"player_field_unit_death_map":{"Opponent":{"dead_field_unit_index_list":[]}}}
            print(f"{Fore.RED}process_first_passive_skill_response:{Fore.GREEN} {process_first_passive_skill_response}{Style.RESET_ALL}")

            is_success = process_first_passive_skill_response['is_success']
            if is_success is False:
                return FieldAreaAction.Dummy

            your_animation_actor = self.your_field_unit_repository.find_field_unit_by_index(recently_added_card_index)
            self.attack_animation_object.set_animation_actor(your_animation_actor)
            self.field_area_inside_handler.set_field_area_action(FieldAreaAction.PLAY_ANIMATION)

            damage = self.card_info_repository.getCardPassiveFirstDamageForCardNumber(your_animation_actor.get_card_number())
            self.attack_animation_object.set_animation_actor_damage(damage)

            extra_ability = self.your_field_unit_repository.get_your_unit_extra_ability_at_index(recently_added_card_index)
            self.attack_animation_object.set_extra_ability(extra_ability)

            if self.field_area_inside_handler.get_unit_action() is UnitAction.NETHER_BLADE_FIRST_WIDE_AREA_PASSIVE_SKILL:
                self.master.after(0, self.nether_blade_first_passive_skill_animation)

            self.attack_animation_object.set_animation_action(AnimationAction.DUMMY)
            # self.field_area_inside_handler.clear_field_area_action()

        if self.opponent_field_area_inside_handler.get_field_area_action() is OpponentFieldAreaActionProcess.REQUIRE_TO_PROCESS_PASSIVE_SKILL_PROCESS:
            print(f"{Fore.RED}Opponent Unit 패시브 처리가 필요합니다!{Style.RESET_ALL}")

            if self.opponent_field_area_inside_handler.get_unit_action() is OpponentUnitAction.NETHER_BLADE_FIRST_WIDE_AREA_PASSIVE_SKILL:
                self.master.after(2000, self.opponent_nether_blade_first_passive_skill_animation)

            if self.opponent_field_area_inside_handler.get_unit_action() is OpponentUnitAction.NETHER_BLADE_SECOND_TARGETING_PASSIVE_SKILL:
                self.master.after(2000, self.opponent_nether_blade_second_passive_skill_animation)

            self.opponent_field_area_inside_handler.set_field_area_action(OpponentFieldAreaActionProcess.Dummy)

        if self.opponent_field_area_inside_handler.get_field_area_action() is OpponentFieldAreaActionProcess.REQUIRE_TO_PROCESS_GENERAL_ATTACK_TO_MAIN_CHARACTER_PROCESS:
            print(f"{Fore.RED}Opponent Unit이 Your 메인 캐릭터를 공격합니다!{Style.RESET_ALL}")

            self.attack_animation_object.set_your_main_character(self.your_main_character_panel)
            self.master.after(2000, self.opponent_attack_main_character_animation)

            self.opponent_field_area_inside_handler.set_field_area_action(OpponentFieldAreaActionProcess.Dummy)
            self.opponent_field_area_inside_handler.clear_field_area_action()
        if self.opponent_field_area_inside_handler.get_field_area_action() is OpponentFieldAreaActionProcess.REQUIRE_TO_PROCESS_GENERAL_ATTACK_TO_YOUR_UNIT_PROCESS:
            print(f"{Fore.RED}Opponent Unit이 Your 유닛을 공격합니다!{Style.RESET_ALL}")

            self.master.after(2000, self.opponent_attack_your_unit_animation)
            # self.opponent_attack_animation

            self.opponent_field_area_inside_handler.set_field_area_action(OpponentFieldAreaActionProcess.Dummy)
            self.opponent_field_area_inside_handler.clear_field_area_action()
        if self.opponent_field_area_inside_handler.get_field_area_action() is OpponentFieldAreaActionProcess.REQUIRE_TO_PROCESS_VALRN_ACTIVE_TARGETING_SKILL_TO_YOUR_UNIT:
            print(f"{Fore.RED}Opponent valrn이 Your 유닛에 쉐도우 볼을 사용합니다!{Style.RESET_ALL}")

            self.master.after(2000, self.opponent_valrn_shadow_ball_to_your_unit_animation)

            self.opponent_field_area_inside_handler.set_field_area_action(OpponentFieldAreaActionProcess.Dummy)
            self.opponent_field_area_inside_handler.clear_field_area_action()
        if self.opponent_field_area_inside_handler.get_field_area_action() is OpponentFieldAreaActionProcess.REQUIRE_TO_PROCESS_VALRN_ACTIVE_TARGETING_SKILL_TO_YOUR_MAIN_CHARACTER:
            print(f"{Fore.RED}Opponent valrn이 Your 메인 캐릭터에 쉐도우 볼을 사용합니다!{Style.RESET_ALL}")

            self.master.after(2000, self.opponent_valrn_shadow_ball_to_your_main_character_animation)

            self.opponent_field_area_inside_handler.set_field_area_action(OpponentFieldAreaActionProcess.Dummy)
            self.opponent_field_area_inside_handler.clear_field_area_action()
        if self.opponent_field_area_inside_handler.get_field_area_action() is OpponentFieldAreaActionProcess.REQUIRE_TO_PROCESS_VALRN_ACTIVE_NON_TARGETING_SKILL_TO_YOUR_FIELD:
            print(f"{Fore.RED}Opponent valrn이 Your Field에 망령의 바다를 사용합니다!{Style.RESET_ALL}")

            self.master.after(2000, self.opponent_valrn_sea_of_wraith_to_your_field_animation)

            self.opponent_field_area_inside_handler.set_field_area_action(OpponentFieldAreaActionProcess.Dummy)
            self.opponent_field_area_inside_handler.clear_field_area_action()
        # self.post_draw()

        if self.current_fixed_details_card:
            self.current_fixed_details_card.set_width_ratio(self.width_ratio)
            self.current_fixed_details_card.set_height_ratio(self.height_ratio)
            self.current_fixed_details_card.draw()

            current_attached_shape_list = self.current_fixed_details_card.get_attached_shapes()

            for attached_shape in current_attached_shape_list:
                if isinstance(attached_shape, Rectangle):
                    if attached_shape.get_rectangle_kinds() is RectangleKinds.DETAIL:
                        glEnable(GL_BLEND)
                        glBlendFunc(GL_ONE_MINUS_SRC_ALPHA, GL_SRC_ALPHA)
                        attached_shape.set_width_ratio(self.width_ratio)
                        attached_shape.set_height_ratio(self.height_ratio)
                        attached_shape.draw()
                        glDisable(GL_BLEND)

            for attached_shape in current_attached_shape_list:
                if isinstance(attached_shape, Rectangle):
                    if attached_shape.get_rectangle_kinds() is RectangleKinds.DETAIL:
                        continue
                attached_shape.set_width_ratio(self.width_ratio)
                attached_shape.set_height_ratio(self.height_ratio)
                attached_shape.draw()



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

        # if self.selected_object is None:
        #     self.lightning_border.remove_lightning_border()

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

        if self.opponent_details_panel_rectangle:
            glEnable(GL_BLEND)
            glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

            self.opponent_details_panel_rectangle.draw()

            glDisable(GL_BLEND)

            self.opponent_details_button.draw()

        if self.your_hand_details_panel_rectangle:
            glEnable(GL_BLEND)
            glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

            self.your_hand_details_panel_rectangle.draw()

            glDisable(GL_BLEND)

            self.your_hand_details_button.draw()

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
            if self.your_deck_search_panel is not None:
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
            # glEnable(GL_BLEND)
            # glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

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

            # glDisable(GL_BLEND)

        if self.opponent_tomb_panel_selected:
            # elif self.selected_tomb is TombType.Opponent:
            # glEnable(GL_BLEND)
            # glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

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

            # glDisable(GL_BLEND)

        if self.your_lost_zone_panel_selected:
            # glEnable(GL_BLEND)
            # glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

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

            # glDisable(GL_BLEND)

        if self.opponent_lost_zone_panel_selected:
            # glEnable(GL_BLEND)
            # glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

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

            # glDisable(GL_BLEND)

        if self.notice_card.get_fixed_card_base():

            notice_card_base = self.notice_card.get_fixed_card_base()
            notice_card_base.set_width_ratio(self.width_ratio)
            notice_card_base.set_height_ratio(self.height_ratio)
            notice_card_base.draw()

            attached_shape_list = notice_card_base.get_attached_shapes()
            for attached_shape in attached_shape_list:
                attached_shape.set_width_ratio(self.width_ratio)
                attached_shape.set_height_ratio(self.height_ratio)
                attached_shape.draw()

        if self.message_on_the_screen.get_current_message_on_the_battle_screen():
            glEnable(GL_DEPTH_TEST)
            glDepthFunc(GL_ALWAYS)
            # glEnable(GL_BLEND)
            # glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

            self.message_on_the_screen.set_width_ratio(self.width_ratio)
            self.message_on_the_screen.set_height_ratio(self.height_ratio)
            self.current_field_message_on_the_battle_screen_panel = (
                self.message_on_the_screen.get_current_message_on_the_battle_screen()
            )
            self.current_field_message_on_the_battle_screen_panel.draw()

            # glDisable(GL_BLEND)
            glDisable(GL_DEPTH_TEST)




        if self.option_popup_surrender_button_selected:
            for surrender_confirm_panel in self.surrender_confirm_panel_list:
                surrender_confirm_panel.draw()


        # self.post_draw()

        # if len(self.battle_result_panel_list) != 0:
        #     if self.is_playing_action_animation == False and self.field_area_inside_handler.get_field_area_action() == None:
        #         # glEnable(GL_BLEND)
        #         # glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        #         # glEnable(GL_DEPTH_TEST)
        #         # glDepthFunc(GL_ALWAYS)
        #
        #         self.battle_result.set_width_ratio(self.width_ratio)
        #         self.battle_result.set_height_ratio(self.height_ratio)
        #         self.battle_result_panel_list[1].draw()
        #
        #         # glDisable(GL_BLEND)
        #
        # if len(self.battle_result_panel_list) != 0:
        #     if self.is_playing_action_animation == False and self.field_area_inside_handler.get_field_area_action() == None:
        #     # if len(self.battle_result_panel_list) != 0:
        #         self.battle_result.set_width_ratio(self.width_ratio)
        #         self.battle_result.set_height_ratio(self.height_ratio)
        #         self.battle_result_panel_list[0].draw()

        if len(self.battle_result_panel_list) != 0:
            if not self.is_playing_action_animation and self.field_area_inside_handler.get_field_area_action() is None:
                for battle_result_panel in self.battle_result_panel_list:
                    battle_result_panel.set_width_ratio(self.width_ratio)
                    battle_result_panel.set_height_ratio(self.height_ratio)
                    battle_result_panel.draw()
                if self.battle_field_repository.get_is_win() == BattleFinishPosition.Winner and not self.game_end_sound_call:
                    self.__music_player_repository.play_sound_effect_of_game_end('winner')
                    self.game_end_sound_call = True
                elif self.battle_field_repository.get_is_win() == BattleFinishPosition.Loser and not self.game_end_sound_call:
                    self.__music_player_repository.play_sound_effect_of_game_end('loser')
                    self.game_end_sound_call = True



        if self.skill_focus_background_panel:
            glEnable(GL_BLEND)
            glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

            self.skill_focus_background_panel.draw()
            # self.skill_focus_panel.draw()

            glDisable(GL_BLEND)

        #self.check_my_turn()

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

    # 카드 내리기기
    def on_canvas_release(self, event):
        x, y = event.x, event.y
        y = self.winfo_reqheight() - y

        if isinstance(self.selected_object, PickableCard):
            # Opponent Field Area 시작
            # is_pickable_card_inside_opponent_field =

            if self.is_point_inside_opponent_field_area((x, y), self.opponent_field_panel):
                self.__music_player_repository.play_sound_effect_of_mouse_on_click('hand_card_drop')

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

                            #damage = 15

                            response = self.__fake_battle_field_frame_repository.request_use_contract_of_doom(
                                RequestUseContractOfDoom(
                                    _sessionInfo=self.__session_repository.get_first_fake_session_info(),
                                    _itemCardId="25"
                                )
                            )
                            print(f"{Fore.RED}파멸의 계약 -> response:{Fore.GREEN} {response}{Style.RESET_ALL}")
                            is_contract_of_doom_success_value = response.get('is_success', False)

                            if is_contract_of_doom_success_value == False:
                                # self.selected_object = None
                                self.return_to_initial_location()
                                self.reset_every_selected_action()
                                is_contract_of_doom_false_message = response.get('false_message_enum')
                                self.message_on_the_screen.create_message_on_the_battle_screen(
                                    is_contract_of_doom_false_message)
                                return

                            self.attack_animation_object.set_your_usage_card_id(your_card_id)

                            # 추후 이 부분은 노티로 받아야함
                            opponent_deck_card_lost_list = response['player_deck_card_lost_list_map']['Opponent']
                            lost_card_id = opponent_deck_card_lost_list[0]

                            self.attack_animation_object.set_opponent_lost_card_id(lost_card_id)

                            field_vertices = self.opponent_field_panel.get_vertices()
                            main_character_vertices = self.opponent_main_character_panel.get_vertices()

                            vertices = [(field_vertices[0][0], main_character_vertices[0][1]), (field_vertices[2][0], main_character_vertices[1][1]),
                                        field_vertices[3], field_vertices[0]]

                            # vertices = [field_vertices[0], (field_vertices[1][0], main_character_vertices[1][1]),
                            #             (field_vertices[2][0], main_character_vertices[2][1]), field_vertices[3]]

                            self.create_effect_animation_with_vertices_and_play_animation_and_call_function(
                                'contract_of_doom', vertices, self.opponent_contract_of_doom_attack_animation
                            )

                            if response.get('player_main_character_survival_map', {}).get('Opponent', None) == 'Death':
                                self.opponent_hp_repository.opponent_character_die()
                                self.is_playing_action_animation = True




                            # # TODO: 즉발이므로 대기 액션이 필요없음 (서버와의 통신을 위해 대기가 발생 할 수 있긴함) 그 때 가서 추가
                            # for index in range(
                            #         len(self.opponent_field_unit_repository.get_current_field_unit_card_object_list()) - 1,
                            #         -1,
                            #         -1):
                            #     opponent_field_unit = \
                            #         self.opponent_field_unit_repository.get_current_field_unit_card_object_list()[index]
                            #
                            #     if opponent_field_unit is None:
                            #         continue
                            #
                            #     remove_from_field = False
                            #
                            #     fixed_card_base = opponent_field_unit.get_fixed_card_base()
                            #     attached_shape_list = fixed_card_base.get_attached_shapes()
                            #
                            #     # TODO: 가만 보면 이 부분이 은근히 많이 사용되고 있음 (중복 많이 발생함)
                            #     for attached_shape in attached_shape_list:
                            #         if isinstance(attached_shape, NonBackgroundNumberImage):
                            #             if attached_shape.get_circle_kinds() is CircleKinds.HP:
                            #
                            #                 hp_number = attached_shape.get_number()
                            #                 hp_number -= damage
                            #
                            #                 # TODO: n 턴간 불사 특성을 검사해야하므로 사실 이것도 summary 방식으로 빼는 것이 맞으나 우선은 진행한다.
                            #                 # (지금 당장 불사가 존재하지 않음)
                            #                 if hp_number <= 0:
                            #                     remove_from_field = True
                            #                     break
                            #
                            #                 print(f"contract_of_doom -> hp_number: {hp_number}")
                            #                 attached_shape.set_number(hp_number)
                            #
                            #                 # attached_shape.set_image_data(
                            #                 #     # TODO: 실제로 여기서 서버로부터 계산 받은 값을 적용해야함
                            #                 #     self.pre_drawed_image_instance.get_pre_draw_number_image(hp_number))
                            #
                            #                 attached_shape.set_image_data(
                            #                     self.pre_drawed_image_instance.get_pre_draw_unit_hp(hp_number))
                            #
                            #     if remove_from_field:
                            #         card_id = opponent_field_unit.get_card_number()
                            #
                            #         self.opponent_field_unit_repository.remove_current_field_unit_card(index)
                            #         self.opponent_tomb_repository.create_opponent_tomb_card(card_id)
                            #
                            # # your_card_index = self.your_hand_repository.find_index_by_selected_object(self.selected_object)
                            # # self.your_hand_repository.remove_card_by_index(your_card_index)
                            # your_card_index = self.your_hand_repository.find_index_by_selected_object_with_page(
                            #     self.selected_object)
                            # self.your_hand_repository.remove_card_by_index_with_page(your_card_index)
                            #
                            # self.your_tomb_repository.create_tomb_card(your_card_id)
                            #
                            # # self.your_hand_repository.replace_hand_card_position()
                            # self.your_hand_repository.update_your_hand()
                            # self.opponent_field_unit_repository.replace_opponent_field_unit_card_position()
                            #
                            # # 실제 날리는 데이터의 경우 서버로부터 응답 받은 정보를 로스트 존으로 배치
                            # self.opponent_lost_zone_repository.create_opponent_lost_zone_card(32)

                            # self.selected_object = None
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

                if card_type in [CardType.ITEM.value]:
                    if your_card_id == 36:
                        if self.is_point_inside_opponent_field_area((x, y), self.opponent_field_panel):
                            print("죽음의 대지 사용")

                            response = self.your_hand_repository.request_use_field_of_death(
                                RequestUseFieldOfDeath(
                                    _sessionInfo=self.__session_repository.get_first_fake_session_info(),
                                    _itemCardId=your_card_id)
                            )

                            is_death_success_value = response.get('is_success', False)

                            if is_death_success_value == False:
                                # self.selected_object = None
                                self.return_to_initial_location()
                                self.reset_every_selected_action()
                                is_death_false_message = response.get('false_message_enum')
                                self.message_on_the_screen.create_message_on_the_battle_screen(
                                    is_death_false_message)
                                return

                            def field_of_death(param):

                                self.__music_player_repository.play_sound_effect_of_card_execution('field_of_death')

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

                            self.create_effect_animation_to_opponent_field_and_play_animation_and_call_function_with_param(
                                'field_of_death', field_of_death, None
                            )

            # Opponent Field Area 끝
            self.__music_player_repository.play_sound_effect_of_mouse_on_click('hand_card_drop')

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


                if isinstance(is_pickable_card_inside_unit, int):
                    self.return_to_initial_location()
                    self.reset_every_selected_action()
                    self.message_on_the_screen.create_message_on_the_battle_screen(
                        is_pickable_card_inside_unit)
                elif is_pickable_card_inside_unit:
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
                                # self.selected_object = None
                                self.return_to_initial_location()
                                self.reset_every_selected_action()
                                return

                            elif placed_card_id == 35:
                                print(f"사기 전환(35) -> placed_card_id: {placed_card_id}")

                                response = self.your_hand_repository.request_use_morale_conversion(
                                    RequestUseMoraleConversion(
                                        _sessionInfo=self.__session_repository.get_first_fake_session_info(),
                                        _unitIndex=unit_index,
                                        _itemCardId=placed_card_id)
                                )

                                print(f"response: {response}")
                                is_morale_conversion_success_value = response.get('is_success', False)

                                if is_morale_conversion_success_value == False:
                                    # self.selected_object = None
                                    self.return_to_initial_location()
                                    self.reset_every_selected_action()
                                    is_morale_conversion_false_message = response.get('false_message_enum')
                                    self.message_on_the_screen.create_message_on_the_battle_screen(
                                        is_morale_conversion_false_message)
                                    return

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

                            elif placed_card_id == 33:
                                print(f"시체 폭발(33) -> placed_card_id: {placed_card_id}")
                                card_id = current_field_unit.get_card_number()
                                print(current_field_unit.get_index())
                                print(current_field_unit.get_card_number())

                                opponent_field_unit_object_list = self.opponent_field_unit_repository.get_current_field_unit_card_object_list()
                                if opponent_field_unit_object_list == [] or len(opponent_field_unit_object_list) == 0:
                                    self.return_to_initial_location()
                                    return
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

                            else:
                                self.return_to_initial_location()

                            self.selected_object = None
                            return


                        elif card_type == CardType.ENERGY.value:

                            print("에너지를 붙입니다!")
                            card_id = self.selected_object.get_card_number()

                            if card_id == 151:
                                response = self.your_hand_repository.request_use_energy_card_to_unit(
                                    RequestUseSpecialEnergyCardToUnit(
                                        _sessionInfo=self.__session_repository.get_first_fake_session_info(),
                                        _unitIndex=unit_index,
                                        _energyCardId=card_id)
                                )

                                print(f"response: {response}")
                                is_success_value = response.get('is_success', False)

                                if is_success_value == False:
                                    self.return_to_initial_location()
                                    self.reset_every_selected_action()
                                    is_false_message = response.get('false_message_enum')
                                    self.message_on_the_screen.create_message_on_the_battle_screen(
                                        is_false_message)
                                    return

                                self.your_field_unit_repository.update_your_unit_extra_effect_at_index(unit_index, ["DarkFire","Freeze"])
                                print('attached extra effect to unit at index ', unit_index)
                            else:
                                response = self.your_hand_repository.request_use_energy_card_to_unit(
                                    RequestUseEnergyCardToUnit(
                                        _sessionInfo=self.__session_repository.get_first_fake_session_info(),
                                        _unitIndex=unit_index,
                                        _energyCardId=card_id)
                                )

                                print(f"response: {response}")
                                is_success_value = response.get('is_success', False)

                                if is_success_value == False:
                                    self.return_to_initial_location()
                                    self.reset_every_selected_action()
                                    is_false_message = response.get('false_message_enum')
                                    self.message_on_the_screen.create_message_on_the_battle_screen(
                                        is_false_message)
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



                                # print(f"placed_card_id : {placed_card_id}사용")
                                # card_freezing_image_circle = (
                                #     your_fixed_field_unit.creat_fixed_card_freezing_image_circle(
                                #         image_data=self.pre_drawed_image_instance.get_pre_draw_freezing_energy(),
                                #         vertices=(20, 50)
                                #     )
                                # )
                                # card_dark_flame_image_circle = (
                                #     your_fixed_field_unit.creat_fixed_card_dark_flame_image_circle(
                                #         image_data=self.pre_drawed_image_instance.get_pre_draw_dark_flame_energy(),
                                #         vertices=(40, 100)
                                #     )
                                # )
                                # fixed_card_base.set_attached_shapes(card_freezing_image_circle)
                                # fixed_card_base.set_attached_shapes(card_dark_flame_image_circle)
                                # print(
                                #     f"fixed_card_base.get_attached_shapes() : {fixed_card_base.get_attached_shapes()}")





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

            if isinstance(drop_action_result ,int):
                self.return_to_initial_location()
                self.reset_every_selected_action()
                self.message_on_the_screen.create_message_on_the_battle_screen(drop_action_result)
            # elif drop_action_result is MessageNumber.CARD_UNAVAILABLE_OPPONENT_TURN.value:
            #     print("상대턴 사용 불가")
            #     self.return_to_initial_location()
            #     self.reset_every_selected_action()
            #     self.message_on_the_screen.create_message_on_the_battle_screen(drop_action_result)
            elif drop_action_result is None or drop_action_result is FieldAreaAction.Dummy:
                print("self.field_area_inside_handler.get_field_area_action() = None")
                self.selected_object = None
                self.return_to_initial_location()
            elif drop_action_result is FieldAreaAction.ENERGY_BOOST:
                print("self.field_area_inside_handler.get_field_area_action() = EnergyBoost")
                self.return_to_initial_location()
                self.field_area_inside_handler.set_placed_card_page(self.your_hand_repository.get_current_your_hand_page())
            else:
                print("self.field_area_inside_handler.get_field_area_action() = Some Action")
                # self.selected_object = None
                self.return_to_initial_location()
                self.field_area_inside_handler.set_placed_card_page(
                    self.your_hand_repository.get_current_your_hand_page())
                print(f"추정된 필드 액션 : {self.field_area_inside_handler.get_field_area_action()}")
                if drop_action_result is FieldAreaAction.PLACE_UNIT:
                    self.field_area_inside_handler.clear_field_area_action()
                    self.selected_object = None
                if drop_action_result is FieldAreaAction.DRAW_DECK:
                    self.field_area_inside_handler.clear_field_area_action()
                    self.selected_object = None
                if drop_action_result is FieldAreaAction.REQUIRED_FIRST_PASSIVE_SKILL_PROCESS:
                    self.selected_object = None
                # 서포트 관련하여 시작 포인트
                # handler에서 id 와 index를 받아서 저장 해놓고
                # false가 떳을 경우의 함수를 추가하여 return값으로 selection_object를 주는 함수를 만든다.

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

    #화면 좌클릭
    def on_canvas_left_click(self, event):
        try:
            x, y = event.x, event.y
            y = self.winfo_reqheight() - y
            print(f"x: {x}, y: {y}")

            # if self.is_playing_action_animation:
            #     return

            # if len(self.battle_result_panel_list) != 0:
            if self.battle_field_repository.get_is_game_end():
                # print(self.battle_result_panel_list)

                self.battle_field_function_controller.callGameEndReward()
                self.repository_clear()
                self.battle_result_panel_list = []
                return

            if self.current_field_message_on_the_battle_screen_panel is not None:
                self.message_on_the_screen.clear_current_message_on_the_battle_screen()

            if self.current_fixed_details_card is not None:
                self.current_fixed_details_card = None

            if self.active_panel_rectangle is not None:
                self.active_panel_rectangle = None

            if self.opponent_details_panel_rectangle is not None:
                self.opponent_details_panel_rectangle = None

            if self.your_hand_details_panel_rectangle is not None:
                self.your_hand_details_panel_rectangle = None

            if self.opponent_details_panel.get_opponent_details_panel_button() is not None:
                if self.opponent_details_panel.is_point_inside_details_button((x, y)):
                    print("상대방 상세 보기 클릭")

                    opponent_field_unit_id = self.opponent_selected_object.get_card_number()
                    opponent_field_unit_index = self.opponent_selected_object.get_index()
                    opponent_field_unit_attached_energy = self.opponent_field_unit_repository.get_attached_energy_info()

                    select_details_card = FixedDetailsCard((self.width / 2 - 150, self.height / 2 - (150 * 1.618)))
                    select_details_card.init_card(opponent_field_unit_id)
                    select_details_card_base = select_details_card.get_fixed_card_base()
                    select_details_card_base_vertices = select_details_card_base.get_vertices()

                    opponent_field_unit_extra_effect_info = (
                        self.opponent_field_unit_repository.get_opponent_unit_extra_ability_at_index(opponent_field_unit_index))

                    print(f"opponent_field_unit_extra_effect_info : {opponent_field_unit_extra_effect_info}")

                    opponent_field_unit_total_energy = opponent_field_unit_attached_energy.get_total_energy_at_index(
                        opponent_field_unit_index)
                    print(f"opponent_field_unit_total_energy: {opponent_field_unit_total_energy}")


                    if opponent_field_unit_total_energy:
                        opponent_field_unit_attached_energy_info = opponent_field_unit_attached_energy.get_energy_info_at_index(
                            opponent_field_unit_id)
                        print(f"opponent_field_unit_attached_energy_info: {opponent_field_unit_attached_energy_info}")

                        opponent_field_unit_attached_undead_energy = opponent_field_unit_attached_energy.get_race_energy_at_index(
                            opponent_field_unit_index, EnergyType.Undead)
                        print(f"opponent_field_unit_attached_undead_energy: {opponent_field_unit_attached_undead_energy}")
                        opponent_field_unit_attached_human_energy = opponent_field_unit_attached_energy.get_race_energy_at_index(
                            opponent_field_unit_index, EnergyType.Human)
                        print(f"your_field_unit_attached_human_energy: {opponent_field_unit_attached_human_energy}")
                        opponent_field_unit_attached_trent_energy = opponent_field_unit_attached_energy.get_race_energy_at_index(
                            opponent_field_unit_index, EnergyType.Trent)
                        print(f"opponent_field_unit_attached_trent_energy: {opponent_field_unit_attached_trent_energy}")
                        race_energy_count = 0

                        if opponent_field_unit_extra_effect_info is not None:
                            select_details_card_base.set_attached_shapes(
                                select_details_card.creat_fixed_card_dark_flame_image(
                                    image_data=self.pre_drawed_image_instance.get_pre_draw_dark_flame_energy(),
                                    local_translation=select_details_card_base.get_local_translation(),
                                    vertices=[(select_details_card_base_vertices[2][0] + 30,
                                              select_details_card_base_vertices[2][1] - 25),
                                              (select_details_card_base_vertices[2][0] + 80,
                                              select_details_card_base_vertices[2][1] - 25),
                                              (select_details_card_base_vertices[2][0] + 80,
                                              select_details_card_base_vertices[2][1] + 25),
                                              (select_details_card_base_vertices[2][0] + 30,
                                              select_details_card_base_vertices[2][1] + 25)
                                              ]
                                )
                            )

                            select_details_card_base.set_attached_shapes(
                                select_details_card.creat_fixed_card_freezing_image(
                                    image_data=self.pre_drawed_image_instance.get_pre_draw_freezing_energy(),
                                    local_translation=select_details_card_base.get_local_translation(),
                                    vertices=[(select_details_card_base_vertices[2][0] + 80,
                                              select_details_card_base_vertices[2][1] - 25),
                                              (select_details_card_base_vertices[2][0] + 130,
                                              select_details_card_base_vertices[2][1] - 25),
                                              (select_details_card_base_vertices[2][0] + 130,
                                              select_details_card_base_vertices[2][1] + 25),
                                              (select_details_card_base_vertices[2][0] + 80,
                                              select_details_card_base_vertices[2][1] + 25)
                                              ]
                                )
                            )

                        # 언데드 에너지 갯수에 따른 표시
                        if opponent_field_unit_attached_undead_energy > 0:
                            print("상세 보기 언데드 생성")
                            energy_length = race_energy_count * 80
                            select_details_card_base.set_attached_shapes(
                                select_details_card.creat_fixed_card_energy_race_circle(
                                    image_data=self.pre_drawed_image_instance.get_pre_draw_energy_race_with_race_number(
                                        EnergyType.Undead.value),
                                    local_translation=select_details_card_base.get_local_translation(),
                                    vertices=(select_details_card_base_vertices[0][0] - 220 + energy_length,
                                              select_details_card_base_vertices[0][1] - 40)
                                )
                            )
                            if opponent_field_unit_attached_undead_energy > 1:
                                print("상세 보기 언데드 숫자 생성")
                                select_details_card_base.set_attached_shapes(
                                    select_details_card.create_number_of_cards(
                                        number_of_cards_data=
                                        self.pre_drawed_image_instance.get_pre_draw_number_of_details_energy(
                                            opponent_field_unit_attached_undead_energy),
                                        local_translation=select_details_card_base.get_local_translation(),
                                        vertices=[(select_details_card_base_vertices[0][0] - 200 + energy_length,
                                                   select_details_card_base_vertices[0][1] - 80),
                                                  (select_details_card_base_vertices[0][0] - 160 + energy_length,
                                                   select_details_card_base_vertices[0][1] - 80),
                                                  (select_details_card_base_vertices[0][0] - 160 + energy_length,
                                                   select_details_card_base_vertices[0][1] - 0),
                                                  (select_details_card_base_vertices[0][0] - 200 + energy_length,
                                                   select_details_card_base_vertices[0][1] - 0)
                                                  ]
                                    )
                                )
                            race_energy_count += 1

                        # 휴먼 에너지 갯수에 따른 표시
                        if opponent_field_unit_attached_human_energy > 0:
                            print("상세 보기 휴먼 생성")
                            energy_length = race_energy_count * 80
                            select_details_card_base.set_attached_shapes(
                                select_details_card.creat_fixed_card_energy_race_circle(
                                    image_data=self.pre_drawed_image_instance.get_pre_draw_energy_race_with_race_number(
                                        EnergyType.Human.value),
                                    local_translation=select_details_card_base.get_local_translation(),
                                    vertices=(select_details_card_base_vertices[0][0] - 220 + energy_length,
                                              select_details_card_base_vertices[0][1] - 40)
                                )
                            )

                            if opponent_field_unit_attached_human_energy > 1:
                                print("상세 보기 휴먼 숫자 생성")
                                select_details_card_base.set_attached_shapes(
                                    select_details_card.create_number_of_cards(
                                        number_of_cards_data=
                                        self.pre_drawed_image_instance.get_pre_draw_number_of_details_energy(
                                            opponent_field_unit_attached_human_energy),
                                        local_translation=select_details_card_base.get_local_translation(),
                                        vertices=[(select_details_card_base_vertices[0][0] - 200 + energy_length,
                                                   select_details_card_base_vertices[0][1] - 80),
                                                  (select_details_card_base_vertices[0][0] - 160 + energy_length,
                                                   select_details_card_base_vertices[0][1] - 80),
                                                  (select_details_card_base_vertices[0][0] - 160 + energy_length,
                                                   select_details_card_base_vertices[0][1] - 0),
                                                  (select_details_card_base_vertices[0][0] - 200 + energy_length,
                                                   select_details_card_base_vertices[0][1] - 0)
                                                  ]
                                    )
                                )
                            race_energy_count += 1

                        # 트런트 에너지 갯수에 따른 표시
                        if opponent_field_unit_attached_trent_energy > 0:
                            print("상세 보기 트런트 생성")
                            energy_length = race_energy_count * 80
                            select_details_card_base.set_attached_shapes(
                                select_details_card.creat_fixed_card_energy_race_circle(
                                    image_data=self.pre_drawed_image_instance.get_pre_draw_energy_race_with_race_number(
                                        EnergyType.Trent.value),
                                    local_translation=select_details_card_base.get_local_translation(),
                                    vertices=(select_details_card_base_vertices[0][0] - 220 + race_energy_count * 80,
                                              select_details_card_base_vertices[0][1] - 40)
                                )
                            )

                            if opponent_field_unit_attached_trent_energy > 1:
                                print("상세 보기 트런트 숫자 생성")
                                select_details_card_base.set_attached_shapes(
                                    select_details_card.create_number_of_cards(
                                        number_of_cards_data=
                                        self.pre_drawed_image_instance.get_pre_draw_number_of_details_energy(
                                            opponent_field_unit_attached_trent_energy),
                                        local_translation=select_details_card_base.get_local_translation(),
                                        vertices=[(select_details_card_base_vertices[0][0] - 200 + energy_length,
                                                   select_details_card_base_vertices[0][1] - 80),
                                                  (select_details_card_base_vertices[0][0] - 160 + energy_length,
                                                   select_details_card_base_vertices[0][1] - 80),
                                                  (select_details_card_base_vertices[0][0] - 160 + energy_length,
                                                   select_details_card_base_vertices[0][1] - 0),
                                                  (select_details_card_base_vertices[0][0] - 200 + energy_length,
                                                   select_details_card_base_vertices[0][1] - 0)
                                                  ]
                                    )
                                )

                    self.current_fixed_details_card = select_details_card_base
                    self.opponent_details_panel_rectangle = None
                    self.opponent_details_panel.clear_all_opponent_details_panel()
                    return

            if self.your_hand_details_panel.get_your_hand_details_panel_button() is not None:
                if self.your_hand_details_panel.is_point_inside_details_button((x, y)):
                    print("내 손에 있는 카드 상세 보기")
                    your_hand_card_id = self.selected_object.get_card_number()

                    select_details_card = FixedDetailsCard((self.width / 2 - 150, self.height / 2 - (150 * 1.618)))
                    select_details_card.init_card(your_hand_card_id)
                    select_details_card_base = select_details_card.get_fixed_card_base()

                    self.current_fixed_details_card = select_details_card_base
                    self.your_hand_details_panel_rectangle = None
                    self.your_hand_details_panel.clear_all_your_hand_details_panel()
                    return

            if self.your_active_panel.get_your_active_panel_attack_button() is not None:
                if self.your_active_panel.is_point_inside_attack_button((x, y)):
                    your_field_unit_index = self.selected_object.get_index()

                    your_selected_unit_action_status = self.your_field_unit_action_repository.get_current_field_unit_action_status(
                        your_field_unit_index)

                    if your_selected_unit_action_status == FieldUnitActionStatus.WAIT:
                        print(f"처음 필드에 출격한 유닛은 공격 할 수 없습니다")
                        # self.selected_object = None
                        # self.current_fixed_details_card = None
                        # self.active_panel_rectangle = None
                        # self.current_fixed_details_card = None
                        # self.your_active_panel.clear_all_your_active_panel()
                        self.reset_every_selected_action()
                        self.message_on_the_screen.create_message_on_the_battle_screen(MessageNumber.CARD_UNABLE_ATTACK_SUMMON_TURN.value)
                        return

                    elif your_selected_unit_action_status == FieldUnitActionStatus.Dummy:
                        print(f"Dummy 상태입니다")
                        return

                    your_selected_unit_action_count = self.your_field_unit_action_repository.get_current_field_unit_action_count(
                        your_field_unit_index)

                    if your_selected_unit_action_count <= 0:
                        print("행동을 마친 유닛은 더 이상 공격 할 수 없습니다")
                        # self.selected_object = None
                        # self.active_panel_rectangle = None
                        # self.current_fixed_details_card = None
                        # self.your_active_panel.clear_all_your_active_panel()
                        self.reset_every_selected_action()
                        self.message_on_the_screen.create_message_on_the_battle_screen(MessageNumber.CARD_UNABLE_ATTACK_LACK_ACTION_COUNT.value)
                        return

                    print("일반 공격 클릭")

                    your_field_unit_id = self.selected_object.get_card_number()
                    your_field_unit_index = self.selected_object.get_index()
                    your_field_unit_attached_energy = self.your_field_unit_repository.get_attached_energy_info()

                    your_field_unit_total_energy = your_field_unit_attached_energy.get_total_energy_at_index(
                        your_field_unit_index)
                    print(f"your_field_unit_total_energy: {your_field_unit_total_energy}")

                    your_field_unit_attached_undead_energy = your_field_unit_attached_energy.get_race_energy_at_index(
                        your_field_unit_index, EnergyType.Undead)

                    your_field_unit_required_undead_energy = self.card_info_repository.getCardEnergyForCardNumber(
                        your_field_unit_id)

                    if your_field_unit_required_undead_energy > your_field_unit_attached_undead_energy:
                        print("에너지 부족으로 인한 공격 불가")
                        # self.selected_object = None
                        # self.active_panel_rectangle = None
                        # self.current_fixed_details_card = None
                        # self.your_active_panel.clear_all_your_active_panel()
                        self.reset_every_selected_action()
                        self.message_on_the_screen.create_message_on_the_battle_screen(MessageNumber.CARD_UNABLE_ATTACK_LACK_ENERGY.value)
                        return


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

                    self.attack_animation_object.set_animation_actor(self.selected_object)

                    # self.targeting_ememy_select_using_hand_card_id

                    self.targeting_enemy_select_using_your_field_card_index = your_field_unit_index
                    self.targeting_enemy_select_using_your_field_card_id = your_field_unit_id

                    return

            if self.your_active_panel.get_your_active_panel_first_skill_button() is not None:
                if self.your_active_panel.is_point_inside_first_skill_button((x, y)):
                    your_field_unit_index = self.selected_object.get_index()
                    your_selected_unit_action_count = self.your_field_unit_action_repository.get_current_field_unit_action_count(
                        your_field_unit_index)

                    your_selected_unit_action_status = self.your_field_unit_action_repository.get_current_field_unit_action_status(
                        your_field_unit_index)

                    if your_selected_unit_action_status == FieldUnitActionStatus.WAIT:
                        print(f"처음 필드에 출격한 유닛은 공격 할 수 없습니다")
                        # self.selected_object = None
                        # self.current_fixed_details_card = None
                        # self.active_panel_rectangle = None
                        # self.your_active_panel.clear_all_your_active_panel()
                        self.reset_every_selected_action()
                        self.message_on_the_screen.create_message_on_the_battle_screen(MessageNumber.CARD_UNABLE_ATTACK_SUMMON_TURN.value)
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
                    print(f"your_field_unit_attached_undead_energy: {your_field_unit_attached_undead_energy}")

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
                        print("에너지 부족으로 인한 스킬 사용 불가")
                        # self.selected_object = None
                        # self.active_panel_rectangle = None
                        # self.current_fixed_details_card = None
                        # self.your_active_panel.clear_all_your_active_panel()
                        self.reset_every_selected_action()
                        self.message_on_the_screen.create_message_on_the_battle_screen(MessageNumber.CARD_UNAVAILABLE_USE_SKILL_LACK_ENERGY.value)
                        return

                    if your_field_unit_required_human_energy > your_field_unit_attached_human_energy:
                        # self.selected_object = None
                        # self.active_panel_rectangle = None
                        # self.current_fixed_details_card = None
                        # self.your_active_panel.clear_all_your_active_panel()
                        self.reset_every_selected_action()
                        self.message_on_the_screen.create_message_on_the_battle_screen(MessageNumber.CARD_UNAVAILABLE_USE_SKILL_LACK_ENERGY.value)
                        return

                    if your_field_unit_required_trent_energy > your_field_unit_attached_trent_energy:
                        # self.selected_object = None
                        # self.active_panel_rectangle = None
                        # self.current_fixed_details_card = None
                        # self.your_active_panel.clear_all_your_active_panel()
                        self.reset_every_selected_action()
                        self.message_on_the_screen.create_message_on_the_battle_screen(MessageNumber.CARD_UNAVAILABLE_USE_SKILL_LACK_ENERGY.value)
                        return

                    skill_type = self.card_info_repository.getCardSkillFirstForCardNumber(your_field_unit_id)
                    print(f"skill_type: {skill_type}")

                    if your_selected_unit_action_count <= 0:
                        print("행동을 마친 유닛은 더 이상 공격 할 수 없습니다")
                        # self.selected_object = None
                        # self.active_panel_rectangle = None
                        # self.current_fixed_details_card = None
                        # self.your_active_panel.clear_all_your_active_panel()
                        self.reset_every_selected_action()
                        self.message_on_the_screen.create_message_on_the_battle_screen(MessageNumber.CARD_UNABLE_ATTACK_LACK_ACTION_COUNT.value)
                        return

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

                    your_selected_unit_action_status = self.your_field_unit_action_repository.get_current_field_unit_action_status(
                        your_field_unit_index)

                    if your_selected_unit_action_status == FieldUnitActionStatus.WAIT:
                        print(f"처음 필드에 출격한 유닛은 공격 할 수 없습니다")
                        self.reset_every_selected_action()
                        # self.selected_object = None
                        # self.current_fixed_details_card = None
                        # self.active_panel_rectangle = None
                        # self.current_fixed_details_card = None
                        # self.your_active_panel.clear_all_your_active_panel()
                        self.message_on_the_screen.create_message_on_the_battle_screen(MessageNumber.CARD_UNABLE_ATTACK_SUMMON_TURN.value)
                        return
                    elif your_selected_unit_action_status == FieldUnitActionStatus.Dummy:
                        print(f"Dummy 상태입니다")
                        return

                    print("두 번째 스킬 클릭")

                    # your_field_card_index = self.targeting_enemy_select_using_your_field_card_index
                    # print(f"스킬 사용 확정 -> your_field_card_index: {your_field_card_index}")
                    # self.your_field_unit_action_repository.use_field_unit_action_count_by_index(your_field_unit_index)

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
                        # self.selected_object = None
                        # self.active_panel_rectangle = None
                        # self.current_fixed_details_card = None
                        # self.your_active_panel.clear_all_your_active_panel()
                        self.reset_every_selected_action()
                        self.message_on_the_screen.create_message_on_the_battle_screen(MessageNumber.CARD_UNAVAILABLE_USE_SKILL_LACK_ENERGY.value)
                        return

                    if your_field_unit_required_human_energy > your_field_unit_attached_human_energy:
                        self.reset_every_selected_action()
                        # self.selected_object = None
                        # self.active_panel_rectangle = None
                        # self.current_fixed_details_card = None
                        # self.your_active_panel.clear_all_your_active_panel()
                        self.message_on_the_screen.create_message_on_the_battle_screen(MessageNumber.CARD_UNAVAILABLE_USE_SKILL_LACK_ENERGY.value)
                        return

                    if your_field_unit_required_trent_energy > your_field_unit_attached_trent_energy:
                        self.reset_every_selected_action()
                        # self.selected_object = None
                        # self.active_panel_rectangle = None
                        # self.current_fixed_details_card = None
                        # self.your_active_panel.clear_all_your_active_panel()
                        self.message_on_the_screen.create_message_on_the_battle_screen(MessageNumber.CARD_UNAVAILABLE_USE_SKILL_LACK_ENERGY.value)
                        return

                    if your_selected_unit_action_count <= 0:
                        print("행동을 마친 유닛은 더 이상 공격 할 수 없습니다")
                        self.reset_every_selected_action()
                        # self.selected_object = None
                        # self.active_panel_rectangle = None
                        # self.current_fixed_details_card = None
                        # self.your_active_panel.clear_all_your_active_panel()
                        self.message_on_the_screen.create_message_on_the_battle_screen(MessageNumber.CARD_UNABLE_ATTACK_LACK_ACTION_COUNT.value)
                        return

                    skill_type = self.card_info_repository.getCardSkillSecondForCardNumber(your_field_unit_id)
                    print(f"skill_type: {skill_type}")

                    # 단일기
                    if skill_type == 1:
                        pass

                    # 광역기
                    elif skill_type == 2:


                        response = self.__fake_battle_field_frame_repository.request_attack_opponent_unit(
                            RequestAttackWithNonTargetingActiveSkill(
                                _sessionInfo = self.__session_repository.get_first_fake_session_info(),
                                _unitCardIndex = your_field_unit_index
                            )
                        )

                        print(f"non targeting active skill response : {response}")

                        if response.get('is_success',False) == False:
                            print('non targeting active skill error!! ')
                            self.reset_every_selected_action()
                            is_false_message = response.get('false_message_enum')
                            self.message_on_the_screen.create_message_on_the_battle_screen(
                                is_false_message)
                            return



                        damage = self.card_info_repository.getCardSkillSecondDamageForCardNumber(your_field_unit_id)
                        self.attack_animation_object.set_animation_actor(self.selected_object)
                        self.attack_animation_object.set_animation_actor_damage(damage)

                        self.your_field_unit_action_repository.use_field_unit_action_count_by_index(
                            your_field_unit_index)

                        extra_ability = self.your_field_unit_repository.get_your_unit_extra_ability_at_index(your_field_unit_index)
                        self.attack_animation_object.set_extra_ability(extra_ability)

                        self.field_area_inside_handler.set_field_area_action(FieldAreaAction.PLAY_ANIMATION)

                        self.master.after(0, self.wide_area_attack_animation)

                        # try:
                        #     for unit_index, remain_hp in response['player_field_unit_health_point_map']['Opponent']['field_unit_health_point_map'].items():
                        #         opponent_field_unit = self.opponent_field_unit_repository.get_current_field_unit_card_object_list()[int(unit_index)]
                        #         if opponent_field_unit is None:
                        #             continue
                        #         fixed_card_base = opponent_field_unit.get_fixed_card_base()
                        #         attached_shape_list = fixed_card_base.get_attached_shapes()
                        #
                        #         # TODO: 가만 보면 이 부분이 은근히 많이 사용되고 있음 (중복 많이 발생함)
                        #         for attached_shape in attached_shape_list:
                        #             if isinstance(attached_shape, NonBackgroundNumberImage):
                        #                 if attached_shape.get_circle_kinds() is CircleKinds.HP:
                        #                     attached_shape.set_number(remain_hp)
                        #
                        #                     attached_shape.set_image_data(
                        #                         self.pre_drawed_image_instance.get_pre_draw_unit_hp(remain_hp))
                        # except Exception as e:
                        #     print('no field units!! : ', e)
                        #
                        # try:
                        #     dead_unit_index_list = \
                        #         response['player_field_unit_death_map']['Opponent']['dead_field_unit_index_list']
                        #
                        #     for dead_unit_index in dead_unit_index_list:
                        #         card_id = self.opponent_field_unit_repository.get_opponent_card_id_by_index(dead_unit_index)
                        #
                        #         self.opponent_field_unit_repository.remove_current_field_unit_card(dead_unit_index)
                        #         self.opponent_tomb_repository.create_opponent_tomb_card(card_id)
                        #
                        #     self.opponent_field_unit_repository.replace_opponent_field_unit_card_position()
                        # except Exception as e:
                        #     print('no dead units!! : ', e)



                        # damage = self.card_info_repository.getCardSkillSecondDamageForCardNumber(your_field_unit_id)
                        # print(f"wide area damage: {damage}")
                        #
                        # # TODO: 즉발이므로 대기 액션이 필요없음 (서버와의 통신을 위해 대기가 발생 할 수 있긴함) 그 때 가서 추가
                        # for index in range(
                        #         len(self.opponent_field_unit_repository.get_current_field_unit_card_object_list()) - 1,
                        #         -1,
                        #         -1):
                        #     opponent_field_unit = \
                        #         self.opponent_field_unit_repository.get_current_field_unit_card_object_list()[index]
                        #
                        #     if opponent_field_unit is None:
                        #         continue
                        #
                        #     remove_from_field = False
                        #
                        #     fixed_card_base = opponent_field_unit.get_fixed_card_base()
                        #     attached_shape_list = fixed_card_base.get_attached_shapes()
                        #
                        #     # TODO: 가만 보면 이 부분이 은근히 많이 사용되고 있음 (중복 많이 발생함)
                        #     for attached_shape in attached_shape_list:
                        #         if isinstance(attached_shape, NonBackgroundNumberImage):
                        #             if attached_shape.get_circle_kinds() is CircleKinds.HP:
                        #
                        #                 hp_number = attached_shape.get_number()
                        #                 hp_number -= damage
                        #
                        #                 # TODO: n 턴간 불사 특성을 검사해야하므로 사실 이것도 summary 방식으로 빼는 것이 맞으나 우선은 진행한다.
                        #                 # (지금 당장 불사가 존재하지 않음)
                        #                 if hp_number <= 0:
                        #                     remove_from_field = True
                        #                     break
                        #
                        #                 print(f"contract_of_doom -> hp_number: {hp_number}")
                        #                 attached_shape.set_number(hp_number)
                        #
                        #                 # attached_shape.set_image_data(
                        #                 #     # TODO: 실제로 여기서 서버로부터 계산 받은 값을 적용해야함
                        #                 #     self.pre_drawed_image_instance.get_pre_draw_number_image(hp_number))
                        #
                        #                 attached_shape.set_image_data(
                        #                     self.pre_drawed_image_instance.get_pre_draw_unit_hp(hp_number))
                        #
                        #     if remove_from_field:
                        #         card_id = opponent_field_unit.get_card_number()
                        #
                        #         self.opponent_field_unit_repository.remove_current_field_unit_card(index)
                        #         self.opponent_tomb_repository.create_opponent_tomb_card(card_id)
                        #
                        # self.opponent_field_unit_repository.replace_opponent_field_unit_card_position()

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
                    your_field_unit_id = self.selected_object.get_card_number()
                    your_field_unit_index = self.selected_object.get_index()
                    your_field_unit_attached_energy = self.your_field_unit_repository.get_attached_energy_info()

                    select_details_card = FixedDetailsCard((self.width / 2 - 150, self.height / 2 - (150 * 1.618)))
                    select_details_card.init_card(your_field_unit_id)
                    select_details_card_base = select_details_card.get_fixed_card_base()
                    select_details_card_base_vertices = select_details_card_base.get_vertices()

                    your_field_unit_extra_effect_info = (
                        self.your_field_unit_repository.get_your_unit_extra_ability_at_index(your_field_unit_index))

                    print(f"your_field_unit_extra_effect_info : {your_field_unit_extra_effect_info}")

                    your_field_unit_total_energy = your_field_unit_attached_energy.get_total_energy_at_index(
                        your_field_unit_index)
                    print(f"your_field_unit_total_energy: {your_field_unit_total_energy}")

                    if your_field_unit_total_energy:
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
                        race_energy_count = 0

                        if your_field_unit_extra_effect_info is not None:
                            select_details_card_base.set_attached_shapes(
                                select_details_card.creat_fixed_card_dark_flame_image(
                                    image_data=self.pre_drawed_image_instance.get_pre_draw_dark_flame_energy(),
                                    local_translation=select_details_card_base.get_local_translation(),
                                    vertices=[(select_details_card_base_vertices[2][0] + 30,
                                              select_details_card_base_vertices[2][1] - 25),
                                              (select_details_card_base_vertices[2][0] + 80,
                                              select_details_card_base_vertices[2][1] - 25),
                                              (select_details_card_base_vertices[2][0] + 80,
                                              select_details_card_base_vertices[2][1] + 25),
                                              (select_details_card_base_vertices[2][0] + 30,
                                              select_details_card_base_vertices[2][1] + 25)
                                              ]
                                )
                            )

                            select_details_card_base.set_attached_shapes(
                                select_details_card.creat_fixed_card_freezing_image(
                                    image_data=self.pre_drawed_image_instance.get_pre_draw_freezing_energy(),
                                    local_translation=select_details_card_base.get_local_translation(),
                                    vertices=[(select_details_card_base_vertices[2][0] + 80,
                                              select_details_card_base_vertices[2][1] - 25),
                                              (select_details_card_base_vertices[2][0] + 130,
                                              select_details_card_base_vertices[2][1] - 25),
                                              (select_details_card_base_vertices[2][0] + 130,
                                              select_details_card_base_vertices[2][1] + 25),
                                              (select_details_card_base_vertices[2][0] + 80,
                                              select_details_card_base_vertices[2][1] + 25)
                                              ]
                                )
                            )

                        # 언데드 에너지 갯수에 따른 표시
                        if your_field_unit_attached_undead_energy > 0:
                            print("상세 보기 언데드 생성")
                            energy_length = race_energy_count * 80
                            select_details_card_base.set_attached_shapes(
                                select_details_card.creat_fixed_card_energy_race_circle(
                                    image_data=self.pre_drawed_image_instance.get_pre_draw_energy_race_with_race_number(
                                        EnergyType.Undead.value),
                                    local_translation=select_details_card_base.get_local_translation(),
                                    vertices=(select_details_card_base_vertices[0][0] - 220 + energy_length,
                                              select_details_card_base_vertices[0][1] - 40)
                                )
                            )
                            if your_field_unit_attached_undead_energy > 1:
                                print("상세 보기 언데드 숫자 생성")
                                select_details_card_base.set_attached_shapes(
                                    select_details_card.create_number_of_cards(
                                        number_of_cards_data=
                                        self.pre_drawed_image_instance.get_pre_draw_number_of_details_energy(
                                            your_field_unit_attached_undead_energy),
                                        local_translation=select_details_card_base.get_local_translation(),
                                        vertices=[(select_details_card_base_vertices[0][0] - 200 + energy_length,
                                                   select_details_card_base_vertices[0][1] - 80),
                                                  (select_details_card_base_vertices[0][0] - 160 + energy_length,
                                                   select_details_card_base_vertices[0][1] - 80),
                                                  (select_details_card_base_vertices[0][0] - 160 + energy_length,
                                                   select_details_card_base_vertices[0][1] - 0),
                                                  (select_details_card_base_vertices[0][0] - 200 + energy_length,
                                                   select_details_card_base_vertices[0][1] - 0)
                                                  ]
                                    )
                                )
                            race_energy_count += 1

                        # 휴먼 에너지 갯수에 따른 표시
                        if your_field_unit_attached_human_energy > 0:
                            print("상세 보기 휴먼 생성")
                            energy_length = race_energy_count * 80
                            select_details_card_base.set_attached_shapes(
                                select_details_card.creat_fixed_card_energy_race_circle(
                                    image_data=self.pre_drawed_image_instance.get_pre_draw_energy_race_with_race_number(
                                        EnergyType.Human.value),
                                    local_translation=select_details_card_base.get_local_translation(),
                                    vertices=(select_details_card_base_vertices[0][0] - 220 + energy_length,
                                              select_details_card_base_vertices[0][1] - 40)
                                )
                            )

                            if your_field_unit_attached_human_energy > 1:
                                print("상세 보기 휴먼 숫자 생성")
                                select_details_card_base.set_attached_shapes(
                                    select_details_card.create_number_of_cards(
                                        number_of_cards_data=
                                        self.pre_drawed_image_instance.get_pre_draw_number_of_details_energy(
                                            your_field_unit_attached_human_energy),
                                        local_translation=select_details_card_base.get_local_translation(),
                                        vertices=[(select_details_card_base_vertices[0][0] - 200 + energy_length,
                                                   select_details_card_base_vertices[0][1] - 80),
                                                  (select_details_card_base_vertices[0][0] - 160 + energy_length,
                                                   select_details_card_base_vertices[0][1] - 80),
                                                  (select_details_card_base_vertices[0][0] - 160 + energy_length,
                                                   select_details_card_base_vertices[0][1] - 0),
                                                  (select_details_card_base_vertices[0][0] - 200 + energy_length,
                                                   select_details_card_base_vertices[0][1] - 0)
                                                  ]
                                    )
                                )
                            race_energy_count += 1

                        # 트런트 에너지 갯수에 따른 표시
                        if your_field_unit_attached_trent_energy > 0:
                            print("상세 보기 트런트 생성")
                            energy_length = race_energy_count * 80
                            select_details_card_base.set_attached_shapes(
                                select_details_card.creat_fixed_card_energy_race_circle(
                                    image_data=self.pre_drawed_image_instance.get_pre_draw_energy_race_with_race_number(
                                        EnergyType.Trent.value),
                                    local_translation=select_details_card_base.get_local_translation(),
                                    vertices=(select_details_card_base_vertices[0][0] - 220 + race_energy_count * 80,
                                              select_details_card_base_vertices[0][1] - 40)
                                )
                            )

                            if your_field_unit_attached_trent_energy > 1:
                                print("상세 보기 트런트 숫자 생성")
                                select_details_card_base.set_attached_shapes(
                                    select_details_card.create_number_of_cards(
                                        number_of_cards_data=
                                        self.pre_drawed_image_instance.get_pre_draw_number_of_details_energy(
                                            your_field_unit_attached_trent_energy),
                                        local_translation=select_details_card_base.get_local_translation(),
                                        vertices=[(select_details_card_base_vertices[0][0] - 200 + energy_length,
                                                   select_details_card_base_vertices[0][1] - 80),
                                                  (select_details_card_base_vertices[0][0] - 160 + energy_length,
                                                   select_details_card_base_vertices[0][1] - 80),
                                                  (select_details_card_base_vertices[0][0] - 160 + energy_length,
                                                   select_details_card_base_vertices[0][1] - 0),
                                                  (select_details_card_base_vertices[0][0] - 200 + energy_length,
                                                   select_details_card_base_vertices[0][1] - 0)
                                                  ]
                                    )
                                )

                    self.current_fixed_details_card = select_details_card_base
                    self.active_panel_rectangle = None
                    self.your_active_panel.clear_all_your_active_panel()
                    self.selected_object = None
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
                        self.timer.stop_timer()
                        self.battle_field_function_controller.callSurrender()
                        self.is_playing_action_animation = False
                        self.field_area_inside_handler.clear_field_area_action()
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
                    # print(f"hand_card: {hand_card}")
                    # for hand_card in reversed(self.your_hand_repository.get_current_page_your_hand_list()):
                    pickable_card_base = hand_card.get_pickable_card_base()
                    pickable_card_base.set_width_ratio(self.width_ratio)
                    pickable_card_base.set_height_ratio(self.height_ratio)

                    if pickable_card_base.is_point_inside((x, y)):
                        self.__music_player_repository.play_sound_effect_of_mouse_on_click('hand_card_pick')
                        print("카드 선택!")
                        hand_card.selected = not hand_card.selected
                        self.selected_object = hand_card
                        self.drag_start = (x, y)

                        if self.selected_object != self.prev_selected_object:
                            self.your_active_panel.clear_all_your_active_panel()
                            self.active_panel_rectangle = None
                            self.current_fixed_details_card = None

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

                        # 내 턴 아닐 때 붙이면 안됨

                        # response = self.__field_energy_application.send_request_to_attach_field_energy_to_unit(
                        #     unitIndex=unit_index, energyRace = energy_race, energyCount=energy_count
                        # )
                        if not response.get('is_success'):
                            self.reset_every_selected_action()
                            is_false_message = response.get('false_message_enum')
                            self.message_on_the_screen.create_message_on_the_battle_screen(
                                is_false_message)
                            return

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
                print(f"{Fore.RED}일반 공격 진행 -> self.selected_object{Fore.GREEN} {self.selected_object}{Style.RESET_ALL}")

                if self.opponent_main_character.is_point_inside((x, y)):
                    print("메인 캐릭터 공격")

                    your_field_card_index = self.targeting_enemy_select_using_your_field_card_index

                    # Todo : response방식 변경 필요
                    response = self.__fake_battle_field_frame_repository.request_attack_main_character(
                        RequestAttackMainCharacter(
                            _sessionInfo=self.__session_repository.get_first_fake_session_info(),
                            _attacker_unit_index=your_field_card_index,
                            _target_game_main_character_index="0")
                    )
                    print(f"{Fore.RED}attack main character -> response:{Fore.GREEN} {response}{Style.RESET_ALL}")
                    is_success_value = response.get('is_success', False)

                    if is_success_value == False:
                        self.reset_every_selected_action()
                        is_false_message = response.get('false_message_enum')
                        self.message_on_the_screen.create_message_on_the_battle_screen(
                            is_false_message)
                        return

                    self.attack_animation_object.set_opponent_main_character(self.opponent_main_character_panel)
                    self.your_field_unit_action_repository.use_field_unit_action_count_by_index(your_field_card_index)

                    your_field_card_id = self.targeting_enemy_select_using_your_field_card_id
                    print(f"your_field_card_id: {your_field_card_id}")

                    your_damage = self.card_info_repository.getCardAttackForCardNumber(your_field_card_id)
                    print(f"your_damage: {your_damage}")

                    self.attack_animation_object.set_animation_actor_damage(your_damage)


                    your_unit_job_number = self.card_info_repository.getCardJobForCardNumber(your_field_card_id)
                    your_effect_animation_name = ''
                    for attack_type in AttackType:
                        if attack_type.value == your_unit_job_number:
                            your_effect_animation_name = attack_type.name
                            print('your effect animation name: ', your_effect_animation_name)
                            break

                    effect_animation = EffectAnimation()
                    effect_animation.set_animation_name(your_effect_animation_name)
                    effect_animation.set_total_window_size(self.width, self.height)
                    vertices = self.opponent_main_character_panel.get_vertices()
                    effect_animation.draw_animation_panel_with_vertices(vertices)
                    effect_animation_panel = effect_animation.get_animation_panel()

                    self.effect_animation_repository.save_effect_animation_at_dictionary_with_index(
                        your_field_card_index, effect_animation)

                    self.effect_animation_repository.save_effect_animation_panel_at_dictionary_with_index(
                        your_field_card_index, effect_animation_panel)

                    self.targeting_enemy_select_support_lightning_border_list = []
                    self.opponent_you_selected_lightning_border_list = []

                    self.master.after(0, self.you_attack_main_character_animation)

                    if response.get('player_main_character_survival_map_for_notice',{}).get('Opponent',None) == 'Death':
                        self.opponent_hp_repository.opponent_character_die()
                    # self.opponent_hp_repository.take_damage(your_damage)

                    # self.opponent_fixed_unit_card_inside_handler.clear_opponent_field_area_action()
                    # self.targeting_enemy_select_using_your_field_card_index = None
                    # self.targeting_enemy_select_using_your_field_card_id = None
                    # self.targeting_enemy_select_support_lightning_border_list = []
                    # self.opponent_you_selected_lightning_border_list = []
                    #
                    # self.selected_object = None
                    # self.active_panel_rectangle = None
                    # self.current_fixed_details_card = None
                    # self.your_active_panel.clear_all_your_active_panel()
                    self.reset_every_selected_action()

                    return

                # self.targeting_ememy_select_using_hand_card_id = placed_card_id행
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
                    opponent_field_card_index = opponent_field_unit_object.get_index()
                    print("지정한 상대 유닛 베이스 찾기")
                    print('찾아4')
                    # 애니메이션
                    self.attack_animation_object.set_opponent_field_unit(opponent_field_unit_object)
                    # print(f"{Fore.RED}self.selected_object{Fore.GREEN} {self.selected_object}{Style.RESET_ALL}")
                    # self.attack_animation_object.set_animation_actor(self.selected_object)

                    if opponent_fixed_card_base.is_point_inside((x, y)):
                        your_field_card_index = self.targeting_enemy_select_using_your_field_card_index
                        your_field_card_id = self.targeting_enemy_select_using_your_field_card_id
                        your_unit_job_number = self.card_info_repository.getCardJobForCardNumber(your_field_card_id)
                        your_effect_animation_name = ''
                        for attack_type in AttackType:
                            if attack_type.value == your_unit_job_number:
                                your_effect_animation_name = attack_type.name
                                print('your effect animation name: ', your_effect_animation_name)
                                break

                        effect_animation = EffectAnimation()
                        effect_animation.set_animation_name(your_effect_animation_name)
                        effect_animation.set_total_window_size(self.width, self.height)
                        effect_animation.change_local_translation(
                            self.opponent_field_unit_repository.find_opponent_field_unit_by_index(
                                opponent_field_card_index).get_fixed_card_base().get_local_translation()
                        )
                        effect_animation.draw_animation_panel()
                        effect_animation_panel = effect_animation.get_animation_panel()
                        print(effect_animation_panel)
                        self.effect_animation_repository.save_effect_animation_at_dictionary_with_index(
                            your_field_card_index, effect_animation)
                        self.effect_animation_repository.save_effect_animation_panel_at_dictionary_with_index(
                            your_field_card_index, effect_animation_panel)

                        print(f'save effect animation: {self.effect_animation_repository.get_effect_animation_by_index(your_field_card_index)}')
                        print(f'save effect animation panel: {self.effect_animation_repository.get_effect_animation_panel_by_index(your_field_card_index)}')

                        # self.your_field_unit_action_repository.use_field_unit_action_count_by_index(
                        #     your_field_card_index)

                        attack_opponent_unit_response = self.__fake_battle_field_frame_repository.request_attack_opponent_unit(
                            RequestAttackOpponentUnit(
                                _sessionInfo = self.__session_repository.get_first_fake_session_info(),
                                _attackerUnitIndex = your_field_card_index,
                                _targetUnitIndex = opponent_field_card_index
                            )
                        )

                        print(f"attack unit response : {attack_opponent_unit_response}")

                        if attack_opponent_unit_response.get('is_success', False) == False:
                            print("attack unit failed!! ")
                            self.reset_every_selected_action()
                            is_false_message = attack_opponent_unit_response.get('false_message_enum')
                            self.message_on_the_screen.create_message_on_the_battle_screen(
                                is_false_message)
                            return

                        self.your_field_unit_action_repository.use_field_unit_action_count_by_index(
                            your_field_card_index)

                        # self.opponent_you_selected_lightning_border_list.append(opponent_fixed_card_base)
                        # opponent_fixed_card_attached_shape_list = opponent_fixed_card_base.get_attached_shapes()
                        # are_opponent_field_unit_death = False
                        # opponent_field_card_index = None
                        # opponent_field_card_id = None
                        #
                        # for opponent_fixed_card_attached_shape in opponent_fixed_card_attached_shape_list:
                        #     if isinstance(opponent_fixed_card_attached_shape, NonBackgroundNumberImage):
                        #         if opponent_fixed_card_attached_shape.get_circle_kinds() is CircleKinds.HP:
                        #             print("지정한 상대방 유닛 HP Circle 찾기")
                        #
                        #             # self.targeting_enemy_select_using_your_field_card_index = your_field_unit_index
                        #             # self.targeting_enemy_select_using_your_field_card_id
                        #             # your_field_card_id = self.targeting_ememy_select_using_hand_card_id
                        #             # print(f"your_field_card_id: {your_field_card_id}")
                        #             # your_field_card_index = self.targeting_ememy_select_using_hand_card_index
                        #             # print(f"your_field_card_index: {your_field_card_index}")
                        #             your_field_card_id = self.targeting_enemy_select_using_your_field_card_id
                        #             print(f"your_field_card_id: {your_field_card_id}")
                        #
                        #             your_field_card_index = self.targeting_enemy_select_using_your_field_card_index
                        #             print(f"your_field_card_index: {your_field_card_index}")
                        #
                        #             your_damage = self.card_info_repository.getCardAttackForCardNumber(
                        #                 your_field_card_id)
                        #             print(f"your_damage: {your_damage}")
                        #
                        #             your_field_unit = self.your_field_unit_repository.find_field_unit_by_index(
                        #                 your_field_card_index)
                        #
                        #             your_fixed_card_base = your_field_unit.get_fixed_card_base()
                        #             your_fixed_card_attached_shape_list = your_fixed_card_base.get_attached_shapes()
                        #
                        #             opponent_field_card_id = opponent_field_unit_object.get_card_number()
                        #             opponent_field_card_index = opponent_field_unit_object.get_index()
                        #             opponent_damage = self.card_info_repository.getCardAttackForCardNumber(
                        #                 opponent_field_card_id)
                        #             print(f"opponent_damage: {opponent_damage}")
                        #
                        #             are_your_field_unit_death = False
                        #             your_extra_ability = self.your_field_unit_repository.get_your_unit_extra_ability_at_index(your_field_card_index)
                        #             opponent_harmful_status = self.opponent_field_unit_repository.get_harmful_status_by_index(opponent_field_card_index)
                        #
                        #             for your_fixed_card_attached_shape in your_fixed_card_attached_shape_list:
                        #                 if isinstance(your_fixed_card_attached_shape, NonBackgroundNumberImage):
                        #                     if your_fixed_card_attached_shape.get_circle_kinds() is CircleKinds.HP:
                        #                         your_hp_number = your_fixed_card_attached_shape.get_number()
                        #                         your_hp_number -= opponent_damage
                        #                         print(f"your 유닛 hp number: {your_hp_number}")
                        #
                        #                         if your_hp_number <= 0:
                        #                             are_your_field_unit_death = True
                        #                             break
                        #
                        #                         print(f"공격 후 your unit 체력 -> hp_number: {your_hp_number}")
                        #                         your_fixed_card_attached_shape.set_number(your_hp_number)
                        #
                        #                         # your_fixed_card_attached_shape.set_image_data(
                        #                         #     # TODO: 실제로 여기서 서버로부터 계산 받은 값을 적용해야함
                        #                         #     self.pre_drawed_image_instance.get_pre_draw_number_image(
                        #                         #         your_hp_number))
                        #
                        #                         your_fixed_card_attached_shape.set_image_data(
                        #                             self.pre_drawed_image_instance.get_pre_draw_unit_hp(
                        #                                 your_hp_number))
                        #
                        #             if are_your_field_unit_death is True:
                        #                 self.your_field_unit_repository.remove_card_by_index(
                        #                     your_field_card_index)
                        #                 self.your_tomb_repository.create_tomb_card(
                        #                     your_field_card_id)
                        #                 self.your_field_unit_repository.replace_field_card_position()
                        #
                        #             print("your 유닛 hp 갱신")
                        #
                        #
                        #
                        #             opponent_hp_number = opponent_fixed_card_attached_shape.get_number()
                        #             opponent_hp_number -= your_damage
                        #
                        #             print(f"opponent_hp_number: {opponent_hp_number}")
                        #
                        #             # TODO: n 턴간 불사 특성을 검사해야하므로 사실 이것도 summary 방식으로 빼는 것이 맞으나 우선은 진행한다.
                        #             # (지금 당장 불사가 존재하지 않음)
                        #             if opponent_hp_number <= 0:
                        #                 are_opponent_field_unit_death = True
                        #                 break
                        #
                        #             print(f"공격 후 opponent unit 체력 -> hp_number: {opponent_hp_number}")
                        #             opponent_fixed_card_attached_shape.set_number(opponent_hp_number)
                        #
                        #             # opponent_fixed_card_attached_shape.set_image_data(
                        #             #     # TODO: 실제로 여기서 서버로부터 계산 받은 값을 적용해야함
                        #             #     self.pre_drawed_image_instance.get_pre_draw_number_image(opponent_hp_number))
                        #
                        #             opponent_fixed_card_attached_shape.set_image_data(
                        #                 self.pre_drawed_image_instance.get_pre_draw_unit_hp(opponent_hp_number))
                        #
                        #             if your_extra_ability:
                        #                 self.opponent_field_unit_repository.apply_harmful_status(
                        #                     opponent_field_card_index, your_extra_ability)
                        #
                        # print(f"opponent_field_card_index: {opponent_field_card_index}")
                        #
                        # if are_opponent_field_unit_death is True:
                        #     self.opponent_field_unit_repository.remove_card_by_multiple_index(
                        #         [opponent_field_card_index])
                        #     self.opponent_tomb_repository.create_opponent_tomb_card(
                        #         opponent_field_card_id)
                        #
                        #     self.opponent_field_unit_repository.replace_opponent_field_unit_card_position()


                        self.apply_basic_attack_result_to_ui_with_response(attack_opponent_unit_response)

                        self.apply_response_data_of_harmful_status(attack_opponent_unit_response["player_field_unit_harmful_effect_map"])

                        # is_opponent_data_in_response = False
                        # is_your_data_in_response = False
                        #
                        # try:
                        #     dead_opponent_unit_index_list = (
                        #         attack_opponent_unit_response.get('player_field_unit_death_map', {})
                        #         .get('Opponent', {})['dead_field_unit_index_list'])
                        #
                        #     opponent_unit_index = int(list(
                        #         attack_opponent_unit_response.get('player_field_unit_health_point_map', {})
                        #         .get('Opponent', {}).get('field_unit_health_point_map', {}).keys())[0])
                        #
                        #     remain_opponent_unit_hp = (
                        #         attack_opponent_unit_response.get('player_field_unit_health_point_map', {})
                        #                                .get('Opponent', {}).get('field_unit_health_point_map',{})
                        #                                .get(str(opponent_field_card_index), None))
                        #
                        #     is_opponent_data_in_response = True
                        # except:
                        #     print("opponent data is not in response")
                        #
                        # if is_opponent_data_in_response:
                        #     opponent_fixed_card_attached_shape_list = opponent_fixed_card_base.get_attached_shapes()
                        #
                        #     for opponent_fixed_card_attached_shape in opponent_fixed_card_attached_shape_list:
                        #         if isinstance(opponent_fixed_card_attached_shape, NonBackgroundNumberImage):
                        #             if opponent_fixed_card_attached_shape.get_circle_kinds() is CircleKinds.HP:
                        #                 print("지정한 상대방 유닛 HP Circle 찾기")
                        #
                        #                 opponent_field_card_id = opponent_field_unit_object.get_card_number()
                        #                 opponent_field_card_index = opponent_field_unit_object.get_index()
                        #
                        #                 print(f"opponent_hp_number: {remain_opponent_unit_hp}")
                        #
                        #                 # TODO: n 턴간 불사 특성을 검사해야하므로 사실 이것도 summary 방식으로 빼는 것이 맞으나 우선은 진행한다.
                        #                 # (지금 당장 불사가 존재하지 않음)
                        #                 if remain_opponent_unit_hp <= 0:
                        #                     break
                        #
                        #                 print(f"공격 후 opponent unit 체력 -> hp_number: {remain_opponent_unit_hp}")
                        #                 opponent_fixed_card_attached_shape.set_number(remain_opponent_unit_hp)
                        #
                        #                 # opponent_fixed_card_attached_shape.set_image_data(
                        #                 #     # TODO: 실제로 여기서 서버로부터 계산 받은 값을 적용해야함
                        #                 #     self.pre_drawed_image_instance.get_pre_draw_number_image(opponent_hp_number))
                        #
                        #                 opponent_fixed_card_attached_shape.set_image_data(
                        #                     self.pre_drawed_image_instance.get_pre_draw_unit_hp(remain_opponent_unit_hp))
                        #
                        #     for dead_opponent_unit_index in dead_opponent_unit_index_list:
                        #         opponent_field_card_id = self.opponent_field_unit_repository.get_opponent_card_id_by_index(
                        #             dead_opponent_unit_index)
                        #
                        #         self.opponent_field_unit_repository.remove_current_field_unit_card(dead_opponent_unit_index)
                        #         self.opponent_tomb_repository.create_opponent_tomb_card(opponent_field_card_id)
                        #
                        #     self.opponent_field_unit_repository.replace_opponent_field_unit_card_position()
                        #
                        #
                        # try:
                        #     dead_your_unit_index_list = (
                        #         attack_opponent_unit_response.get('player_field_unit_death_map', {})
                        #         .get('You', {})['dead_field_unit_index_list'])
                        #
                        #     your_unit_index = int(list(
                        #         attack_opponent_unit_response.get('player_field_unit_health_point_map', {})
                        #         .get('You', {}).get('field_unit_health_point_map', {}).keys())[0])
                        #
                        #     remain_your_unit_hp = (
                        #         attack_opponent_unit_response.get('player_field_unit_health_point_map', {})
                        #         .get('You', {}).get('field_unit_health_point_map', {})
                        #         .get(str(your_field_card_index), None))
                        #     is_your_data_in_response = True
                        # except:
                        #     print("your data is not in response")
                        #
                        # if is_your_data_in_response:
                        #     your_field_unit = self.your_field_unit_repository.find_field_unit_by_index(
                        #         your_unit_index)
                        #     your_fixed_card_base = your_field_unit.get_fixed_card_base()
                        #     your_fixed_card_attached_shape_list = your_fixed_card_base.get_attached_shapes()
                        #
                        #     for your_fixed_card_attached_shape in your_fixed_card_attached_shape_list:
                        #         if isinstance(your_fixed_card_attached_shape, NonBackgroundNumberImage):
                        #             if your_fixed_card_attached_shape.get_circle_kinds() is CircleKinds.HP:
                        #
                        #                 if remain_your_unit_hp <= 0:
                        #                     break
                        #
                        #                 print(f"공격 후 your unit 체력 -> hp_number: {remain_your_unit_hp}")
                        #                 your_fixed_card_attached_shape.set_number(remain_your_unit_hp)
                        #
                        #                 # your_fixed_card_attached_shape.set_image_data(
                        #                 #     # TODO: 실제로 여기서 서버로부터 계산 받은 값을 적용해야함
                        #                 #     self.pre_drawed_image_instance.get_pre_draw_number_image(
                        #                 #         your_hp_number))
                        #
                        #                 your_fixed_card_attached_shape.set_image_data(
                        #                     self.pre_drawed_image_instance.get_pre_draw_unit_hp(
                        #                         remain_your_unit_hp))
                        #
                        #
                        #     print("your 유닛 hp 갱신 완료")
                        #
                        #     for dead_your_unit_index in dead_your_unit_index_list:
                        #         your_field_card_id = self.your_field_unit_repository.get_card_id_by_index(
                        #             dead_your_unit_index)
                        #         self.your_tomb_repository.create_tomb_card(your_field_card_id)
                        #         self.your_field_unit_repository.remove_card_by_index(dead_your_unit_index)
                        #
                        #     self.your_field_unit_repository.replace_field_card_position()

                        # self.opponent_fixed_unit_card_inside_handler.clear_opponent_field_area_action()
                        # self.targeting_enemy_select_using_your_field_card_index = None
                        # self.targeting_enemy_select_using_your_field_card_id = None
                        # self.targeting_enemy_select_support_lightning_border_list = []
                        # self.opponent_you_selected_lightning_border_list = []
                        #
                        # self.selected_object = None
                        # self.active_panel_rectangle = None
                        # self.current_fixed_details_card = None
                        # self.your_active_panel.clear_all_your_active_panel()
                        self.reset_every_selected_action()

                        return

            if self.opponent_fixed_unit_card_inside_handler.get_action_to_apply_opponent() is ActionToApplyOpponent.NETHER_BLADE_SECOND_TARGETING_PASSIVE_SKILL:
                print("네더 블레이드 타겟팅 패시브")

                if self.opponent_main_character.is_point_inside((x, y)):
                    print("메인 캐릭터 공격")

                    your_field_card_id = self.targeting_enemy_select_using_your_field_card_id
                    print(f"your_field_card_id: {your_field_card_id}")

                    your_damage = self.card_info_repository.getCardPassiveSecondDamageForCardNumber(your_field_card_id)
                    print(f"your_damage: {your_damage}")

                    self.attack_animation_object.set_animation_actor_damage(your_damage)
                    self.attack_animation_object.set_opponent_main_character(self.opponent_main_character_panel)
                    self.attack_animation_object.set_is_your_attack_main_character(True)
                    # self.opponent_hp_repository.take_damage(your_damage)

                    # self.opponent_fixed_unit_card_inside_handler.set_action_to_apply_opponent(ActionToApplyOpponent.Dummy)
                    # self.targeting_enemy_select_using_your_field_card_index = None
                    # self.targeting_enemy_select_using_your_field_card_id = None
                    # self.targeting_enemy_select_support_lightning_border_list = []
                    # self.opponent_you_selected_lightning_border_list = []
                    #
                    # self.selected_object = None
                    # self.active_panel_rectangle = None
                    # self.current_fixed_details_card = None
                    # self.your_active_panel.clear_all_your_active_panel()
                    self.reset_every_selected_action()

                    animation_actor = self.attack_animation_object.get_animation_actor()

                    # turn_start_second_passive_skill_to_main_character_response = self.__fake_battle_field_frame_repository.request_to_process_turn_start_second_passive_skill_to_main_character(
                    #     TurnStartSecondPassiveSkillToMainCharacterRequest(
                    #         _sessionInfo=self.__session_repository.get_first_fake_session_info(),
                    #         _unitCardIndex=str(animation_actor.get_index()),
                    #         _targetGameMainCharacterIndex="0",
                    #         _usageSkillIndex="2"))

                    # self.__fake_battle_field_frame_repository.request_attack_main_character_with_active_skill(
                    #     RequestAttackMainCharacterWithActiveSkill(
                    #         _sessionInfo=self.__session_repository.get_first_fake_session_info(),
                    #         _unitCardIndex=str(animation_actor.get_index()),
                    #         _targetGameMainCharacterIndex="0"
                    #     )
                    # )

                    process_second_passive_skill_response = self.__fake_battle_field_frame_repository.request_to_process_second_passive_skill_to_main_character(
                        TargetingPassiveSkillToMainCharacterFromDeployRequest(
                            _sessionInfo=self.__session_repository.get_first_fake_session_info(),
                            _unitCardIndex=str(animation_actor.get_index()),
                            _targetGameMainCharacterIndex="0",
                            _usageSkillIndex="2"))

                    print(f"{Fore.RED}your second_passive_skill_response:{Fore.GREEN} {process_second_passive_skill_response}{Style.RESET_ALL}")

                    is_success = process_second_passive_skill_response['is_success']
                    if is_success is False:
                        self.opponent_fixed_unit_card_inside_handler.set_action_to_apply_opponent(ActionToApplyOpponent.Dummy)
                        is_false_message = process_second_passive_skill_response.get('false_message_enum')
                        self.message_on_the_screen.create_message_on_the_battle_screen(
                            is_false_message)
                        return

                    self.attack_animation_object.set_is_your_attack_main_character(True)
                    self.attack_animation_object.set_response_data(process_second_passive_skill_response)
                    # self.create_effect_animation_with_vertices_and_play_animation_and_call_function(
                    #     'nether_blade_targeting_skill', self.opponent_main_character_panel.get_vertices(),
                    #     self.start_nether_blade_second_passive_targeting_motion_animation
                    # )
                    self.master.after(0, self.nether_blade_second_passive_skill_animation)

                    # self.create_effect_animation_to_full_screen_and_play_animation_and_call_function_with_param(
                    #     'nether_blade_targeting_skill', wide_area_attack, 1)

                    if process_second_passive_skill_response.get('player_main_character_survival_map_for_notice', {}).get('Opponent',
                                                                                             None) == 'Death':
                        self.opponent_hp_repository.opponent_character_die()
                        print("opponent die")
                    # self.master.after(0, self.start_nether_blade_second_passive_targeting_motion_animation)

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
                    print('일단 어딘지 찾아')

                    if opponent_fixed_card_base.is_point_inside((x, y)):
                        self.attack_animation_object.set_opponent_field_unit(opponent_field_unit_object)

                        animation_actor = self.attack_animation_object.get_animation_actor()
                        self.attack_animation_object.set_is_your_attack_main_character(False)
                        self.attack_animation_object.set_opponent_main_character(None)

                        process_second_passive_skill_response = self.__fake_battle_field_frame_repository.request_to_process_second_passive_skill_to_opponent_field_unit(
                            TargetingPassiveSkillToOpponentFieldUnitFromDeployRequest(
                                _sessionInfo=self.__session_repository.get_first_fake_session_info(),
                                _unitCardIndex=str(animation_actor.get_index()),
                                _opponentTargetCardIndex=str(opponent_field_unit_object.get_index()),
                                _usageSkillIndex="2"))

                        is_success = process_second_passive_skill_response['is_success']
                        if is_success is False:
                            self.opponent_fixed_unit_card_inside_handler.set_action_to_apply_opponent(
                                ActionToApplyOpponent.Dummy)
                            is_false_message = process_second_passive_skill_response.get('false_message_enum')
                            self.message_on_the_screen.create_message_on_the_battle_screen(
                                is_false_message)
                            return FieldAreaAction.Dummy

                        self.attack_animation_object.set_response_data(process_second_passive_skill_response)

                        # self.attack_animation_object.set_animation_actor_damage(20)
                        # self.create_effect_animation_to_opponent_unit_and_play_animation_and_call_function(
                        #     'nether_blade_targeting_skill', opponent_field_unit_object.get_index(),
                        #     self.start_nether_blade_second_passive_targeting_motion_animation
                        # )
                        self.attack_animation_object.set_opponent_field_unit(opponent_field_unit_object)

                        self.master.after(0, self.nether_blade_second_passive_skill_animation)
                        self.opponent_you_selected_lightning_border_list.append(opponent_fixed_card_base)

                        # opponent_fixed_card_attached_shape_list = opponent_fixed_card_base.get_attached_shapes()
                        #
                        # are_opponent_field_unit_death = False
                        # opponent_field_card_index = None
                        # opponent_field_card_id = None
                        #
                        # print("지정한 상대 유닛 모양 찾기")
                        #
                        # for opponent_fixed_card_attached_shape in opponent_fixed_card_attached_shape_list:
                        #     if isinstance(opponent_fixed_card_attached_shape, NonBackgroundNumberImage):
                        #         if opponent_fixed_card_attached_shape.get_circle_kinds() is CircleKinds.HP:
                        #             print("지정한 상대방 유닛 HP Circle 찾기")
                        #
                        #             your_field_card_id = self.targeting_enemy_select_using_your_field_card_id
                        #             print(f"your_field_card_id: {your_field_card_id}")
                        #
                        #             your_second_passive_skill_damage = self.card_info_repository.getCardPassiveSecondDamageForCardNumber(
                        #                 your_field_card_id)
                        #             print(f"your_skill_damage: {your_second_passive_skill_damage}")
                        #
                        #             opponent_field_card_id = opponent_field_unit_object.get_card_number()
                        #             opponent_field_card_index = opponent_field_unit_object.get_index()
                        #
                        #             opponent_hp_number = opponent_fixed_card_attached_shape.get_number()
                        #             opponent_hp_number -= your_second_passive_skill_damage
                        #
                        #             print(f"opponent_hp_number: {opponent_hp_number}")
                        #
                        #             # TODO: n 턴간 불사 특성을 검사해야하므로 사실 이것도 summary 방식으로 빼는 것이 맞으나 우선은 진행한다.
                        #             # (지금 당장 불사가 존재하지 않음)
                        #             if opponent_hp_number <= 0:
                        #                 are_opponent_field_unit_death = True
                        #
                        #                 break
                        #
                        #             print(f"공격 후 opponent unit 체력 -> hp_number: {opponent_hp_number}")
                        #             opponent_fixed_card_attached_shape.set_number(opponent_hp_number)
                        #
                        #             # opponent_fixed_card_attached_shape.set_image_data(
                        #             #     # TODO: 실제로 여기서 서버로부터 계산 받은 값을 적용해야함
                        #             #     self.pre_drawed_image_instance.get_pre_draw_number_image(opponent_hp_number))
                        #
                        #             opponent_fixed_card_attached_shape.set_image_data(
                        #                 self.pre_drawed_image_instance.get_pre_draw_unit_hp(opponent_hp_number))
                        #
                        # print(f"opponent_field_card_index: {opponent_field_card_index}")
                        #
                        # if are_opponent_field_unit_death is True:
                        #     self.opponent_field_unit_repository.remove_card_by_multiple_index(
                        #         [opponent_field_card_index])
                        #     self.opponent_tomb_repository.create_opponent_tomb_card(
                        #         opponent_field_card_id)
                        #
                        #     self.opponent_field_unit_repository.replace_opponent_field_unit_card_position()

                        # self.opponent_fixed_unit_card_inside_handler.set_action_to_apply_opponent(ActionToApplyOpponent.Dummy)
                        # self.opponent_fixed_unit_card_inside_handler.clear_opponent_field_area_action()
                        # self.targeting_enemy_select_using_your_field_card_index = None
                        # self.targeting_enemy_select_using_your_field_card_id = None
                        # self.targeting_enemy_select_support_lightning_border_list = []
                        # self.opponent_you_selected_lightning_border_list = []
                        #
                        # self.selected_object = None
                        # self.active_panel_rectangle = None
                        # self.current_fixed_details_card = None
                        # self.your_active_panel.clear_all_your_active_panel()
                        self.reset_every_selected_action()

                        return

            if self.opponent_fixed_unit_card_inside_handler.get_action_to_apply_opponent() is ActionToApplyOpponent.NETHER_BLADE_TURN_START_SECOND_TARGETING_PASSIVE_SKILL:
                print("턴 시작 시 Your 네더 블레이드 타겟팅 패시브")

                if self.opponent_main_character.is_point_inside((x, y)):
                    print("메인 캐릭터 공격")

                    your_field_card_id = self.targeting_enemy_select_using_your_field_card_id
                    print(f"your_field_card_id: {your_field_card_id}")

                    your_damage = self.card_info_repository.getCardPassiveSecondDamageForCardNumber(your_field_card_id)
                    print(f"your_damage: {your_damage}")

                    self.attack_animation_object.set_animation_actor_damage(your_damage)
                    self.attack_animation_object.set_opponent_main_character(self.opponent_main_character_panel)
                    self.attack_animation_object.set_is_your_attack_main_character(True)

                    self.reset_every_selected_action()

                    animation_actor = self.attack_animation_object.get_animation_actor()

                    # turn_start_second_passive_skill_to_main_character_response = self.__fake_battle_field_frame_repository.request_to_process_turn_start_second_passive_skill_to_main_character(
                    #     TurnStartSecondPassiveSkillToMainCharacterRequest(
                    #         _sessionInfo=self.__session_repository.get_first_fake_session_info(),
                    #         _unitCardIndex=str(animation_actor.get_index()),
                    #         _targetGameMainCharacterIndex="0",
                    #         _usageSkillIndex="2"))

                    # self.__fake_battle_field_frame_repository.request_attack_main_character_with_active_skill(
                    #     RequestAttackMainCharacterWithActiveSkill(
                    #         _sessionInfo=self.__session_repository.get_first_fake_session_info(),
                    #         _unitCardIndex=str(animation_actor.get_index()),
                    #         _targetGameMainCharacterIndex="0"
                    #     )
                    # )

                    # turn_start_second_passive_skill_to_main_character_response = self.__fake_battle_field_frame_repository.request_to_process_turn_start_second_passive_skill_to_your_field_unit(
                    #     TurnStartSecondPassiveSkillToYourFieldUnitRequest(
                    #         _sessionInfo=self.__session_repository.get_second_fake_session_info(),
                    #         _unitCardIndex=str(animation_actor.get_index()),
                    #         _opponentTargetCardIndex=str(first_non_none_index),
                    #         _usageSkillIndex="2"))

                    process_second_passive_skill_response = self.__fake_battle_field_frame_repository.request_to_process_second_passive_skill_to_main_character(
                        TargetingPassiveSkillToMainCharacterFromDeployRequest(
                            _sessionInfo=self.__session_repository.get_first_fake_session_info(),
                            _unitCardIndex=str(animation_actor.get_index()),
                            _targetGameMainCharacterIndex="0",
                            _usageSkillIndex="2"))

                    print(f"{Fore.RED}your second_passive_skill_response:{Fore.GREEN} {process_second_passive_skill_response}{Style.RESET_ALL}")

                    is_success = process_second_passive_skill_response['is_success']
                    if is_success is False:
                        self.opponent_fixed_unit_card_inside_handler.set_action_to_apply_opponent(ActionToApplyOpponent.Dummy)
                        is_false_message = process_second_passive_skill_response.get('false_message_enum')
                        self.message_on_the_screen.create_message_on_the_battle_screen(
                            is_false_message)
                        return FieldAreaAction.Dummy

                    self.attack_animation_object.set_response_data(process_second_passive_skill_response)
                    # self.create_effect_animation_with_vertices_and_play_animation_and_call_function(
                    #     'nether_blade_targeting_skill', self.opponent_main_character_panel.get_vertices(),
                    #     self.start_nether_blade_second_passive_targeting_motion_animation
                    # )
                    self.master.after(0, self.nether_blade_turn_start_second_passive_skill_animation)

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
                    print('찾아2')

                    if opponent_fixed_card_base.is_point_inside((x, y)):
                        self.attack_animation_object.set_opponent_main_character(None)
                        self.attack_animation_object.set_is_your_attack_main_character(False)
                        self.attack_animation_object.set_opponent_field_unit(opponent_field_unit_object)

                        # turn_start_second_passive_skill_to_main_character_response = self.__fake_battle_field_frame_repository.request_to_process_turn_start_second_passive_skill_to_main_character(
                        #     TurnStartSecondPassiveSkillToMainCharacterRequest(
                        #         _sessionInfo=self.__session_repository.get_first_fake_session_info(),
                        #         _unitCardIndex=str(opponent_field_unit_object.get_index()),
                        #         _targetGameMainCharacterIndex="0",
                        #         _usageSkillIndex="2"))
                        
                        # turn_start_second_passive_skill_to_main_character_response = self.__fake_battle_field_frame_repository.request_to_process_turn_start_second_passive_skill_to_main_character(
                        #     TurnStartSecondPassiveSkillToMainCharacterRequest(
                        #         _sessionInfo=self.__session_repository.get_first_fake_session_info(),
                        #         _unitCardIndex=str(opponent_field_unit_object.get_index()),
                        #         _targetGameMainCharacterIndex="0",
                        #         _usageSkillIndex="2"))

                        animation_actor = self.attack_animation_object.get_animation_actor()

                        turn_start_second_passive_skill_to_main_character_response = self.__fake_battle_field_frame_repository.request_to_process_turn_start_second_passive_skill_to_your_field_unit(
                            TurnStartSecondPassiveSkillToYourFieldUnitRequest(
                                _sessionInfo=self.__session_repository.get_first_fake_session_info(),
                                _unitCardIndex=str(animation_actor.get_index()),
                                _opponentTargetCardIndex=str(opponent_field_unit_object.get_index()),
                                _usageSkillIndex="2"))

                        # self.attack_animation_object.set_animation_actor_damage(20)
                        # self.create_effect_animation_to_opponent_unit_and_play_animation_and_call_function(
                        #     'nether_blade_targeting_skill', opponent_field_unit_object.get_index(),
                        #     self.start_nether_blade_turn_start_second_passive_targeting_motion_animation
                        # )

                        # opponent_field_unit = self.attack_animation_object.get_opponent_field_unit()
                        self.attack_animation_object.set_opponent_field_unit(opponent_field_unit_object)

                        self.master.after(0, self.nether_blade_turn_start_second_passive_skill_animation)

                        # self.master.after(0, self.start_nether_blade_turn_start_second_passive_targeting_motion_animation)
                        self.opponent_you_selected_lightning_border_list.append(opponent_fixed_card_base)

                        self.reset_every_selected_action()

                        return

            if self.opponent_fixed_unit_card_inside_handler.get_opponent_field_area_action() is OpponentFieldAreaAction.PASSIVE_SKILL_TARGETING_ENEMY:
                print("단일기 패시브")

                if self.opponent_main_character.is_point_inside((x, y)):
                    print("메인 캐릭터 공격")

                    # your_field_card_index = self.targeting_enemy_select_using_your_field_card_index
                    # self.your_field_unit_action_repository.use_field_unit_action_count_by_index(your_field_card_index)

                    your_field_card_id = self.targeting_enemy_select_using_your_field_card_id
                    print(f"your_field_card_id: {your_field_card_id}")

                    your_damage = self.card_info_repository.getCardPassiveSecondDamageForCardNumber(your_field_card_id)
                    print(f"your_damage: {your_damage}")

                    self.opponent_hp_repository.take_damage(your_damage)

                    # self.opponent_fixed_unit_card_inside_handler.clear_opponent_field_area_action()
                    # self.targeting_enemy_select_using_your_field_card_index = None
                    # self.targeting_enemy_select_using_your_field_card_id = None
                    # self.targeting_enemy_select_support_lightning_border_list = []
                    # self.opponent_you_selected_lightning_border_list = []
                    #
                    # self.selected_object = None
                    # self.active_panel_rectangle = None
                    # self.current_fixed_details_card = None
                    # self.your_active_panel.clear_all_your_active_panel()
                    self.reset_every_selected_action()

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
                    print('찾아3')

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
                            effect_animation = EffectAnimation()
                            effect_animation.set_animation_name('death')
                            effect_animation.set_total_window_size(self.width, self.height)
                            effect_animation.change_local_translation(self.opponent_field_unit_repository.find_opponent_field_unit_by_index(
                                opponent_field_card_index).get_fixed_card_base().get_local_translation())
                            effect_animation.draw_animation_panel()
                            effect_animation_panel = effect_animation.get_animation_panel()

                            animation_index = self.effect_animation_repository.save_effect_animation_at_dictionary_without_index_and_return_index(
                                effect_animation)

                            self.effect_animation_repository.save_effect_animation_panel_at_dictionary_with_index(
                                animation_index, effect_animation_panel)

                            def remove_opponent_unit(_index):
                                opponent_unit_card_id = (
                                    self.opponent_field_unit_repository.find_opponent_field_unit_by_index(_index))
                                self.opponent_field_unit_repository.remove_current_field_unit_card(_index)
                                self.opponent_tomb_repository.create_opponent_tomb_card(opponent_unit_card_id)

                                self.opponent_field_unit_repository.replace_opponent_field_unit_card_position()
                                self.opponent_field_unit_repository.remove_harmful_status_by_index(_index)

                            # self.play_effect_animation_by_index_and_call_function(animation_index, remove_opponent_unit)
                            self.play_effect_animation_by_index_and_call_function_with_param(
                                animation_index, remove_opponent_unit, opponent_field_card_index)

                        # self.opponent_fixed_unit_card_inside_handler.clear_opponent_field_area_action()
                        # self.targeting_enemy_select_using_your_field_card_index = None
                        # self.targeting_enemy_select_using_your_field_card_id = None
                        # self.targeting_enemy_select_support_lightning_border_list = []
                        # self.opponent_you_selected_lightning_border_list = []
                        #
                        # self.selected_object = None
                        # self.active_panel_rectangle = None
                        # self.current_fixed_details_card = None
                        # self.your_active_panel.clear_all_your_active_panel()
                        self.reset_every_selected_action()
                        return

            if self.opponent_fixed_unit_card_inside_handler.get_opponent_field_area_action() is OpponentFieldAreaAction.SKILL_TARGETING_ENEMY:
                print("단일기 사용")

                # self.targeting_ememy_select_using_hand_card_id = placed_card_id
                # self.targeting_ememy_select_using_hand_card_index = placed_index

                if self.opponent_main_character.is_point_inside((x, y)):
                    print("메인 캐릭터 공격")

                    your_field_card_index = self.targeting_enemy_select_using_your_field_card_index

                    your_field_card_id = self.targeting_enemy_select_using_your_field_card_id
                    print(f"your_field_card_id: {your_field_card_id}")

                    response = self.__fake_battle_field_frame_repository.request_attack_main_character_with_active_skill(
                        RequestAttackMainCharacterWithActiveSkill(
                            _sessionInfo = self.__session_repository.get_first_fake_session_info(),
                            _unitCardIndex=your_field_card_index,
                            _targetGameMainCharacterIndex="0"
                        )
                    )

                    if response.get('is_success', False) == False:
                        print('active skill target one error : ', response)
                        self.reset_every_selected_action()
                        is_false_message = response.get('false_message_enum')
                        self.message_on_the_screen.create_message_on_the_battle_screen(
                            is_false_message)
                        return

                    self.your_field_unit_action_repository.use_field_unit_action_count_by_index(your_field_card_index)



                    # opponent_character_survival_state = response['player_main_character_survival_map_for_notice']['Opponent']
                    #
                    # if opponent_character_survival_state != 'Survival':
                    #     print('상대방이 죽었습니다!!')
                    #     return
                    #
                    # remain_character_hp = response['player_main_character_health_point_map_for_notice']['Opponent']
                    #
                    # self.opponent_hp_repository.change_opponent_hp(remain_character_hp)


                    #### 모션 프레임
                    your_field_unit = self.your_field_unit_repository.find_field_unit_by_index(your_field_card_index)
                    print(f"{Fore.RED}valrn ready to use shadow ball -> your_field_unit: {Fore.GREEN}{your_field_unit}{Style.RESET_ALL}")
                    self.attack_animation_object.set_animation_actor(your_field_unit)
                    self.field_area_inside_handler.set_field_area_action(FieldAreaAction.PLAY_ANIMATION)
                    self.master.after(0, self.valrn_ready_to_use_shadow_ball_to_opponent_main_character_animation)
                    if response.get('player_main_character_survival_map_for_notice', {}).get('Opponent', None) == 'Death':
                        self.opponent_hp_repository.opponent_character_die()
                    #### 애니메이션 프레임
                    return

                    # self.__effect_animation_dictionary[index] = effect_animation
                    # self.__effect_animation_panel_dictionary[index] = effect_animation_panel

                    # def get_effect_animation_by_index(self, index):
                    #     return self.__effect_animation_dictionary[index]

                    # effect_animation = EffectAnimation()
                    # effect_animation.set_animation_name('burst_shadow_ball')
                    # effect_animation.set_total_window_size(self.width, self.height)
                    # vertices = self.opponent_main_character_panel.get_vertices()
                    # effect_animation.draw_animation_panel_with_vertices(vertices)
                    # effect_animation_panel = effect_animation.get_animation_panel()
                    # 
                    # self.effect_animation_repository.save_effect_animation_at_dictionary_with_index(
                    #     your_field_card_index, effect_animation)
                    # 
                    # self.effect_animation_repository.save_effect_animation_panel_at_dictionary_with_index(
                    #     your_field_card_index, effect_animation_panel)
                    # 
                    # self.targeting_enemy_select_support_lightning_border_list = []
                    # self.opponent_you_selected_lightning_border_list = []
                    # 
                    # def calculate_shadow_ball_to_main_character():
                    #     your_field_card_id = self.targeting_enemy_select_using_your_field_card_id
                    #     your_damage = self.card_info_repository.getCardSkillFirstDamageForCardNumber(your_field_card_id)
                    #     print(f"your_damage: {your_damage}")
                    #     self.opponent_hp_repository.take_damage(your_damage)
                    # 
                    #     self.opponent_fixed_unit_card_inside_handler.clear_opponent_field_area_action()
                    #     self.targeting_enemy_select_using_your_field_card_index = None
                    #     self.targeting_enemy_select_using_your_field_card_id = None
                    #     self.targeting_enemy_select_support_lightning_border_list = []
                    #     self.opponent_you_selected_lightning_border_list = []
                    # 
                    #     self.selected_object = None
                    #     self.active_panel_rectangle = None
                    #     self.current_fixed_details_card = None
                    #     self.your_active_panel.clear_all_your_active_panel()
                    # 
                    #     return

                    # self.play_effect_animation_by_index_and_call_function(your_field_card_index,
                    #                                                       calculate_shadow_ball_to_main_character)

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

                        response = self.__fake_battle_field_frame_repository.request_attack_opponent_unit(
                            RequestAttackToOpponentFieldUnitWithActiveSkill(
                                _sessionInfo = self.__session_repository.get_first_fake_session_info(),
                                _unitCardIndex = your_field_card_index,
                                _opponentTargetCardIndex = opponent_field_unit_object.get_index()
                            )
                        )

                        print('active skill response: ',response)

                        if response.get('is_success', False) == False:
                            print('active skill error occured!! ')
                            self.reset_every_selected_action()
                            is_false_message = response.get('false_message_enum')
                            self.message_on_the_screen.create_message_on_the_battle_screen(
                                is_false_message)
                            return

                        self.your_field_unit_action_repository.use_field_unit_action_count_by_index(
                            your_field_card_index)

                        self.opponent_you_selected_lightning_border_list.append(opponent_fixed_card_base)

                        ### 애니메이션 준비
                        your_field_unit = self.your_field_unit_repository.find_field_unit_by_index(your_field_card_index)

                        self.attack_animation_object.set_animation_actor(your_field_unit)
                        self.attack_animation_object.set_opponent_field_unit(opponent_field_unit_object)
                        self.field_area_inside_handler.set_field_area_action(FieldAreaAction.PLAY_ANIMATION)

                        ### 애니메이션 실행
                        self.master.after(0, self.valrn_ready_to_use_shadow_ball_to_opponent_unit_animation)
                        return

                        # opponent_unit_index = opponent_field_unit_object.get_index()
                        # effect_animation = EffectAnimation()
                        # effect_animation.set_animation_name('burst_shadow_ball')
                        # effect_animation.set_total_window_size(self.width, self.height)
                        # effect_animation.change_local_translation(opponent_fixed_card_base.get_local_translation())
                        # effect_animation.draw_animation_panel()
                        # effect_animation_panel = effect_animation.get_animation_panel()
                        # print(effect_animation_panel)
                        # self.effect_animation_repository.save_effect_animation_at_dictionary_with_index(
                        #     your_field_card_index,effect_animation)
                        #
                        # self.effect_animation_repository.save_effect_animation_panel_at_dictionary_with_index(
                        #     your_field_card_index, effect_animation_panel)
                        #
                        # self.targeting_enemy_select_support_lightning_border_list = []
                        # self.opponent_you_selected_lightning_border_list = []

                        # def calculate_shadow_ball():
                            # dead_field_unit_index_list = response['player_field_unit_death_map']['Opponent']['dead_field_unit_index_list']
                            #
                            # for opponent_field_unit_index, opponent_field_unit_remain_hp in response['player_field_unit_health_point_map']['Opponent'][
                            #     'field_unit_health_point_map'].items():
                            #
                            #     if opponent_field_unit_remain_hp == 0:
                            #         break
                            #
                            #     opponent_field_unit = (
                            #         self.opponent_field_unit_repository.find_opponent_field_unit_by_index(int(opponent_field_unit_index)))
                            #     opponent_fixed_card_base = opponent_field_unit.get_fixed_card_base()
                            #     opponent_fixed_card_attached_shape_list = opponent_fixed_card_base.get_attached_shapes()
                            #     for opponent_fixed_card_attached_shape in opponent_fixed_card_attached_shape_list:
                            #         if isinstance(opponent_fixed_card_attached_shape, NonBackgroundNumberImage):
                            #             if opponent_fixed_card_attached_shape.get_circle_kinds() is CircleKinds.HP:
                            #                 opponent_fixed_card_attached_shape.set_number(opponent_field_unit_remain_hp)
                            #
                            #                 opponent_fixed_card_attached_shape.set_image_data(
                            #                     self.pre_drawed_image_instance.get_pre_draw_unit_hp(opponent_field_unit_remain_hp))
                            #
                            # for dead_field_unit_index in dead_field_unit_index_list:
                            #     card_id = self.opponent_field_unit_repository.get_opponent_card_id_by_index(dead_field_unit_index)
                            #     self.opponent_tomb_repository.create_opponent_tomb_card(card_id)
                            #     self.opponent_field_unit_repository.remove_current_field_unit_card(dead_field_unit_index)
                            #     self.opponent_field_unit_repository.replace_opponent_field_unit_card_position()

                            # opponent_fixed_card_attached_shape_list = opponent_fixed_card_base.get_attached_shapes()

                        #     are_opponent_field_unit_death = False
                        #     opponent_field_card_index = None
                        #     opponent_field_card_id = None
                        #     your_field_card_index = self.targeting_enemy_select_using_your_field_card_index
                        #     your_extra_ability = self.your_field_unit_repository.get_your_unit_extra_ability_at_index(your_field_card_index)
                        #
                        #     for opponent_fixed_card_attached_shape in opponent_fixed_card_attached_shape_list:
                        #         if isinstance(opponent_fixed_card_attached_shape, NonBackgroundNumberImage):
                        #             if opponent_fixed_card_attached_shape.get_circle_kinds() is CircleKinds.HP:
                        #                 print("지정한 상대방 유닛 HP Circle 찾기")
                        #
                        #                 your_field_card_id = self.targeting_enemy_select_using_your_field_card_id
                        #                 print(f"your_field_card_id: {your_field_card_id}")
                        #                 your_field_card_index = self.targeting_enemy_select_using_your_field_card_index
                        #                 print(f"your_field_card_index: {your_field_card_index}")
                        #                 # your_skill_damage = self.card_info_repository.getCardAttackForCardNumber(your_field_card_id)
                        #                 # your_skill_damage = self.card_info_repository.getCardAttackForCardNumber(your_field_card_id)
                        #                 # your_skill_damage = 20
                        #                 your_skill_damage = self.card_info_repository.getCardSkillFirstDamageForCardNumber(
                        #                     your_field_card_id)
                        #                 print(f"your_skill_damage: {your_skill_damage}")
                        #
                        #                 opponent_field_card_id = opponent_field_unit_object.get_card_number()
                        #                 opponent_field_card_index = opponent_field_unit_object.get_index()
                        #
                        #                 opponent_hp_number = opponent_fixed_card_attached_shape.get_number()
                        #                 opponent_hp_number -= your_skill_damage
                        #
                        #                 print(f"opponent_hp_number: {opponent_hp_number}")
                        #
                        #                 # TODO: n 턴간 불사 특성을 검사해야하므로 사실 이것도 summary 방식으로 빼는 것이 맞으나 우선은 진행한다.
                        #                 # (지금 당장 불사가 존재하지 않음)
                        #                 if opponent_hp_number <= 0:
                        #                     are_opponent_field_unit_death = True
                        #
                        #                     break
                        #
                        #                 print(f"공격 후 opponent unit 체력 -> hp_number: {opponent_hp_number}")
                        #                 opponent_fixed_card_attached_shape.set_number(opponent_hp_number)
                        #
                        #                 # opponent_fixed_card_attached_shape.set_image_data(
                        #                 #     # TODO: 실제로 여기서 서버로부터 계산 받은 값을 적용해야함
                        #                 #     self.pre_drawed_image_instance.get_pre_draw_number_image(opponent_hp_number))
                        #
                        #                 opponent_fixed_card_attached_shape.set_image_data(
                        #                     self.pre_drawed_image_instance.get_pre_draw_unit_hp(opponent_hp_number))
                        #
                        #                 if your_extra_ability:
                        #                     self.opponent_field_unit_repository.apply_harmful_status(opponent_field_card_index, your_extra_ability)
                        #
                        #
                        #     print(f"opponent_field_card_index: {opponent_field_card_index}")
                        #
                        #     if are_opponent_field_unit_death is True:
                        #         self.opponent_field_unit_repository.remove_card_by_multiple_index(
                        #             [opponent_field_card_index])
                        #         self.opponent_tomb_repository.create_opponent_tomb_card(
                        #             opponent_field_card_id)
                        #
                        #         self.opponent_field_unit_repository.replace_opponent_field_unit_card_position()
                        #
                        #     self.opponent_fixed_unit_card_inside_handler.clear_opponent_field_area_action()
                        #     self.targeting_enemy_select_using_your_field_card_index = None
                        #     self.targeting_enemy_select_using_your_field_card_id = None
                        #     self.targeting_enemy_select_support_lightning_border_list = []
                        #     self.opponent_you_selected_lightning_border_list = []
                        #
                        #     self.selected_object = None
                        #     self.active_panel_rectangle = None
                        #     self.current_fixed_details_card = None
                        #     self.your_active_panel.clear_all_your_active_panel()
                        #
                        #     return
                        #
                        # self.play_effect_animation_by_index_and_call_function(
                        #     your_field_card_index, calculate_shadow_ball)

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

                # print(f"your field unit (field_unit) = {type(your_field_unit)}")
                fixed_card_base = your_field_unit.get_fixed_card_base()
                # page_selected_card = self.your_hand_repository.get_current_your_hand_page()
                # print(f"your field unit type (fixed_card_base) = {type(fixed_card_base)}")
                # print(f"page_selected_card = {page_selected_card}")

                if fixed_card_base.is_point_inside((x, y)):
                    # if self.your_field_unit_action_repository.get_current_field_unit_action_status(your_field_unit.get_index()) == FieldUnitActionStatus.WAIT:
                    #     print(f"처음 필드에 출격한 유닛은 공격 할 수 없습니다")

                    if self.field_area_inside_handler.get_field_area_action() is FieldAreaAction.ENERGY_BOOST:
                        self.field_area_inside_handler.clear_lightning_border_list()
                        self.field_area_inside_handler.clear_field_area_action()
                        self.your_field_unit_lightning_border_list = []

                        your_unit_index = your_field_unit.get_index()

                        response = self.your_hand_repository.request_use_overflow_of_energy(
                            RequestUseOverflowOfEnergy(
                                _sessionInfo=self.__session_repository.get_first_fake_session_info(),
                                _unitIndex=your_unit_index,
                                _supportCardId="2")
                        )

                        is_success_value = response.get('is_success', False)

                        if is_success_value == False:
                            # self.selected_object = None
                            self.reset_every_selected_action()
                            is_false_message = response.get('false_message_enum')
                            self.message_on_the_screen.create_message_on_the_battle_screen(
                                is_false_message)
                            return

                        print("덱에서 에너지 검색해서 부스팅 진행")

                        def overflow_of_energy(response):
                            self.__music_player_repository.play_sound_effect_of_card_execution('overflow_of_energy')

                            current_process_card_id = self.field_area_inside_handler.get_action_set_card_id()

                            proper_handler = self.support_card_handler.getSupportCardHandler(current_process_card_id)
                            # proper_handler(your_field_unit.get_index())

                            # your_field_unit_index = your_field_unit.get_index()
                            # print(f"your_field_unit index: {your_unit_index}")

                            # real_field_unit_index = self.your_field_unit_repository.find_field_unit_by_index(your_field_unit.get_index())
                            # print(f"real_field_unit_index: {real_field_unit_index}")

                            updated_deck_card_list = response.get('updated_deck_card_list')
                            your_field_unit_index = int(list(response['player_field_unit_energy_map']['You']['field_unit_energy_map'].keys())[0])
                            print(f"updated_deck_card_list: {updated_deck_card_list}")

                            proper_handler(your_field_unit_index, updated_deck_card_list)

                            used_energy_card_list_from_deck = response['player_deck_card_use_list_map']['You']
                            print(f"used_energy_card_list_from_deck: {used_energy_card_list_from_deck}")
                            for used_energy_card in used_energy_card_list_from_deck:
                                self.your_tomb_repository.create_tomb_card(used_energy_card)

                            self.selected_object = None
                            self.your_tomb_repository.create_tomb_card(current_process_card_id)

                            current_hand_list = self.your_hand_repository.get_current_hand_state()
                            print(f"get_current_hand_state: {current_hand_list}")

                            placed_card_page = self.field_area_inside_handler.get_placed_card_page()
                            placed_card_index = self.field_area_inside_handler.get_placed_card_index()
                            self.your_hand_repository.remove_card_by_index_and_page_number(placed_card_page,
                                                                                           placed_card_index)
                            self.your_hand_repository.update_your_hand()

                            updated_hand_list = self.your_hand_repository.get_current_hand_state()
                            print(f"updated_hand_list: {updated_hand_list}")

                            # self.boost_selection = False

                        self.create_effect_animation_to_your_unit_and_play_animation_and_call_function_with_param(
                            'overflow_of_energy', your_unit_index, overflow_of_energy, response
                        )

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
                        self.current_fixed_details_card = None
                        self.your_active_panel.clear_all_your_active_panel()

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

                    # search_request_index_list = []
                    #
                    # processing_length = len(self.selected_search_unit_index_list)
                    # for index in range(processing_length):
                    #     search_request_index_list.append(
                    #         self.selected_search_unit_index_list[index] + 12 *
                    #         self.selected_search_unit_page_number_list[index])

                    search_request_index_list = [
                        str(index + 12 * page_number)
                        for index, page_number in
                        zip(self.selected_search_unit_index_list, self.selected_search_unit_page_number_list)
                    ]

                    response = self.your_deck_repository.request_use_call_of_leonic(
                        RequestUseCallOfLeonic(
                            _sessionInfo=self.__session_repository.get_first_fake_session_info(),
                            _supportCardId="30",
                            _targetUnitCardIndexList=search_request_index_list)
                    )
                    print(f"{Fore.RED}call_of_leonic -> response:{Fore.GREEN} {response}{Style.RESET_ALL}")
                    is_success_value = response.get('is_success', False)

                    if is_success_value == False:
                        self.reset_every_selected_action()
                        self.field_area_inside_handler.clear_field_area_action()

                        self.selected_search_unit_lightning_border = []
                        self.selected_search_unit_index_list = []
                        self.selected_search_unit_id_list = []
                        self.selected_search_unit_page_number_list = []
                        print(f"self.field_area_inside_handler.get - > {self.field_area_inside_handler.get_field_area_action()}")
                        is_false_message = response.get('false_message_enum')
                        self.message_on_the_screen.create_message_on_the_battle_screen(
                            is_false_message)
                        return
                    # 서포트
                    self.field_area_inside_handler.clear_field_area_action()

                    def call_of_leonic(response):
                        self.__music_player_repository.play_sound_effect_of_card_execution('call_of_leonic')


                        # 실제로 지울 때 몇 개 지우는지만 알면 된다.
                        # 어차피 셔플 받아서 이미지만 갈아 끼워넣을 것이기 때문
                        processing_length = len(self.selected_search_unit_index_list)
                        self.your_deck_repository.remove_card_object_list_with_count(processing_length)

                        self.your_hand_repository.remove_card_by_index_with_page(
                            self.field_area_inside_handler.get_placed_card_index())
                        self.your_tomb_repository.create_tomb_card(self.field_area_inside_handler.get_action_set_card_id())

                        # self.your_hand_repository.create_additional_hand_card_list(self.selected_search_unit_id_list)
                        self.your_hand_repository.save_current_hand_state(self.selected_search_unit_id_list)
                        self.your_hand_repository.update_your_hand()
                        # self.selected_search_unit_page_number_list
                        self.selected_search_unit_lightning_border = []


                        shuffled_deck_list = response.get('updated_deck_card_list')

                        self.your_deck_repository.update_deck(shuffled_deck_list)

                        # 셔플 받았다 가정
                        # current_deck_list = self.your_deck_repository.get_current_deck_state()
                        #
                        # will_remove_index_from_deck = []
                        # processing_length = len(self.selected_search_unit_index_list)
                        # for index in range(processing_length):
                        #     will_remove_index_from_deck.append(
                        #         self.selected_search_unit_index_list[index] + 12 *
                        #         self.selected_search_unit_page_number_list[index])
                        #
                        # print(f"will_remove_index_from_deck: {will_remove_index_from_deck}")
                        #
                        # remaining_shuffled_deck_list = [card for i, card in enumerate(current_deck_list) if
                        #                                 i not in will_remove_index_from_deck]
                        #
                        # # 셔플
                        # random.shuffle(remaining_shuffled_deck_list)
                        # print(f"Shuffled deck (excluding removed indices): {remaining_shuffled_deck_list}")

                        self.selected_search_unit_index_list = []
                        self.selected_search_unit_id_list = []
                        self.selected_search_unit_page_number_list = []

                    self.create_effect_animation_to_your_field_and_play_animation_and_call_function_with_param(
                        'call_of_leonic', call_of_leonic, response)

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

                opponent_field_unit_object_list = (
                    self.opponent_field_unit_repository.get_current_field_unit_card_object_list())

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
                            opponent_you_selected_object_index_list = []
                            for selected_object in self.opponent_you_selected_object_list:
                                opponent_you_selected_object_index_list.append(selected_object.get_index())

                            corpse_explosion_response = self.your_hand_repository.request_use_corpse_explosion(
                                RequestUseCorpseExplosion(
                                    _sessionInfo=self.__session_repository.get_first_fake_session_info(),
                                    _itemCardId=33,
                                    _unitIndex=self.targeting_enemy_select_using_your_field_card_index,
                                    _opponentTargetUnitIndexList=opponent_you_selected_object_index_list
                                )
                            )
                            print(f"corpse_explosion_response : {corpse_explosion_response}")

                            is_success_value = corpse_explosion_response.get('is_success', False)

                            if is_success_value == False:
                                # self.fixed_unit_card_inside_action = FixedUnitCardInsideAction.Dummy
                                #
                                # self.targeting_ememy_select_using_hand_card_id = -1
                                # self.targeting_ememy_select_using_hand_card_index = -1
                                # self.targeting_enemy_select_using_your_field_card_index = -1
                                # self.targeting_enemy_for_sacrifice_unit_id = -1
                                #
                                # self.targeting_enemy_select_support_lightning_border_list = []
                                # self.opponent_you_selected_lightning_border_list = []
                                # self.opponent_you_selected_object_list = []
                                self.return_to_initial_location()
                                self.reset_every_selected_action()
                                is_false_message = corpse_explosion_response.get('false_message_enum')
                                self.message_on_the_screen.create_message_on_the_battle_screen(
                                    is_false_message)
                                return

                            def calculate_corpse_explosion():
                                print(f"calculate_corpse_explosion : {corpse_explosion_response}")
                                remove_from_field_index_list = []
                                remove_from_field_id_list = []

                                sacrificed_unit_hp = 0

                                for opponent_field_unit_index, opponent_field_unit_remain_hp in corpse_explosion_response.get(
                                        'player_field_unit_health_point_map', {}).get('Opponent', {}).get(
                                        'field_unit_health_point_map', {}).items():
                                    if opponent_field_unit_remain_hp == 0:
                                        continue

                                    opponent_field_unit = self.opponent_field_unit_repository.find_opponent_field_unit_by_index(int(opponent_field_unit_index))
                                    opponent_fixed_card_base = opponent_field_unit.get_fixed_card_base()

                                    for opponent_fixed_base_attached_shape in opponent_fixed_card_base.get_attached_shapes():
                                        if isinstance(opponent_fixed_base_attached_shape, NonBackgroundNumberImage):
                                            if opponent_fixed_base_attached_shape.get_circle_kinds() is CircleKinds.HP:

                                                # def calculate_remain_hp_to_opponent_unit(param):
                                                #     _opponent_fixed_card_attached_shape = param[0]
                                                #     _hp_number = param[1]
                                                #     print(f"corpse explosion -> hp_number: {_hp_number}")
                                                #     _opponent_fixed_card_attached_shape.set_number(_hp_number)
                                                #
                                                #     _opponent_fixed_card_attached_shape.set_image_data(
                                                #         self.pre_drawed_image_instance.get_pre_draw_unit_hp(_hp_number))
                                                #
                                                # self.create_effect_animation_to_opponent_unit_and_play_animation_and_call_function_with_param(
                                                #     'dark_blast', int(opponent_field_unit_index),
                                                #     calculate_remain_hp_to_opponent_unit,
                                                #     (opponent_fixed_base_attached_shape, opponent_field_unit_remain_hp))

                                                opponent_fixed_base_attached_shape.set_number(opponent_field_unit_remain_hp)
                                                opponent_fixed_base_attached_shape.set_image_data(
                                                    self.pre_drawed_image_instance.get_pre_draw_character_hp_image(opponent_field_unit_remain_hp)
                                                )


                                for player, dead_unit_list_map in corpse_explosion_response['player_field_unit_death_map'].items():
                                    dead_unit_list = dead_unit_list_map['dead_field_unit_index_list']

                                    if player == 'You':
                                        print('희생당한 유닛 사망처리')
                                        for dead_unit in dead_unit_list:
                                            def remove_field_unit(unit_index):
                                                card_id = self.your_field_unit_repository.get_card_id_by_index(unit_index)
                                                self.your_tomb_repository.create_tomb_card(card_id)
                                                self.your_field_unit_repository.remove_card_by_index(unit_index)
                                                self.your_field_unit_repository.remove_harmful_status_by_index(unit_index)
                                                self.your_field_unit_repository.replace_field_card_position()

                                            self.create_effect_animation_to_your_unit_and_play_animation_and_call_function_with_param(
                                                'death', dead_unit,  remove_field_unit ,dead_unit)


                                    elif player == 'Opponent':
                                        print('죽은 상대 유닛 사망처리')
                                        for dead_unit in dead_unit_list:
                                            def remove_field_unit(unit_index):
                                                card_id = self.opponent_field_unit_repository.get_opponent_card_id_by_index(unit_index)
                                                self.opponent_tomb_repository.create_opponent_tomb_card(card_id)
                                                self.opponent_field_unit_repository.remove_current_field_unit_card(unit_index)
                                                self.opponent_field_unit_repository.remove_harmful_status_by_index(unit_index)
                                                self.opponent_field_unit_repository.replace_opponent_field_unit_card_position()

                                            self.create_effect_animation_to_opponent_unit_and_play_animation_and_call_function_with_param(
                                                'death', dead_unit, remove_field_unit, dead_unit)

                                    else:
                                        print('unknown player!!')

                                # your_field_unit_list = self.your_field_unit_repository.get_current_field_unit_list()
                                # for your_field_unit in your_field_unit_list:
                                #     if your_field_unit is None:
                                #         continue
                                #
                                #     if isinstance(your_field_unit, FixedFieldCard):
                                #         your_field_unit.selected = False
                                #
                                # for your_field_unit in self.your_field_unit_repository.get_current_field_unit_list():
                                #     if your_field_unit is None:
                                #         continue
                                #
                                #     if self.targeting_enemy_select_using_your_field_card_index ==  your_field_unit.get_index():
                                #
                                #         # if self.selected_object.get_card_number() == 9:
                                #         #     self.return_to_initial_location()
                                #
                                #         print(f"your field unit (field_unit) = {type(your_field_unit)}")
                                #         fixed_card_base = your_field_unit.get_fixed_card_base()
                                #         # page_selected_card = self.your_hand_repository.get_current_your_hand_page()
                                #         print(f"your field unit type (fixed_card_base) = {type(fixed_card_base)}")
                                #
                                #         for fixed_card_base_attached_shape in fixed_card_base.get_attached_shapes():
                                #             if isinstance(fixed_card_base_attached_shape, NonBackgroundNumberImage):
                                #                 if fixed_card_base_attached_shape.get_circle_kinds() is CircleKinds.HP:
                                #
                                #                     sacrificed_unit_hp_number = fixed_card_base_attached_shape.get_number()
                                #                     print(f'sacrificed_unit_hp_number : {sacrificed_unit_hp_number}')
                                #                     sacrificed_unit_hp = sacrificed_unit_hp_number
                                #                     break
                                #         break
                                #
                                # for opponent_you_selected_object in self.opponent_you_selected_object_list:
                                #     opponent_fixed_card_base = opponent_you_selected_object.get_fixed_card_base()
                                #
                                #     opponent_fixed_card_attached_shape_list = opponent_fixed_card_base.get_attached_shapes()
                                #     # remove_from_field = False
                                #
                                #     for opponent_fixed_card_attached_shape in opponent_fixed_card_attached_shape_list:
                                #         if isinstance(opponent_fixed_card_attached_shape, NonBackgroundNumberImage):
                                #             if opponent_fixed_card_attached_shape.get_circle_kinds() is CircleKinds.HP:
                                #                 print(f'{opponent_you_selected_object.get_index()} hp changed! ')
                                #                 print(f"{opponent_fixed_card_attached_shape.get_number()} -> ")
                                #                 print(f"{opponent_fixed_card_attached_shape.get_number() - sacrificed_unit_hp}")
                                #                 hp_number = opponent_fixed_card_attached_shape.get_number()
                                #                 hp_number -= sacrificed_unit_hp
                                #
                                #
                                #                 # TODO: n 턴간 불사 특성을 검사해야하므로 사실 이것도 summary 방식으로 빼는 것이 맞으나 우선은 진행한다.
                                #                 # (지금 당장 불사가 존재하지 않음)
                                #                 if hp_number <= 0:
                                #                     # remove_from_field = True
                                #                     remove_from_field_index_list.append(
                                #                         opponent_you_selected_object.get_index())
                                #                     remove_from_field_id_list.append(
                                #                         opponent_you_selected_object.get_card_number())
                                #
                                #                     break
                                #
                                #                 def calculate_remain_hp_to_opponent_unit(param):
                                #                     _opponent_fixed_card_attached_shape = param[0]
                                #                     _hp_number = param[1]
                                #                     print(f"corpse explosion -> hp_number: {hp_number}")
                                #                     _opponent_fixed_card_attached_shape.set_number(_hp_number)
                                #
                                #                     # opponent_fixed_card_attached_shape.set_image_data(
                                #                     #     # TODO: 실제로 여기서 서버로부터 계산 받은 값을 적용해야함
                                #                     #     self.pre_drawed_image_instance.get_pre_draw_number_image(hp_number))
                                #
                                #                     _opponent_fixed_card_attached_shape.set_image_data(
                                #                         self.pre_drawed_image_instance.get_pre_draw_unit_hp(_hp_number))
                                #
                                #                 self.create_effect_animation_to_opponent_unit_and_play_animation_and_call_function_with_param(
                                #                     'dark_blast', opponent_you_selected_object.get_index(), calculate_remain_hp_to_opponent_unit,
                                #                     (opponent_fixed_card_attached_shape,hp_number))
                                #
                                #     # if remove_from_field:
                                #     #     card_id = opponent_you_selected_object.get_card_number()
                                #     #
                                #     #     self.opponent_field_unit_repository.remove_current_field_unit_card(opponent_you_selected_object.get_index())
                                #     #     self.opponent_tomb_repository.create_opponent_tomb_card(card_id)
                                #
                                # # for remove_from_field in remove_from_field_list:

                                print(
                                    f"corpse explosion your hand index: {self.targeting_ememy_select_using_hand_card_index}")
                                # self.your_hand_repository.remove_card_by_index(
                                #     self.targeting_ememy_select_using_hand_card_index)

                                self.your_hand_repository.remove_card_by_index_with_page(
                                    self.targeting_ememy_select_using_hand_card_index)
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
                                # self.your_tomb_repository.create_tomb_card(
                                #     self.targeting_ememy_select_using_hand_card_id)
                                #
                                # for card_id in remove_from_field_id_list:
                                #     self.opponent_tomb_repository.create_opponent_tomb_card(card_id)
                                #
                                # for index in remove_from_field_index_list:
                                #     effect_animation = EffectAnimation()
                                #     effect_animation.set_animation_name('death')
                                #     effect_animation.set_total_window_size(self.width, self.height)
                                #     effect_animation.change_local_translation(
                                #         self.opponent_field_unit_repository.find_opponent_field_unit_by_index(
                                #         index).get_fixed_card_base().get_local_translation())
                                #     effect_animation.draw_animation_panel()
                                #     effect_animation_panel = effect_animation.get_animation_panel()
                                #
                                #     animation_index = self.effect_animation_repository.save_effect_animation_at_dictionary_without_index_and_return_index(
                                #         effect_animation)
                                #
                                #     self.effect_animation_repository.save_effect_animation_panel_at_dictionary_with_index(
                                #         animation_index, effect_animation_panel)
                                #
                                #     def remove_opponent_unit(_index):
                                #         self.opponent_field_unit_repository.remove_current_field_unit_card(_index)
                                #         # TODO: ID 와 index 로 처리하는 것은 명확히 구분될 필요가 있음
                                #         # self.opponent_tomb_repository.create_opponent_tomb_card(card_id)
                                #         self.opponent_field_unit_repository.replace_opponent_field_unit_card_position()
                                #         self.opponent_field_unit_repository.remove_harmful_status_by_index(_index)
                                #
                                #     self.play_effect_animation_by_index_and_call_function_with_param(animation_index, remove_opponent_unit, index)
                                #
                                #
                                #
                                # print(
                                #     f"corpse explosion your field index: {self.targeting_enemy_select_using_your_field_card_index}")

                                # def remove_your_unit_by_index():
                                #
                                #     self.your_field_unit_repository.remove_card_by_index(
                                #         self.targeting_enemy_select_using_your_field_card_index)
                                #     self.your_tomb_repository.create_tomb_card(self.targeting_enemy_for_sacrifice_unit_id)
                                #     self.your_field_unit_repository.remove_harmful_status_by_index(self.targeting_enemy_select_using_your_field_card_index)
                                #     # self.your_hand_repository.replace_hand_card_position()
                                #
                                #     return
                                #
                                # self.create_effect_animation_to_your_unit_and_play_animation_and_call_function(
                                #     'death', self.targeting_enemy_select_using_your_field_card_index,
                                #     remove_your_unit_by_index)

                            def vibration_corpse_explosion():
                                vibration_object_list = self.opponent_you_selected_object_list
                                sacrificed_unit = self.your_field_unit_repository.find_field_unit_by_index(self.targeting_enemy_select_using_your_field_card_index)
                                vibration_object_list.append(sacrificed_unit)
                                self.corpse_explosion_vibration_finish_count = len(vibration_object_list)
                                # self.corpse_explosion_vibration_finish_count = len(self.opponent_you_selected_object_list)
                                self.corpse_explosion_vibration_current_count = 0
                                for selected_object in vibration_object_list:

                                    steps = 30



                                    def vibration(selected_object, step_count):

                                        fixed_card_base = selected_object.get_fixed_card_base()
                                        tool_card = selected_object.get_tool_card()
                                        attached_shape_list = fixed_card_base.get_attached_shapes()

                                        if step_count % 2 == 1:
                                            vibration_factor = 10
                                            random_translation = (random.uniform(-vibration_factor, vibration_factor),
                                                                  random.uniform(-vibration_factor, vibration_factor))

                                            new_fixed_card_base_vertices = [
                                                (vx + random_translation[0], vy + random_translation[1]) for vx, vy in
                                                fixed_card_base.get_vertices()
                                            ]
                                            fixed_card_base.update_vertices(new_fixed_card_base_vertices)

                                            if tool_card is not None:
                                                new_tool_card_vertices = [
                                                    (vx + random_translation[0], vy + random_translation[1]) for vx, vy in
                                                    tool_card.get_vertices()
                                                ]
                                                tool_card.update_vertices(new_tool_card_vertices)

                                            for attached_shape in attached_shape_list:
                                                new_attached_shape_vertices = [
                                                    (vx + random_translation[0], vy + random_translation[1]) for vx, vy in
                                                    attached_shape.get_vertices()
                                                ]
                                                attached_shape.update_vertices(new_attached_shape_vertices)

                                        else:
                                            fixed_card_base.update_vertices(fixed_card_base.get_initial_vertices())
                                            if tool_card is not None:
                                                tool_card.update_vertices(tool_card.get_initial_vertices())
                                            for attached_shape in attached_shape_list:
                                                attached_shape.update_vertices(attached_shape.get_initial_vertices())

                                        if step_count < steps:
                                            self.master.after(20, vibration, selected_object, step_count + 1)
                                        else:
                                            self.corpse_explosion_vibration_current_count += 1
                                            if self.corpse_explosion_vibration_current_count == self.corpse_explosion_vibration_finish_count:
                                                calculate_corpse_explosion()

                                    vibration(selected_object, 1)



                            field_vertices = self.opponent_field_panel.get_vertices()
                            main_character_vertices = self.opponent_main_character_panel.get_vertices()

                            vertices = [(field_vertices[0][0], main_character_vertices[0][1]),
                                        (field_vertices[2][0], main_character_vertices[1][1]),
                                        field_vertices[3], field_vertices[0]]

                            self.create_effect_animation_with_vertices_and_play_animation_and_call_function(
                                'corpse_explosion', vertices, vibration_corpse_explosion)

            your_hand_next_button_clicked = self.your_hand.is_point_inside_next_button_hand((x, y))
            if your_hand_next_button_clicked:
                print("Your Hand Next Button Clicked!")
                self.__music_player_repository.play_sound_effect_of_mouse_on_click('page_button_click')

                self.your_hand_repository.next_your_hand_page()
                self.selected_object = None

            your_hand_prev_button_clicked = self.your_hand.is_point_inside_prev_button_hand((x, y))
            if your_hand_prev_button_clicked:
                print("Your Hand Prev Button Clicked!")
                self.__music_player_repository.play_sound_effect_of_mouse_on_click('page_button_click')

                self.your_hand_repository.prev_your_hand_page()
                self.selected_object = None

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
                self.message_on_the_screen.create_message_on_the_battle_screen(MessageNumber.YOUR_TOMB.value)
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
                self.message_on_the_screen.create_message_on_the_battle_screen(MessageNumber.OPPONENT_TOMB.value)
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
                self.message_on_the_screen.create_message_on_the_battle_screen(MessageNumber.YOUR_LOST_ZONE.value)

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
                self.message_on_the_screen.create_message_on_the_battle_screen(MessageNumber.OPPONENT_LOST_ZONE.value)

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
                # self.your_deck_repository.clear_deck_state()
                self.your_deck_repository.update_deck(deck_card_list)

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

                self.your_deck_repository.update_deck(multi_draw_response.get('updated_deck_card_list'))

                # before_current_deck_list = self.your_deck_repository.get_current_deck_state_object().get_current_deck()
                # print(f"{Fore.RED}before multi draw -> before_current_deck_list:{Fore.GREEN} {before_current_deck_list}{Style.RESET_ALL}")
                #
                # for _ in range(20):
                #     self.your_deck_repository.get_current_deck_state_object().draw_card()

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
        #self.timer.stop_timer()
        turn_end_request_result = self.round_repository.request_turn_end(
            TurnEndRequest(
                self.__session_repository.get_session_info()))
        print(f"turn_end_request_result: {turn_end_request_result}")

        if not turn_end_request_result.get('is_success', False):
            return

        if turn_end_request_result.get('player_main_character_survival_map', {}).get('Opponent', None) == 'Death':
            # self.opponent_hp_repository.opponent_character_die()
            self.timer.stop_timer()
            self.battle_field_repository.win()
            return

        self.__notify_reader_repository.set_is_your_turn_for_check_fake_process(False)
        whose_turn = self.__notify_reader_repository.get_is_your_turn_for_check_fake_process()
        print(f"{Fore.RED}call_turn_end() -> whose_turn True(Your) or False(Opponent):{Fore.GREEN} {whose_turn}{Style.RESET_ALL}")

        hp_data = turn_end_request_result['player_field_unit_health_point_map']
        harmful_data = turn_end_request_result['player_field_unit_harmful_effect_map']
        dead_data = turn_end_request_result['player_field_unit_death_map']

        self.apply_response_data_of_field_unit_hp(hp_data)
        self.apply_response_data_of_harmful_status(harmful_data)
        self.apply_response_data_of_dead_unit(dead_data)

        # self.opponent_

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

        whose_turn = self.__notify_reader_repository.get_is_your_turn_for_check_fake_process()
        if whose_turn is False:
            self.timer.stop_timer()
            self.timer_repository.set_timer(60)
            self.timer_repository.set_function(self.fake_opponent_turn_end)
            self.timer.get_timer()
            self.timer.start_timer()
            self.message_on_the_screen.create_message_on_the_battle_screen(MessageNumber.OPPONENT_TURN.value)
            self.reset_every_selected_action()

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

        current_opponent_field_unit_list = self.opponent_field_unit_repository.get_current_field_unit_card_object_list()
        for opponent_field_unit in current_opponent_field_unit_list:
            if opponent_field_unit is None:
                continue

            opponent_fixed_card_base = opponent_field_unit.get_fixed_card_base()
            convert_y = self.winfo_reqheight() - y

            if opponent_fixed_card_base.is_point_inside((x, convert_y)):
                print(f"Inside Unit")
                self.opponent_selected_object = opponent_field_unit
                self.opponent_details_panel.create_opponent_details_panel((x, y), opponent_field_unit)

                new_rectangle = self.opponent_details_panel.get_opponent_details_panel()
                self.opponent_details_panel_rectangle = new_rectangle

                self.opponent_details_button = self.opponent_details_panel.get_opponent_details_panel_button()
            else:
                print(f"Outside Unit")

        current_page_your_hand_list = self.your_hand_repository.get_current_page_your_hand_list()
        if current_page_your_hand_list is not None:
            for current_page_hand_card in current_page_your_hand_list:
                your_hand_pickable_card_base = current_page_hand_card.get_pickable_card_base()
                convert_y = self.winfo_reqheight() - y

                if your_hand_pickable_card_base.is_point_inside((x, convert_y)):
                    print(f"Inside Unit")
                    self.selected_object = current_page_hand_card
                    self.your_hand_details_panel.create_your_hand_details_panel((x, y), current_page_hand_card)

                    new_rectangle = self.your_hand_details_panel.get_your_hand_details_panel()
                    self.your_hand_details_panel_rectangle = new_rectangle

                    self.your_hand_details_button = self.your_hand_details_panel.get_your_hand_details_panel_button()
                else:
                    print(f"Outside Unit")


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

    def damage_to_your_field_unit(self, field_unit_info):

        for dead_field_unit_index in field_unit_info["dead_field_unit_index_list"]:
            self.your_tomb_repository.create_tomb_card(
                self.your_field_unit_repository.find_field_unit_by_index(dead_field_unit_index).get_card_number())
            self.your_field_unit_repository.remove_card_by_index(dead_field_unit_index)
            self.your_field_unit_repository.replace_field_card_position()


        try:
            your_unit_index = field_unit_info['field_unit_index']

            your_field_unit = self.your_field_unit_repository.find_field_unit_by_index(your_unit_index)

            your_fixed_card_base = your_field_unit.get_fixed_card_base()
            your_fixed_card_attached_shape_list = your_fixed_card_base.get_attached_shapes()

            for your_fixed_card_attached_shape in your_fixed_card_attached_shape_list:
                if isinstance(your_fixed_card_attached_shape, NonBackgroundNumberImage):
                    if your_fixed_card_attached_shape.get_circle_kinds() is CircleKinds.HP:

                        hp_number = your_fixed_card_attached_shape.get_number()
                        hp_number -= 10

                        your_fixed_card_attached_shape.set_image_data(
                            self.pre_drawed_image_instance.get_pre_draw_unit_hp(
                                hp_number))

                        print(f"changed hp: {your_fixed_card_attached_shape.get_circle_kinds()}")
        except Exception as e:
            print(f"error occured!! : {e}")


    def damage_to_multiple_unit_by_sacrifice(self, field_unit_info):

        sacrifice_opponent_unit_index = field_unit_info['opponent_dead_field_unit_index_list'][0]
        dead_your_unit_index_list = field_unit_info['your_dead_field_unit_index_list']
        target_unit_index_list = field_unit_info['target_unit_index_list']
        target_unit_hp_list = field_unit_info['target_unit_hp_list']
        try:

            self.opponent_field_unit_repository.remove_current_field_unit_card(sacrifice_opponent_unit_index)

            for dead_your_unit_index in dead_your_unit_index_list:
                self.your_field_unit_repository.remove_card_by_index(dead_your_unit_index)

            for target_unit_index, target_unit_hp in zip(target_unit_index_list, target_unit_hp_list):
                if target_unit_hp == 0:
                    continue

                your_field_unit = self.your_field_unit_repository.find_field_unit_by_index(target_unit_index)

                your_fixed_card_base = your_field_unit.get_fixed_card_base()
                your_fixed_card_attached_shape_list = your_fixed_card_base.get_attached_shapes()

                for your_fixed_card_attached_shape in your_fixed_card_attached_shape_list:
                    if isinstance(your_fixed_card_attached_shape, NonBackgroundNumberImage):
                        if your_fixed_card_attached_shape.get_circle_kinds() is CircleKinds.HP:
                            your_fixed_card_attached_shape.set_image_data(
                                self.pre_drawed_image_instance.get_pre_draw_unit_hp(
                                    target_unit_hp))


        except Exception as e:
            print(f"notify corpse explision error!! : {e}")

    def apply_basic_attack_result_to_ui_with_response(self, response):
        is_opponent_data_in_response = False
        is_your_data_in_response = False

        opponent_unit_index = -1
        remain_opponent_unit_hp = -1

        try:
            dead_opponent_unit_index_list = (
                response.get('player_field_unit_death_map', {})
                .get('Opponent', {})['dead_field_unit_index_list'])

            opponent_unit_index = int(list(
                response.get('player_field_unit_health_point_map', {})
                .get('Opponent', {}).get('field_unit_health_point_map', {}).keys())[0])

            remain_opponent_unit_hp = (
                response.get('player_field_unit_health_point_map', {})
                .get('Opponent', {}).get('field_unit_health_point_map', {})
                .get(str(opponent_unit_index), None))

            is_opponent_data_in_response = True

        except:
            print("opponent data is not in response")

        if is_opponent_data_in_response:
            self.master.after(0, self.attack_animation)

            opponent_field_unit = (
                self.opponent_field_unit_repository.find_opponent_field_unit_by_index(opponent_unit_index))
            opponent_fixed_card_base = opponent_field_unit.get_fixed_card_base()
            opponent_fixed_card_attached_shape_list = opponent_fixed_card_base.get_attached_shapes()

            for opponent_fixed_card_attached_shape in opponent_fixed_card_attached_shape_list:
                if isinstance(opponent_fixed_card_attached_shape, NonBackgroundNumberImage):
                    if opponent_fixed_card_attached_shape.get_circle_kinds() is CircleKinds.HP:
                        print("지정한 상대방 유닛 HP Circle 찾기")

                        opponent_field_card_id = opponent_field_unit.get_card_number()
                        opponent_field_card_index = opponent_field_unit.get_index()

                        print(f"opponent_hp_number: {remain_opponent_unit_hp}")

                        self.attack_animation_object.set_opponent_field_hp_shape(opponent_fixed_card_attached_shape)

                        # TODO: n 턴간 불사 특성을 검사해야하므로 사실 이것도 summary 방식으로 빼는 것이 맞으나 우선은 진행한다.
                        # (지금 당장 불사가 존재하지 않음)
                        if remain_opponent_unit_hp <= 0:
                            self.attack_animation_object.set_opponent_field_unit_death(True)
                            self.attack_animation_object.set_opponent_field_death_unit_index(opponent_field_card_index)

                            break

                        print(f"공격 후 opponent unit 체력 -> hp_number: {remain_opponent_unit_hp}")
                        opponent_fixed_card_attached_shape.set_number(remain_opponent_unit_hp)
                        self.attack_animation_object.set_opponent_field_unit_death(False)

                        # opponent_fixed_card_attached_shape.set_image_data(
                        #     # TODO: 실제로 여기서 서버로부터 계산 받은 값을 적용해야함
                        #     self.pre_drawed_image_instance.get_pre_draw_number_image(opponent_hp_number))

                        # opponent_fixed_card_attached_shape.set_image_data(
                        #     self.pre_drawed_image_instance.get_pre_draw_unit_hp(remain_opponent_unit_hp))

            # for dead_opponent_unit_index in dead_opponent_unit_index_list:
            #     opponent_field_card_id = self.opponent_field_unit_repository.get_opponent_card_id_by_index(
            #         dead_opponent_unit_index)
            #
            #     self.opponent_field_unit_repository.remove_current_field_unit_card(dead_opponent_unit_index)
            #     self.opponent_tomb_repository.create_opponent_tomb_card(opponent_field_card_id)
            #
            # self.opponent_field_unit_repository.replace_opponent_field_unit_card_position()

        your_unit_index = -1
        remain_your_unit_hp = -1

        try:
            dead_your_unit_index_list = (
                response.get('player_field_unit_death_map', {})
                .get('You', {})['dead_field_unit_index_list'])

            your_unit_index = int(list(
                response.get('player_field_unit_health_point_map', {})
                .get('You', {}).get('field_unit_health_point_map', {}).keys())[0])

            remain_your_unit_hp = (
                response.get('player_field_unit_health_point_map', {})
                .get('You', {}).get('field_unit_health_point_map', {})
                .get(str(your_unit_index), None))

            is_your_data_in_response = True

        except:
            print("your data is not in response")

        if is_your_data_in_response:
            your_field_unit = self.your_field_unit_repository.find_field_unit_by_index(
                your_unit_index)
            your_fixed_card_base = your_field_unit.get_fixed_card_base()
            your_fixed_card_attached_shape_list = your_fixed_card_base.get_attached_shapes()

            for your_fixed_card_attached_shape in your_fixed_card_attached_shape_list:
                if isinstance(your_fixed_card_attached_shape, NonBackgroundNumberImage):
                    if your_fixed_card_attached_shape.get_circle_kinds() is CircleKinds.HP:

                        if remain_your_unit_hp <= 0:
                            self.attack_animation_object.set_your_field_unit_death(True)

                            self.attack_animation_object.set_your_field_death_unit_index(
                                your_unit_index)
                            break

                        print(f"공격 후 your unit 체력 -> hp_number: {remain_your_unit_hp}")
                        your_fixed_card_attached_shape.set_number(remain_your_unit_hp)

                        self.attack_animation_object.set_your_field_hp_shape(your_fixed_card_attached_shape)
                        self.attack_animation_object.set_your_field_unit_death(False)

                        # your_fixed_card_attached_shape.set_image_data(
                        #     # TODO: 실제로 여기서 서버로부터 계산 받은 값을 적용해야함
                        #     self.pre_drawed_image_instance.get_pre_draw_number_image(
                        #         your_hp_number))

                        # your_fixed_card_attached_shape.set_image_data(
                        #     self.pre_drawed_image_instance.get_pre_draw_unit_hp(
                        #         remain_your_unit_hp))

            print("your 유닛 hp 갱신 완료")

            # for dead_your_unit_index in dead_your_unit_index_list:
            #     your_field_card_id = self.your_field_unit_repository.get_card_id_by_index(
            #         dead_your_unit_index)
            #     self.your_tomb_repository.create_tomb_card(your_field_card_id)
            #     self.your_field_unit_repository.remove_card_by_index(dead_your_unit_index)
            #
            # self.your_field_unit_repository.replace_field_card_position()



    def attack_animation(self):
        self.is_playing_action_animation = True
        attack_animation_object = AttackAnimation.getInstance()
        animation_actor = attack_animation_object.get_animation_actor()
        # print(f"{Fore.RED}animation_actor(selected_object){Fore.GREEN} {animation_actor}{Style.RESET_ALL}")
        animation_actor_card_id = animation_actor.get_card_number()

        your_fixed_card_base = animation_actor.get_fixed_card_base()
        current_your_attacker_unit_vertices = your_fixed_card_base.get_vertices()
        # print(f"{Fore.RED}current_your_attacker_unit_vertices{Fore.GREEN} {current_your_attacker_unit_vertices}{Style.RESET_ALL}")
        current_your_attacker_unit_local_translation = your_fixed_card_base.get_local_translation()
        print(f"{Fore.RED}current_your_attacker_unit_local_translation{Fore.GREEN} {current_your_attacker_unit_local_translation}{Style.RESET_ALL}")

        new_y_value = current_your_attacker_unit_local_translation[1] + 30
        your_attacker_unit_destination_local_translation = (current_your_attacker_unit_local_translation[0], new_y_value)
        # print(f"{Fore.RED}your_attacker_unit_destination_local_translation{Fore.GREEN} {your_attacker_unit_destination_local_translation}{Style.RESET_ALL}")

        steps = 20
        step_x = (your_attacker_unit_destination_local_translation[0] - current_your_attacker_unit_local_translation[0]) / steps
        step_y = (your_attacker_unit_destination_local_translation[1] - current_your_attacker_unit_local_translation[1]) / steps
        step_y *= -1


        opponent_unit = attack_animation_object.get_opponent_field_unit()
        opponent_fixed_base = opponent_unit.get_fixed_card_base()
        opponent_fixed_base_vertices = opponent_fixed_base.get_vertices()
        opponent_unit_local_translation = opponent_fixed_base.get_local_translation()
        print(f"{Fore.RED}opponent_unit_local_translation: {Fore.GREEN}{opponent_unit_local_translation}{Style.RESET_ALL}")
        # opponent_unit_destination_x = opponent_unit_local_translation[0] - 125
        opponent_unit_destination_y = opponent_unit_local_translation[1] - 300
        # print(f"{Fore.RED}opponent_unit_destination -> {Fore.GREEN}x: {opponent_unit_destination_x}, y: {opponent_unit_destination_y}{Style.RESET_ALL}")
        your_biased_local_translation = 0

        epsilon = 1e-6
        if (abs(current_your_attacker_unit_local_translation[0] - opponent_unit_local_translation[0]) < epsilon or
                current_your_attacker_unit_local_translation[0] - opponent_unit_local_translation[0] > 0):
            # 이 경우 칼은 왼쪽으로 카드 width 만큼 추가 이동이 필요함
            angle_radians = math.radians(-65)
            bias_result = 170 * math.cos(angle_radians)
            # print(f"200 * cos(x): {bias_result}")
            your_biased_local_translation = current_your_attacker_unit_local_translation[0] - bias_result
            # your_biased_local_translation = current_your_attacker_unit_local_translation[0]
            opponent_unit_destination_x = opponent_unit_local_translation[0] - 145
            print("자신을 기준으로 같은 위치 혹은 좌측 공격 -> x 보정 진행")
        else:
            # opponent_unit_destination_x = opponent_unit_local_translation[0] - 145
            angle_radians = math.radians(-65)
            bias_result = 170 * math.cos(angle_radians)
            # print(f"200 * cos(x): {bias_result}")
            # your_biased_local_translation = current_your_attacker_unit_local_translation[0] - bias_result
            your_biased_local_translation = current_your_attacker_unit_local_translation[0]
            opponent_unit_destination_x = opponent_unit_local_translation[0] - 145

            print("자신을 기준으로 우측 공격 -> 보정 없음")

        # S = v0 * t + 0.5 * a * t^2
        # S = 0.5 * a * t^2 => step = 15
        # S = 0.5 * a * 225 = 580 / 225 = 2.57777

        # 670 -> 450 = 220 -> 440 / 225 = 1.9555
        # 670 -> 420 = 250 -> 500 / 225 = 2.2222
        # 670 -> 400 = 270 -> 540 / 225 = 2.4
        sword_accel_y = (current_your_attacker_unit_local_translation[1] - opponent_unit_destination_y) / 400
        print(f"{Fore.RED}sword_accel_y: {Fore.GREEN}{sword_accel_y}{Style.RESET_ALL}")
        # sword_accel_y *= -1
        # sword_accel_y = 2.4

        # 370 - 215 = 155 -> 310 / 225
        # sword_accel_x = (opponent_unit_destination_x - current_your_attacker_unit_local_translation[0]) / 400

        sword_accel_x = (opponent_unit_destination_x - your_biased_local_translation) / 200
        # sword_accel_x = opponent_unit_destination_x / 400
        print(f"{Fore.RED}sword_accel_x: {Fore.GREEN}{sword_accel_x}{Style.RESET_ALL}")
        # sword_accel_x = 1.3777

        def update_position(step_count):
            # print(f"{Fore.RED}step_count: {Fore.GREEN}{step_count}{Style.RESET_ALL}")

            new_x = current_your_attacker_unit_local_translation[0] + step_x * step_count
            new_y = current_your_attacker_unit_local_translation[1] + step_y * step_count

            new_vertices = [
                (vx + step_x * step_count, vy + step_y * step_count) for vx, vy in current_your_attacker_unit_vertices
            ]
            your_fixed_card_base.update_vertices(new_vertices)

            # tool_card = self.selected_object.get_tool_card()
            # if tool_card is not None:
            #     new_tool_card_vertices = [
            #         (vx + new_x, vy + new_y) for vx, vy in tool_card.vertices
            #     ]
            #     tool_card.update_vertices(new_tool_card_vertices)

            for attached_shape in your_fixed_card_base.get_attached_shapes():
                # theta = w0 * t + 0.5 * alpha * t^2
                # theta = 0.5 * alpha * t^2 => step_count = 15
                # theta = 0.5 * alpha * 225 = 65 / 225 = 0.28888
                # theta = 0.5 * alpha * 400 = 65 / 400 = 0.1625
                omega_accel_alpha = -0.1625

                if isinstance(attached_shape, NonBackgroundNumberImage):
                    if attached_shape.get_circle_kinds() is CircleKinds.ATTACK:
                        accel_y_dist = sword_accel_y * step_count
                        accel_y_dist *= -1

                        accel_x_dist = sword_accel_x * step_count
                        # x: 236 / 1920, y: -367 / 1043
                        new_attached_shape_vertices = [
                            (vx + accel_x_dist, vy + accel_y_dist) for vx, vy in attached_shape.vertices
                        ]
                        attached_shape.update_vertices(new_attached_shape_vertices)
                        attached_shape.update_rotation_angle(omega_accel_alpha * step_count * step_count)
                        print(f"{Fore.RED}sword new_attached_shape_vertices{Fore.GREEN} {new_attached_shape_vertices}{Style.RESET_ALL}")

                        if step_count == 20:
                            attack_animation_object.set_your_weapon_shape(attached_shape)

                        continue

                new_attached_shape_vertices = [
                    (vx + step_x, vy + step_y) for vx, vy in attached_shape.vertices
                ]
                attached_shape.update_vertices(new_attached_shape_vertices)
                # print(f"{Fore.RED}new_attached_shape_vertices: {Fore.GREEN}{new_attached_shape_vertices}{Style.RESET_ALL}")

            if step_count < steps:
                self.master.after(20, update_position, step_count + 1)
                # if step_count == 8 and self.card_info_repository.getCardJobForCardNumber(animation_actor_card_id) == 2:
                #     self.__music_player_repository.play_sound_effect_with_event_name_for_wav('magician_basic_attack')
            else:
                self.start_post_animation(attack_animation_object)
                self.is_attack_motion_finished = True
                attack_animation_object.set_is_finished(True)
                attack_animation_object.set_need_post_process(True)

        update_position(1)


    def start_post_animation(self, attack_animation_object):
        sword_shape = attack_animation_object.get_your_weapon_shape()
        your_animation_actor = attack_animation_object.get_animation_actor()
        animation_actor_card_id = your_animation_actor.get_card_number()

        steps = 30
        # (390 - 153) / 1848 = 0.1282
        sword_target_x = 0.1282 * attack_animation_object.get_total_width()
        print(f"{Fore.RED}sword_target_x{Fore.GREEN} {sword_target_x}{Style.RESET_ALL}")

        # S = v0 * t + 0.5 * a * t^2
        # S = 0.5 * a * t^2 => step = 10
        # S = 0.5 * a * 225 = sword_target_x / 100 = 2
        # 100 = (steps * steps)

        sword_accel_x = sword_target_x / 100
        print(f"{Fore.RED}sword_accel_x{Fore.GREEN} {sword_accel_x}{Style.RESET_ALL}")

        # theta = w0 * t + 0.5 * alpha * t^2
        # theta = 0.5 * alpha * t^2 => step_count = 10
        # theta = 0.5 * alpha * 100 = 30 / 100 = 0.3
        omega_accel_alpha = 0.3

        opponent_field_unit = self.attack_animation_object.get_opponent_field_unit()

        def slash_with_sword(step_count):
            if step_count == 1:
                if self.card_info_repository.getCardJobForCardNumber(animation_actor_card_id) == 1:
                    self.__music_player_repository.play_sound_effect_with_event_name('warrior_basic_attack')
                elif self.card_info_repository.getCardJobForCardNumber(animation_actor_card_id) == 2:
                    self.__music_player_repository.play_sound_effect_with_event_name('magician_basic_attack')
            if step_count < 11:
                sword_accel_x_dist = sword_accel_x * step_count

                new_attached_shape_vertices = [
                    (vx + sword_accel_x_dist, vy) for vx, vy in sword_shape.vertices
                ]
                sword_shape.update_vertices(new_attached_shape_vertices)

                current_angle = sword_shape.get_rotation_angle()
                sword_shape.update_rotation_angle(current_angle + omega_accel_alpha * step_count * step_count)

            if step_count > 2:
                fixed_card_base = opponent_field_unit.get_fixed_card_base()
                tool_card = opponent_field_unit.get_tool_card()
                attached_shape_list = fixed_card_base.get_attached_shapes()

                if step_count % 2 == 1:
                    vibration_factor = 10
                    random_translation = (random.uniform(-vibration_factor, vibration_factor),
                                          random.uniform(-vibration_factor, vibration_factor))

                    new_fixed_card_base_vertices = [
                        (vx + random_translation[0], vy + random_translation[1]) for vx, vy in
                        fixed_card_base.get_vertices()
                    ]
                    fixed_card_base.update_vertices(new_fixed_card_base_vertices)

                    if tool_card is not None:
                        new_tool_card_vertices = [
                            (vx + random_translation[0], vy + random_translation[1]) for vx, vy in tool_card.get_vertices()
                        ]
                        tool_card.update_vertices(new_tool_card_vertices)

                    for attached_shape in attached_shape_list:
                        new_attached_shape_vertices = [
                            (vx + random_translation[0], vy + random_translation[1]) for vx, vy in
                            attached_shape.get_vertices()
                        ]
                        attached_shape.update_vertices(new_attached_shape_vertices)

                else:
                    fixed_card_base.update_vertices(fixed_card_base.get_initial_vertices())
                    if tool_card is not None:
                        tool_card.update_vertices(tool_card.get_initial_vertices())
                    for attached_shape in attached_shape_list:
                        attached_shape.update_vertices(attached_shape.get_initial_vertices())

            if step_count < steps:
                self.master.after(20, slash_with_sword, step_count + 1)
            else:
                self.finish_post_animation(attack_animation_object)

        self.play_effect_animation_by_index(attack_animation_object.get_animation_actor().get_index())
        slash_with_sword(1)



    def finish_post_animation(self, attack_animation_object):
        sword_shape = attack_animation_object.get_your_weapon_shape()

        animation_actor = attack_animation_object.get_animation_actor()
        your_fixed_card_base = animation_actor.get_fixed_card_base()
        tool_card = animation_actor.get_tool_card()
        attached_shape_list = your_fixed_card_base.get_attached_shapes()

        current_your_attacker_unit_vertices = your_fixed_card_base.get_vertices()
        current_your_attacker_unit_local_translation = your_fixed_card_base.get_local_translation()

        new_y_value = current_your_attacker_unit_local_translation[1] + 30
        your_attacker_unit_destination_local_translation = (
        current_your_attacker_unit_local_translation[0], new_y_value)

        steps = 15
        step_y = (your_attacker_unit_destination_local_translation[1] - current_your_attacker_unit_local_translation[1]) / steps
        step_y *= -1

        # (390 - 153) / 1848 = 0.1282
        current_sword_shape = attack_animation_object.get_your_weapon_shape()
        current_sword_shape_target = current_sword_shape.get_initial_vertices()

        current_sword_shape_target_x = current_sword_shape_target[0][0]
        current_sword_shape_target_y = current_sword_shape_target[0][1]

        # theta = w0 * t + 0.5 * alpha * t^2
        # theta = 0.5 * alpha * t^2 => step_count = 15
        # theta = 0.5 * alpha * 225 = angle / 112.5
        target_rotation_angle = sword_shape.get_rotation_angle()
        return_omega_accel_alpha = target_rotation_angle / 112.5

        def move_to_origin_location(step_count):
            new_y = current_your_attacker_unit_local_translation[1] + step_y * step_count
            print(f"{Fore.RED}step ->{Fore.GREEN}new_y: {new_y}{Style.RESET_ALL}")

            new_vertices = [
                (vx, vy - step_y * step_count) for vx, vy in current_your_attacker_unit_vertices
            ]
            your_fixed_card_base.update_vertices(new_vertices)
            # print(f"{Fore.RED}new_vertices{Fore.GREEN} {new_vertices}{Style.RESET_ALL}")

            # tool_card = self.selected_object.get_tool_card()
            # if tool_card is not None:
            #     new_tool_card_vertices = [
            #         (vx + new_x, vy + new_y) for vx, vy in tool_card.vertices
            #     ]
            #     tool_card.update_vertices(new_tool_card_vertices)

            for attached_shape in your_fixed_card_base.get_attached_shapes():
                # theta = w0 * t + 0.5 * alpha * t^2
                # theta = 0.5 * alpha * t^2 => step_count = 15
                # theta = 0.5 * alpha * 225 = 65 / 225 = 0.28888
                omega_accel_alpha = -0.28888

                if isinstance(attached_shape, NonBackgroundNumberImage):
                    if attached_shape.get_circle_kinds() is CircleKinds.ATTACK:
                        current_sword_shape_vertices = current_sword_shape.get_vertices()

                        current_sword_shape_x_vertex = current_sword_shape_vertices[0][0]
                        current_sword_shape_y_vertex = current_sword_shape_vertices[0][1]

                        # S = v0 * t + 0.5 * a * t^2
                        # S = 0.5 * a * t^2 => step = 15
                        # S = 0.5 * a * 225 = distance / 112.5
                        # 225 = (steps * steps)

                        # difference_x: 11.434448575145638, difference_y: 94.0313609929536

                        sword_accel_x = (current_sword_shape_target_x - current_sword_shape_x_vertex + 15.1677706645) / 112.5
                        sword_accel_y = (current_sword_shape_target_y - current_sword_shape_y_vertex + 124.732391723) / 112.5

                        sword_accel_x_dist = sword_accel_x * step_count
                        sword_accel_y_dist = sword_accel_y * step_count

                        new_attached_shape_vertices = [
                            (vx + sword_accel_x_dist, vy + sword_accel_y_dist) for vx, vy in sword_shape.vertices
                        ]
                        sword_shape.update_vertices(new_attached_shape_vertices)
                        # print(f"{Fore.RED}new_attached_shape_vertices: {Fore.GREEN}{new_attached_shape_vertices}{Style.RESET_ALL}")

                        current_angle = sword_shape.get_rotation_angle()
                        sword_shape.update_rotation_angle(current_angle - return_omega_accel_alpha * step_count)

                        continue

                print(
                    f"{Fore.RED}attached_shape.vertices: {Fore.GREEN}{attached_shape.vertices}{Style.RESET_ALL}")

                new_attached_shape_vertices = [
                    (vx, vy - step_y) for vx, vy in attached_shape.vertices
                ]
                attached_shape.update_vertices(new_attached_shape_vertices)
                # print(f"{Fore.RED}new_attached_shape_vertices: {Fore.GREEN}{new_attached_shape_vertices}{Style.RESET_ALL}")

            if step_count < steps:
                self.master.after(20, move_to_origin_location, step_count + 1)
            else:
                is_playing_action_animation = False
                your_fixed_card_base.update_vertices(your_fixed_card_base.get_initial_vertices())
                if tool_card is not None:
                    tool_card.update_vertices(tool_card.get_initial_vertices())
                for attached_shape in attached_shape_list:
                    attached_shape.update_vertices(attached_shape.get_initial_vertices())

                self.is_attack_motion_finished = True
                attack_animation_object.set_is_finished(True)
                attack_animation_object.set_need_post_process(True)

                if self.attack_animation_object.get_your_field_unit_death():
                    def remove_your_field_unit():
                        your_field_death_unit_index = self.attack_animation_object.get_your_field_death_unit_index()
                        card_id = self.your_field_unit_repository.get_card_id_by_index(your_field_death_unit_index)
                        self.your_field_unit_repository.remove_card_by_index(your_field_death_unit_index)
                        self.your_field_unit_repository.replace_field_card_position()
                        self.your_field_unit_repository.remove_harmful_status_by_index(your_field_death_unit_index)
                        self.your_tomb_repository.create_tomb_card(card_id)
                    self.create_effect_animation_to_your_unit_and_play_animation_and_call_function(
                        'death', self.attack_animation_object.get_your_field_death_unit_index(), remove_your_field_unit
                    )
                else:

                    your_field_hp_shape = self.attack_animation_object.get_your_field_hp_shape()
                    if your_field_hp_shape:
                        your_hp_number = your_field_hp_shape.get_number()

                        your_field_hp_shape.set_image_data(
                            self.pre_drawed_image_instance.get_pre_draw_unit_hp(
                                your_hp_number))

                if self.attack_animation_object.get_opponent_field_unit_death():
                    opponent_field_unit = self.attack_animation_object.get_opponent_field_unit()
                    opponent_field_unit_index = opponent_field_unit.get_index()
                    
                    def remove_field_unit_by_index():
                        self.opponent_field_unit_repository.remove_card_by_multiple_index([opponent_field_unit_index])
                        self.opponent_field_unit_repository.replace_opponent_field_unit_card_position()
                        self.opponent_field_unit_repository.remove_harmful_status_by_index(opponent_field_unit_index)
                        self.opponent_tomb_repository.create_opponent_tomb_card(opponent_field_unit.get_card_number())
                        
                    self.create_effect_animation_to_opponent_unit_and_play_animation_and_call_function('death', opponent_field_unit_index, remove_field_unit_by_index)
                else:
                    opponent_field_hp_shape = self.attack_animation_object.get_opponent_field_hp_shape()
                    if opponent_field_hp_shape:
                        opponent_hp_number = opponent_field_hp_shape.get_number()

                        opponent_field_hp_shape.set_image_data(
                            self.pre_drawed_image_instance.get_pre_draw_unit_hp(
                                opponent_hp_number))

        move_to_origin_location(1)

    def opponent_attack_your_unit_animation(self):
        self.is_playing_action_animation = True
        attack_animation_object = AttackAnimation.getInstance()

        notify_data = self.attack_animation_object.get_notify_data()

        opponent_animation_actor_index = int(next(iter(notify_data['player_field_unit_attack_map']['Opponent']['field_unit_attack_map'])))

        # opponent_animation_actor_index = next(iter(notify_data['player_field_unit_attack_map']['Opponent']['field_unit_attack_map'].values()))
        opponent_animation_actor = self.opponent_field_unit_repository.find_opponent_field_unit_by_index(opponent_animation_actor_index)
        attack_animation_object.set_opponent_animation_actor(opponent_animation_actor)
        animation_actor_card_id = opponent_animation_actor.get_card_number()

        opponent_fixed_card_base = opponent_animation_actor.get_fixed_card_base()
        current_opponent_attacker_unit_vertices = opponent_fixed_card_base.get_vertices()
        # print(f"{Fore.RED}current_your_attacker_unit_vertices{Fore.GREEN} {current_your_attacker_unit_vertices}{Style.RESET_ALL}")
        current_opponent_attacker_unit_local_translation = opponent_fixed_card_base.get_local_translation()
        print(f"{Fore.RED}current_your_attacker_unit_local_translation{Fore.GREEN} {current_opponent_attacker_unit_local_translation}{Style.RESET_ALL}")

        new_y_value = current_opponent_attacker_unit_local_translation[1] + 30
        opponent_attacker_unit_destination_local_translation = (current_opponent_attacker_unit_local_translation[0], new_y_value)
        # print(f"{Fore.RED}your_attacker_unit_destination_local_translation{Fore.GREEN} {your_attacker_unit_destination_local_translation}{Style.RESET_ALL}")

        steps = 20
        step_x = (opponent_attacker_unit_destination_local_translation[0] - current_opponent_attacker_unit_local_translation[0]) / steps
        step_y = (opponent_attacker_unit_destination_local_translation[1] - current_opponent_attacker_unit_local_translation[1]) / steps
        step_y *= -1

        target_index = notify_data['player_field_unit_attack_map']['Opponent']['field_unit_attack_map'][str(opponent_animation_actor_index)]['target_unit_index']
        your_unit = self.your_field_unit_repository.find_field_unit_by_index(target_index)
        attack_animation_object.set_your_field_unit(your_unit)
        # your_unit = attack_animation_object.get_your_field_unit()
        your_fixed_base = your_unit.get_fixed_card_base()
        your_fixed_base_vertices = your_fixed_base.get_vertices()
        your_unit_local_translation = your_fixed_base.get_local_translation()
        print(f"{Fore.RED}your_unit_local_translation: {Fore.GREEN}{your_unit_local_translation}{Style.RESET_ALL}")
        # opponent_unit_destination_x = opponent_unit_local_translation[0] - 125
        your_unit_destination_y = your_unit_local_translation[1] + 130
        # print(f"{Fore.RED}opponent_unit_destination -> {Fore.GREEN}x: {opponent_unit_destination_x}, y: {opponent_unit_destination_y}{Style.RESET_ALL}")
        your_biased_local_translation = 0

        epsilon = 1e-6
        if (abs(current_opponent_attacker_unit_local_translation[0] - your_unit_local_translation[0]) < epsilon or
                current_opponent_attacker_unit_local_translation[0] - your_unit_local_translation[0] > 0):
            # 이 경우 칼은 왼쪽으로 카드 width 만큼 추가 이동이 필요함
            angle_radians = math.radians(-65)
            bias_result = 170 * math.cos(angle_radians)
            # print(f"200 * cos(x): {bias_result}")
            opponent_biased_local_translation = current_opponent_attacker_unit_local_translation[0] - bias_result
            # your_biased_local_translation = current_your_attacker_unit_local_translation[0]
            your_unit_destination_x = your_unit_local_translation[0] - 145
            print("자신을 기준으로 같은 위치 혹은 좌측 공격 -> x 보정 진행")
        else:
            # opponent_unit_destination_x = opponent_unit_local_translation[0] - 145
            angle_radians = math.radians(-65)
            bias_result = 170 * math.cos(angle_radians)
            # print(f"200 * cos(x): {bias_result}")
            # your_biased_local_translation = current_your_attacker_unit_local_translation[0] - bias_result
            opponent_biased_local_translation = current_opponent_attacker_unit_local_translation[0]
            your_unit_destination_x = your_unit_local_translation[0] - 145

            print("자신을 기준으로 우측 공격 -> 보정 없음")

        # S = v0 * t + 0.5 * a * t^2
        # S = 0.5 * a * t^2 => step = 15
        # S = 0.5 * a * 225 = 580 / 225 = 2.57777

        # 670 -> 450 = 220 -> 440 / 225 = 1.9555
        # 670 -> 420 = 250 -> 500 / 225 = 2.2222
        # 670 -> 400 = 270 -> 540 / 225 = 2.4
        sword_accel_y = (current_opponent_attacker_unit_local_translation[1] - your_unit_destination_y) / 400
        print(f"{Fore.RED}sword_accel_y: {Fore.GREEN}{sword_accel_y}{Style.RESET_ALL}")
        # sword_accel_y *= -1
        # sword_accel_y = 2.4

        # 370 - 215 = 155 -> 310 / 225
        # sword_accel_x = (opponent_unit_destination_x - current_your_attacker_unit_local_translation[0]) / 400

        sword_accel_x = (your_unit_destination_x - opponent_biased_local_translation) / 200
        # sword_accel_x = opponent_unit_destination_x / 400
        print(f"{Fore.RED}sword_accel_x: {Fore.GREEN}{sword_accel_x}{Style.RESET_ALL}")

        # sword_accel_x = 1.3777

        def update_position(step_count):
            # print(f"{Fore.RED}step_count: {Fore.GREEN}{step_count}{Style.RESET_ALL}")

            new_x = current_opponent_attacker_unit_local_translation[0] + step_x * step_count
            new_y = current_opponent_attacker_unit_local_translation[1] + step_y * step_count

            new_vertices = [
                (vx + step_x * step_count, vy + step_y * step_count) for vx, vy in current_opponent_attacker_unit_vertices
            ]
            opponent_fixed_card_base.update_vertices(new_vertices)

            # tool_card = self.selected_object.get_tool_card()
            # if tool_card is not None:
            #     new_tool_card_vertices = [
            #         (vx + new_x, vy + new_y) for vx, vy in tool_card.vertices
            #     ]
            #     tool_card.update_vertices(new_tool_card_vertices)

            for attached_shape in opponent_fixed_card_base.get_attached_shapes():
                # theta = w0 * t + 0.5 * alpha * t^2
                # theta = 0.5 * alpha * t^2 => step_count = 15
                # theta = 0.5 * alpha * 225 = 65 / 225 = 0.28888
                # theta = 0.5 * alpha * 400 = 65 / 400 = 0.1625
                omega_accel_alpha = -0.1625

                if isinstance(attached_shape, NonBackgroundNumberImage):
                    if attached_shape.get_circle_kinds() is CircleKinds.ATTACK:
                        accel_y_dist = sword_accel_y * step_count
                        accel_y_dist *= -1

                        accel_x_dist = sword_accel_x * step_count
                        # x: 236 / 1920, y: -367 / 1043
                        new_attached_shape_vertices = [
                            (vx + accel_x_dist, vy + accel_y_dist) for vx, vy in attached_shape.vertices
                        ]
                        attached_shape.update_vertices(new_attached_shape_vertices)
                        attached_shape.update_rotation_angle(omega_accel_alpha * step_count * step_count)
                        print(
                            f"{Fore.RED}sword new_attached_shape_vertices{Fore.GREEN} {new_attached_shape_vertices}{Style.RESET_ALL}")

                        if step_count == 20:
                            attack_animation_object.set_opponent_weapon_shape(attached_shape)

                        continue

                new_attached_shape_vertices = [
                    (vx + step_x, vy + step_y) for vx, vy in attached_shape.vertices
                ]
                attached_shape.update_vertices(new_attached_shape_vertices)
                # print(f"{Fore.RED}new_attached_shape_vertices: {Fore.GREEN}{new_attached_shape_vertices}{Style.RESET_ALL}")

            if step_count < steps:
                self.master.after(20, update_position, step_count + 1)
                # if step_count == 8 and self.card_info_repository.getCardJobForCardNumber(animation_actor_card_id) == 2:
                #     self.__music_player_repository.play_sound_effect_with_event_name_for_wav('magician_basic_attack')
            else:
                self.start_opponent_attack_your_unit_post_animation(attack_animation_object)
                self.is_attack_motion_finished = True
                attack_animation_object.set_is_finished(True)
                attack_animation_object.set_need_post_process(True)

        update_position(1)

    def start_opponent_attack_your_unit_post_animation(self, attack_animation_object):
        sword_shape = attack_animation_object.get_opponent_weapon_shape()
        opponent_animation_actor = attack_animation_object.get_opponent_animation_actor()
        animation_actor_card_id = opponent_animation_actor.get_card_number()

        steps = 30
        # (390 - 153) / 1848 = 0.1282
        sword_target_x = 0.1282 * attack_animation_object.get_total_width()
        print(f"{Fore.RED}sword_target_x{Fore.GREEN} {sword_target_x}{Style.RESET_ALL}")

        # S = v0 * t + 0.5 * a * t^2
        # S = 0.5 * a * t^2 => step = 10
        # S = 0.5 * a * 225 = sword_target_x / 100 = 2
        # 100 = (steps * steps)

        sword_accel_x = sword_target_x / 100
        print(f"{Fore.RED}sword_accel_x{Fore.GREEN} {sword_accel_x}{Style.RESET_ALL}")

        # theta = w0 * t + 0.5 * alpha * t^2
        # theta = 0.5 * alpha * t^2 => step_count = 10
        # theta = 0.5 * alpha * 100 = 30 / 100 = 0.3
        omega_accel_alpha = 0.3

        your_field_unit = self.attack_animation_object.get_your_field_unit()

        def slash_with_sword(step_count):
            if step_count == 1:
                if self.card_info_repository.getCardJobForCardNumber(animation_actor_card_id) == 1:
                    self.__music_player_repository.play_sound_effect_with_event_name('warrior_basic_attack')
                elif self.card_info_repository.getCardJobForCardNumber(animation_actor_card_id) == 2:
                    self.__music_player_repository.play_sound_effect_with_event_name('magician_basic_attack')
            if step_count < 11:
                sword_accel_x_dist = sword_accel_x * step_count

                new_attached_shape_vertices = [
                    (vx + sword_accel_x_dist, vy) for vx, vy in sword_shape.vertices
                ]
                sword_shape.update_vertices(new_attached_shape_vertices)

                current_angle = sword_shape.get_rotation_angle()
                sword_shape.update_rotation_angle(current_angle + omega_accel_alpha * step_count * step_count)

            if step_count > 2:
                fixed_card_base = your_field_unit.get_fixed_card_base()
                tool_card = your_field_unit.get_tool_card()
                attached_shape_list = fixed_card_base.get_attached_shapes()

                if step_count % 2 == 1:
                    vibration_factor = 10
                    random_translation = (random.uniform(-vibration_factor, vibration_factor),
                                          random.uniform(-vibration_factor, vibration_factor))

                    new_fixed_card_base_vertices = [
                        (vx + random_translation[0], vy + random_translation[1]) for vx, vy in
                        fixed_card_base.get_vertices()
                    ]
                    fixed_card_base.update_vertices(new_fixed_card_base_vertices)

                    if tool_card is not None:
                        new_tool_card_vertices = [
                            (vx + random_translation[0], vy + random_translation[1]) for vx, vy in
                            tool_card.get_vertices()
                        ]
                        tool_card.update_vertices(new_tool_card_vertices)

                    for attached_shape in attached_shape_list:
                        new_attached_shape_vertices = [
                            (vx + random_translation[0], vy + random_translation[1]) for vx, vy in
                            attached_shape.get_vertices()
                        ]
                        attached_shape.update_vertices(new_attached_shape_vertices)

                else:
                    fixed_card_base.update_vertices(fixed_card_base.get_initial_vertices())
                    if tool_card is not None:
                        tool_card.update_vertices(tool_card.get_initial_vertices())
                    for attached_shape in attached_shape_list:
                        attached_shape.update_vertices(attached_shape.get_initial_vertices())

            if step_count < steps:
                self.master.after(20, slash_with_sword, step_count + 1)
            else:
                self.finish_opponent_attack_your_unit_post_animation(attack_animation_object)

        # self.play_effect_animation_by_index(attack_animation_object.get_animation_actor().get_index())


        opponent_field_unit_job_number = self.card_info_repository.getCardJobForCardNumber(animation_actor_card_id)
        effect_animation_name = ''
        for attack_type in AttackType:
            if attack_type.value == opponent_field_unit_job_number:
                effect_animation_name = attack_type.name
                print('effect animation name: ', effect_animation_name)
                break

        self.create_effect_animation_to_your_unit_and_play_animation_and_call_function(
            effect_animation_name, your_field_unit.get_index(), None)

        slash_with_sword(1)

    def finish_opponent_attack_your_unit_post_animation(self, attack_animation_object):
        sword_shape = attack_animation_object.get_opponent_weapon_shape()

        opponent_animation_actor = attack_animation_object.get_opponent_animation_actor()
        opponent_fixed_card_base = opponent_animation_actor.get_fixed_card_base()
        tool_card = opponent_animation_actor.get_tool_card()
        attached_shape_list = opponent_fixed_card_base.get_attached_shapes()

        current_opponent_attacker_unit_vertices = opponent_fixed_card_base.get_vertices()
        current_opponent_attacker_unit_local_translation = opponent_fixed_card_base.get_local_translation()

        new_y_value = current_opponent_attacker_unit_local_translation[1] + 30
        opponent_attacker_unit_destination_local_translation = (current_opponent_attacker_unit_local_translation[0], new_y_value)

        steps = 15
        step_y = (opponent_attacker_unit_destination_local_translation[1] - current_opponent_attacker_unit_local_translation[1]) / steps
        step_y *= -1

        # (390 - 153) / 1848 = 0.1282
        current_sword_shape = attack_animation_object.get_opponent_weapon_shape()
        current_sword_shape_target = current_sword_shape.get_initial_vertices()

        current_sword_shape_target_x = current_sword_shape_target[0][0]
        current_sword_shape_target_y = current_sword_shape_target[0][1]

        # theta = w0 * t + 0.5 * alpha * t^2
        # theta = 0.5 * alpha * t^2 => step_count = 15
        # theta = 0.5 * alpha * 225 = angle / 112.5
        target_rotation_angle = sword_shape.get_rotation_angle()
        return_omega_accel_alpha = target_rotation_angle / 112.5

        current_sword_shape_vertices = current_sword_shape.get_vertices()

        current_sword_shape_x_vertex = current_sword_shape_vertices[0][0]
        current_sword_shape_y_vertex = current_sword_shape_vertices[0][1]
        print(f"{Fore.RED}current_sword_shape_y_vertex: {Fore.GREEN}{current_sword_shape_y_vertex}{Style.RESET_ALL}")
        print(f"{Fore.RED}current_sword_shape_target_y: {Fore.GREEN}{current_sword_shape_target_y}{Style.RESET_ALL}")

        # S = v0 * t + 0.5 * a * t^2
        # S = 0.5 * a * t^2 => step = 15
        # S = 0.5 * a * 225 = distance / 112.5
        # 225 = (steps * steps)

        # difference_x: 11.434448575145638, difference_y: 94.0313609929536

        sword_accel_x = (current_sword_shape_target_x - current_sword_shape_x_vertex + 15.1677706645) / 112.5
        sword_accel_y = (current_sword_shape_target_y - current_sword_shape_y_vertex) / 112.5

        def move_to_origin_location(step_count):
            new_y = current_opponent_attacker_unit_local_translation[1] + step_y * step_count
            print(f"{Fore.RED}step ->{Fore.GREEN}new_y: {new_y}{Style.RESET_ALL}")

            new_vertices = [
                (vx, vy - step_y * step_count) for vx, vy in current_opponent_attacker_unit_vertices
            ]
            opponent_fixed_card_base.update_vertices(new_vertices)
            # print(f"{Fore.RED}new_vertices{Fore.GREEN} {new_vertices}{Style.RESET_ALL}")

            # tool_card = self.selected_object.get_tool_card()
            # if tool_card is not None:
            #     new_tool_card_vertices = [
            #         (vx + new_x, vy + new_y) for vx, vy in tool_card.vertices
            #     ]
            #     tool_card.update_vertices(new_tool_card_vertices)

            for attached_shape in opponent_fixed_card_base.get_attached_shapes():
                # theta = w0 * t + 0.5 * alpha * t^2
                # theta = 0.5 * alpha * t^2 => step_count = 15
                # theta = 0.5 * alpha * 225 = 65 / 225 = 0.28888
                omega_accel_alpha = -0.28888

                if isinstance(attached_shape, NonBackgroundNumberImage):
                    if attached_shape.get_circle_kinds() is CircleKinds.ATTACK:
                        # current_sword_shape_vertices = current_sword_shape.get_vertices()
                        #
                        # current_sword_shape_x_vertex = current_sword_shape_vertices[0][0]
                        # current_sword_shape_y_vertex = current_sword_shape_vertices[0][1]
                        # print(f"{Fore.RED}current_sword_shape_y_vertex: {Fore.GREEN}{current_sword_shape_y_vertex}{Style.RESET_ALL}")
                        # print(f"{Fore.RED}current_sword_shape_target_y: {Fore.GREEN}{current_sword_shape_target_y}{Style.RESET_ALL}")
                        #
                        # # S = v0 * t + 0.5 * a * t^2
                        # # S = 0.5 * a * t^2 => step = 15
                        # # S = 0.5 * a * 225 = distance / 112.5
                        # # 225 = (steps * steps)
                        #
                        # # difference_x: 11.434448575145638, difference_y: 94.0313609929536
                        #
                        # sword_accel_x = (
                        #                             current_sword_shape_target_x - current_sword_shape_x_vertex + 15.1677706645) / 112.5
                        # sword_accel_y = (
                        #                             current_sword_shape_target_y - current_sword_shape_target_y) / 112.5
                                            # 124.732391723) / 112.5

                        sword_accel_x_dist = sword_accel_x * step_count
                        sword_accel_y_dist = sword_accel_y * step_count
                        print(f"sword_accel_x_dist: {sword_accel_x_dist}, sword_accel_y_dist: {sword_accel_y_dist}")

                        new_attached_shape_vertices = [
                            (vx + sword_accel_x_dist, vy + sword_accel_y_dist) for vx, vy in sword_shape.vertices
                        ]
                        sword_shape.update_vertices(new_attached_shape_vertices)
                        # print(f"{Fore.RED}new_attached_shape_vertices: {Fore.GREEN}{new_attached_shape_vertices}{Style.RESET_ALL}")

                        current_angle = sword_shape.get_rotation_angle()
                        sword_shape.update_rotation_angle(current_angle - return_omega_accel_alpha * step_count)

                        continue

                # print(f"{Fore.RED}attached_shape.vertices: {Fore.GREEN}{attached_shape.vertices}{Style.RESET_ALL}")

                new_attached_shape_vertices = [
                    (vx, vy - step_y) for vx, vy in attached_shape.vertices
                ]
                attached_shape.update_vertices(new_attached_shape_vertices)
                # print(f"{Fore.RED}new_attached_shape_vertices: {Fore.GREEN}{new_attached_shape_vertices}{Style.RESET_ALL}")

            if step_count < steps:
                self.master.after(20, move_to_origin_location, step_count + 1)
            else:
                is_playing_action_animation = False
                opponent_fixed_card_base.update_vertices(opponent_fixed_card_base.get_initial_vertices())
                if tool_card is not None:
                    tool_card.update_vertices(tool_card.get_initial_vertices())
                for attached_shape in attached_shape_list:
                    attached_shape.update_vertices(attached_shape.get_initial_vertices())

                self.is_attack_motion_finished = True
                attack_animation_object.set_is_finished(True)
                attack_animation_object.set_need_post_process(True)

                notify_data = attack_animation_object.get_notify_data()
                # opponent_dead_unit_index_list = notify_data["player_field_unit_death_map"]["Opponent"]["dead_field_unit_index_list"]
                # your_dead_unit_index_list = notify_data["player_field_unit_death_map"]["You"]["dead_field_unit_index_list"]
                # 
                # opponent_unit_health_index_map = notify_data["player_field_unit_health_point_map"]["Opponent"]["field_unit_health_point_map"]
                # your_unit_health_index_map = notify_data["player_field_unit_health_point_map"]["You"]["field_unit_health_point_map"]

                if "Opponent" in notify_data["player_field_unit_death_map"]:
                    opponent_dead_unit_index_list = notify_data["player_field_unit_death_map"]["Opponent"]["dead_field_unit_index_list"]
                    opponent_unit_health_index_map = notify_data["player_field_unit_health_point_map"]["Opponent"]["field_unit_health_point_map"]
                else:
                    # Opponent 키가 없는 경우 처리할 작업 수행
                    opponent_dead_unit_index_list = []
                    opponent_unit_health_index_map = {}

                # You 키가 있는지 확인
                if "You" in notify_data["player_field_unit_death_map"]:
                    your_dead_unit_index_list = notify_data["player_field_unit_death_map"]["You"]["dead_field_unit_index_list"]
                    your_unit_health_index_map = notify_data["player_field_unit_health_point_map"]["You"]["field_unit_health_point_map"]
                else:
                    # You 키가 없는 경우 처리할 작업 수행
                    your_dead_unit_index_list = []
                    your_unit_health_index_map = {}

                for opponent_dead_unit_index in opponent_dead_unit_index_list:
                    # opponent_dead_unit_index = opponent_dead_unit.get_index()
                    self.opponent_field_unit_repository.remove_card_by_multiple_index([int(opponent_dead_unit_index)])
                    self.opponent_field_unit_repository.remove_harmful_status_by_index(int(opponent_dead_unit_index))

                for your_dead_unit_index in your_dead_unit_index_list:
                    # your_dead_unit_index = your_dead_unit.get_index()
                    self.your_field_unit_repository.remove_card_by_index(int(your_dead_unit_index))
                    self.your_field_unit_repository.remove_harmful_status_by_index(int(your_dead_unit_index))

                for index, health in opponent_unit_health_index_map.items():
                    opponent_field_unit = self.opponent_field_unit_repository.find_opponent_field_unit_by_index(int(index))
                    if opponent_field_unit is not None:
                        opponent_field_unit_fixed_card_base = opponent_field_unit.get_fixed_card_base()
                        for attached_shape in opponent_field_unit_fixed_card_base.get_attached_shapes():
                            if isinstance(attached_shape, NonBackgroundNumberImage):
                                if attached_shape.get_circle_kinds() is CircleKinds.HP:
                                    attached_shape.set_image_data(
                                        self.pre_drawed_image_instance.get_pre_draw_unit_hp(health))

                for index, health in your_unit_health_index_map.items():
                    your_field_unit = self.your_field_unit_repository.find_field_unit_by_index(int(index))
                    if your_field_unit is not None:
                        your_field_unit_fixed_card_base = your_field_unit.get_fixed_card_base()
                        for attached_shape in your_field_unit_fixed_card_base.get_attached_shapes():
                            if isinstance(attached_shape, NonBackgroundNumberImage):
                                if attached_shape.get_circle_kinds() is CircleKinds.HP:
                                    attached_shape.set_image_data(
                                        self.pre_drawed_image_instance.get_pre_draw_unit_hp(health))

                self.your_field_unit_repository.replace_field_card_position()
                self.opponent_field_unit_repository.replace_opponent_field_unit_card_position()

                # if self.attack_animation_object.get_your_field_unit_death():
                #     your_field_death_unit_index = self.attack_animation_object.get_your_field_death_unit_index()
                #     self.your_field_unit_repository.remove_card_by_index(your_field_death_unit_index)
                #     self.your_field_unit_repository.replace_field_card_position()
                #     self.your_field_unit_repository.remove_harmful_status_by_index(your_field_death_unit_index)
                # else:
                #
                #     your_field_hp_shape = self.attack_animation_object.get_your_field_hp_shape()
                #     if your_field_hp_shape:
                #         your_hp_number = your_field_hp_shape.get_number()
                #
                #         your_field_hp_shape.set_image_data(
                #             self.pre_drawed_image_instance.get_pre_draw_unit_hp(
                #                 your_hp_number))
                #
                # if self.attack_animation_object.get_opponent_field_unit_death():
                #     opponent_field_unit = self.attack_animation_object.get_opponent_field_unit()
                #     opponent_field_unit_index = opponent_field_unit.get_index()
                #
                #     def remove_field_unit_by_index():
                #         self.opponent_field_unit_repository.remove_card_by_multiple_index([opponent_field_unit_index])
                #         self.opponent_field_unit_repository.replace_opponent_field_unit_card_position()
                #         self.opponent_field_unit_repository.remove_harmful_status_by_index(opponent_field_unit_index)
                #         self.opponent_tomb_repository.create_opponent_tomb_card(opponent_field_unit.get_card_number())
                #
                #     self.create_effect_animation_to_opponent_unit_and_play_animation_and_call_function('death',
                #                                                                                        opponent_field_unit_index,
                #                                                                                        remove_field_unit_by_index)
                # else:
                #     opponent_field_hp_shape = self.attack_animation_object.get_opponent_field_hp_shape()
                #     if opponent_field_hp_shape:
                #         opponent_hp_number = opponent_field_hp_shape.get_number()
                #
                #         opponent_field_hp_shape.set_image_data(
                #             self.pre_drawed_image_instance.get_pre_draw_unit_hp(
                #                 opponent_hp_number))

        move_to_origin_location(1)

    def wide_area_attack_animation(self):
        self.is_playing_action_animation = True
        steps = 10
        attack_animation_object = AttackAnimation.getInstance()
        animation_actor = attack_animation_object.get_animation_actor()

        your_fixed_card_base = animation_actor.get_fixed_card_base()
        current_your_attacker_unit_vertices = your_fixed_card_base.get_vertices()
        current_your_attacker_unit_local_translation = your_fixed_card_base.get_local_translation()

        new_y_value = current_your_attacker_unit_local_translation[1] - 270
        new_x_value = attack_animation_object.get_total_width() / 2 - 52.5
        # your_attacker_unit_destination_local_translation = (current_your_attacker_unit_local_translation[0], new_y_value)
        your_attacker_unit_destination_local_translation = (new_x_value, new_y_value)

        attack_animation_object.set_your_attacker_unit_moving_x(your_attacker_unit_destination_local_translation[0] - current_your_attacker_unit_local_translation[0])

        step_x = (your_attacker_unit_destination_local_translation[0] - current_your_attacker_unit_local_translation[0]) / steps
        step_y = (your_attacker_unit_destination_local_translation[1] - current_your_attacker_unit_local_translation[1]) / steps
        step_y *= -1

        def update_position(step_count):
            print(f"{Fore.RED}step_count: {Fore.GREEN}{step_count}{Style.RESET_ALL}")

            new_vertices = [
                (vx + step_x * step_count, vy + step_y * step_count) for vx, vy in current_your_attacker_unit_vertices
            ]
            your_fixed_card_base.update_vertices(new_vertices)

            # tool_card = self.selected_object.get_tool_card()
            # if tool_card is not None:
            #     new_tool_card_vertices = [
            #         (vx + new_x, vy + new_y) for vx, vy in tool_card.vertices
            #     ]
            #     tool_card.update_vertices(new_tool_card_vertices)

            for attached_shape in your_fixed_card_base.get_attached_shapes():
                # theta = w0 * t + 0.5 * alpha * t^2
                # theta = 0.5 * alpha * t^2 => step_count = 15
                # theta = 0.5 * alpha * 225 = 65 / 225 = 0.28888
                # theta = 0.5 * alpha * 400 = 65 / 400 = 0.1625
                # omega_accel_alpha = -0.1625

                # if isinstance(attached_shape, NonBackgroundNumberImage):
                #     if attached_shape.get_circle_kinds() is CircleKinds.ATTACK:
                #         accel_y_dist = sword_accel_y * step_count
                #         accel_y_dist *= -1
                #
                #         accel_x_dist = sword_accel_x * step_count
                #         # x: 236 / 1920, y: -367 / 1043
                #         new_attached_shape_vertices = [
                #             (vx + accel_x_dist, vy + accel_y_dist) for vx, vy in attached_shape.vertices
                #         ]
                #         attached_shape.update_vertices(new_attached_shape_vertices)
                #         attached_shape.update_rotation_angle(omega_accel_alpha * step_count * step_count)
                #         print(f"{Fore.RED}sword new_attached_shape_vertices{Fore.GREEN} {new_attached_shape_vertices}{Style.RESET_ALL}")
                #
                #         if step_count == 20:
                #             attack_animation_object.set_your_weapon_shape(attached_shape)
                #
                #         continue

                new_attached_shape_vertices = [
                    (vx + step_x, vy + step_y) for vx, vy in attached_shape.vertices
                ]
                attached_shape.update_vertices(new_attached_shape_vertices)
                # print(f"{Fore.RED}new_attached_shape_vertices: {Fore.GREEN}{new_attached_shape_vertices}{Style.RESET_ALL}")

            skill_focus_background_panel_alpha = self.skill_focus_background_panel.color[3]

            # 0.6 = 0.5 * a * 100
            # 0.6 = 50 * a = 0.012
            # 0.65 = 0.013
            # 0.7 -> 0.014
            # 0.75 -> 0.015
            # 0.8 -> 0.016
            skill_focus_background_panel_alpha += 0.013 * step_count
            # print(f"{Fore.RED}0.012 * step_count: {Fore.GREEN}{0.012 * step_count}{Style.RESET_ALL}")
            # print(
            #     f"{Fore.RED}skill_focus_background_panel_alpha: {Fore.GREEN}{skill_focus_background_panel_alpha}{Style.RESET_ALL}")
            self.skill_focus_background_panel.color = (
                self.skill_focus_background_panel.color[0],
                self.skill_focus_background_panel.color[1],
                self.skill_focus_background_panel.color[2],
                skill_focus_background_panel_alpha
            )
            self.skill_focus_background_panel.draw()

            # skill_focus_panel_alpha = self.skill_focus_panel.color[3]
            # skill_focus_panel_alpha -= 0.013 * step_count
            #
            # self.skill_focus_panel.color = (
            #     self.skill_focus_panel.color[0],
            #     self.skill_focus_panel.color[1],
            #     self.skill_focus_panel.color[2],
            #     skill_focus_panel_alpha
            # )
            # self.skill_focus_panel.draw()

            if step_count < steps:
                self.master.after(20, update_position, step_count + 1)
                if step_count == 6:
                    self.__music_player_repository.play_sound_effect_with_event_name('valrn_active_skill_2')
            else:
                self.start_wide_area_motion_animation(attack_animation_object)
                self.is_attack_motion_finished = True
                attack_animation_object.set_is_finished(True)
                attack_animation_object.set_need_post_process(True)

        update_position(1)

    def start_wide_area_motion_animation(self, attack_animation_object):
        steps = 50

        opponent_field_unit_list = self.opponent_field_unit_repository.get_current_field_unit_card_object_list()
        opponent_field_unit_list_length = len(self.opponent_field_unit_repository.get_current_field_unit_card_object_list())

        def wide_area_attack(step_count):

            for index in range(
                    opponent_field_unit_list_length - 1,
                    -1,
                    -1):
                opponent_field_unit = opponent_field_unit_list[index]

                if opponent_field_unit is None:
                    continue

                fixed_card_base = opponent_field_unit.get_fixed_card_base()
                tool_card = opponent_field_unit.get_tool_card()
                attached_shape_list = fixed_card_base.get_attached_shapes()

                if step_count % 2 == 1:
                    vibration_factor = 10
                    random_translation = (random.uniform(-vibration_factor, vibration_factor),
                                          random.uniform(-vibration_factor, vibration_factor))

                    new_fixed_card_base_vertices = [
                        (vx + random_translation[0], vy + random_translation[1]) for vx, vy in
                        fixed_card_base.get_vertices()
                    ]
                    fixed_card_base.update_vertices(new_fixed_card_base_vertices)

                    if tool_card is not None:
                        new_tool_card_vertices = [
                            (vx + random_translation[0], vy + random_translation[1]) for vx, vy in
                            tool_card.get_vertices()
                        ]
                        tool_card.update_vertices(new_tool_card_vertices)

                    for attached_shape in attached_shape_list:
                        # Apply random translation
                        new_attached_shape_vertices = [
                            (vx + random_translation[0], vy + random_translation[1]) for vx, vy in
                            attached_shape.get_vertices()
                        ]
                        attached_shape.update_vertices(new_attached_shape_vertices)

                else:
                    # Return to the original position
                    # fixed_card_base.update_vertices(fixed_card_base.get_vertices())
                    # if tool_card is not None:
                    #     tool_card.update_vertices(tool_card.get_vertices())
                    # for attached_shape in attached_shape_list:
                    #     attached_shape.update_vertices(attached_shape.get_vertices())

                    # self.opponent_field_unit_repository.replace_opponent_field_unit_card_position()

                    fixed_card_base.update_vertices(fixed_card_base.get_initial_vertices())
                    if tool_card is not None:
                        tool_card.update_vertices(tool_card.get_initial_vertices())
                    for attached_shape in attached_shape_list:
                        attached_shape.update_vertices(attached_shape.get_initial_vertices())

            if step_count < steps:
                self.master.after(20, wide_area_attack, step_count + 1)
            else:
                self.finish_wide_area_motion_animation(attack_animation_object)
                # self.is_attack_motion_finished = True
                # attack_animation_object.set_is_finished(True)
                # attack_animation_object.set_need_post_process(True)


        #todo : 망령의 바다 이펙트로 바꿔야함
        # self.create_effect_animation_to_opponent_field_and_play_animation_and_call_function_with_param_full_transparency(
        #     'legacy_sea_of_wraith', wide_area_attack, 1)

        # self.create_effect_animation_to_opponent_field_and_play_animation_and_call_function_with_param(
        #     'legacy_sea_of_wraith', wide_area_attack, 1)
        
        self.create_effect_animation_to_full_screen_and_play_animation_and_call_function_with_param(
            'sea_of_wraith', wide_area_attack, 1)

        # effect_animation = EffectAnimation()
        # effect_animation.set_animation_name('legacy_sea_of_wraith')
        # effect_animation.set_total_window_size(self.width, self.height)
        # field_vertices = self.opponent_field_panel.get_vertices()
        # main_character_vertices = self.opponent_main_character_panel.get_vertices()
        # vertices = [(field_vertices[0][0], main_character_vertices[0][1]),
        #             (field_vertices[2][0], main_character_vertices[1][1]),
        #             field_vertices[3], field_vertices[0]]
        #
        # effect_animation.draw_animation_panel_with_vertices(vertices)
        # effect_animation_panel = effect_animation.get_animation_panel()
        # effect_animation_panel.set_image_data(
        #         self.pre_drawed_image_instance.get_pre_draw_effect_animation('legacy_sea_of_wraith', 23))
        #
        # glEnable(GL_BLEND)
        # glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        #
        # effect_animation_panel.draw()
        #
        # glDisable(GL_BLEND)
        #
        # wide_area_attack(1)

        # animation_index = self.effect_animation_repository.save_effect_animation_at_dictionary_without_index_and_return_index(effect_animation)
        # self.effect_animation_repository.save_effect_animation_panel_at_dictionary_with_index(
        #     animation_index, effect_animation_panel)

        # self.play_effect_animation_by_index_and_call_function_with_param(animation_index, function, param)

        # def animate(animation_index, function, param):
        #     effect_animation = self.effect_animation_repository.get_effect_animation_by_index(animation_index)
        #     effect_animation.update_effect_animation_panel()
        #     if not effect_animation.is_finished:
        #         self.master.after(17, animate)
        #     else:
        #         self.effect_animation_repository.remove_effect_animation_by_index(animation_index)
        #         function(param)
        #         print("finish animation")
        #
        # print(f"animation playing at index : {animation_index}")
        # effect_animation = self.effect_animation_repository.get_effect_animation_by_index(animation_index)
        # print(f"effect_animation : {effect_animation}")
        # effect_animation.reset_animation_count()
        #
        # self.master.after(0, animate, animation_index, wide_area_attack, 1)

        # self.create_effect_animation_to_opponent_field_and_play_animation_and_call_function_with_param(
        #     'sea_of_wraith', wide_area_attack, 1)

        # wide_area_attack(1)

        # effect_animation = EffectAnimation()
        # effect_animation.set_animation_name('legacy_sea_of_wraith')
        # effect_animation.set_total_window_size(self.width, self.height)
        # field_vertices = self.opponent_field_panel.get_vertices()
        # main_character_vertices = self.opponent_main_character_panel.get_vertices()
        # vertices = [(field_vertices[0][0], main_character_vertices[0][1]),
        #             (field_vertices[2][0], main_character_vertices[1][1]),
        #             field_vertices[3], field_vertices[0]]
        # 
        # effect_animation.draw_animation_panel_with_vertices(vertices)
        # effect_animation_panel = effect_animation.get_animation_panel()
        # animation_index = self.effect_animation_repository.save_effect_animation_at_dictionary_without_index_and_return_index(effect_animation)
        # self.effect_animation_repository.save_effect_animation_panel_at_dictionary_with_index(animation_index, effect_animation_panel)
        # 
        # self.play_effect_animation_by_index_and_call_function_with_param(animation_index, wide_area_attack, 1)
        # wide_area_attack(1)

    def finish_wide_area_motion_animation(self, attack_animation_object):
        animation_actor = attack_animation_object.get_animation_actor()
        your_fixed_card_base = animation_actor.get_fixed_card_base()
        tool_card = animation_actor.get_tool_card()
        attached_shape_list = your_fixed_card_base.get_attached_shapes()

        # your_fixed_card_base_initial_vertices = your_fixed_card_base.get_initial_vertices()
        # print(f"{Fore.RED}your_fixed_card_base_initial_vertices{Fore.GREEN} {your_fixed_card_base_initial_vertices}{Style.RESET_ALL}")

        current_your_attacker_unit_vertices = your_fixed_card_base.get_vertices()
        current_your_attacker_unit_local_translation = your_fixed_card_base.get_local_translation()

        your_attacker_unit_moving_x = attack_animation_object.get_your_attacker_unit_moving_x()

        new_y_value = current_your_attacker_unit_local_translation[1] + 270
        your_attacker_unit_destination_local_translation = (0, new_y_value)
        print(f"{Fore.RED}your_attacker_unit_destination_local_translation{Fore.GREEN} {your_attacker_unit_destination_local_translation}{Style.RESET_ALL}")

        steps = 15
        step_x = your_attacker_unit_moving_x / steps
        step_y = (your_attacker_unit_destination_local_translation[1] - current_your_attacker_unit_local_translation[1]) / steps
        # step_y *= -1

        def move_to_origin_location(step_count):
            new_y = current_your_attacker_unit_local_translation[1] + step_y * step_count
            # print(f"{Fore.RED}step ->{Fore.GREEN}new_y: {new_y}{Style.RESET_ALL}")

            new_vertices = [
                (vx  - step_x * step_count, vy - step_y * step_count) for vx, vy in current_your_attacker_unit_vertices
            ]
            your_fixed_card_base.update_vertices(new_vertices)
            # print(f"{Fore.RED}new_vertices{Fore.GREEN} {new_vertices}{Style.RESET_ALL}")

            # tool_card = self.selected_object.get_tool_card()
            # if tool_card is not None:
            #     new_tool_card_vertices = [
            #         (vx + new_x, vy + new_y) for vx, vy in tool_card.vertices
            #     ]
            #     tool_card.update_vertices(new_tool_card_vertices)

            for attached_shape in your_fixed_card_base.get_attached_shapes():
                new_attached_shape_vertices = [
                    (vx - step_x, vy - step_y) for vx, vy in attached_shape.vertices
                ]
                attached_shape.update_vertices(new_attached_shape_vertices)
                # print(f"{Fore.RED}new_attached_shape_vertices: {Fore.GREEN}{new_attached_shape_vertices}{Style.RESET_ALL}")

            skill_focus_background_panel_alpha = self.skill_focus_background_panel.color[3]

            # 0.65 = 112.5 * a = 0.00577
            # 0.7 = 0.5 * a * 225
            # 0.7 = 112.5 * a = 0.0062
            # 0.75 = 112.5 * a = 0.00666
            # 0.8 -> 0.00711
            skill_focus_background_panel_alpha -= 0.00577 * step_count
            # print(f"{Fore.RED}0.012 * step_count: {Fore.GREEN}{0.012 * step_count}{Style.RESET_ALL}")
            # print(
            #     f"{Fore.RED}skill_focus_background_panel_alpha: {Fore.GREEN}{skill_focus_background_panel_alpha}{Style.RESET_ALL}")
            self.skill_focus_background_panel.color = (
                self.skill_focus_background_panel.color[0],
                self.skill_focus_background_panel.color[1],
                self.skill_focus_background_panel.color[2],
                skill_focus_background_panel_alpha
            )
            self.skill_focus_background_panel.draw()

            # skill_focus_panel_alpha = self.skill_focus_panel.color[3]
            # skill_focus_panel_alpha -= 0.00577 * step_count
            #
            # self.skill_focus_panel.color = (
            #     self.skill_focus_panel.color[0],
            #     self.skill_focus_panel.color[1],
            #     self.skill_focus_panel.color[2],
            #     skill_focus_panel_alpha
            # )
            # self.skill_focus_panel.draw()

            if step_count < steps:

                self.master.after(20, move_to_origin_location, step_count + 1)
            else:
                self.skill_focus_background_panel.color = (
                    self.skill_focus_background_panel.color[0],
                    self.skill_focus_background_panel.color[1],
                    self.skill_focus_background_panel.color[2],
                    0
                )
                self.skill_focus_background_panel.draw()

                # self.skill_focus_panel.color = (
                #     self.skill_focus_panel.color[0],
                #     self.skill_focus_panel.color[1],
                #     self.skill_focus_panel.color[2],
                #     0
                # )
                # self.skill_focus_panel.draw()

                self.is_playing_action_animation = False
                opponent_field_unit_list = self.opponent_field_unit_repository.get_current_field_unit_card_object_list()
                opponent_field_unit_list_length = len(
                    self.opponent_field_unit_repository.get_current_field_unit_card_object_list())

                your_actor_damage = attack_animation_object.get_animation_actor_damage()
                your_actor_extra_ability = attack_animation_object.get_extra_ability()

                for index in range(
                        opponent_field_unit_list_length - 1,
                        -1,
                        -1):
                    opponent_field_unit = opponent_field_unit_list[index]

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
                                hp_number -= your_actor_damage

                                # opponent_field_hp_list = attack_animation_object.get_wide_attack_opponent_field_hp_list()
                                # hp_number = opponent_field_hp_list[index]
                                print(f"{Fore.RED}hp_number: {Fore.GREEN}{hp_number}{Style.RESET_ALL}")

                                # TODO: n 턴간 불사 특성을 검사해야하므로 사실 이것도 summary 방식으로 빼는 것이 맞으나 우선은 진행한다.
                                if hp_number <= 0:
                                    remove_from_field = True
                                    break

                                # print(f"hp_number: {hp_number}")
                                attached_shape.set_number(hp_number)

                                # attached_shape.set_image_data(
                                #     # TODO: 실제로 여기서 서버로부터 계산 받은 값을 적용해야함
                                #     self.pre_drawed_image_instance.get_pre_draw_number_image(hp_number))

                                attached_shape.set_image_data(
                                    self.pre_drawed_image_instance.get_pre_draw_unit_hp(hp_number))

                                if your_actor_extra_ability:
                                    self.opponent_field_unit_repository.apply_harmful_status(opponent_field_unit.get_index(), your_actor_extra_ability)

                    if remove_from_field:
                        card_id = opponent_field_unit.get_card_number()

                        effect_animation = EffectAnimation()
                        effect_animation.set_animation_name('death')
                        effect_animation.set_total_window_size(self.width, self.height)
                        effect_animation.change_local_translation(self.opponent_field_unit_repository.find_opponent_field_unit_by_index(
                            index).get_fixed_card_base().get_local_translation())
                        effect_animation.draw_animation_panel()
                        effect_animation_panel = effect_animation.get_animation_panel()

                        animation_index = self.effect_animation_repository.save_effect_animation_at_dictionary_without_index_and_return_index(
                            effect_animation)

                        self.effect_animation_repository.save_effect_animation_panel_at_dictionary_with_index(
                            animation_index, effect_animation_panel)

                        def remove_opponent_unit(unit_index):
                            unit_card_id = self.opponent_field_unit_repository.get_opponent_card_id_by_index(unit_index)
                            self.opponent_field_unit_repository.remove_current_field_unit_card(unit_index)
                            self.opponent_tomb_repository.create_opponent_tomb_card(unit_card_id)
                            self.opponent_field_unit_repository.replace_opponent_field_unit_card_position()
                            self.opponent_field_unit_repository.remove_harmful_status_by_index(unit_index)

                        self.play_effect_animation_by_index_and_call_function_with_param(animation_index, remove_opponent_unit, index)

                self.field_area_inside_handler.clear_field_area_action()

                pass

        move_to_origin_location(1)

    def opponent_valrn_sea_of_wraith_to_your_field_animation(self):
        self.is_playing_action_animation = True
        steps = 10
        attack_animation_object = AttackAnimation.getInstance()
        opponent_animation_actor = attack_animation_object.get_opponent_animation_actor()

        opponent_fixed_card_base = opponent_animation_actor.get_fixed_card_base()
        current_opponent_attacker_unit_vertices = opponent_fixed_card_base.get_vertices()
        current_opponent_attacker_unit_local_translation = opponent_fixed_card_base.get_local_translation()

        new_y_value = current_opponent_attacker_unit_local_translation[1] + 240
        new_x_value = attack_animation_object.get_total_width() / 2 - 52.5
        # your_attacker_unit_destination_local_translation = (current_your_attacker_unit_local_translation[0], new_y_value)
        opponent_attacker_unit_destination_local_translation = (new_x_value, new_y_value)

        attack_animation_object.set_opponent_attacker_unit_moving_x(opponent_attacker_unit_destination_local_translation[0] - current_opponent_attacker_unit_local_translation[0])

        step_x = (opponent_attacker_unit_destination_local_translation[0] - current_opponent_attacker_unit_local_translation[0]) / steps
        step_y = (opponent_attacker_unit_destination_local_translation[1] - current_opponent_attacker_unit_local_translation[1]) / steps
        step_y *= -1

        def update_position(step_count):
            print(f"{Fore.RED}step_count: {Fore.GREEN}{step_count}{Style.RESET_ALL}")

            new_vertices = [
                (vx + step_x * step_count, vy + step_y * step_count) for vx, vy in current_opponent_attacker_unit_vertices
            ]
            opponent_fixed_card_base.update_vertices(new_vertices)

            # tool_card = self.selected_object.get_tool_card()
            # if tool_card is not None:
            #     new_tool_card_vertices = [
            #         (vx + new_x, vy + new_y) for vx, vy in tool_card.vertices
            #     ]
            #     tool_card.update_vertices(new_tool_card_vertices)

            for attached_shape in opponent_fixed_card_base.get_attached_shapes():
                # theta = w0 * t + 0.5 * alpha * t^2
                # theta = 0.5 * alpha * t^2 => step_count = 15
                # theta = 0.5 * alpha * 225 = 65 / 225 = 0.28888
                # theta = 0.5 * alpha * 400 = 65 / 400 = 0.1625
                # omega_accel_alpha = -0.1625

                # if isinstance(attached_shape, NonBackgroundNumberImage):
                #     if attached_shape.get_circle_kinds() is CircleKinds.ATTACK:
                #         accel_y_dist = sword_accel_y * step_count
                #         accel_y_dist *= -1
                #
                #         accel_x_dist = sword_accel_x * step_count
                #         # x: 236 / 1920, y: -367 / 1043
                #         new_attached_shape_vertices = [
                #             (vx + accel_x_dist, vy + accel_y_dist) for vx, vy in attached_shape.vertices
                #         ]
                #         attached_shape.update_vertices(new_attached_shape_vertices)
                #         attached_shape.update_rotation_angle(omega_accel_alpha * step_count * step_count)
                #         print(f"{Fore.RED}sword new_attached_shape_vertices{Fore.GREEN} {new_attached_shape_vertices}{Style.RESET_ALL}")
                #
                #         if step_count == 20:
                #             attack_animation_object.set_your_weapon_shape(attached_shape)
                #
                #         continue

                new_attached_shape_vertices = [
                    (vx + step_x, vy + step_y) for vx, vy in attached_shape.vertices
                ]
                attached_shape.update_vertices(new_attached_shape_vertices)
                # print(f"{Fore.RED}new_attached_shape_vertices: {Fore.GREEN}{new_attached_shape_vertices}{Style.RESET_ALL}")

            skill_focus_background_panel_alpha = self.skill_focus_background_panel.color[3]
            skill_focus_background_panel_alpha += 0.013 * step_count

            self.skill_focus_background_panel.color = (
                self.skill_focus_background_panel.color[0],
                self.skill_focus_background_panel.color[1],
                self.skill_focus_background_panel.color[2],
                skill_focus_background_panel_alpha
            )
            self.skill_focus_background_panel.draw()

            if step_count < steps:
                self.master.after(20, update_position, step_count + 1)
                if step_count == 6:
                    self.__music_player_repository.play_sound_effect_with_event_name('valrn_active_skill_2')
            else:
                self.start_opponent_valrn_sea_of_wraith_motion_animation(attack_animation_object)

        update_position(1)

    def start_opponent_valrn_sea_of_wraith_motion_animation(self, attack_animation_object):

        # todo : 망바 이름으로 바꿔야함
        effect_animation = EffectAnimation()
        effect_animation.set_animation_name('sea_of_wraith')
        effect_animation.set_total_window_size(self.width, self.height)
        field_vertices = self.your_field_panel.get_vertices()
        main_character_vertices = self.your_main_character_panel.get_vertices()
        vertices = [field_vertices[1], field_vertices[2],
                    (field_vertices[3][0], main_character_vertices[2][1]),
                    (field_vertices[0][0], main_character_vertices[3][1])]

        effect_animation.draw_animation_panel_with_vertices(vertices)
        effect_animation_panel = effect_animation.get_animation_panel()
        animation_index = self.effect_animation_repository.save_effect_animation_at_dictionary_without_index_and_return_index(
            effect_animation)
        self.effect_animation_repository.save_effect_animation_panel_at_dictionary_with_index(
            animation_index, effect_animation_panel)


        def wide_area_attack(step_count):

            steps = 50
            your_field_unit_list = self.your_field_unit_repository.get_current_field_unit_list()
            your_field_unit_list_length = len(self.your_field_unit_repository.get_current_field_unit_list())

            for index in range(
                    your_field_unit_list_length - 1,
                    -1,
                    -1):
                your_field_unit = your_field_unit_list[index]

                if your_field_unit is None:
                    continue

                fixed_card_base = your_field_unit.get_fixed_card_base()
                tool_card = your_field_unit.get_tool_card()
                attached_shape_list = fixed_card_base.get_attached_shapes()

                if step_count % 2 == 1:
                    vibration_factor = 10
                    random_translation = (random.uniform(-vibration_factor, vibration_factor),
                                          random.uniform(-vibration_factor, vibration_factor))

                    new_fixed_card_base_vertices = [
                        (vx + random_translation[0], vy + random_translation[1]) for vx, vy in
                        fixed_card_base.get_vertices()
                    ]
                    fixed_card_base.update_vertices(new_fixed_card_base_vertices)

                    if tool_card is not None:
                        new_tool_card_vertices = [
                            (vx + random_translation[0], vy + random_translation[1]) for vx, vy in
                            tool_card.get_vertices()
                        ]
                        tool_card.update_vertices(new_tool_card_vertices)

                    for attached_shape in attached_shape_list:
                        # Apply random translation
                        new_attached_shape_vertices = [
                            (vx + random_translation[0], vy + random_translation[1]) for vx, vy in
                            attached_shape.get_vertices()
                        ]
                        attached_shape.update_vertices(new_attached_shape_vertices)

                else:
                    # Return to the original position
                    # fixed_card_base.update_vertices(fixed_card_base.get_vertices())
                    # if tool_card is not None:
                    #     tool_card.update_vertices(tool_card.get_vertices())
                    # for attached_shape in attached_shape_list:
                    #     attached_shape.update_vertices(attached_shape.get_vertices())

                    # self.opponent_field_unit_repository.replace_opponent_field_unit_card_position()

                    fixed_card_base.update_vertices(fixed_card_base.get_initial_vertices())
                    if tool_card is not None:
                        tool_card.update_vertices(tool_card.get_initial_vertices())
                    for attached_shape in attached_shape_list:
                        attached_shape.update_vertices(attached_shape.get_initial_vertices())

            if step_count < steps:
                self.master.after(20, wide_area_attack, step_count + 1)
            else:
                self.finish_opponent_valrn_sea_of_wraith_motion_animation(attack_animation_object)
                # self.is_attack_motion_finished = True
                # attack_animation_object.set_is_finished(True)
                # attack_animation_object.set_need_post_process(True)

        # self.play_effect_animation_by_index_and_call_function_with_param(animation_index, wide_area_attack, 1)

        self.create_effect_animation_to_full_screen_and_play_animation_and_call_function_with_param(
            'sea_of_wraith', wide_area_attack, 1)

    def finish_opponent_valrn_sea_of_wraith_motion_animation(self, attack_animation_object):
        opponent_animation_actor = attack_animation_object.get_opponent_animation_actor()
        opponent_fixed_card_base = opponent_animation_actor.get_fixed_card_base()
        tool_card = opponent_animation_actor.get_tool_card()
        attached_shape_list = opponent_fixed_card_base.get_attached_shapes()

        # your_fixed_card_base_initial_vertices = your_fixed_card_base.get_initial_vertices()
        # print(f"{Fore.RED}your_fixed_card_base_initial_vertices{Fore.GREEN} {your_fixed_card_base_initial_vertices}{Style.RESET_ALL}")

        current_opponent_attacker_unit_vertices = opponent_fixed_card_base.get_vertices()
        current_opponent_attacker_unit_local_translation = opponent_fixed_card_base.get_local_translation()

        opponent_attacker_unit_moving_x = attack_animation_object.get_opponent_attacker_unit_moving_x()

        new_y_value = current_opponent_attacker_unit_local_translation[1] - 240
        opponent_attacker_unit_destination_local_translation = (0, new_y_value)
        print(f"{Fore.RED}opponent_attacker_unit_destination_local_translation{Fore.GREEN} {opponent_attacker_unit_destination_local_translation}{Style.RESET_ALL}")

        steps = 15
        step_x = opponent_attacker_unit_moving_x / steps
        step_y = (opponent_attacker_unit_destination_local_translation[1] - current_opponent_attacker_unit_local_translation[1]) / steps
        # step_y *= -1

        def move_to_origin_location(step_count):
            new_y = current_opponent_attacker_unit_local_translation[1] + step_y * step_count
            print(f"{Fore.RED}step ->{Fore.GREEN}new_y: {new_y}{Style.RESET_ALL}")

            new_vertices = [
                (vx  - step_x * step_count, vy - step_y * step_count) for vx, vy in current_opponent_attacker_unit_vertices
            ]
            opponent_fixed_card_base.update_vertices(new_vertices)
            print(f"{Fore.RED}new_vertices{Fore.GREEN} {new_vertices}{Style.RESET_ALL}")

            # tool_card = self.selected_object.get_tool_card()
            # if tool_card is not None:
            #     new_tool_card_vertices = [
            #         (vx + new_x, vy + new_y) for vx, vy in tool_card.vertices
            #     ]
            #     tool_card.update_vertices(new_tool_card_vertices)

            for attached_shape in opponent_fixed_card_base.get_attached_shapes():
                new_attached_shape_vertices = [
                    (vx - step_x, vy - step_y) for vx, vy in attached_shape.vertices
                ]
                attached_shape.update_vertices(new_attached_shape_vertices)
                # print(f"{Fore.RED}new_attached_shape_vertices: {Fore.GREEN}{new_attached_shape_vertices}{Style.RESET_ALL}")

            skill_focus_background_panel_alpha = self.skill_focus_background_panel.color[3]
            skill_focus_background_panel_alpha -= 0.00577 * step_count

            self.skill_focus_background_panel.color = (
                self.skill_focus_background_panel.color[0],
                self.skill_focus_background_panel.color[1],
                self.skill_focus_background_panel.color[2],
                skill_focus_background_panel_alpha
            )
            self.skill_focus_background_panel.draw()

            if step_count < steps:

                self.master.after(20, move_to_origin_location, step_count + 1)
            else:
                self.is_playing_action_animation = False
                your_field_unit_list = self.your_field_unit_repository.get_current_field_unit_list()
                your_field_unit_list_length = len(self.your_field_unit_repository.get_current_field_unit_list())

                # your_actor_damage = attack_animation_object.get_animation_actor_damage()
                # your_actor_extra_ability = attack_animation_object.get_extra_ability()
                #
                # for index in range(
                #         opponent_field_unit_list_length - 1,
                #         -1,
                #         -1):
                #     opponent_field_unit = opponent_field_unit_list[index]
                #
                #     if opponent_field_unit is None:
                #         continue
                #
                #     remove_from_field = False
                #
                #     fixed_card_base = opponent_field_unit.get_fixed_card_base()
                #     attached_shape_list = fixed_card_base.get_attached_shapes()
                #
                #
                #
                #     # TODO: 가만 보면 이 부분이 은근히 많이 사용되고 있음 (중복 많이 발생함)
                #     for attached_shape in attached_shape_list:
                #         if isinstance(attached_shape, NonBackgroundNumberImage):
                #             if attached_shape.get_circle_kinds() is CircleKinds.HP:
                #                 hp_number = attached_shape.get_number()
                #                 hp_number -= your_actor_damage
                #
                #                 # opponent_field_hp_list = attack_animation_object.get_wide_attack_opponent_field_hp_list()
                #                 # hp_number = opponent_field_hp_list[index]
                #                 print(f"{Fore.RED}hp_number: {Fore.GREEN}{hp_number}{Style.RESET_ALL}")
                #
                #                 # TODO: n 턴간 불사 특성을 검사해야하므로 사실 이것도 summary 방식으로 빼는 것이 맞으나 우선은 진행한다.
                #                 if hp_number <= 0:
                #                     remove_from_field = True
                #                     break
                #
                #                 # print(f"hp_number: {hp_number}")
                #                 attached_shape.set_number(hp_number)
                #
                #                 # attached_shape.set_image_data(
                #                 #     # TODO: 실제로 여기서 서버로부터 계산 받은 값을 적용해야함
                #                 #     self.pre_drawed_image_instance.get_pre_draw_number_image(hp_number))
                #
                #                 attached_shape.set_image_data(
                #                     self.pre_drawed_image_instance.get_pre_draw_unit_hp(hp_number))
                #
                #                 if your_actor_extra_ability:
                #                     self.opponent_field_unit_repository.apply_harmful_status(opponent_field_unit.get_index(), your_actor_extra_ability)
                #
                #     if remove_from_field:
                #         card_id = opponent_field_unit.get_card_number()
                #
                #         effect_animation = EffectAnimation()
                #         effect_animation.set_animation_name('death')
                #         effect_animation.set_total_window_size(self.width, self.height)
                #         effect_animation.change_local_translation(self.opponent_field_unit_repository.find_opponent_field_unit_by_index(
                #             index).get_fixed_card_base().get_local_translation())
                #         effect_animation.draw_animation_panel()
                #         effect_animation_panel = effect_animation.get_animation_panel()
                #
                #         animation_index = self.effect_animation_repository.save_effect_animation_at_dictionary_without_index_and_return_index(
                #             effect_animation)
                #
                #         self.effect_animation_repository.save_effect_animation_panel_at_dictionary_with_index(
                #             animation_index, effect_animation_panel)
                #
                #         def remove_opponent_unit():
                #             self.opponent_field_unit_repository.remove_current_field_unit_card(index)
                #             self.opponent_tomb_repository.create_opponent_tomb_card(card_id)
                #             self.opponent_field_unit_repository.replace_opponent_field_unit_card_position()
                #             self.opponent_field_unit_repository.remove_harmful_status_by_index(index)
                #
                #         self.play_effect_animation_by_index_and_call_function(animation_index, remove_opponent_unit)

                notify_data = self.attack_animation_object.get_notify_data()
                player_field_unit_harmful_effect_data = notify_data['player_field_unit_harmful_effect_map']
                field_unit_health_point_map = notify_data['player_field_unit_health_point_map']['You']['field_unit_health_point_map']
                dead_field_unit_index_list = notify_data['player_field_unit_death_map']['You']['dead_field_unit_index_list']

                for player, field_data in player_field_unit_harmful_effect_data.items():
                    for unit_index, harmful_status_value in field_data.get('field_unit_harmful_status_map', {}).items():
                        harmful_status_list = harmful_status_value.get('harmful_status_list', [])
                        if len(harmful_status_list) == 0:
                            continue

                        if player == 'Opponent':
                            self.opponent_field_unit_repository.apply_harmful_status(int(unit_index), harmful_status_list)
                        elif player == 'You':
                            self.your_field_unit_repository.apply_harmful_status(int(unit_index), harmful_status_list)

                for unit_index, remain_hp in field_unit_health_point_map.items():
                    if remain_hp <= 0:
                        continue

                    your_field_unit = self.your_field_unit_repository.find_field_unit_by_index(int(unit_index))
                    your_fixed_card_base = your_field_unit.get_fixed_card_base()
                    your_fixed_card_attached_shape_list = your_fixed_card_base.get_attached_shapes()

                    for your_fixed_card_attached_shape in your_fixed_card_attached_shape_list:
                        if isinstance(your_fixed_card_attached_shape, NonBackgroundNumberImage):
                            if your_fixed_card_attached_shape.get_circle_kinds() is CircleKinds.HP:
                                your_fixed_card_attached_shape.set_number(remain_hp)

                                your_fixed_card_attached_shape.set_image_data(
                                    self.pre_drawed_image_instance.get_pre_draw_unit_hp(remain_hp))

                for dead_unit_index in dead_field_unit_index_list:

                    def remove_field_unit(index):
                        field_unit_id = self.your_field_unit_repository.get_card_id_by_index(index)
                        self.your_tomb_repository.create_tomb_card(field_unit_id)
                        self.your_field_unit_repository.remove_card_by_index(index)
                        self.your_field_unit_repository.remove_harmful_status_by_index(index)
                        self.your_field_unit_repository.replace_field_card_position()

                    effect_animation = EffectAnimation()
                    effect_animation.set_animation_name('death')
                    effect_animation.set_total_window_size(self.width, self.height)
                    effect_animation.change_local_translation(
                        self.your_field_unit_repository.find_field_unit_by_index(
                            dead_unit_index).get_fixed_card_base().get_local_translation())
                    effect_animation.draw_animation_panel()
                    effect_animation_panel = effect_animation.get_animation_panel()

                    animation_index = self.effect_animation_repository.save_effect_animation_at_dictionary_without_index_and_return_index(
                        effect_animation)

                    self.effect_animation_repository.save_effect_animation_panel_at_dictionary_with_index(
                        animation_index, effect_animation_panel)

                    self.play_effect_animation_by_index_and_call_function_with_param(animation_index, remove_field_unit, dead_unit_index)


                self.opponent_field_area_inside_handler.set_active_field_area_action(OpponentFieldAreaActionProcess.Dummy)
                self.attack_animation_object.set_opponent_animation_actor(None)



                pass

        move_to_origin_location(1)

    def ready_to_use_contract_of_doom_attack_animation(self):
        effect_animation = EffectAnimation()
        effect_animation.set_animation_name('contract_of_doom')
        effect_animation.set_total_window_size(self.width, self.height)
        field_vertices = self.your_field_panel.get_vertices()
        main_character_vertices = self.your_main_character_panel.get_vertices()
        vertices = [field_vertices[1], field_vertices[2],
                    (field_vertices[3][0], main_character_vertices[2][1]),
                    (field_vertices[0][0], main_character_vertices[3][1])]
        effect_animation.draw_animation_panel_with_vertices(vertices)
        effect_animation_panel = effect_animation.get_animation_panel()

        animation_index = self.effect_animation_repository.save_effect_animation_at_dictionary_without_index_and_return_index(
            effect_animation)
        self.effect_animation_repository.save_effect_animation_panel_at_dictionary_with_index(
            animation_index, effect_animation_panel)

        self.play_effect_animation_by_index_and_call_function(animation_index, self.your_contract_of_doom_attack_animation)

    def your_contract_of_doom_attack_animation(self):
        self.is_playing_action_animation = True
        steps = 50

        attack_animation_object = AttackAnimation.getInstance()

        your_field_unit_list = self.your_field_unit_repository.get_current_field_unit_list()
        your_field_unit_list_length = len(
            self.your_field_unit_repository.get_current_field_unit_list())

        def wide_area_attack(step_count):
            vibration_factor = 10

            random_background_translation = (random.uniform(-vibration_factor, vibration_factor),
                                             random.uniform(-vibration_factor, vibration_factor))

            if step_count % 2 == 1:
                for battle_field_background_shape in self.battle_field_background_shape_list:
                    battle_field_background_shape.global_translate(
                        (random_background_translation[0], random_background_translation[1]))
            else:
                for battle_field_background_shape in self.battle_field_background_shape_list:
                    battle_field_background_shape.global_translate((0, 0))

            your_field_unit_list = self.your_field_unit_repository.get_current_field_unit_list()
            your_field_unit_list_length = len(
                self.your_field_unit_repository.get_current_field_unit_list())

            for index in range(
                    your_field_unit_list_length - 1,
                    -1,
                    -1):

                your_field_unit = your_field_unit_list[index]
                if your_field_unit is None:
                    continue

                fixed_card_base = your_field_unit.get_fixed_card_base()
                tool_card = your_field_unit.get_tool_card()
                attached_shape_list = fixed_card_base.get_attached_shapes()

                if step_count % 2 == 1:
                    random_translation = (random.uniform(-vibration_factor, vibration_factor),
                                          random.uniform(-vibration_factor, vibration_factor))

                    new_fixed_card_base_vertices = [
                        (vx + random_translation[0], vy + random_translation[1]) for vx, vy in
                        fixed_card_base.get_vertices()
                    ]
                    fixed_card_base.update_vertices(new_fixed_card_base_vertices)

                    if tool_card is not None:
                        new_tool_card_vertices = [
                            (vx + random_translation[0], vy + random_translation[1]) for vx, vy in
                            tool_card.get_vertices()
                        ]
                        tool_card.update_vertices(new_tool_card_vertices)

                    for attached_shape in attached_shape_list:
                        # Apply random translation
                        new_attached_shape_vertices = [
                            (vx + random_translation[0], vy + random_translation[1]) for vx, vy in
                            attached_shape.get_vertices()
                        ]
                        attached_shape.update_vertices(new_attached_shape_vertices)
                else:
                    fixed_card_base.update_vertices(fixed_card_base.get_initial_vertices())
                    if tool_card is not None:
                        tool_card.update_vertices(tool_card.get_initial_vertices())
                    for attached_shape in attached_shape_list:
                        attached_shape.update_vertices(attached_shape.get_initial_vertices())

            if step_count < steps:
                self.master.after(20, wide_area_attack, step_count + 1)
            else:
                contract_of_doom_damage = attack_animation_object.get_animation_actor_damage()

                # # 체력 정보 Update
                # # for your_field_unit_index in attack_animation_object.get_your_field_unit_index_list():
                # your_field_unit_health_point_map = attack_animation_object.get_your_field_unit_health_point_map()
                # for unit_index, remaining_health_point in your_field_unit_health_point_map.items():
                #     your_field_unit = self.your_field_unit_repository.find_field_unit_by_index(int(unit_index))
                #     your_fixed_card_base = your_field_unit.get_fixed_card_base()
                #     your_fixed_card_attached_shape_list = your_fixed_card_base.get_attached_shapes()
                #
                #     if remaining_health_point <= 0:
                #         continue
                #
                #     for your_fixed_card_attached_shape in your_fixed_card_attached_shape_list:
                #         if isinstance(your_fixed_card_attached_shape, NonBackgroundNumberImage):
                #             if your_fixed_card_attached_shape.get_circle_kinds() is CircleKinds.HP:
                #                 # your_fixed_card_attached_shape.set_number(int(remaining_health_point))
                #                 remaining_hp_number = your_fixed_card_attached_shape.get_number()
                #                 print(f"{Fore.RED}remaining_hp_number: {Fore.GREEN}{remaining_hp_number}{Style.RESET_ALL}")
                #
                #                 your_fixed_card_attached_shape.set_image_data(
                #                     self.pre_drawed_image_instance.get_pre_draw_unit_hp(
                #                         remaining_hp_number))
                #
                # # 죽은 유닛들 묘지에 배치 및 Replacing
                # for dead_unit_index in attack_animation_object.get_your_dead_field_unit_index_list():
                #     # self.__attack_animation_object.add_your_dead_field_unit_index_list(int(dead_unit_index))
                #
                #     effect_animation = EffectAnimation()
                #     effect_animation.set_animation_name('death')
                #     effect_animation.set_total_window_size(self.width, self.height)
                #     effect_animation.change_local_translation(
                #         self.your_field_unit_repository.find_field_unit_by_index(
                #             dead_unit_index).get_fixed_card_base().get_local_translation())
                #     effect_animation.draw_animation_panel()
                #     effect_animation_panel = effect_animation.get_animation_panel()
                #
                #     animation_index = self.effect_animation_repository.save_effect_animation_at_dictionary_without_index_and_return_index(
                #         effect_animation)
                #
                #     self.effect_animation_repository.save_effect_animation_panel_at_dictionary_with_index(
                #         animation_index, effect_animation_panel)
                #
                #     def remove_field_unit(dead_unit_index):
                #         print(dead_unit_index)
                #         dead_unit_card_id = self.your_field_unit_repository.find_field_unit_by_index(
                #             dead_unit_index).get_card_number()
                #         self.your_field_unit_repository.remove_card_by_index(dead_unit_index)
                #         self.your_tomb_repository.create_tomb_card(dead_unit_card_id)
                #         self.your_field_unit_repository.replace_field_card_position()
                #         self.your_field_unit_repository.remove_harmful_status_by_index(dead_unit_index)
                #
                #     self.play_effect_animation_by_index_and_call_function_with_param(animation_index,
                #                                                                      remove_field_unit, dead_unit_index)
                #
                # # 메인 캐릭터 상태 확인 및 체력 Update
                # # if your_main_character_survival_state != 'Survival':
                # #     print("Player who get notice is dead.")
                # #     # TODO: 배틀 정리 요청을 띄우는 화면으로 넘어가야 함
                #
                # your_main_character_health_point = self.attack_animation_object.get_your_main_character_health_point()
                #
                # self.your_hp_repository.change_hp(your_main_character_health_point)
                # print(f"{Fore.RED}current_main_character_health:{Fore.GREEN} "
                #       f"{self.your_hp_repository.get_current_your_hp_state().get_current_health()}{Style.RESET_ALL}")
                #
                # # 덱 위에서 카드 한 장 뽑아서 로스트 존 보내기
                # for lost_card_id in attack_animation_object.get_your_lost_card_id_list():
                #     # attack_animation_object.add_your_lost_card_id_list(lost_card_id)
                #     self.your_deck_repository.draw_deck()
                #     print(f"{Fore.RED}current_deck: {Fore.GREEN}"
                #           f"{self.your_deck_repository.get_current_deck_state()}{Style.RESET_ALL}")
                #     self.your_lost_zone_repository.create_your_lost_zone_card(lost_card_id)
                #     print(f"{Fore.RED}current_lost_zone: {Fore.GREEN}"
                #           f"{self.your_lost_zone_repository.get_your_lost_zone_state()}{Style.RESET_ALL}")

                notify_data = self.attack_animation_object.get_notify_data()

                opponent_usage_card_info = (notify_data)['player_hand_use_map']['Opponent']
                your_field_unit_health_point_map = (notify_data)['player_field_unit_health_point_map']['You']['field_unit_health_point_map']
                your_dead_field_unit_index_list = (notify_data)['player_field_unit_death_map']['You']['dead_field_unit_index_list']
                your_main_character_health_point = (notify_data)['player_main_character_health_point_map']['You']
                your_main_character_survival_state = (notify_data)['player_main_character_survival_map']['You']
                your_deck_card_lost_list = (notify_data)['player_deck_card_lost_list_map']['You']

                # 사용된 카드 묘지로 보냄
                used_card_id = opponent_usage_card_info['card_id']
                self.opponent_tomb_repository.create_opponent_tomb_card(used_card_id)

                for unit_index, remaining_health_point in your_field_unit_health_point_map.items():
                    your_field_unit = self.your_field_unit_repository.find_field_unit_by_index(int(unit_index))
                    your_fixed_card_base = your_field_unit.get_fixed_card_base()
                    your_fixed_card_attached_shape_list = your_fixed_card_base.get_attached_shapes()

                    if remaining_health_point <= 0:
                        continue

                    for your_fixed_card_attached_shape in your_fixed_card_attached_shape_list:
                        if isinstance(your_fixed_card_attached_shape, NonBackgroundNumberImage):
                            if your_fixed_card_attached_shape.get_circle_kinds() is CircleKinds.HP:
                                your_fixed_card_attached_shape.set_number(int(remaining_health_point))
                                print(f"{Fore.RED}your_fixed_card -> int(remaining_health_point): {Fore.GREEN}{int(remaining_health_point)}{Style.RESET_ALL}")

                                your_fixed_card_attached_shape.set_image_data(
                                    self.pre_drawed_image_instance.get_pre_draw_unit_hp(int(remaining_health_point)))

                # 죽은 유닛들 묘지에 배치 및 Replacing

                for dead_unit_index in your_dead_field_unit_index_list:
                    # self.__attack_animation_object.add_your_dead_field_unit_index_list(int(dead_unit_index))

                    # effect_animation = EffectAnimation()
                    # effect_animation.set_animation_name('death')
                    # effect_animation.set_total_window_size(self.width, self.height)
                    # effect_animation.change_local_translation(
                    #     self.your_field_unit_repository.find_field_unit_by_index(
                    #         dead_unit_index).get_fixed_card_base().get_local_translation())
                    # effect_animation.draw_animation_panel()
                    # effect_animation_panel = effect_animation.get_animation_panel()
                    #
                    # animation_index = self.effect_animation_repository.save_effect_animation_at_dictionary_without_index_and_return_index(
                    #     effect_animation)
                    #
                    # self.effect_animation_repository.save_effect_animation_panel_at_dictionary_with_index(
                    #     animation_index, effect_animation_panel)

                    def remove_field_unit(unit_index):
                        dead_unit_card_id = self.your_field_unit_repository.find_field_unit_by_index(
                            unit_index).get_card_number()
                        self.your_field_unit_repository.remove_card_by_index(unit_index)
                        self.your_tomb_repository.create_tomb_card(dead_unit_card_id)
                        self.your_field_unit_repository.replace_field_card_position()
                        self.your_field_unit_repository.remove_harmful_status_by_index(unit_index)

                    self.create_effect_animation_to_your_unit_and_play_animation_and_call_function_with_param(
                        'death', dead_unit_index, remove_field_unit, dead_unit_index
                    )
                self.your_field_unit_repository.replace_field_card_position()

                # 메인 캐릭터 상태 확인 및 체력 Update
                if your_main_character_survival_state != 'Survival':
                    print("Player who get notice is dead.")
                    self.timer.stop_timer()
                    self.your_hp_repository.your_character_die()
                    # TODO: 배틀 정리 요청을 띄우는 화면으로 넘어가야 함

                self.your_hp_repository.change_hp(your_main_character_health_point)
                print(f"{Fore.RED}current_main_character_health:{Fore.GREEN} "
                      f"{self.your_hp_repository.get_current_your_hp_state().get_current_health()}{Style.RESET_ALL}")

                # 덱 위에서 카드 한 장 뽑아서 로스트 존 보내기
                for lost_card_id in your_deck_card_lost_list:
                    self.your_deck_repository.draw_deck()
                    print(f"{Fore.RED}current_deck: {Fore.GREEN}"
                          f"{self.your_deck_repository.get_current_deck_state()}{Style.RESET_ALL}")
                    self.your_lost_zone_repository.create_your_lost_zone_card(int(lost_card_id))
                    print(f"{Fore.RED}current_lost_zone: {Fore.GREEN}"
                          f"{self.your_lost_zone_repository.get_your_lost_zone_state()}{Style.RESET_ALL}")

                self.is_attack_motion_finished = True
                self.field_area_inside_handler.clear_field_area_action()
                self.opponent_field_area_inside_handler.clear_field_area_action()

                # attack_animation_object.set_is_finished(True)
                # attack_animation_object.set_need_post_process(True)

        wide_area_attack(1)

    def opponent_contract_of_doom_attack_animation(self):
        self.is_playing_action_animation = True
        steps = 50
        damage = 15

        attack_animation_object = AttackAnimation.getInstance()

        opponent_field_unit_list = self.opponent_field_unit_repository.get_current_field_unit_card_object_list()
        opponent_field_unit_list_length = len(
            self.opponent_field_unit_repository.get_current_field_unit_card_object_list())


        
        def opponent_wide_area_attack(step_count):
            vibration_factor = 10

            random_background_translation = (random.uniform(-vibration_factor, vibration_factor),
                                             random.uniform(-vibration_factor, vibration_factor))

            if step_count % 2 == 1:
                for battle_field_background_shape in self.battle_field_background_shape_list:
                    battle_field_background_shape.global_translate(
                        (random_background_translation[0], random_background_translation[1]))
            else:
                for battle_field_background_shape in self.battle_field_background_shape_list:
                    battle_field_background_shape.global_translate((0, 0))

            for index in range(
                    opponent_field_unit_list_length - 1,
                    -1,
                    -1):
                opponent_field_unit = opponent_field_unit_list[index]

                if opponent_field_unit is None:
                    continue

                fixed_card_base = opponent_field_unit.get_fixed_card_base()
                tool_card = opponent_field_unit.get_tool_card()
                attached_shape_list = fixed_card_base.get_attached_shapes()

                if step_count % 2 == 1:
                    vibration_factor = 10
                    random_translation = (random.uniform(-vibration_factor, vibration_factor),
                                          random.uniform(-vibration_factor, vibration_factor))

                    new_fixed_card_base_vertices = [
                        (vx + random_translation[0], vy + random_translation[1]) for vx, vy in
                        fixed_card_base.get_vertices()
                    ]
                    fixed_card_base.update_vertices(new_fixed_card_base_vertices)

                    if tool_card is not None:
                        new_tool_card_vertices = [
                            (vx + random_translation[0], vy + random_translation[1]) for vx, vy in
                            tool_card.get_vertices()
                        ]
                        tool_card.update_vertices(new_tool_card_vertices)

                    for attached_shape in attached_shape_list:
                        # Apply random translation
                        new_attached_shape_vertices = [
                            (vx + random_translation[0], vy + random_translation[1]) for vx, vy in
                            attached_shape.get_vertices()
                        ]
                        attached_shape.update_vertices(new_attached_shape_vertices)

                else:
                    fixed_card_base.update_vertices(fixed_card_base.get_initial_vertices())
                    if tool_card is not None:
                        tool_card.update_vertices(tool_card.get_initial_vertices())
                    for attached_shape in attached_shape_list:
                        attached_shape.update_vertices(attached_shape.get_initial_vertices())

            if step_count < steps:
                self.master.after(20, opponent_wide_area_attack, step_count + 1)
            else:
                contract_of_doom_damage = 15

                self.opponent_hp_repository.take_damage(contract_of_doom_damage)
                if self.opponent_hp_repository.get_opponent_character_survival_info() == SurvivalType.DEATH:
                    self.is_playing_action_animation = False
                    self.field_area_inside_handler.clear_field_area_action()
                    self.timer.stop_timer()

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
                                hp_number -= contract_of_doom_damage

                                # TODO: n 턴간 불사 특성을 검사해야하므로 사실 이것도 summary 방식으로 빼는 것이 맞으나 우선은 진행한다.
                                if hp_number <= 0:
                                    remove_from_field = True
                                    break

                                print(f"contract_of_doom -> hp_number: {hp_number}")
                                attached_shape.set_number(hp_number)

                                attached_shape.set_image_data(
                                    self.pre_drawed_image_instance.get_pre_draw_unit_hp(hp_number))

                    if remove_from_field:
                        card_id = opponent_field_unit.get_card_number()

                        effect_animation = EffectAnimation()
                        effect_animation.set_animation_name('death')
                        effect_animation.set_total_window_size(self.width, self.height)
                        effect_animation.change_local_translation(self.opponent_field_unit_repository.find_opponent_field_unit_by_index(
                            index).get_fixed_card_base().get_local_translation())
                        effect_animation.draw_animation_panel()
                        effect_animation_panel = effect_animation.get_animation_panel()

                        animation_index = self.effect_animation_repository.save_effect_animation_at_dictionary_without_index_and_return_index(
                            effect_animation)

                        self.effect_animation_repository.save_effect_animation_panel_at_dictionary_with_index(
                            animation_index, effect_animation_panel)

                        def remove_opponent_unit(dead_unit_index):

                            print(dead_unit_index)
                            dead_unit_card_id = self.opponent_field_unit_repository.find_opponent_field_unit_by_index(dead_unit_index).get_card_number()
                            self.opponent_field_unit_repository.remove_current_field_unit_card(dead_unit_index)
                            self.opponent_tomb_repository.create_opponent_tomb_card(dead_unit_card_id)
                            self.opponent_field_unit_repository.replace_opponent_field_unit_card_position()
                            self.opponent_field_unit_repository.remove_harmful_status_by_index(dead_unit_index)



                        self.play_effect_animation_by_index_and_call_function_with_param(animation_index, remove_opponent_unit, index)

                # your_card_index = self.your_hand_repository.find_index_by_selected_object(self.selected_object)
                # self.your_hand_repository.remove_card_by_index(your_card_index)
                your_card_index = self.your_hand_repository.find_index_by_selected_object_with_page(
                    self.selected_object)
                self.your_hand_repository.remove_card_by_index_with_page(your_card_index)
                your_card_id = attack_animation_object.get_your_usage_card_id()
                self.your_tomb_repository.create_tomb_card(your_card_id)

                # self.your_hand_repository.replace_hand_card_position()
                self.your_hand_repository.update_your_hand()
                self.opponent_field_unit_repository.replace_opponent_field_unit_card_position()


                # 로스트 존 배치의 경우 서버로부터 응답을 받아야만 배치 할 수 있음
                # Eventually Consistency 상황이라면 여기서 상대 어떤 것이 Lost Zone으로 들어가야 하는지 확인
                lost_card_id = attack_animation_object.get_opponent_lost_card_id()
                self.opponent_lost_zone_repository.create_opponent_lost_zone_card(lost_card_id)
                self.selected_object = None

        opponent_wide_area_attack(1)

    def you_attack_main_character_animation(self):
        self.is_playing_action_animation = True
        steps = 20
        attack_animation_object = AttackAnimation.getInstance()
        animation_actor = attack_animation_object.get_animation_actor()
        animation_actor_card_id = animation_actor.get_card_number()

        your_fixed_card_base = animation_actor.get_fixed_card_base()
        current_your_attacker_unit_vertices = your_fixed_card_base.get_vertices()
        current_your_attacker_unit_local_translation = your_fixed_card_base.get_local_translation()
        print(f"{Fore.RED}current_your_attacker_unit_local_translation{Fore.GREEN} {current_your_attacker_unit_local_translation}{Style.RESET_ALL}")

        new_y_value = current_your_attacker_unit_local_translation[1] + 30
        your_attacker_unit_destination_local_translation = (current_your_attacker_unit_local_translation[0], new_y_value)

        step_x = (your_attacker_unit_destination_local_translation[0] - current_your_attacker_unit_local_translation[0]) / steps
        step_y = (your_attacker_unit_destination_local_translation[1] - current_your_attacker_unit_local_translation[1]) / steps
        step_y *= -1

        new_y_value = current_your_attacker_unit_local_translation[1] + 30
        your_attacker_unit_destination_local_translation = (current_your_attacker_unit_local_translation[0], new_y_value)

        opponent_main_character = attack_animation_object.get_opponent_main_character()
        opponent_main_character_vertices = opponent_main_character.get_vertices()
        print(f"{Fore.RED}opponent_main_character_vertices: {Fore.GREEN}{opponent_main_character_vertices}{Style.RESET_ALL}")

        angle_radians = math.radians(-65)
        bias_result = 85 * math.cos(angle_radians)

        opponent_main_character_destination_y = opponent_main_character_vertices[0][1]
        opponent_main_character_destination_x = opponent_main_character_vertices[0][0] - 105 - bias_result
        your_biased_local_translation = 0

        # S = v0 * t + 0.5 * a * t^2
        # S = 0.5 * a * t^2 => step = 20
        # S = 0.5 * a * 400 => a = xxx / 200
        sword_accel_y = (current_your_attacker_unit_local_translation[1] - opponent_main_character_destination_y) / 200
        print(f"{Fore.RED}sword_accel_y: {Fore.GREEN}{sword_accel_y}{Style.RESET_ALL}")
        # sword_accel_y *= -1

        # 370 - 215 = 155 -> 310 / 225
        sword_accel_x = (opponent_main_character_destination_x - current_your_attacker_unit_local_translation[0]) / 200
        print(f"{Fore.RED}sword_accel_x: {Fore.GREEN}{sword_accel_x}{Style.RESET_ALL}")

        def update_position(step_count):
            new_x = current_your_attacker_unit_local_translation[0] + step_x * step_count
            new_y = current_your_attacker_unit_local_translation[1] + step_y * step_count

            new_vertices = [
                (vx + step_x * step_count, vy + step_y * step_count) for vx, vy in current_your_attacker_unit_vertices
            ]
            your_fixed_card_base.update_vertices(new_vertices)

            # tool_card = self.selected_object.get_tool_card()
            # if tool_card is not None:
            #     new_tool_card_vertices = [
            #         (vx + new_x, vy + new_y) for vx, vy in tool_card.vertices
            #     ]
            #     tool_card.update_vertices(new_tool_card_vertices)

            for attached_shape in your_fixed_card_base.get_attached_shapes():
                # theta = w0 * t + 0.5 * alpha * t^2
                # theta = 0.5 * alpha * t^2 => step_count = 15
                # theta = 0.5 * alpha * 225 = 65 / 225 = 0.28888
                # theta = 0.5 * alpha * 400 = 65 / 400 = 0.1625
                omega_accel_alpha = -0.1625

                if isinstance(attached_shape, NonBackgroundNumberImage):
                    if attached_shape.get_circle_kinds() is CircleKinds.ATTACK:
                        accel_y_dist = sword_accel_y * step_count
                        accel_y_dist *= -1

                        accel_x_dist = sword_accel_x * step_count
                        # x: 236 / 1920, y: -367 / 1043
                        new_attached_shape_vertices = [
                            (vx + accel_x_dist, vy + accel_y_dist) for vx, vy in attached_shape.vertices
                        ]
                        attached_shape.update_vertices(new_attached_shape_vertices)
                        attached_shape.update_rotation_angle(omega_accel_alpha * step_count * step_count)
                        print(f"{Fore.RED}sword new_attached_shape_vertices{Fore.GREEN} {new_attached_shape_vertices}{Style.RESET_ALL}")

                        if step_count == 20:
                            attack_animation_object.set_your_weapon_shape(attached_shape)

                        continue

                new_attached_shape_vertices = [
                    (vx + step_x, vy + step_y) for vx, vy in attached_shape.vertices
                ]
                attached_shape.update_vertices(new_attached_shape_vertices)
                # print(f"{Fore.RED}new_attached_shape_vertices: {Fore.GREEN}{new_attached_shape_vertices}{Style.RESET_ALL}")

            if step_count < steps:
                self.master.after(20, update_position, step_count + 1)
                # if step_count == 8 and self.card_info_repository.getCardJobForCardNumber(animation_actor_card_id) == 2:
                #     self.__music_player_repository.play_sound_effect_with_event_name_for_wav('magician_basic_attack')
            else:
                self.start_you_attack_main_character_post_animation(attack_animation_object)

        update_position(1)

    def start_you_attack_main_character_post_animation(self, attack_animation_object):
        sword_shape = attack_animation_object.get_your_weapon_shape()
        opponent_main_character = attack_animation_object.get_opponent_main_character()
        opponent_main_character_vertices = opponent_main_character.get_vertices()

        your_animation_actor = attack_animation_object.get_animation_actor()
        animation_actor_card_id = your_animation_actor.get_card_number()

        steps = 30
        # (390 - 153) / 1848 = 0.1282
        sword_shape_vertices = sword_shape.get_vertices()
        need_to_moving_distance_x = opponent_main_character_vertices[1][0] - opponent_main_character_vertices[0][0]
        # sword_target_x = 0.1282 * attack_animation_object.get_total_width()
        print(f"{Fore.RED}need_to_moving_distance_x:{Fore.GREEN} {need_to_moving_distance_x}{Style.RESET_ALL}")

        # S = v0 * t + 0.5 * a * t^2
        # S = 0.5 * a * t^2 => step = 10
        # S = 0.5 * a * 100 = sword_target_x / 50
        sword_accel_x = need_to_moving_distance_x / 50
        print(f"{Fore.RED}sword_accel_x{Fore.GREEN} {sword_accel_x}{Style.RESET_ALL}")

        # theta = w0 * t + 0.5 * alpha * t^2
        # theta = 0.5 * alpha * t^2 => step_count = 10
        # theta = 0.5 * alpha * 100 = 30 / 50 = 0.6
        omega_accel_alpha = 0.3

        opponent_field_unit = self.attack_animation_object.get_opponent_field_unit()

        def slash_with_sword(step_count):
            if step_count == 1:
                if self.card_info_repository.getCardJobForCardNumber(animation_actor_card_id) == 1:
                    self.__music_player_repository.play_sound_effect_with_event_name('warrior_basic_attack')
                elif self.card_info_repository.getCardJobForCardNumber(animation_actor_card_id) == 2:
                    self.__music_player_repository.play_sound_effect_with_event_name('magician_basic_attack')
            if step_count < 11:
                sword_accel_x_dist = sword_accel_x * step_count

                new_attached_shape_vertices = [
                    (vx + sword_accel_x_dist, vy) for vx, vy in sword_shape.vertices
                ]
                sword_shape.update_vertices(new_attached_shape_vertices)

                current_angle = sword_shape.get_rotation_angle()
                sword_shape.update_rotation_angle(current_angle + omega_accel_alpha * step_count * step_count)

            if step_count > 2:
                if step_count % 2 == 1:
                    vibration_factor = 10
                    random_translation = (random.uniform(-vibration_factor, vibration_factor),
                                          random.uniform(-vibration_factor, vibration_factor))

                    for battle_field_background_shape in self.battle_field_background_shape_list:
                        battle_field_background_shape.global_translate((random_translation[0], random_translation[1]))

                else:
                    for battle_field_background_shape in self.battle_field_background_shape_list:
                        battle_field_background_shape.global_translate((0, 0))

            if step_count < steps:
                self.master.after(20, slash_with_sword, step_count + 1)
            else:
                self.finish_you_attack_main_character_post_animation(attack_animation_object)

        self.play_effect_animation_by_index(attack_animation_object.get_animation_actor().get_index())
        slash_with_sword(1)

    def finish_you_attack_main_character_post_animation(self, attack_animation_object):
        sword_shape = attack_animation_object.get_your_weapon_shape()

        animation_actor = attack_animation_object.get_animation_actor()
        your_fixed_card_base = animation_actor.get_fixed_card_base()
        tool_card = animation_actor.get_tool_card()
        attached_shape_list = your_fixed_card_base.get_attached_shapes()

        current_your_attacker_unit_vertices = your_fixed_card_base.get_vertices()
        current_your_attacker_unit_local_translation = your_fixed_card_base.get_local_translation()

        new_y_value = current_your_attacker_unit_local_translation[1] + 30
        your_attacker_unit_destination_local_translation = (current_your_attacker_unit_local_translation[0], new_y_value)

        steps = 15
        step_y = (your_attacker_unit_destination_local_translation[1] - current_your_attacker_unit_local_translation[1]) / steps
        step_y *= -1

        # (390 - 153) / 1848 = 0.1282
        current_sword_shape = attack_animation_object.get_your_weapon_shape()
        current_sword_shape_target = current_sword_shape.get_initial_vertices()

        current_sword_shape_target_x = current_sword_shape_target[0][0]
        current_sword_shape_target_y = current_sword_shape_target[0][1]

        # theta = w0 * t + 0.5 * alpha * t^2
        # theta = 0.5 * alpha * t^2 => step_count = 15
        # theta = 0.5 * alpha * 225 = angle / 112.5
        target_rotation_angle = sword_shape.get_rotation_angle()
        return_omega_accel_alpha = target_rotation_angle / 112.5

        current_sword_shape_vertices = current_sword_shape.get_vertices()
        current_sword_shape_x_vertex = current_sword_shape_vertices[0][0]
        current_sword_shape_y_vertex = current_sword_shape_vertices[0][1]

        sword_accel_x = (current_sword_shape_x_vertex - current_sword_shape_target_x - 52.5 + 15) / 112.5
        sword_accel_y = (current_sword_shape_y_vertex - current_sword_shape_target_y + 85 - 60) / 112.5
        def move_to_origin_location(step_count):
            new_y = current_your_attacker_unit_local_translation[1] + step_y * step_count
            print(f"{Fore.RED}step ->{Fore.GREEN}new_y: {new_y}{Style.RESET_ALL}")

            new_vertices = [
                (vx, vy - step_y * step_count) for vx, vy in current_your_attacker_unit_vertices
            ]
            your_fixed_card_base.update_vertices(new_vertices)
            print(f"{Fore.RED}new_vertices{Fore.GREEN} {new_vertices}{Style.RESET_ALL}")

            # tool_card = self.selected_object.get_tool_card()
            # if tool_card is not None:
            #     new_tool_card_vertices = [
            #         (vx + new_x, vy + new_y) for vx, vy in tool_card.vertices
            #     ]
            #     tool_card.update_vertices(new_tool_card_vertices)

            for attached_shape in your_fixed_card_base.get_attached_shapes():
                # theta = w0 * t + 0.5 * alpha * t^2
                # theta = 0.5 * alpha * t^2 => step_count = 15
                # theta = 0.5 * alpha * 225 = 65 / 225 = 0.28888
                omega_accel_alpha = -0.28888

                if isinstance(attached_shape, NonBackgroundNumberImage):
                    if attached_shape.get_circle_kinds() is CircleKinds.ATTACK:
                        current_sword_shape_vertices = current_sword_shape.get_vertices()

                        current_sword_shape_x_vertex = current_sword_shape_vertices[0][0]
                        current_sword_shape_y_vertex = current_sword_shape_vertices[0][1]

                        # S = v0 * t + 0.5 * a * t^2
                        # S = 0.5 * a * t^2 => step = 15
                        # S = 0.5 * a * 225 = distance / 112.5
                        # 225 = (steps * steps)

                        # difference_x: 11.434448575145638, difference_y: 94.0313609929536

                        # sword_accel_x = (current_sword_shape_target_x - current_sword_shape_x_vertex - 195) / 112.5
                        # sword_accel_x = (current_sword_shape_x_vertex - current_sword_shape_target_x) / 112.5
                        # sword_accel_y = (current_sword_shape_target_y - current_sword_shape_y_vertex + 124.732391723) / 112.5
                        print(f"{Fore.RED}sword_accel -> {Fore.GREEN}x: {sword_accel_x}, y: {sword_accel_y}{Style.RESET_ALL}")

                        sword_accel_x_dist = sword_accel_x * step_count
                        sword_accel_y_dist = sword_accel_y * step_count

                        new_attached_shape_vertices = [
                            (vx - sword_accel_x_dist, vy - sword_accel_y_dist) for vx, vy in sword_shape.vertices
                        ]
                        sword_shape.update_vertices(new_attached_shape_vertices)
                        # print(f"{Fore.RED}new_attached_shape_vertices: {Fore.GREEN}{new_attached_shape_vertices}{Style.RESET_ALL}")

                        current_angle = sword_shape.get_rotation_angle()
                        sword_shape.update_rotation_angle(current_angle - return_omega_accel_alpha * step_count)

                        continue

                new_attached_shape_vertices = [
                    (vx, vy - step_y) for vx, vy in attached_shape.vertices
                ]
                attached_shape.update_vertices(new_attached_shape_vertices)

            if step_count < steps:
                self.master.after(20, move_to_origin_location, step_count + 1)
            else:
                self.is_playing_action_animation = False
                your_fixed_card_base.update_vertices(your_fixed_card_base.get_initial_vertices())
                if tool_card is not None:
                    tool_card.update_vertices(tool_card.get_initial_vertices())
                for attached_shape in attached_shape_list:
                    attached_shape.update_vertices(attached_shape.get_initial_vertices())

                self.is_attack_motion_finished = True
                attack_animation_object.set_is_finished(True)

                your_damage = attack_animation_object.get_animation_actor_damage()
                self.opponent_hp_repository.take_damage(your_damage)

                if self.opponent_hp_repository.get_current_opponent_hp() <= 0:
                    self.opponent_hp_repository.opponent_character_die()
                    self.timer.stop_timer()

        move_to_origin_location(1)

    def opponent_nether_blade_first_passive_skill_animation(self):
        steps = 10
        attack_animation_object = AttackAnimation.getInstance()
        opponent_animation_actor = attack_animation_object.get_opponent_animation_actor()

        opponent_fixed_card_base = opponent_animation_actor.get_fixed_card_base()
        current_opponent_attacker_unit_vertices = opponent_fixed_card_base.get_vertices()
        current_opponent_attacker_unit_local_translation = opponent_fixed_card_base.get_local_translation()

        # x: 608, y: -199 <- top
        # x: 603, y: -437 <- bottom

        new_y_value = current_opponent_attacker_unit_local_translation[1] + 240
        new_x_value = attack_animation_object.get_total_width() / 2 - 52.5
        # your_attacker_unit_destination_local_translation = (current_your_attacker_unit_local_translation[0], new_y_value)
        opponent_attacker_unit_destination_local_translation = (new_x_value, new_y_value)

        attack_animation_object.set_opponent_attacker_unit_moving_x(
            opponent_attacker_unit_destination_local_translation[0] - current_opponent_attacker_unit_local_translation[0])

        step_x = (opponent_attacker_unit_destination_local_translation[0] - current_opponent_attacker_unit_local_translation[0]) / steps
        step_y = (opponent_attacker_unit_destination_local_translation[1] - current_opponent_attacker_unit_local_translation[1]) / steps
        step_y *= -1

        def update_position(step_count):
            print(f"{Fore.RED}step_count: {Fore.GREEN}{step_count}{Style.RESET_ALL}")

            new_vertices = [
                (vx + step_x * step_count, vy + step_y * step_count) for vx, vy in current_opponent_attacker_unit_vertices
            ]
            opponent_fixed_card_base.update_vertices(new_vertices)

            # tool_card = self.selected_object.get_tool_card()
            # if tool_card is not None:
            #     new_tool_card_vertices = [
            #         (vx + new_x, vy + new_y) for vx, vy in tool_card.vertices
            #     ]
            #     tool_card.update_vertices(new_tool_card_vertices)

            for attached_shape in opponent_fixed_card_base.get_attached_shapes():
                new_attached_shape_vertices = [
                    (vx + step_x, vy + step_y) for vx, vy in attached_shape.vertices
                ]
                attached_shape.update_vertices(new_attached_shape_vertices)
                # print(f"{Fore.RED}new_attached_shape_vertices: {Fore.GREEN}{new_attached_shape_vertices}{Style.RESET_ALL}")

            if step_count < steps:
                self.master.after(20, update_position, step_count + 1)
            else:
                self.create_effect_animation_to_full_screen_and_play_animation_and_call_function_with_param(
                    'nether_blade_area_skill', self.start_opponent_nether_blade_first_passive_wide_area_motion_animation,
                    attack_animation_object
                )
                # self.start_opponent_nether_blade_first_passive_wide_area_motion_animation(attack_animation_object)

        update_position(1)

    def start_opponent_nether_blade_first_passive_wide_area_motion_animation(self, attack_animation_object):
        steps = 50

        your_field_unit_list = self.your_field_unit_repository.get_current_field_unit_list()
        your_field_unit_list_length = len(
            self.your_field_unit_repository.get_current_field_unit_list())

        def wide_area_attack(step_count):
            for index in range(
                    your_field_unit_list_length - 1,
                    -1,
                    -1):
                your_field_unit = your_field_unit_list[index]

                if your_field_unit is None:
                    continue

                fixed_card_base = your_field_unit.get_fixed_card_base()
                tool_card = your_field_unit.get_tool_card()
                attached_shape_list = fixed_card_base.get_attached_shapes()

                if step_count % 2 == 1:
                    vibration_factor = 10
                    random_translation = (random.uniform(-vibration_factor, vibration_factor),
                                          random.uniform(-vibration_factor, vibration_factor))

                    new_fixed_card_base_vertices = [
                        (vx + random_translation[0], vy + random_translation[1]) for vx, vy in
                        fixed_card_base.get_vertices()
                    ]
                    fixed_card_base.update_vertices(new_fixed_card_base_vertices)

                    if tool_card is not None:
                        new_tool_card_vertices = [
                            (vx + random_translation[0], vy + random_translation[1]) for vx, vy in
                            tool_card.get_vertices()
                        ]
                        tool_card.update_vertices(new_tool_card_vertices)

                    for attached_shape in attached_shape_list:
                        # Apply random translation
                        new_attached_shape_vertices = [
                            (vx + random_translation[0], vy + random_translation[1]) for vx, vy in
                            attached_shape.get_vertices()
                        ]
                        attached_shape.update_vertices(new_attached_shape_vertices)

                else:
                    # Return to the original position
                    # fixed_card_base.update_vertices(fixed_card_base.get_vertices())
                    # if tool_card is not None:
                    #     tool_card.update_vertices(tool_card.get_vertices())
                    # for attached_shape in attached_shape_list:
                    #     attached_shape.update_vertices(attached_shape.get_vertices())

                    # self.opponent_field_unit_repository.replace_opponent_field_unit_card_position()

                    fixed_card_base.update_vertices(fixed_card_base.get_initial_vertices())
                    if tool_card is not None:
                        tool_card.update_vertices(tool_card.get_initial_vertices())
                    for attached_shape in attached_shape_list:
                        attached_shape.update_vertices(attached_shape.get_initial_vertices())

            if step_count < steps:
                self.master.after(20, wide_area_attack, step_count + 1)
            else:
                self.finish_opponent_nether_blade_first_passive_wide_area_motion_animation(attack_animation_object)
                # pass
                # self.is_attack_motion_finished = True
                # attack_animation_object.set_is_finished(True)
                # attack_animation_object.set_need_post_process(True)



        wide_area_attack(1)

    def finish_opponent_nether_blade_first_passive_wide_area_motion_animation(self, attack_animation_object):
        opponent_animation_actor = attack_animation_object.get_opponent_animation_actor()
        opponent_fixed_card_base = opponent_animation_actor.get_fixed_card_base()
        tool_card = opponent_animation_actor.get_tool_card()
        attached_shape_list = opponent_fixed_card_base.get_attached_shapes()

        # your_fixed_card_base_initial_vertices = your_fixed_card_base.get_initial_vertices()
        # print(f"{Fore.RED}your_fixed_card_base_initial_vertices{Fore.GREEN} {your_fixed_card_base_initial_vertices}{Style.RESET_ALL}")

        current_opponent_attacker_unit_vertices = opponent_fixed_card_base.get_vertices()
        current_opponent_attacker_unit_local_translation = opponent_fixed_card_base.get_local_translation()

        opponent_attacker_unit_moving_x = attack_animation_object.get_opponent_attacker_unit_moving_x()

        new_y_value = current_opponent_attacker_unit_local_translation[1] - 240
        opponent_attacker_unit_destination_local_translation = (0, new_y_value)
        print(
            f"{Fore.RED}opponent_attacker_unit_destination_local_translation{Fore.GREEN} {opponent_attacker_unit_destination_local_translation}{Style.RESET_ALL}")

        steps = 15
        step_x = opponent_attacker_unit_moving_x / steps
        step_y = (opponent_attacker_unit_destination_local_translation[1] -
                  current_opponent_attacker_unit_local_translation[1]) / steps

        # step_y *= -1

        def move_to_origin_location(step_count):
            new_y = current_opponent_attacker_unit_local_translation[1] + step_y * step_count
            print(f"{Fore.RED}step ->{Fore.GREEN}new_y: {new_y}{Style.RESET_ALL}")

            new_vertices = [
                (vx - step_x * step_count, vy - step_y * step_count) for vx, vy in
                current_opponent_attacker_unit_vertices
            ]
            opponent_fixed_card_base.update_vertices(new_vertices)
            print(f"{Fore.RED}new_vertices{Fore.GREEN} {new_vertices}{Style.RESET_ALL}")

            # tool_card = self.selected_object.get_tool_card()
            # if tool_card is not None:
            #     new_tool_card_vertices = [
            #         (vx + new_x, vy + new_y) for vx, vy in tool_card.vertices
            #     ]
            #     tool_card.update_vertices(new_tool_card_vertices)

            for attached_shape in opponent_fixed_card_base.get_attached_shapes():
                new_attached_shape_vertices = [
                    (vx - step_x, vy - step_y) for vx, vy in attached_shape.vertices
                ]
                attached_shape.update_vertices(new_attached_shape_vertices)
                # print(f"{Fore.RED}new_attached_shape_vertices: {Fore.GREEN}{new_attached_shape_vertices}{Style.RESET_ALL}")

            if step_count < steps:

                self.master.after(20, move_to_origin_location, step_count + 1)
            else:
                notify_data = attack_animation_object.get_notify_data()
                your_field_unit_health_point_map = (
                    notify_data)['player_field_unit_health_point_map']['You']['field_unit_health_point_map']
                your_field_unit_harmful_effect_list = (
                    notify_data)['player_field_unit_harmful_effect_map']['You']['field_unit_harmful_status_map']
                your_dead_field_unit_index_list = (
                    notify_data)['player_field_unit_death_map']['You']['dead_field_unit_index_list']

                for unit_index, remaining_health_point in your_field_unit_health_point_map.items():
                    your_field_unit = self.your_field_unit_repository.find_field_unit_by_index(int(unit_index))
                    your_fixed_card_base = your_field_unit.get_fixed_card_base()
                    your_fixed_card_attached_shape_list = your_fixed_card_base.get_attached_shapes()

                    if remaining_health_point <= 0:
                        continue

                    for your_fixed_card_attached_shape in your_fixed_card_attached_shape_list:
                        if isinstance(your_fixed_card_attached_shape, NonBackgroundNumberImage):
                            if your_fixed_card_attached_shape.get_circle_kinds() is CircleKinds.HP:
                                your_fixed_card_attached_shape.set_number(int(remaining_health_point))

                                your_fixed_card_attached_shape.set_image_data(
                                    self.pre_drawed_image_instance.get_pre_draw_unit_hp(int(remaining_health_point)))

                for unit_index, harmful_effect_info in your_field_unit_harmful_effect_list.items():
                    harmful_effect_list = harmful_effect_info['harmful_status_list']
                    self.your_field_unit_repository.apply_harmful_status(int(unit_index), harmful_effect_list)

                # 죽은 유닛들 묘지에 배치 및 Replacing
                for dead_unit_index in your_dead_field_unit_index_list:
                    def remove_field_unit(unit_index):
                        field_unit_id = self.your_field_unit_repository.get_card_id_by_index(unit_index)
                        self.your_tomb_repository.create_tomb_card(field_unit_id)
                        self.your_field_unit_repository.remove_card_by_index(unit_index)
                        self.your_field_unit_repository.remove_harmful_status_by_index(unit_index)
                        self.your_field_unit_repository.replace_field_card_position()

                    self.create_effect_animation_to_your_unit_and_play_animation_and_call_function_with_param(
                        'death', dead_unit_index, remove_field_unit, dead_unit_index
                    )


                self.attack_animation_object.set_opponent_animation_actor(None)
                self.opponent_field_unit_repository.replace_opponent_field_unit_card_position()
                self.opponent_field_area_inside_handler.set_active_field_area_action(OpponentFieldAreaActionProcess.Dummy)
                # self.opponent_nether_blade_second_passive_skill_animation()

        move_to_origin_location(1)

    def opponent_nether_blade_second_passive_skill_animation(self):
        steps = 10
        attack_animation_object = AttackAnimation.getInstance()
        opponent_animation_actor = attack_animation_object.get_opponent_animation_actor()

        opponent_fixed_card_base = opponent_animation_actor.get_fixed_card_base()
        current_opponent_attacker_unit_vertices = opponent_fixed_card_base.get_vertices()
        current_opponent_attacker_unit_local_translation = opponent_fixed_card_base.get_local_translation()

        new_y_value = current_opponent_attacker_unit_local_translation[1] + 240
        new_x_value = attack_animation_object.get_total_width() / 2 - 52.5
        # your_attacker_unit_destination_local_translation = (current_your_attacker_unit_local_translation[0], new_y_value)
        opponent_attacker_unit_destination_local_translation = (new_x_value, new_y_value)

        attack_animation_object.set_opponent_attacker_unit_moving_x(
            opponent_attacker_unit_destination_local_translation[0] - current_opponent_attacker_unit_local_translation[0])

        step_x = (opponent_attacker_unit_destination_local_translation[0] - current_opponent_attacker_unit_local_translation[0]) / steps
        step_y = (opponent_attacker_unit_destination_local_translation[1] - current_opponent_attacker_unit_local_translation[1]) / steps
        step_y *= -1

        def update_position(step_count):
            print(f"{Fore.RED}step_count: {Fore.GREEN}{step_count}{Style.RESET_ALL}")

            new_vertices = [
                (vx + step_x * step_count, vy + step_y * step_count) for vx, vy in current_opponent_attacker_unit_vertices
            ]
            opponent_fixed_card_base.update_vertices(new_vertices)

            # tool_card = self.selected_object.get_tool_card()
            # if tool_card is not None:
            #     new_tool_card_vertices = [
            #         (vx + new_x, vy + new_y) for vx, vy in tool_card.vertices
            #     ]
            #     tool_card.update_vertices(new_tool_card_vertices)

            for attached_shape in opponent_fixed_card_base.get_attached_shapes():
                new_attached_shape_vertices = [
                    (vx + step_x, vy + step_y) for vx, vy in attached_shape.vertices
                ]
                attached_shape.update_vertices(new_attached_shape_vertices)
                # print(f"{Fore.RED}new_attached_shape_vertices: {Fore.GREEN}{new_attached_shape_vertices}{Style.RESET_ALL}")

            if step_count < steps:
                self.master.after(20, update_position, step_count + 1)
            else:
                # self.opponent_field_area_inside_handler.set_field_area_action(OpponentFieldAreaActionProcess.REQUIRE_TO_PROCESS_PASSIVE_SKILL_PROCESS)



                self.start_opponent_nether_blade_second_passive_targeting_motion_animation(self.attack_animation_object)


        update_position(1)

    ### Opponent Second Passive
    def start_opponent_nether_blade_second_passive_targeting_motion_animation(self, attack_animation_object):
        steps = 50

        is_attack_main_character = False
        your_field_unit = None
        # targeting_damage = self.attack_animation_object.get_animation_actor_damage()
        is_opponent_attack_main_character = self.attack_animation_object.get_is_opponent_attack_main_character()
        if is_opponent_attack_main_character is not False:
            is_attack_main_character = True
        else:
            your_field_unit = self.attack_animation_object.get_your_field_unit()

        def targeting_attack(step_count):
            vibration_factor = 10
            random_translation = (random.uniform(-vibration_factor, vibration_factor),
                                  random.uniform(-vibration_factor, vibration_factor))

            if is_attack_main_character is False:
                print(f"{Fore.RED}필드 유닛 공격 -> is_attack_main_character(False): {Fore.GREEN}{is_attack_main_character}{Style.RESET_ALL}")
                fixed_card_base = your_field_unit.get_fixed_card_base()
                tool_card = your_field_unit.get_tool_card()
                attached_shape_list = fixed_card_base.get_attached_shapes()

                if step_count % 2 == 1:
                    new_fixed_card_base_vertices = [
                        (vx + random_translation[0], vy + random_translation[1]) for vx, vy in
                        fixed_card_base.get_vertices()
                    ]
                    fixed_card_base.update_vertices(new_fixed_card_base_vertices)

                    if tool_card is not None:
                        new_tool_card_vertices = [
                            (vx + random_translation[0], vy + random_translation[1]) for vx, vy in
                            tool_card.get_vertices()
                        ]
                        tool_card.update_vertices(new_tool_card_vertices)

                    for attached_shape in attached_shape_list:
                        # Apply random translation
                        new_attached_shape_vertices = [
                            (vx + random_translation[0], vy + random_translation[1]) for vx, vy in
                            attached_shape.get_vertices()
                        ]
                        attached_shape.update_vertices(new_attached_shape_vertices)

                else:
                    fixed_card_base.update_vertices(fixed_card_base.get_initial_vertices())
                    if tool_card is not None:
                        tool_card.update_vertices(tool_card.get_initial_vertices())
                    for attached_shape in attached_shape_list:
                        attached_shape.update_vertices(attached_shape.get_initial_vertices())

            else:
                # print(f"{Fore.RED}메인 캐릭터 공격 -> is_attack_main_character(True): {Fore.GREEN}{is_attack_main_character}{Style.RESET_ALL}")
                if step_count % 2 == 1:
                    for battle_field_background_shape in self.battle_field_background_shape_list:
                        battle_field_background_shape.global_translate((random_translation[0], random_translation[1]))

                else:
                    for battle_field_background_shape in self.battle_field_background_shape_list:
                        battle_field_background_shape.global_translate((0, 0))

            if step_count < steps:
                self.master.after(20, targeting_attack, step_count + 1)
            else:
                self.finish_opponent_nether_blade_second_passive_targeting_animation(self.attack_animation_object)
                # self.is_attack_motion_finished = True
                # attack_animation_object.set_is_finished(True)
                # attack_animation_object.set_need_post_process(True)

        if is_attack_main_character:
            self.create_effect_animation_to_full_screen_and_play_animation_and_call_function_with_param(
                'nether_blade_targeting_skill', targeting_attack, 1)
            # self.create_effect_animation_with_vertices_and_play_animation_and_call_function_with_param(
            #     'nether_blade_targeting_skill', self.your_main_character_panel.get_vertices(),
            #     targeting_attack, 1
            # )
        else:
            self.create_effect_animation_to_full_screen_and_play_animation_and_call_function_with_param(
                'nether_blade_targeting_skill', targeting_attack, 1)
            # self.create_effect_animation_to_your_unit_and_play_animation_and_call_function_with_param(
            #     'nether_blade_targeting_skill', your_field_unit.get_index(), targeting_attack, 1
            # )

        # targeting_attack(1)

    def finish_opponent_nether_blade_second_passive_targeting_animation(self, attack_animation_object):
        opponent_animation_actor = attack_animation_object.get_opponent_animation_actor()
        opponent_fixed_card_base = opponent_animation_actor.get_fixed_card_base()
        opponent_actor_extra_ability = attack_animation_object.get_extra_ability()

        current_opponent_attacker_unit_vertices = opponent_fixed_card_base.get_vertices()
        current_opponent_attacker_unit_local_translation = opponent_fixed_card_base.get_local_translation()

        opponent_attacker_unit_moving_x = attack_animation_object.get_opponent_attacker_unit_moving_x()

        new_y_value = current_opponent_attacker_unit_local_translation[1] - 240
        opponent_attacker_unit_destination_local_translation = (0, new_y_value)

        steps = 15
        step_x = opponent_attacker_unit_moving_x / steps
        step_y = (opponent_attacker_unit_destination_local_translation[1] - current_opponent_attacker_unit_local_translation[1]) / steps
        # step_y *= -1

        is_attack_main_character = False
        your_field_unit = None
        is_opponent_attack_main_character = self.attack_animation_object.get_is_opponent_attack_main_character()
        if is_opponent_attack_main_character is not False:
            is_attack_main_character = True
        else:
            your_field_unit = self.attack_animation_object.get_your_field_unit()

        def move_to_origin_location(step_count):
            new_vertices = [
                (vx  - step_x * step_count, vy - step_y * step_count) for vx, vy in current_opponent_attacker_unit_vertices
            ]
            opponent_fixed_card_base.update_vertices(new_vertices)

            # tool_card = self.selected_object.get_tool_card()
            # if tool_card is not None:
            #     new_tool_card_vertices = [
            #         (vx + new_x, vy + new_y) for vx, vy in tool_card.vertices
            #     ]
            #     tool_card.update_vertices(new_tool_card_vertices)

            for attached_shape in opponent_fixed_card_base.get_attached_shapes():
                new_attached_shape_vertices = [
                    (vx - step_x, vy - step_y) for vx, vy in attached_shape.vertices
                ]
                attached_shape.update_vertices(new_attached_shape_vertices)
                # print(f"{Fore.RED}new_attached_shape_vertices: {Fore.GREEN}{new_attached_shape_vertices}{Style.RESET_ALL}")

            if step_count < steps:

                self.master.after(20, move_to_origin_location, step_count + 1)
            else:
                self.is_playing_action_animation = False
                targeting_damage = 20
                if is_attack_main_character is False:
                    print(f"{Fore.RED}필드 유닛 공격 -> is_attack_main_character(False): {Fore.GREEN}{is_attack_main_character}{Style.RESET_ALL}")

                    # fixed_card_base = your_field_unit.get_fixed_card_base()
                    # tool_card = your_field_unit.get_tool_card()
                    # attached_shape_list = fixed_card_base.get_attached_shapes()
                    #
                    # remove_from_field = False
                    # for attached_shape in attached_shape_list:
                    #     if isinstance(attached_shape, NonBackgroundNumberImage):
                    #         if attached_shape.get_circle_kinds() is CircleKinds.HP:
                    #             hp_number = attached_shape.get_number()
                    #             print(f"{Fore.RED}current hp_number: {Fore.GREEN}{hp_number}{Style.RESET_ALL}")
                    #
                    #             hp_number -= targeting_damage
                    #             print(f"{Fore.RED}hp_number: {Fore.GREEN}{hp_number}{Style.RESET_ALL}")
                    #
                    #             # TODO: n 턴간 불사 특성을 검사해야하므로 사실 이것도 summary 방식으로 빼는 것이 맞으나 우선은 진행한다.
                    #             if hp_number <= 0:
                    #                 remove_from_field = True
                    #                 break
                    #
                    #             attached_shape.set_number(hp_number)
                    #
                    #             # attached_shape.set_image_data(
                    #             #     # TODO: 실제로 여기서 서버로부터 계산 받은 값을 적용해야함
                    #             #     self.pre_drawed_image_instance.get_pre_draw_number_image(hp_number))
                    #
                    #             attached_shape.set_image_data(
                    #                 self.pre_drawed_image_instance.get_pre_draw_unit_hp(hp_number))
                    #
                    #             if opponent_actor_extra_ability:
                    #                 self.your_field_unit_repository.apply_harmful_status(your_field_unit.get_index(), opponent_actor_extra_ability)
                    #
                    # if remove_from_field:
                    #     card_id = your_field_unit.get_card_number()
                    #     card_index = your_field_unit.get_index()
                    #
                    #     self.your_field_unit_repository.remove_card_by_index(card_index)
                    #
                    #     self.your_field_unit_repository.remove_harmful_status_by_index(card_index)
                    #     self.your_tomb_repository.create_opponent_tomb_card(card_id)

                    notify_data = attack_animation_object.get_notify_data()

                    your_field_unit_health_point_map = (
                        notify_data)['player_field_unit_health_point_map']['You']['field_unit_health_point_map']
                    your_field_unit_harmful_effect_list = (
                        notify_data)['player_field_unit_harmful_effect_map']['You']['field_unit_harmful_status_map']
                    your_dead_field_unit_index_list = (
                        notify_data)['player_field_unit_death_map']['You']['dead_field_unit_index_list']

                    for unit_index, remaining_health_point in your_field_unit_health_point_map.items():
                        your_field_unit = self.your_field_unit_repository.find_field_unit_by_index(int(unit_index))
                        your_fixed_card_base = your_field_unit.get_fixed_card_base()
                        your_fixed_card_attached_shape_list = your_fixed_card_base.get_attached_shapes()

                        if remaining_health_point <= 0:
                            continue

                        for your_fixed_card_attached_shape in your_fixed_card_attached_shape_list:
                            if isinstance(your_fixed_card_attached_shape, NonBackgroundNumberImage):
                                if your_fixed_card_attached_shape.get_circle_kinds() is CircleKinds.HP:
                                    your_fixed_card_attached_shape.set_number(int(remaining_health_point))

                                    your_fixed_card_attached_shape.set_image_data(
                                        self.pre_drawed_image_instance.get_pre_draw_unit_hp(int(remaining_health_point)))

                    for unit_index, harmful_effect_info in your_field_unit_harmful_effect_list.items():
                        harmful_effect_list = harmful_effect_info['harmful_status_list']
                        self.your_field_unit_repository.apply_harmful_status(int(unit_index), harmful_effect_list)

                    # 죽은 유닛들 묘지에 배치 및 Replacing
                    for dead_unit_index in your_dead_field_unit_index_list:
                        def remove_field_unit(unit_index):
                            field_unit_id = self.your_field_unit_repository.get_card_id_by_index(unit_index)
                            self.your_tomb_repository.create_tomb_card(field_unit_id)
                            self.your_field_unit_repository.remove_card_by_index(unit_index)
                            self.your_field_unit_repository.remove_harmful_status_by_index(unit_index)
                            self.your_field_unit_repository.replace_field_card_position()

                        self.create_effect_animation_to_your_unit_and_play_animation_and_call_function_with_param(
                            'death', dead_unit_index, remove_field_unit, dead_unit_index
                        )

                else:
                    print(f"{Fore.RED}메인 캐릭터 공격 -> is_attack_main_character(True): {Fore.GREEN}{is_attack_main_character}{Style.RESET_ALL}")

                    notify_data = attack_animation_object.get_notify_data()

                    your_main_character_health_point = (
                        notify_data)['player_main_character_health_point_map']['You']
                    your_main_character_survival_state = (
                        notify_data)['player_main_character_survival_map']['You']

                    self.your_hp_repository.change_hp(int(your_main_character_health_point))
                    print(f"{Fore.RED}current_main_character_health:{Fore.GREEN} "
                          f"{self.your_hp_repository.get_current_your_hp_state().get_current_health()}{Style.RESET_ALL}")

                    if your_main_character_survival_state == 'Death':
                        print('Your main character is dead!')
                        self.your_hp_repository.your_character_die()
                        self.timer.stop_timer()
                        self.battle_field_repository.lose()
                        return



                    # self.your_hp_repository.take_damage(targeting_damage)
                    self.attack_animation_object.set_is_opponent_attack_main_character(False)

                self.your_field_unit_repository.replace_field_card_position()
                self.opponent_field_area_inside_handler.clear_field_area_action()
                self.opponent_field_area_inside_handler.clear_active_field_area_action()
                # self.opponent_field_area_inside_handler.clear_field_turn_start_action()
                self.opponent_fixed_unit_card_inside_handler.clear_opponent_field_area_action()

                self.attack_animation_object.set_opponent_animation_actor(None)

        move_to_origin_location(1)

    ### Your Nether Blade

    def nether_blade_first_passive_skill_animation(self):
        self.is_playing_action_animation = True
        steps = 10
        attack_animation_object = AttackAnimation.getInstance()
        animation_actor = attack_animation_object.get_animation_actor()

        your_fixed_card_base = animation_actor.get_fixed_card_base()
        current_your_attacker_unit_vertices = your_fixed_card_base.get_vertices()
        current_your_attacker_unit_local_translation = your_fixed_card_base.get_local_translation()

        new_y_value = current_your_attacker_unit_local_translation[1] - 270
        new_x_value = attack_animation_object.get_total_width() / 2 - 52.5
        # your_attacker_unit_destination_local_translation = (current_your_attacker_unit_local_translation[0], new_y_value)
        your_attacker_unit_destination_local_translation = (new_x_value, new_y_value)

        attack_animation_object.set_your_attacker_unit_moving_x(
            your_attacker_unit_destination_local_translation[0] - current_your_attacker_unit_local_translation[0])

        step_x = (your_attacker_unit_destination_local_translation[0] - current_your_attacker_unit_local_translation[0]) / steps
        step_y = (your_attacker_unit_destination_local_translation[1] - current_your_attacker_unit_local_translation[1]) / steps
        step_y *= -1

        def update_position(step_count):
            print(f"{Fore.RED}step_count: {Fore.GREEN}{step_count}{Style.RESET_ALL}")

            new_vertices = [
                (vx + step_x * step_count, vy + step_y * step_count) for vx, vy in current_your_attacker_unit_vertices
            ]
            your_fixed_card_base.update_vertices(new_vertices)

            # tool_card = self.selected_object.get_tool_card()
            # if tool_card is not None:
            #     new_tool_card_vertices = [
            #         (vx + new_x, vy + new_y) for vx, vy in tool_card.vertices
            #     ]
            #     tool_card.update_vertices(new_tool_card_vertices)

            for attached_shape in your_fixed_card_base.get_attached_shapes():
                new_attached_shape_vertices = [
                    (vx + step_x, vy + step_y) for vx, vy in attached_shape.vertices
                ]
                attached_shape.update_vertices(new_attached_shape_vertices)
                # print(f"{Fore.RED}new_attached_shape_vertices: {Fore.GREEN}{new_attached_shape_vertices}{Style.RESET_ALL}")

            if step_count < steps:
                self.master.after(20, update_position, step_count + 1)
                if step_count == 9:
                    self.__music_player_repository.play_sound_effect_with_event_name('nether_passive_skill_1')
            else:

                # effect_animation.draw_full_screen_animation_panel()
                # self.__music_player_repository.play_sound_effect_with_event_name('nether_passive_skill_1')
                self.create_effect_animation_to_full_screen_and_play_animation_and_call_function_with_param(
                    'nether_blade_area_skill', self.start_nether_blade_first_passive_wide_area_motion_animation, attack_animation_object
                )

                # self.create_effect_animation_to_opponent_field_and_play_animation_and_call_function_with_param(
                #     'nether_blade_area_skill', self.start_nether_blade_first_passive_wide_area_motion_animation, attack_animation_object
                # )
                # self.start_nether_blade_first_passive_wide_area_motion_animation(attack_animation_object)

        update_position(1)

    def start_nether_blade_first_passive_wide_area_motion_animation(self, attack_animation_object):
        steps = 50

        opponent_field_unit_list = self.opponent_field_unit_repository.get_current_field_unit_card_object_list()
        opponent_field_unit_list_length = len(
            self.opponent_field_unit_repository.get_current_field_unit_card_object_list())

        def wide_area_attack(step_count):
            for index in range(
                    opponent_field_unit_list_length - 1,
                    -1,
                    -1):
                opponent_field_unit = opponent_field_unit_list[index]

                if opponent_field_unit is None:
                    continue

                fixed_card_base = opponent_field_unit.get_fixed_card_base()
                tool_card = opponent_field_unit.get_tool_card()
                attached_shape_list = fixed_card_base.get_attached_shapes()

                if step_count % 2 == 1:
                    vibration_factor = 10
                    random_translation = (random.uniform(-vibration_factor, vibration_factor),
                                          random.uniform(-vibration_factor, vibration_factor))

                    new_fixed_card_base_vertices = [
                        (vx + random_translation[0], vy + random_translation[1]) for vx, vy in
                        fixed_card_base.get_vertices()
                    ]
                    fixed_card_base.update_vertices(new_fixed_card_base_vertices)

                    if tool_card is not None:
                        new_tool_card_vertices = [
                            (vx + random_translation[0], vy + random_translation[1]) for vx, vy in
                            tool_card.get_vertices()
                        ]
                        tool_card.update_vertices(new_tool_card_vertices)

                    for attached_shape in attached_shape_list:
                        # Apply random translation
                        new_attached_shape_vertices = [
                            (vx + random_translation[0], vy + random_translation[1]) for vx, vy in
                            attached_shape.get_vertices()
                        ]
                        attached_shape.update_vertices(new_attached_shape_vertices)

                else:
                    # Return to the original position
                    # fixed_card_base.update_vertices(fixed_card_base.get_vertices())
                    # if tool_card is not None:
                    #     tool_card.update_vertices(tool_card.get_vertices())
                    # for attached_shape in attached_shape_list:
                    #     attached_shape.update_vertices(attached_shape.get_vertices())

                    # self.opponent_field_unit_repository.replace_opponent_field_unit_card_position()

                    fixed_card_base.update_vertices(fixed_card_base.get_initial_vertices())
                    if tool_card is not None:
                        tool_card.update_vertices(tool_card.get_initial_vertices())
                    for attached_shape in attached_shape_list:
                        attached_shape.update_vertices(attached_shape.get_initial_vertices())

            if step_count < steps:
                self.master.after(20, wide_area_attack, step_count + 1)
            else:
                self.finish_nether_blade_first_passive_wide_area_motion_animation(attack_animation_object)
                # pass
                # self.is_attack_motion_finished = True
                # attack_animation_object.set_is_finished(True)
                # attack_animation_object.set_need_post_process(True)

        wide_area_attack(1)

    def finish_nether_blade_first_passive_wide_area_motion_animation(self, attack_animation_object):
        animation_actor = attack_animation_object.get_animation_actor()
        your_fixed_card_base = animation_actor.get_fixed_card_base()
        tool_card = animation_actor.get_tool_card()
        attached_shape_list = your_fixed_card_base.get_attached_shapes()

        # your_fixed_card_base_initial_vertices = your_fixed_card_base.get_initial_vertices()
        # print(f"{Fore.RED}your_fixed_card_base_initial_vertices{Fore.GREEN} {your_fixed_card_base_initial_vertices}{Style.RESET_ALL}")

        current_your_attacker_unit_vertices = your_fixed_card_base.get_vertices()
        current_your_attacker_unit_local_translation = your_fixed_card_base.get_local_translation()

        your_attacker_unit_moving_x = attack_animation_object.get_your_attacker_unit_moving_x()

        new_y_value = current_your_attacker_unit_local_translation[1] + 270
        your_attacker_unit_destination_local_translation = (0, new_y_value)
        print(f"{Fore.RED}your_attacker_unit_destination_local_translation{Fore.GREEN} {your_attacker_unit_destination_local_translation}{Style.RESET_ALL}")

        steps = 15
        step_x = your_attacker_unit_moving_x / steps
        step_y = (your_attacker_unit_destination_local_translation[1] - current_your_attacker_unit_local_translation[1]) / steps
        # step_y *= -1

        def move_to_origin_location(step_count):
            new_y = current_your_attacker_unit_local_translation[1] + step_y * step_count
            print(f"{Fore.RED}step ->{Fore.GREEN}new_y: {new_y}{Style.RESET_ALL}")

            new_vertices = [
                (vx  - step_x * step_count, vy - step_y * step_count) for vx, vy in current_your_attacker_unit_vertices
            ]
            your_fixed_card_base.update_vertices(new_vertices)
            print(f"{Fore.RED}new_vertices{Fore.GREEN} {new_vertices}{Style.RESET_ALL}")

            # tool_card = self.selected_object.get_tool_card()
            # if tool_card is not None:
            #     new_tool_card_vertices = [
            #         (vx + new_x, vy + new_y) for vx, vy in tool_card.vertices
            #     ]
            #     tool_card.update_vertices(new_tool_card_vertices)

            for attached_shape in your_fixed_card_base.get_attached_shapes():
                new_attached_shape_vertices = [
                    (vx - step_x, vy - step_y) for vx, vy in attached_shape.vertices
                ]
                attached_shape.update_vertices(new_attached_shape_vertices)
                # print(f"{Fore.RED}new_attached_shape_vertices: {Fore.GREEN}{new_attached_shape_vertices}{Style.RESET_ALL}")

            if step_count < steps:

                self.master.after(20, move_to_origin_location, step_count + 1)
            else:
                self.is_playing_action_animation = False
                opponent_field_unit_list = self.opponent_field_unit_repository.get_current_field_unit_card_object_list()
                opponent_field_unit_list_length = len(
                    self.opponent_field_unit_repository.get_current_field_unit_card_object_list())

                your_actor_damage = attack_animation_object.get_animation_actor_damage()
                your_actor_extra_ability = attack_animation_object.get_extra_ability()

                for index in range(
                        opponent_field_unit_list_length - 1,
                        -1,
                        -1):
                    opponent_field_unit = opponent_field_unit_list[index]

                    if opponent_field_unit is None:
                        continue

                    remove_from_field = False

                    fixed_card_base = opponent_field_unit.get_fixed_card_base()
                    attached_shape_list = fixed_card_base.get_attached_shapes()

                    for attached_shape in attached_shape_list:
                        if isinstance(attached_shape, NonBackgroundNumberImage):
                            if attached_shape.get_circle_kinds() is CircleKinds.HP:
                                hp_number = attached_shape.get_number()
                                hp_number -= your_actor_damage

                                # opponent_field_hp_list = attack_animation_object.get_wide_attack_opponent_field_hp_list()
                                # hp_number = opponent_field_hp_list[index]
                                print(f"{Fore.RED}hp_number: {Fore.GREEN}{hp_number}{Style.RESET_ALL}")

                                # TODO: n 턴간 불사 특성을 검사해야하므로 사실 이것도 summary 방식으로 빼는 것이 맞으나 우선은 진행한다.
                                if hp_number <= 0:
                                    remove_from_field = True
                                    break

                                # print(f"hp_number: {hp_number}")
                                attached_shape.set_number(hp_number)

                                # attached_shape.set_image_data(
                                #     # TODO: 실제로 여기서 서버로부터 계산 받은 값을 적용해야함
                                #     self.pre_drawed_image_instance.get_pre_draw_number_image(hp_number))

                                attached_shape.set_image_data(
                                    self.pre_drawed_image_instance.get_pre_draw_unit_hp(hp_number))

                                if your_actor_extra_ability:
                                    self.opponent_field_unit_repository.apply_harmful_status(opponent_field_unit.get_index(), your_actor_extra_ability)

                    if remove_from_field:
                        # effect_animation = EffectAnimation()
                        # effect_animation.set_animation_name('death')
                        # effect_animation.set_total_window_size(self.width, self.height)
                        # effect_animation.change_local_translation(self.opponent_field_unit_repository.find_opponent_field_unit_by_index(
                        #     index).get_fixed_card_base().get_local_translation())
                        # effect_animation.draw_animation_panel()
                        # effect_animation_panel = effect_animation.get_animation_panel()
                        #
                        # animation_index = self.effect_animation_repository.save_effect_animation_at_dictionary_without_index_and_return_index(
                        #     effect_animation)
                        #
                        # self.effect_animation_repository.save_effect_animation_panel_at_dictionary_with_index(
                        #     animation_index, effect_animation_panel)

                        def remove_opponent_unit(_unit_index):
                            print(f"remove opponent unit : {_unit_index}")
                            card_id = self.opponent_field_unit_repository.get_opponent_card_id_by_index(_unit_index)
                            self.opponent_field_unit_repository.remove_current_field_unit_card(_unit_index)
                            self.opponent_tomb_repository.create_opponent_tomb_card(card_id)
                            self.opponent_field_unit_repository.replace_opponent_field_unit_card_position()
                            self.opponent_field_unit_repository.remove_harmful_status_by_index(_unit_index)

                        self.create_effect_animation_to_opponent_unit_and_play_animation_and_call_function_with_param(
                            'death', index, remove_opponent_unit, index)
                        # self.play_effect_animation_by_index_and_call_function_with_param(animation_index, remove_opponent_unit, index)

                def ready_to_operate_deploy_nether_blade_second_passive_skill_animation():
                    if len(self.effect_animation_repository.get_effect_animation_dictionary().keys()) == 0:
                        self.targeting_enemy_select_support_lightning_border_list.append(
                            self.opponent_main_character_panel)

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

                        self.targeting_enemy_select_support_lightning_border_list.append(
                            self.opponent_main_character_panel)

                        # ActionToApplyOpponent.NETHER_BLADE_SECOND_TARGETING_PASSIVE_SKILL
                        self.opponent_fixed_unit_card_inside_handler.set_action_to_apply_opponent(
                            ActionToApplyOpponent.NETHER_BLADE_SECOND_TARGETING_PASSIVE_SKILL)
                            # ActionToApplyOpponent.NETHER_BLADE_TURN_START_SECOND_TARGETING_PASSIVE_SKILL)

                        your_field_unit_id = 19
                        self.targeting_enemy_select_using_your_field_card_id = your_field_unit_id
                    else:
                        self.master.after(100, ready_to_operate_deploy_nether_blade_second_passive_skill_animation)

                ready_to_operate_deploy_nether_blade_second_passive_skill_animation()

                # def call_nether_blade_second_passive_skill_animation():
                #     if len(self.effect_animation_repository.get_effect_animation_dictionary().keys()) == 0:
                #         self.nether_blade_second_passive_skill_animation()
                #     else:
                #         self.master.after(100, call_nether_blade_second_passive_skill_animation)
                # 
                # call_nether_blade_second_passive_skill_animation()
        move_to_origin_location(1)

    def nether_blade_second_passive_skill_animation(self):
        self.is_playing_action_animation = True
        steps = 10
        attack_animation_object = AttackAnimation.getInstance()
        animation_actor = attack_animation_object.get_animation_actor()

        your_fixed_card_base = animation_actor.get_fixed_card_base()
        current_your_attacker_unit_vertices = your_fixed_card_base.get_vertices()
        current_your_attacker_unit_local_translation = your_fixed_card_base.get_local_translation()

        new_y_value = current_your_attacker_unit_local_translation[1] - 270
        new_x_value = attack_animation_object.get_total_width() / 2 - 52.5
        # your_attacker_unit_destination_local_translation = (current_your_attacker_unit_local_translation[0], new_y_value)
        your_attacker_unit_destination_local_translation = (new_x_value, new_y_value)

        attack_animation_object.set_your_attacker_unit_moving_x(
            your_attacker_unit_destination_local_translation[0] - current_your_attacker_unit_local_translation[0])

        step_x = (your_attacker_unit_destination_local_translation[0] - current_your_attacker_unit_local_translation[0]) / steps
        step_y = (your_attacker_unit_destination_local_translation[1] - current_your_attacker_unit_local_translation[1]) / steps
        step_y *= -1
        #
        # def nether_blade_second_passive_skill_timeout():
        #     self.unit_timer.stop_unit_timer()
        #     self.timer_repository.set_unit_timer(10)
        #     self.timer_repository.set_unit_timeout_function(nether_blade_second_passive_skill_timeout)
        #     self.return_to_initial_location()
        #     self.reset_every_selected_action()
        #
        #
        # self.timer_repository.set_unit_timeout_function(nether_blade_second_passive_skill_timeout)
        # self.timer_repository.set_unit_timer(10)
        # self.unit_timer.get_unit_timer()
        # self.unit_timer.start_unit_timer()

        def update_position(step_count):
            print(f"{Fore.RED}step_count: {Fore.GREEN}{step_count}{Style.RESET_ALL}")

            new_vertices = [
                (vx + step_x * step_count, vy + step_y * step_count) for vx, vy in current_your_attacker_unit_vertices
            ]
            your_fixed_card_base.update_vertices(new_vertices)

            # tool_card = self.selected_object.get_tool_card()
            # if tool_card is not None:
            #     new_tool_card_vertices = [
            #         (vx + new_x, vy + new_y) for vx, vy in tool_card.vertices
            #     ]
            #     tool_card.update_vertices(new_tool_card_vertices)

            for attached_shape in your_fixed_card_base.get_attached_shapes():
                new_attached_shape_vertices = [
                    (vx + step_x, vy + step_y) for vx, vy in attached_shape.vertices
                ]
                attached_shape.update_vertices(new_attached_shape_vertices)
                # print(f"{Fore.RED}new_attached_shape_vertices: {Fore.GREEN}{new_attached_shape_vertices}{Style.RESET_ALL}")

            if step_count < steps:
                self.master.after(20, update_position, step_count + 1)
            else:
                # self.start_nether_blade_first_passive_wide_area_motion_animation(attack_animation_object)
                self.start_nether_blade_second_passive_targeting_motion_animation()

                # #### 두 번째 패시브 단일기
                # second_passive_skill_type = self.card_info_repository.getCardPassiveSecondForCardNumber(19)
                # if second_passive_skill_type == 1:
                #     print("단일기")
                # 
                #     # TODO: 여기서 본체 공격 할 수 있어야 함
                #     self.targeting_enemy_select_support_lightning_border_list.append(self.opponent_main_character_panel)
                # 
                #     opponent_field_unit_object_list = self.opponent_field_unit_repository.get_current_field_unit_card_object_list()
                #     valid_opponent_field_units_object_list = [unit for unit in opponent_field_unit_object_list if unit is not None]
                #     print(f"실제 유효한 상대 필드 유닛 숫자: {len(valid_opponent_field_units_object_list)}")
                # 
                #     # if len(valid_opponent_field_units_object_list) == 0:
                #     #     return
                # 
                #     for opponent_field_unit_object in opponent_field_unit_object_list:
                #         if opponent_field_unit_object is None:
                #             continue
                # 
                #         fixed_opponent_card_base = opponent_field_unit_object.get_fixed_card_base()
                #         self.targeting_enemy_select_support_lightning_border_list.append(fixed_opponent_card_base)
                # 
                #     self.targeting_enemy_select_support_lightning_border_list.append(self.opponent_main_character_panel)
                # 
                #     self.opponent_fixed_unit_card_inside_handler.set_action_to_apply_opponent(
                #         ActionToApplyOpponent.NETHER_BLADE_SECOND_TARGETING_PASSIVE_SKILL)
                # 
                #     your_field_unit_id = 19
                #     self.targeting_enemy_select_using_your_field_card_id = your_field_unit_id

        update_position(1)
        self.timer_repository.set_check_nether_blade_second_passive_targeting_animation(True)

    def start_nether_blade_second_passive_targeting_motion_animation(self):
        steps = 50
        self.__music_player_repository.play_sound_effect_with_event_name('nether_passive_skill_2')

        is_attack_main_character = self.attack_animation_object.get_is_your_attack_main_character()
        opponent_field_unit = None
        # targeting_damage = self.attack_animation_object.get_animation_actor_damage()
        # opponent_main_character = self.attack_animation_object.get_opponent_main_character()
        if is_attack_main_character:
            is_attack_main_character = True
        else:
            opponent_field_unit = self.attack_animation_object.get_opponent_field_unit()

        def targeting_attack(step_count):
            # if step_count == 1:
            #     self.__music_player_repository.play_sound_effect_with_event_name('nether_passive_skill_2')
            vibration_factor = 10
            random_translation = (random.uniform(-vibration_factor, vibration_factor),
                                  random.uniform(-vibration_factor, vibration_factor))

            if is_attack_main_character is False:
                # print(f"{Fore.RED}필드 유닛 공격 -> is_attack_main_character(False): {Fore.GREEN}{is_attack_main_character}{Style.RESET_ALL}")
                fixed_card_base = opponent_field_unit.get_fixed_card_base()
                tool_card = opponent_field_unit.get_tool_card()
                attached_shape_list = fixed_card_base.get_attached_shapes()

                if step_count % 2 == 1:
                    new_fixed_card_base_vertices = [
                        (vx + random_translation[0], vy + random_translation[1]) for vx, vy in
                        fixed_card_base.get_vertices()
                    ]
                    fixed_card_base.update_vertices(new_fixed_card_base_vertices)

                    if tool_card is not None:
                        new_tool_card_vertices = [
                            (vx + random_translation[0], vy + random_translation[1]) for vx, vy in
                            tool_card.get_vertices()
                        ]
                        tool_card.update_vertices(new_tool_card_vertices)

                    for attached_shape in attached_shape_list:
                        # Apply random translation
                        new_attached_shape_vertices = [
                            (vx + random_translation[0], vy + random_translation[1]) for vx, vy in
                            attached_shape.get_vertices()
                        ]
                        attached_shape.update_vertices(new_attached_shape_vertices)

                else:
                    fixed_card_base.update_vertices(fixed_card_base.get_initial_vertices())
                    if tool_card is not None:
                        tool_card.update_vertices(tool_card.get_initial_vertices())
                    for attached_shape in attached_shape_list:
                        attached_shape.update_vertices(attached_shape.get_initial_vertices())

            else:
                # print(f"{Fore.RED}메인 캐릭터 공격 -> is_attack_main_character(True): {Fore.GREEN}{is_attack_main_character}{Style.RESET_ALL}")
                if step_count % 2 == 1:
                    for battle_field_background_shape in self.battle_field_background_shape_list:
                        battle_field_background_shape.global_translate((random_translation[0], random_translation[1]))

                else:
                    for battle_field_background_shape in self.battle_field_background_shape_list:
                        battle_field_background_shape.global_translate((0, 0))

            if step_count < steps:
                self.master.after(20, targeting_attack, step_count + 1)
            else:
                self.finish_nether_blade_second_passive_targeting_animation(self.attack_animation_object)
                # self.is_attack_motion_finished = True
                # attack_animation_object.set_is_finished(True)
                # attack_animation_object.set_need_post_process(True)

        # targeting_attack(1)
        self.create_effect_animation_to_full_screen_and_play_animation_and_call_function_with_param(
            'nether_blade_targeting_skill', targeting_attack, 1)
        self.timer_repository.set_check_nether_blade_second_passive_targeting_animation(False)


    def finish_nether_blade_second_passive_targeting_animation(self, attack_animation_object):
        animation_actor = attack_animation_object.get_animation_actor()
        your_fixed_card_base = animation_actor.get_fixed_card_base()
        your_actor_extra_ability = attack_animation_object.get_extra_ability()

        current_your_attacker_unit_vertices = your_fixed_card_base.get_vertices()
        current_your_attacker_unit_local_translation = your_fixed_card_base.get_local_translation()

        your_attacker_unit_moving_x = attack_animation_object.get_your_attacker_unit_moving_x()

        new_y_value = current_your_attacker_unit_local_translation[1] + 270
        your_attacker_unit_destination_local_translation = (0, new_y_value)

        steps = 15
        step_x = your_attacker_unit_moving_x / steps
        step_y = (your_attacker_unit_destination_local_translation[1] - current_your_attacker_unit_local_translation[1]) / steps
        # step_y *= -1

        is_attack_main_character = False
        opponent_field_unit = None
        # targeting_damage = self.attack_animation_object.get_animation_actor_damage()
        # self.attack_animation_object.set_is_your_attack_main_character(False)
        is_your_attack_main_character = self.attack_animation_object.get_is_your_attack_main_character()
        if is_your_attack_main_character is True:
            is_attack_main_character = True
        else:
            opponent_field_unit = self.attack_animation_object.get_opponent_field_unit()

        def move_to_origin_location(step_count):
            new_vertices = [
                (vx  - step_x * step_count, vy - step_y * step_count) for vx, vy in current_your_attacker_unit_vertices
            ]
            your_fixed_card_base.update_vertices(new_vertices)

            # tool_card = self.selected_object.get_tool_card()
            # if tool_card is not None:
            #     new_tool_card_vertices = [
            #         (vx + new_x, vy + new_y) for vx, vy in tool_card.vertices
            #     ]
            #     tool_card.update_vertices(new_tool_card_vertices)

            for attached_shape in your_fixed_card_base.get_attached_shapes():
                new_attached_shape_vertices = [
                    (vx - step_x, vy - step_y) for vx, vy in attached_shape.vertices
                ]
                attached_shape.update_vertices(new_attached_shape_vertices)
                # print(f"{Fore.RED}new_attached_shape_vertices: {Fore.GREEN}{new_attached_shape_vertices}{Style.RESET_ALL}")

            if step_count < steps:

                self.master.after(20, move_to_origin_location, step_count + 1)
            else:
                self.is_playing_action_animation = False
                process_second_passive_skill_response_data = self.attack_animation_object.get_response_data()

                if is_attack_main_character is False:
                    print(f"{Fore.RED}필드 유닛 공격 -> is_attack_main_character(False): {Fore.GREEN}{is_attack_main_character}{Style.RESET_ALL}")

                    # 상대방 필드의 유닛 체력 정보
                    opponent_unit_health_map = process_second_passive_skill_response_data["player_field_unit_health_point_map"]["Opponent"]["field_unit_health_point_map"]

                    # 상대방 필드의 유해한 효과 정보
                    opponent_harmful_effect_map = process_second_passive_skill_response_data["player_field_unit_harmful_effect_map"]["Opponent"]["field_unit_harmful_status_map"]

                    # 상대방 필드의 유닛 사망 인덱스
                    opponent_dead_unit_index_list = process_second_passive_skill_response_data["player_field_unit_death_map"]["Opponent"]["dead_field_unit_index_list"]

                    # 처리할 수 있는 패시브 스킬 인덱스 목록
                    passive_skill_index_list = process_second_passive_skill_response_data["index_list_of_passive_skill_to_handle"]

                    # fixed_card_base = opponent_field_unit.get_fixed_card_base()
                    # tool_card = opponent_field_unit.get_tool_card()
                    # attached_shape_list = fixed_card_base.get_attached_shapes()

                    for opponent_field_unit_index, remaining_health_point in opponent_unit_health_map.items():
                        opponent_field_unit = self.opponent_field_unit_repository.find_opponent_field_unit_by_index(
                            int(opponent_field_unit_index))
                        opponent_fixed_card_base = opponent_field_unit.get_fixed_card_base()
                        opponent_fixed_card_attached_shape_list = opponent_fixed_card_base.get_attached_shapes()

                        if remaining_health_point <= 0:
                            continue

                        for opponent_fixed_card_attached_shape in opponent_fixed_card_attached_shape_list:
                            if isinstance(opponent_fixed_card_attached_shape, NonBackgroundNumberImage):
                                if opponent_fixed_card_attached_shape.get_circle_kinds() is CircleKinds.HP:
                                    opponent_fixed_card_attached_shape.set_number(int(remaining_health_point))

                                    opponent_fixed_card_attached_shape.set_image_data(
                                        self.pre_drawed_image_instance.get_pre_draw_unit_hp(
                                            int(remaining_health_point)))

                    for opponent_field_unit_index, harmful_effect_info in opponent_harmful_effect_map.items():
                        harmful_effect_list = harmful_effect_info['harmful_status_list']
                        self.opponent_field_unit_repository.apply_harmful_status(int(opponent_field_unit_index),
                                                                                 harmful_effect_list)

                    # 죽은 유닛들 묘지에 배치 및 Replacing
                    for opponent_dead_unit_index in opponent_dead_unit_index_list:

                        def remove_field_unit(_opponent_field_dead_unit):
                            card_id = _opponent_field_dead_unit.get_card_number()
                            card_index = _opponent_field_dead_unit.get_index()

                            self.opponent_field_unit_repository.remove_current_field_unit_card(card_index)

                            self.opponent_field_unit_repository.remove_harmful_status_by_index(card_index)
                            self.opponent_tomb_repository.create_opponent_tomb_card(card_id)

                            self.opponent_field_unit_repository.replace_opponent_field_unit_card_position()

                        opponent_field_dead_unit = self.opponent_field_unit_repository.find_opponent_field_unit_by_index(int(opponent_dead_unit_index))

                        self.create_effect_animation_to_opponent_unit_and_play_animation_and_call_function_with_param(
                            'death', opponent_dead_unit_index, remove_field_unit, opponent_field_dead_unit
                        )

                    self.opponent_field_unit_repository.replace_opponent_field_unit_card_position()

                    # remove_from_field = False
                    # for attached_shape in attached_shape_list:
                    #     if isinstance(attached_shape, NonBackgroundNumberImage):
                    #         if attached_shape.get_circle_kinds() is CircleKinds.HP:
                    #             hp_number = attached_shape.get_number()
                    #             print(f"{Fore.RED}current hp_number: {Fore.GREEN}{hp_number}{Style.RESET_ALL}")
                    #
                    #             hp_number -= targeting_damage
                    #             print(f"{Fore.RED}hp_number: {Fore.GREEN}{hp_number}{Style.RESET_ALL}")
                    #
                    #
                    #             # TODO: n 턴간 불사 특성을 검사해야하므로 사실 이것도 summary 방식으로 빼는 것이 맞으나 우선은 진행한다.
                    #             if hp_number <= 0:
                    #                 remove_from_field = True
                    #                 break
                    #
                    #             attached_shape.set_number(hp_number)
                    #
                    #             # attached_shape.set_image_data(
                    #             #     # TODO: 실제로 여기서 서버로부터 계산 받은 값을 적용해야함
                    #             #     self.pre_drawed_image_instance.get_pre_draw_number_image(hp_number))
                    #
                    #             attached_shape.set_image_data(
                    #                 self.pre_drawed_image_instance.get_pre_draw_unit_hp(hp_number))
                    #
                    #             if your_actor_extra_ability:
                    #                 self.opponent_field_unit_repository.apply_harmful_status(opponent_field_unit.get_index(), your_actor_extra_ability)
                    #
                    # if remove_from_field:
                    #     def remove_field_unit(_opponent_field_unit):
                    #         card_id = _opponent_field_unit.get_card_number()
                    #         card_index = _opponent_field_unit.get_index()
                    #
                    #         self.opponent_field_unit_repository.remove_current_field_unit_card(card_index)
                    #
                    #         self.opponent_field_unit_repository.remove_harmful_status_by_index(card_index)
                    #         self.opponent_tomb_repository.create_opponent_tomb_card(card_id)
                    #
                    #         self.opponent_field_unit_repository.replace_opponent_field_unit_card_position()
                    #
                    #     self.create_effect_animation_to_opponent_unit_and_play_animation_and_call_function_with_param(
                    #         'death', opponent_field_unit.get_index(), remove_field_unit, opponent_field_unit
                    #     )

                else:
                    print(f"{Fore.RED}opponent 메인 캐릭터 공격 -> is_attack_main_character(True): {Fore.GREEN}{is_attack_main_character}{Style.RESET_ALL}")
                    remain_hp = process_second_passive_skill_response_data['player_main_character_health_point_map']['Opponent']
                    self.opponent_hp_repository.change_opponent_hp(remain_hp)

                    survival_info = process_second_passive_skill_response_data['player_main_character_survival_map']['Opponent']
                    if survival_info == 'Death':
                        self.timer.stop_timer()
                        self.battle_field_repository.win()


                # opponent_field_unit_list = self.opponent_field_unit_repository.get_current_field_unit_card_object_list()
                # opponent_field_unit_list_length = len(
                #     self.opponent_field_unit_repository.get_current_field_unit_card_object_list())
                #
                # your_actor_damage = attack_animation_object.get_animation_actor_damage()
                # your_actor_extra_ability = attack_animation_object.get_extra_ability()
                #
                # for index in range(
                #         opponent_field_unit_list_length - 1,
                #         -1,
                #         -1):
                #     opponent_field_unit = opponent_field_unit_list[index]
                #
                #     if opponent_field_unit is None:
                #         continue
                #
                #     remove_from_field = False
                #
                #     fixed_card_base = opponent_field_unit.get_fixed_card_base()
                #     attached_shape_list = fixed_card_base.get_attached_shapes()
                #
                #     # TODO: 가만 보면 이 부분이 은근히 많이 사용되고 있음 (중복 많이 발생함)
                #     for attached_shape in attached_shape_list:
                #         if isinstance(attached_shape, NonBackgroundNumberImage):
                #             if attached_shape.get_circle_kinds() is CircleKinds.HP:
                #                 hp_number = attached_shape.get_number()
                #                 hp_number -= your_actor_damage
                #
                #                 # opponent_field_hp_list = attack_animation_object.get_wide_attack_opponent_field_hp_list()
                #                 # hp_number = opponent_field_hp_list[index]
                #                 print(f"{Fore.RED}hp_number: {Fore.GREEN}{hp_number}{Style.RESET_ALL}")
                #
                #                 # TODO: n 턴간 불사 특성을 검사해야하므로 사실 이것도 summary 방식으로 빼는 것이 맞으나 우선은 진행한다.
                #                 if hp_number <= 0:
                #                     remove_from_field = True
                #                     break
                #
                #                 # print(f"hp_number: {hp_number}")
                #                 attached_shape.set_number(hp_number)
                #
                #                 # attached_shape.set_image_data(
                #                 #     # TODO: 실제로 여기서 서버로부터 계산 받은 값을 적용해야함
                #                 #     self.pre_drawed_image_instance.get_pre_draw_number_image(hp_number))
                #
                #                 attached_shape.set_image_data(
                #                     self.pre_drawed_image_instance.get_pre_draw_unit_hp(hp_number))
                #
                #                 if your_actor_extra_ability:
                #                     self.opponent_field_unit_repository.apply_harmful_status(opponent_field_unit.get_index(), your_actor_extra_ability)
                #
                #     if remove_from_field:
                #         card_id = opponent_field_unit.get_card_number()
                #
                #         self.opponent_field_unit_repository.remove_current_field_unit_card(index)
                #
                #         self.opponent_field_unit_repository.remove_harmful_status_by_index(index)
                #         self.opponent_tomb_repository.create_opponent_tomb_card(card_id)

                self.opponent_field_unit_repository.replace_opponent_field_unit_card_position()
                self.field_area_inside_handler.clear_field_area_action()
                self.opponent_fixed_unit_card_inside_handler.clear_opponent_field_area_action()

                self.opponent_fixed_unit_card_inside_handler.set_action_to_apply_opponent(ActionToApplyOpponent.Dummy)

        move_to_origin_location(1)
        self.timer_repository.set_check_nether_blade_second_passive_targeting_animation(False)

    def finish_nether_blade_second_passive_targeting_animation_timeout(self, attack_animation_object):
        animation_actor = attack_animation_object.get_animation_actor()
        your_fixed_card_base = animation_actor.get_fixed_card_base()
        your_actor_extra_ability = attack_animation_object.get_extra_ability()

        current_your_attacker_unit_vertices = your_fixed_card_base.get_vertices()
        current_your_attacker_unit_local_translation = your_fixed_card_base.get_local_translation()

        your_attacker_unit_moving_x = attack_animation_object.get_your_attacker_unit_moving_x()

        new_y_value = current_your_attacker_unit_local_translation[1] + 270
        your_attacker_unit_destination_local_translation = (0, new_y_value)

        steps = 15
        step_x = your_attacker_unit_moving_x / steps
        step_y = (your_attacker_unit_destination_local_translation[1] - current_your_attacker_unit_local_translation[1]) / steps
        # step_y *= -1

        is_attack_main_character = False
        opponent_field_unit = None
        # targeting_damage = self.attack_animation_object.get_animation_actor_damage()
        # self.attack_animation_object.set_is_your_attack_main_character(False)
        is_your_attack_main_character = self.attack_animation_object.get_is_your_attack_main_character()
        if is_your_attack_main_character is True:
            is_attack_main_character = True
        else:
            opponent_field_unit = self.attack_animation_object.get_opponent_field_unit()

        def move_to_origin_location(step_count):
            new_vertices = [
                (vx  - step_x * step_count, vy - step_y * step_count) for vx, vy in current_your_attacker_unit_vertices
            ]
            your_fixed_card_base.update_vertices(new_vertices)

            # tool_card = self.selected_object.get_tool_card()
            # if tool_card is not None:
            #     new_tool_card_vertices = [
            #         (vx + new_x, vy + new_y) for vx, vy in tool_card.vertices
            #     ]
            #     tool_card.update_vertices(new_tool_card_vertices)

            for attached_shape in your_fixed_card_base.get_attached_shapes():
                new_attached_shape_vertices = [
                    (vx - step_x, vy - step_y) for vx, vy in attached_shape.vertices
                ]
                attached_shape.update_vertices(new_attached_shape_vertices)
                # print(f"{Fore.RED}new_attached_shape_vertices: {Fore.GREEN}{new_attached_shape_vertices}{Style.RESET_ALL}")

            if step_count < steps:

                self.master.after(20, move_to_origin_location, step_count + 1)
            else:
                self.is_playing_action_animation = False
                process_second_passive_skill_response_data = self.attack_animation_object.get_response_data()

                # if is_attack_main_character is False:
                #     print(f"{Fore.RED}필드 유닛 공격 -> is_attack_main_character(False): {Fore.GREEN}{is_attack_main_character}{Style.RESET_ALL}")
                #
                #     # 상대방 필드의 유닛 체력 정보
                #     opponent_unit_health_map = process_second_passive_skill_response_data["player_field_unit_health_point_map"]["Opponent"]["field_unit_health_point_map"]
                #
                #     # 상대방 필드의 유해한 효과 정보
                #     opponent_harmful_effect_map = process_second_passive_skill_response_data["player_field_unit_harmful_effect_map"]["Opponent"]["field_unit_harmful_status_map"]
                #
                #     # 상대방 필드의 유닛 사망 인덱스
                #     opponent_dead_unit_index_list = process_second_passive_skill_response_data["player_field_unit_death_map"]["Opponent"]["dead_field_unit_index_list"]
                #
                #     # 처리할 수 있는 패시브 스킬 인덱스 목록
                #     passive_skill_index_list = process_second_passive_skill_response_data["index_list_of_passive_skill_to_handle"]
                #
                #     for opponent_field_unit_index, remaining_health_point in opponent_unit_health_map.items():
                #         opponent_field_unit = self.opponent_field_unit_repository.find_opponent_field_unit_by_index(
                #             int(opponent_field_unit_index))
                #         opponent_fixed_card_base = opponent_field_unit.get_fixed_card_base()
                #         opponent_fixed_card_attached_shape_list = opponent_fixed_card_base.get_attached_shapes()
                #
                #         if remaining_health_point <= 0:
                #             continue
                #
                #         for opponent_fixed_card_attached_shape in opponent_fixed_card_attached_shape_list:
                #             if isinstance(opponent_fixed_card_attached_shape, NonBackgroundNumberImage):
                #                 if opponent_fixed_card_attached_shape.get_circle_kinds() is CircleKinds.HP:
                #                     opponent_fixed_card_attached_shape.set_number(int(remaining_health_point))
                #
                #                     opponent_fixed_card_attached_shape.set_image_data(
                #                         self.pre_drawed_image_instance.get_pre_draw_unit_hp(
                #                             int(remaining_health_point)))
                #
                #     for opponent_field_unit_index, harmful_effect_info in opponent_harmful_effect_map.items():
                #         harmful_effect_list = harmful_effect_info['harmful_status_list']
                #         self.opponent_field_unit_repository.apply_harmful_status(int(opponent_field_unit_index),
                #                                                                  harmful_effect_list)
                #
                #     # 죽은 유닛들 묘지에 배치 및 Replacing
                #     for opponent_dead_unit_index in opponent_dead_unit_index_list:
                #
                #         def remove_field_unit(_opponent_field_dead_unit):
                #             card_id = _opponent_field_dead_unit.get_card_number()
                #             card_index = _opponent_field_dead_unit.get_index()
                #
                #             self.opponent_field_unit_repository.remove_current_field_unit_card(card_index)
                #
                #             self.opponent_field_unit_repository.remove_harmful_status_by_index(card_index)
                #             self.opponent_tomb_repository.create_opponent_tomb_card(card_id)
                #
                #             self.opponent_field_unit_repository.replace_opponent_field_unit_card_position()
                #
                #         opponent_field_dead_unit = self.opponent_field_unit_repository.find_opponent_field_unit_by_index(int(opponent_dead_unit_index))
                #
                #         self.create_effect_animation_to_opponent_unit_and_play_animation_and_call_function_with_param(
                #             'death', opponent_dead_unit_index, remove_field_unit, opponent_field_dead_unit
                #         )
                #
                #     self.opponent_field_unit_repository.replace_opponent_field_unit_card_position()
                #
                # else:
                #     print(f"{Fore.RED}opponent 메인 캐릭터 공격 -> is_attack_main_character(True): {Fore.GREEN}{is_attack_main_character}{Style.RESET_ALL}")
                #     remain_hp = process_second_passive_skill_response_data['player_main_character_health_point_map']['Opponent']
                #     self.opponent_hp_repository.change_opponent_hp(remain_hp)
                #
                #     survival_info = process_second_passive_skill_response_data['player_main_character_survival_map']['Opponent']
                #     if survival_info == 'Death':
                #         self.timer.stop_timer()
                #         self.battle_field_repository.win()
                #
                # self.opponent_field_unit_repository.replace_opponent_field_unit_card_position()
                # self.field_area_inside_handler.clear_field_area_action()
                # self.opponent_fixed_unit_card_inside_handler.clear_opponent_field_area_action()
                #
                # self.opponent_fixed_unit_card_inside_handler.set_action_to_apply_opponent(ActionToApplyOpponent.Dummy)

        move_to_origin_location(1)
        self.timer_repository.set_check_nether_blade_second_passive_targeting_animation(False)

    def nether_blade_turn_start_first_passive_skill_animation(self):
        print(f"{Fore.RED}nether_blade_turn_start_first_passive_skill_animation(){Style.RESET_ALL}")

        self.is_playing_action_animation = True
        steps = 10
        attack_animation_object = AttackAnimation.getInstance()
        animation_actor = attack_animation_object.get_animation_actor()

        your_fixed_card_base = animation_actor.get_fixed_card_base()
        current_your_attacker_unit_vertices = your_fixed_card_base.get_vertices()
        current_your_attacker_unit_local_translation = your_fixed_card_base.get_local_translation()

        new_y_value = current_your_attacker_unit_local_translation[1] - 270
        new_x_value = attack_animation_object.get_total_width() / 2 - 52.5
        # your_attacker_unit_destination_local_translation = (current_your_attacker_unit_local_translation[0], new_y_value)
        your_attacker_unit_destination_local_translation = (new_x_value, new_y_value)

        attack_animation_object.set_your_attacker_unit_moving_x(
            your_attacker_unit_destination_local_translation[0] - current_your_attacker_unit_local_translation[0])

        step_x = (your_attacker_unit_destination_local_translation[0] - current_your_attacker_unit_local_translation[0]) / steps
        step_y = (your_attacker_unit_destination_local_translation[1] - current_your_attacker_unit_local_translation[1]) / steps
        step_y *= -1

        def update_position(step_count):
            print(f"{Fore.RED}step_count: {Fore.GREEN}{step_count}{Style.RESET_ALL}")

            new_vertices = [
                (vx + step_x * step_count, vy + step_y * step_count) for vx, vy in current_your_attacker_unit_vertices
            ]
            your_fixed_card_base.update_vertices(new_vertices)

            # tool_card = self.selected_object.get_tool_card()
            # if tool_card is not None:
            #     new_tool_card_vertices = [
            #         (vx + new_x, vy + new_y) for vx, vy in tool_card.vertices
            #     ]
            #     tool_card.update_vertices(new_tool_card_vertices)

            for attached_shape in your_fixed_card_base.get_attached_shapes():
                new_attached_shape_vertices = [
                    (vx + step_x, vy + step_y) for vx, vy in attached_shape.vertices
                ]
                attached_shape.update_vertices(new_attached_shape_vertices)
                # print(f"{Fore.RED}new_attached_shape_vertices: {Fore.GREEN}{new_attached_shape_vertices}{Style.RESET_ALL}")

            if step_count < steps:
                self.master.after(20, update_position, step_count + 1)
                if step_count == 9:
                    self.__music_player_repository.play_sound_effect_with_event_name('nether_passive_skill_1')
            else:
                self.create_effect_animation_to_full_screen_and_play_animation_and_call_function_with_param(
                    'nether_blade_area_skill', self.start_nether_blade_turn_start_first_passive_wide_area_motion_animation,
                    attack_animation_object
                )
                # self.create_effect_animation_to_opponent_field_and_play_animation_and_call_function_with_param(
                #     'nether_blade_area_skill', self.start_nether_blade_turn_start_first_passive_wide_area_motion_animation,
                #     attack_animation_object
                # )
                # self.start_nether_blade_turn_start_first_passive_wide_area_motion_animation(attack_animation_object)

        update_position(1)

    def start_nether_blade_turn_start_first_passive_wide_area_motion_animation(self, attack_animation_object):
        print(f"{Fore.RED}start_nether_blade_turn_start_first_passive_wide_area_motion_animation(){Style.RESET_ALL}")

        steps = 50

        opponent_field_unit_list = self.opponent_field_unit_repository.get_current_field_unit_card_object_list()
        opponent_field_unit_list_length = len(
            self.opponent_field_unit_repository.get_current_field_unit_card_object_list())

        def wide_area_attack(step_count):
            for index in range(
                    opponent_field_unit_list_length - 1,
                    -1,
                    -1):
                opponent_field_unit = opponent_field_unit_list[index]

                if opponent_field_unit is None:
                    continue

                fixed_card_base = opponent_field_unit.get_fixed_card_base()
                tool_card = opponent_field_unit.get_tool_card()
                attached_shape_list = fixed_card_base.get_attached_shapes()

                if step_count % 2 == 1:
                    vibration_factor = 10
                    random_translation = (random.uniform(-vibration_factor, vibration_factor),
                                          random.uniform(-vibration_factor, vibration_factor))

                    new_fixed_card_base_vertices = [
                        (vx + random_translation[0], vy + random_translation[1]) for vx, vy in
                        fixed_card_base.get_vertices()
                    ]
                    fixed_card_base.update_vertices(new_fixed_card_base_vertices)

                    if tool_card is not None:
                        new_tool_card_vertices = [
                            (vx + random_translation[0], vy + random_translation[1]) for vx, vy in
                            tool_card.get_vertices()
                        ]
                        tool_card.update_vertices(new_tool_card_vertices)

                    for attached_shape in attached_shape_list:
                        # Apply random translation
                        new_attached_shape_vertices = [
                            (vx + random_translation[0], vy + random_translation[1]) for vx, vy in
                            attached_shape.get_vertices()
                        ]
                        attached_shape.update_vertices(new_attached_shape_vertices)

                else:
                    # Return to the original position
                    # fixed_card_base.update_vertices(fixed_card_base.get_vertices())
                    # if tool_card is not None:
                    #     tool_card.update_vertices(tool_card.get_vertices())
                    # for attached_shape in attached_shape_list:
                    #     attached_shape.update_vertices(attached_shape.get_vertices())

                    # self.opponent_field_unit_repository.replace_opponent_field_unit_card_position()

                    fixed_card_base.update_vertices(fixed_card_base.get_initial_vertices())
                    if tool_card is not None:
                        tool_card.update_vertices(tool_card.get_initial_vertices())
                    for attached_shape in attached_shape_list:
                        attached_shape.update_vertices(attached_shape.get_initial_vertices())

            if step_count < steps:
                self.master.after(20, wide_area_attack, step_count + 1)
            else:
                self.finish_nether_blade_turn_start_first_passive_wide_area_motion_animation(attack_animation_object)
                # pass
                # self.is_attack_motion_finished = True
                # attack_animation_object.set_is_finished(True)
                # attack_animation_object.set_need_post_process(True)

        wide_area_attack(1)

    def finish_nether_blade_turn_start_first_passive_wide_area_motion_animation(self, attack_animation_object):
        print(f"{Fore.RED}finish_nether_blade_turn_start_first_passive_wide_area_motion_animation(){Style.RESET_ALL}")
        animation_actor = attack_animation_object.get_animation_actor()
        your_fixed_card_base = animation_actor.get_fixed_card_base()
        tool_card = animation_actor.get_tool_card()
        attached_shape_list = your_fixed_card_base.get_attached_shapes()

        # your_fixed_card_base_initial_vertices = your_fixed_card_base.get_initial_vertices()
        # print(f"{Fore.RED}your_fixed_card_base_initial_vertices{Fore.GREEN} {your_fixed_card_base_initial_vertices}{Style.RESET_ALL}")

        current_your_attacker_unit_vertices = your_fixed_card_base.get_vertices()
        current_your_attacker_unit_local_translation = your_fixed_card_base.get_local_translation()

        your_attacker_unit_moving_x = attack_animation_object.get_your_attacker_unit_moving_x()

        new_y_value = current_your_attacker_unit_local_translation[1] + 270
        your_attacker_unit_destination_local_translation = (0, new_y_value)
        # print(f"{Fore.RED}your_attacker_unit_destination_local_translation{Fore.GREEN} {your_attacker_unit_destination_local_translation}{Style.RESET_ALL}")

        steps = 15
        step_x = your_attacker_unit_moving_x / steps
        step_y = (your_attacker_unit_destination_local_translation[1] - current_your_attacker_unit_local_translation[1]) / steps

        # step_y *= -1

        def move_to_origin_location(step_count):
            new_y = current_your_attacker_unit_local_translation[1] + step_y * step_count
            # print(f"{Fore.RED}step ->{Fore.GREEN}new_y: {new_y}{Style.RESET_ALL}")

            new_vertices = [
                (vx - step_x * step_count, vy - step_y * step_count) for vx, vy in current_your_attacker_unit_vertices
            ]
            your_fixed_card_base.update_vertices(new_vertices)
            # print(f"{Fore.RED}new_vertices{Fore.GREEN} {new_vertices}{Style.RESET_ALL}")

            # tool_card = self.selected_object.get_tool_card()
            # if tool_card is not None:
            #     new_tool_card_vertices = [
            #         (vx + new_x, vy + new_y) for vx, vy in tool_card.vertices
            #     ]
            #     tool_card.update_vertices(new_tool_card_vertices)

            for attached_shape in your_fixed_card_base.get_attached_shapes():
                new_attached_shape_vertices = [
                    (vx - step_x, vy - step_y) for vx, vy in attached_shape.vertices
                ]
                attached_shape.update_vertices(new_attached_shape_vertices)
                # print(f"{Fore.RED}new_attached_shape_vertices: {Fore.GREEN}{new_attached_shape_vertices}{Style.RESET_ALL}")

            if step_count < steps:

                self.master.after(20, move_to_origin_location, step_count + 1)
            else:
                self.is_playing_action_animation = False
                # opponent_field_unit_list = self.opponent_field_unit_repository.get_current_field_unit_card_object_list()
                # opponent_field_unit_list_length = len(
                #     self.opponent_field_unit_repository.get_current_field_unit_card_object_list())
                #
                # your_actor_damage = attack_animation_object.get_animation_actor_damage()
                # your_actor_extra_ability = attack_animation_object.get_extra_ability()

                turn_start_first_passive_skill_response = self.attack_animation_object.get_response_data()

                # 1. 상대방(Opponent)의 unit_index와 체력 정보를 추출
                opponent_health_info = turn_start_first_passive_skill_response['player_field_unit_health_point_map']['Opponent']['field_unit_health_point_map']

                # 2. 상대방(Opponent)의 unit_index와 유해 상태 정보를 추출
                opponent_harmful_status_info = turn_start_first_passive_skill_response['player_field_unit_harmful_effect_map']['Opponent']['field_unit_harmful_status_map']

                # 3. 상대방(Opponent)의 사망 유닛의 인덱스 리스트를 추출
                opponent_dead_unit_index_list = turn_start_first_passive_skill_response['player_field_unit_death_map']['Opponent']['dead_field_unit_index_list']

                # 4. 처리해야 할 스킬의 인덱스 리스트를 추출
                passive_skill_index_list = turn_start_first_passive_skill_response['index_list_of_passive_skill_to_handle']

                for opponent_field_unit_index, remaining_health_point in opponent_health_info.items():
                    opponent_field_unit = self.opponent_field_unit_repository.find_opponent_field_unit_by_index(int(opponent_field_unit_index))
                    opponent_fixed_card_base = opponent_field_unit.get_fixed_card_base()
                    opponent_fixed_card_attached_shape_list = opponent_fixed_card_base.get_attached_shapes()

                    if remaining_health_point <= 0:
                        continue

                    for opponent_fixed_card_attached_shape in opponent_fixed_card_attached_shape_list:
                        if isinstance(opponent_fixed_card_attached_shape, NonBackgroundNumberImage):
                            if opponent_fixed_card_attached_shape.get_circle_kinds() is CircleKinds.HP:
                                opponent_fixed_card_attached_shape.set_number(int(remaining_health_point))

                                opponent_fixed_card_attached_shape.set_image_data(
                                    self.pre_drawed_image_instance.get_pre_draw_unit_hp(int(remaining_health_point)))

                for opponent_field_unit_index, harmful_effect_info in opponent_harmful_status_info.items():
                    harmful_effect_list = harmful_effect_info['harmful_status_list']
                    self.opponent_field_unit_repository.apply_harmful_status(int(opponent_field_unit_index), harmful_effect_list)

                # 죽은 유닛들 묘지에 배치 및 Replacing
                for opponent_dead_unit_index in opponent_dead_unit_index_list:
                    effect_animation = EffectAnimation()
                    effect_animation.set_animation_name('death')
                    effect_animation.set_total_window_size(self.width, self.height)
                    effect_animation.change_local_translation(
                        self.opponent_field_unit_repository.find_opponent_field_unit_by_index(
                            opponent_dead_unit_index).get_fixed_card_base().get_local_translation())
                    effect_animation.draw_animation_panel()
                    effect_animation_panel = effect_animation.get_animation_panel()

                    animation_index = self.effect_animation_repository.save_effect_animation_at_dictionary_without_index_and_return_index(effect_animation)

                    self.effect_animation_repository.save_effect_animation_panel_at_dictionary_with_index(animation_index, effect_animation_panel)

                    def remove_opponent_unit(_opponent_dead_unit_index):
                        opponent_dead_card_id = self.opponent_field_unit_repository.get_opponent_card_id_by_index(_opponent_dead_unit_index)
                        self.opponent_field_unit_repository.remove_current_field_unit_card(_opponent_dead_unit_index)
                        self.opponent_tomb_repository.create_opponent_tomb_card(opponent_dead_card_id)
                        self.opponent_field_unit_repository.remove_harmful_status_by_index(_opponent_dead_unit_index)
                        self.opponent_field_unit_repository.replace_opponent_field_unit_card_position()

                    self.play_effect_animation_by_index_and_call_function_with_param(animation_index, remove_opponent_unit, opponent_dead_unit_index)

                    self.opponent_field_unit_repository.replace_opponent_field_unit_card_position()

                    # opponent_field_dead_unit = self.opponent_field_unit_repository.find_opponent_field_unit_by_index(
                    #     int(opponent_dead_unit_index))
                    # self.create_effect_animation_to_opponent_unit_and_play_animation_and_call_function_with_param(
                    #     'death', opponent_dead_unit_index, remove_opponent_unit, opponent_dead_unit_index
                    # )

                    # def remove_opponent_unit(_unit_index):
                    #     print(f"remove opponent unit : {_unit_index}")
                    #     card_id = self.opponent_field_unit_repository.get_opponent_card_id_by_index(_unit_index)
                    #     self.opponent_field_unit_repository.remove_current_field_unit_card(_unit_index)
                    #     self.opponent_tomb_repository.create_opponent_tomb_card(card_id)
                    #     self.opponent_field_unit_repository.replace_opponent_field_unit_card_position()
                    #     self.opponent_field_unit_repository.remove_harmful_status_by_index(_unit_index)
                    #
                    # self.create_effect_animation_to_opponent_unit_and_play_animation_and_call_function_with_param(
                    #     'death', index, remove_opponent_unit, index)

                # self.opponent_field_unit_repository.replace_opponent_field_unit_card_position()

                # for index in range(
                #         opponent_field_unit_list_length - 1,
                #         -1,
                #         -1):
                #     opponent_field_unit = opponent_field_unit_list[index]
                #
                #     if opponent_field_unit is None:
                #         continue
                #
                #     remove_from_field = False
                #
                #     fixed_card_base = opponent_field_unit.get_fixed_card_base()
                #     attached_shape_list = fixed_card_base.get_attached_shapes()
                #
                #     for attached_shape in attached_shape_list:
                #         if isinstance(attached_shape, NonBackgroundNumberImage):
                #             if attached_shape.get_circle_kinds() is CircleKinds.HP:
                #                 hp_number = attached_shape.get_number()
                #                 hp_number -= your_actor_damage
                #
                #                 # opponent_field_hp_list = attack_animation_object.get_wide_attack_opponent_field_hp_list()
                #                 # hp_number = opponent_field_hp_list[index]
                #                 print(f"{Fore.RED}hp_number: {Fore.GREEN}{hp_number}{Style.RESET_ALL}")
                #
                #                 # TODO: n 턴간 불사 특성을 검사해야하므로 사실 이것도 summary 방식으로 빼는 것이 맞으나 우선은 진행한다.
                #                 if hp_number <= 0:
                #                     remove_from_field = True
                #                     break
                #
                #                 # print(f"hp_number: {hp_number}")
                #                 attached_shape.set_number(hp_number)
                #
                #                 # attached_shape.set_image_data(
                #                 #     # TODO: 실제로 여기서 서버로부터 계산 받은 값을 적용해야함
                #                 #     self.pre_drawed_image_instance.get_pre_draw_number_image(hp_number))
                #
                #                 attached_shape.set_image_data(
                #                     self.pre_drawed_image_instance.get_pre_draw_unit_hp(hp_number))
                #
                #                 if your_actor_extra_ability:
                #                     self.opponent_field_unit_repository.apply_harmful_status(
                #                         opponent_field_unit.get_index(), your_actor_extra_ability)
                #
                #     if remove_from_field:
                #         card_id = opponent_field_unit.get_card_number()
                #
                #         effect_animation = EffectAnimation()
                #         effect_animation.set_animation_name('death')
                #         effect_animation.set_total_window_size(self.width, self.height)
                #         effect_animation.change_local_translation(
                #             self.opponent_field_unit_repository.find_opponent_field_unit_by_index(
                #                 index).get_fixed_card_base().get_local_translation())
                #         effect_animation.draw_animation_panel()
                #         effect_animation_panel = effect_animation.get_animation_panel()
                #
                #         animation_index = self.effect_animation_repository.save_effect_animation_at_dictionary_without_index_and_return_index(
                #             effect_animation)
                #
                #         self.effect_animation_repository.save_effect_animation_panel_at_dictionary_with_index(
                #             animation_index, effect_animation_panel)
                #
                #         def remove_opponent_unit(unit_index):
                #             unit_card_id = self.opponent_field_unit_repository.get_opponent_card_id_by_index(unit_index)
                #             self.opponent_field_unit_repository.remove_current_field_unit_card(unit_index)
                #             self.opponent_tomb_repository.create_opponent_tomb_card(unit_card_id)
                #             self.opponent_field_unit_repository.replace_opponent_field_unit_card_position()
                #             self.opponent_field_unit_repository.remove_harmful_status_by_index(unit_index)
                #
                #         self.play_effect_animation_by_index_and_call_function_with_param(animation_index, remove_opponent_unit, index)

                # def call_nether_blade_second_passive_skill_animation():
                #     print(f"{Fore.RED}call_nether_blade_second_passive_skill_animation(){Style.RESET_ALL}")
                # 
                #     print(f"effect animation repository dictionary key: {self.effect_animation_repository.get_effect_animation_dictionary().keys()}")
                # 
                #     if len(self.effect_animation_repository.get_effect_animation_dictionary().keys()) == 0:
                #         self.nether_blade_turn_start_second_passive_skill_animation()
                #     else:
                #         self.master.after(100, call_nether_blade_second_passive_skill_animation)

                # call_nether_blade_second_passive_skill_animation()

                def ready_to_operate_nether_blade_second_passive_skill_animation():
                    if len(self.effect_animation_repository.get_effect_animation_dictionary().keys()) == 0:
                        self.targeting_enemy_select_support_lightning_border_list.append(
                            self.opponent_main_character_panel)

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

                        self.targeting_enemy_select_support_lightning_border_list.append(
                            self.opponent_main_character_panel)

                        self.opponent_fixed_unit_card_inside_handler.set_action_to_apply_opponent(
                            ActionToApplyOpponent.NETHER_BLADE_TURN_START_SECOND_TARGETING_PASSIVE_SKILL)

                        your_field_unit_id = 19
                        self.targeting_enemy_select_using_your_field_card_id = your_field_unit_id
                    else:
                        self.master.after(100, ready_to_operate_nether_blade_second_passive_skill_animation)

                ready_to_operate_nether_blade_second_passive_skill_animation()

                # start_nether_blade_turn_start_second_passive_targeting_motion_animation
                # self.targeting_enemy_select_support_lightning_border_list.append(self.opponent_main_character_panel)
                #
                #                     opponent_field_unit_object_list = self.opponent_field_unit_repository.get_current_field_unit_card_object_list()
                #                     valid_opponent_field_units_object_list = [unit for unit in opponent_field_unit_object_list if unit is not None]
                #                     print(f"실제 유효한 상대 필드 유닛 숫자: {len(valid_opponent_field_units_object_list)}")
                #
                #                     # if len(valid_opponent_field_units_object_list) == 0:
                #                     #     return
                #
                #                     for opponent_field_unit_object in opponent_field_unit_object_list:
                #                         if opponent_field_unit_object is None:
                #                             continue
                #
                #                         fixed_opponent_card_base = opponent_field_unit_object.get_fixed_card_base()
                #                         self.targeting_enemy_select_support_lightning_border_list.append(fixed_opponent_card_base)
                #
                #                     self.targeting_enemy_select_support_lightning_border_list.append(self.opponent_main_character_panel)
                #
                #                     self.opponent_fixed_unit_card_inside_handler.set_action_to_apply_opponent(
                #                         ActionToApplyOpponent.NETHER_BLADE_TURN_START_SECOND_TARGETING_PASSIVE_SKILL)
                #
                #                     your_field_unit_id = 19
                #                     self.targeting_enemy_select_using_your_field_card_id = your_field_unit_id

        move_to_origin_location(1)

    def nether_blade_turn_start_second_passive_skill_animation(self):
        print(f"{Fore.RED}nether_blade_turn_start_second_passive_skill_animation(){Style.RESET_ALL}")
        self.is_playing_action_animation = True
        steps = 10
        attack_animation_object = AttackAnimation.getInstance()
        animation_actor = attack_animation_object.get_animation_actor()

        your_fixed_card_base = animation_actor.get_fixed_card_base()
        current_your_attacker_unit_vertices = your_fixed_card_base.get_vertices()
        current_your_attacker_unit_local_translation = your_fixed_card_base.get_local_translation()

        new_y_value = current_your_attacker_unit_local_translation[1] - 270
        new_x_value = attack_animation_object.get_total_width() / 2 - 52.5
        # your_attacker_unit_destination_local_translation = (current_your_attacker_unit_local_translation[0], new_y_value)
        your_attacker_unit_destination_local_translation = (new_x_value, new_y_value)

        attack_animation_object.set_your_attacker_unit_moving_x(
            your_attacker_unit_destination_local_translation[0] - current_your_attacker_unit_local_translation[0])

        step_x = (your_attacker_unit_destination_local_translation[0] - current_your_attacker_unit_local_translation[0]) / steps
        step_y = (your_attacker_unit_destination_local_translation[1] - current_your_attacker_unit_local_translation[1]) / steps
        step_y *= -1

        # self.timer_repository.set_unit_timer(10)
        # self.timer_repository.set_unit_timeout_function(self.nether_blade_second_passive_skill_timeout)
        # self.unit_timer.get_unit_timer()
        # self.unit_timer.start_unit_timer()

        def update_position(step_count):
            print(f"{Fore.RED}step_count: {Fore.GREEN}{step_count}{Style.RESET_ALL}")

            new_vertices = [
                (vx + step_x * step_count, vy + step_y * step_count) for vx, vy in current_your_attacker_unit_vertices
            ]
            your_fixed_card_base.update_vertices(new_vertices)

            # tool_card = self.selected_object.get_tool_card()
            # if tool_card is not None:
            #     new_tool_card_vertices = [
            #         (vx + new_x, vy + new_y) for vx, vy in tool_card.vertices
            #     ]
            #     tool_card.update_vertices(new_tool_card_vertices)

            for attached_shape in your_fixed_card_base.get_attached_shapes():
                new_attached_shape_vertices = [
                    (vx + step_x, vy + step_y) for vx, vy in attached_shape.vertices
                ]
                attached_shape.update_vertices(new_attached_shape_vertices)
                # print(f"{Fore.RED}new_attached_shape_vertices: {Fore.GREEN}{new_attached_shape_vertices}{Style.RESET_ALL}")

            # skill_focus_background_panel_alpha = self.skill_focus_background_panel.color[3]
            # skill_focus_background_panel_alpha += 0.013 * step_count
            # 
            # self.skill_focus_background_panel.color = (
            #     self.skill_focus_background_panel.color[0],
            #     self.skill_focus_background_panel.color[1],
            #     self.skill_focus_background_panel.color[2],
            #     skill_focus_background_panel_alpha
            # )
            # self.skill_focus_background_panel.draw()

            if step_count < steps:
                self.master.after(20, update_position, step_count + 1)
            else:
                self.start_nether_blade_turn_start_second_passive_targeting_motion_animation()
                # # self.start_nether_blade_first_passive_wide_area_motion_animation(attack_animation_object)
                #
                # #### 두 번째 패시브 단일기
                # second_passive_skill_type = self.card_info_repository.getCardPassiveSecondForCardNumber(19)
                # if second_passive_skill_type == 1:
                #     print("단일기")
                #
                #     # TODO: 여기서 본체 공격 할 수 있어야 함
                #     self.targeting_enemy_select_support_lightning_border_list.append(self.opponent_main_character_panel)
                #
                #     opponent_field_unit_object_list = self.opponent_field_unit_repository.get_current_field_unit_card_object_list()
                #     valid_opponent_field_units_object_list = [unit for unit in opponent_field_unit_object_list if unit is not None]
                #     print(f"실제 유효한 상대 필드 유닛 숫자: {len(valid_opponent_field_units_object_list)}")
                #
                #     # if len(valid_opponent_field_units_object_list) == 0:
                #     #     return
                #
                #     for opponent_field_unit_object in opponent_field_unit_object_list:
                #         if opponent_field_unit_object is None:
                #             continue
                #
                #         fixed_opponent_card_base = opponent_field_unit_object.get_fixed_card_base()
                #         self.targeting_enemy_select_support_lightning_border_list.append(fixed_opponent_card_base)
                #
                #     self.targeting_enemy_select_support_lightning_border_list.append(self.opponent_main_character_panel)
                #
                #     self.opponent_fixed_unit_card_inside_handler.set_action_to_apply_opponent(
                #         ActionToApplyOpponent.NETHER_BLADE_TURN_START_SECOND_TARGETING_PASSIVE_SKILL)
                #
                #     your_field_unit_id = 19
                #     self.targeting_enemy_select_using_your_field_card_id = your_field_unit_id

        update_position(1)
        self.timer_repository.set_check_nether_blade_turn_start_second_passive_targeting_animation(True)

    def start_nether_blade_turn_start_second_passive_targeting_motion_animation(self):
        steps = 50
        self.__music_player_repository.play_sound_effect_with_event_name('nether_passive_skill_2')

        is_attack_main_character = False
        opponent_field_unit = None
        # targeting_damage = self.attack_animation_object.get_animation_actor_damage()
        opponent_main_character = self.attack_animation_object.get_opponent_main_character()
        if opponent_main_character is not None:
            is_attack_main_character = True
        else:
            opponent_field_unit = self.attack_animation_object.get_opponent_field_unit()

        def targeting_attack(step_count):
            # if step_count == 1:
            #     self.__music_player_repository.play_sound_effect_with_event_name('nether_passive_skill_2')
            vibration_factor = 10
            random_translation = (random.uniform(-vibration_factor, vibration_factor),
                                  random.uniform(-vibration_factor, vibration_factor))

            if is_attack_main_character is False:
                # print(f"{Fore.RED}필드 유닛 공격 -> is_attack_main_character(False): {Fore.GREEN}{is_attack_main_character}{Style.RESET_ALL}")
                fixed_card_base = opponent_field_unit.get_fixed_card_base()
                tool_card = opponent_field_unit.get_tool_card()
                attached_shape_list = fixed_card_base.get_attached_shapes()

                if step_count % 2 == 1:
                    new_fixed_card_base_vertices = [
                        (vx + random_translation[0], vy + random_translation[1]) for vx, vy in
                        fixed_card_base.get_vertices()
                    ]
                    fixed_card_base.update_vertices(new_fixed_card_base_vertices)

                    if tool_card is not None:
                        new_tool_card_vertices = [
                            (vx + random_translation[0], vy + random_translation[1]) for vx, vy in
                            tool_card.get_vertices()
                        ]
                        tool_card.update_vertices(new_tool_card_vertices)

                    for attached_shape in attached_shape_list:
                        # Apply random translation
                        new_attached_shape_vertices = [
                            (vx + random_translation[0], vy + random_translation[1]) for vx, vy in
                            attached_shape.get_vertices()
                        ]
                        attached_shape.update_vertices(new_attached_shape_vertices)

                else:
                    fixed_card_base.update_vertices(fixed_card_base.get_initial_vertices())
                    if tool_card is not None:
                        tool_card.update_vertices(tool_card.get_initial_vertices())
                    for attached_shape in attached_shape_list:
                        attached_shape.update_vertices(attached_shape.get_initial_vertices())

            else:
                # print(f"{Fore.RED}메인 캐릭터 공격 -> is_attack_main_character(True): {Fore.GREEN}{is_attack_main_character}{Style.RESET_ALL}")
                if step_count % 2 == 1:
                    for battle_field_background_shape in self.battle_field_background_shape_list:
                        battle_field_background_shape.global_translate((random_translation[0], random_translation[1]))

                else:
                    for battle_field_background_shape in self.battle_field_background_shape_list:
                        battle_field_background_shape.global_translate((0, 0))

            if step_count < steps:
                self.master.after(20, targeting_attack, step_count + 1)
            else:
                self.finish_nether_blade_turn_start_second_passive_targeting_animation(self.attack_animation_object)
                # self.is_attack_motion_finished = True
                # attack_animation_object.set_is_finished(True)
                # attack_animation_object.set_need_post_process(True)

        # targeting_attack(1)
        self.create_effect_animation_to_full_screen_and_play_animation_and_call_function_with_param(
            'nether_blade_targeting_skill', targeting_attack, 1)
        self.timer_repository.set_check_nether_blade_turn_start_second_passive_targeting_animation(False)            


    def finish_nether_blade_turn_start_second_passive_targeting_animation(self, attack_animation_object):
        animation_actor = attack_animation_object.get_animation_actor()
        your_fixed_card_base = animation_actor.get_fixed_card_base()
        your_actor_extra_ability = attack_animation_object.get_extra_ability()

        current_your_attacker_unit_vertices = your_fixed_card_base.get_vertices()
        current_your_attacker_unit_local_translation = your_fixed_card_base.get_local_translation()

        your_attacker_unit_moving_x = attack_animation_object.get_your_attacker_unit_moving_x()

        new_y_value = current_your_attacker_unit_local_translation[1] + 270
        your_attacker_unit_destination_local_translation = (0, new_y_value)

        steps = 15
        step_x = your_attacker_unit_moving_x / steps
        step_y = (your_attacker_unit_destination_local_translation[1] - current_your_attacker_unit_local_translation[1]) / steps
        # step_y *= -1

        is_attack_main_character = False
        opponent_field_unit = None
        # targeting_damage = self.attack_animation_object.get_animation_actor_damage()
        opponent_main_character = self.attack_animation_object.get_opponent_main_character()
        if opponent_main_character is not None:
            is_attack_main_character = True
        else:
            opponent_field_unit = self.attack_animation_object.get_opponent_field_unit()

        def move_to_origin_location(step_count):
            new_vertices = [
                (vx - step_x * step_count, vy - step_y * step_count) for vx, vy in current_your_attacker_unit_vertices
            ]
            your_fixed_card_base.update_vertices(new_vertices)

            # tool_card = self.selected_object.get_tool_card()
            # if tool_card is not None:
            #     new_tool_card_vertices = [
            #         (vx + new_x, vy + new_y) for vx, vy in tool_card.vertices
            #     ]
            #     tool_card.update_vertices(new_tool_card_vertices)

            for attached_shape in your_fixed_card_base.get_attached_shapes():
                new_attached_shape_vertices = [
                    (vx - step_x, vy - step_y) for vx, vy in attached_shape.vertices
                ]
                attached_shape.update_vertices(new_attached_shape_vertices)
                # print(f"{Fore.RED}new_attached_shape_vertices: {Fore.GREEN}{new_attached_shape_vertices}{Style.RESET_ALL}")

            # 112.5 * a = 0.65
            skill_focus_background_panel_alpha = self.skill_focus_background_panel.color[3]
            skill_focus_background_panel_alpha -= 0.005777 * step_count

            self.skill_focus_background_panel.color = (
                self.skill_focus_background_panel.color[0],
                self.skill_focus_background_panel.color[1],
                self.skill_focus_background_panel.color[2],
                skill_focus_background_panel_alpha
            )
            self.skill_focus_background_panel.draw()

            if step_count < steps:

                self.master.after(20, move_to_origin_location, step_count + 1)
            else:
                self.skill_focus_background_panel.color = (
                    self.skill_focus_background_panel.color[0],
                    self.skill_focus_background_panel.color[1],
                    self.skill_focus_background_panel.color[2],
                    0
                )
                self.skill_focus_background_panel.draw()

                self.is_playing_action_animation = False
                targeting_damage = 20
                if is_attack_main_character is False:
                    print(f"{Fore.RED}필드 유닛 공격 -> is_attack_main_character(False): {Fore.GREEN}{is_attack_main_character}{Style.RESET_ALL}")

                    fixed_card_base = opponent_field_unit.get_fixed_card_base()
                    tool_card = opponent_field_unit.get_tool_card()
                    attached_shape_list = fixed_card_base.get_attached_shapes()

                    remove_from_field = False
                    for attached_shape in attached_shape_list:
                        if isinstance(attached_shape, NonBackgroundNumberImage):
                            if attached_shape.get_circle_kinds() is CircleKinds.HP:
                                hp_number = attached_shape.get_number()
                                print(f"{Fore.RED}current hp_number: {Fore.GREEN}{hp_number}{Style.RESET_ALL}")

                                hp_number -= targeting_damage
                                print(f"{Fore.RED}hp_number: {Fore.GREEN}{hp_number}{Style.RESET_ALL}")

                                # TODO: n 턴간 불사 특성을 검사해야하므로 사실 이것도 summary 방식으로 빼는 것이 맞으나 우선은 진행한다.
                                if hp_number <= 0:
                                    remove_from_field = True
                                    break

                                attached_shape.set_number(hp_number)

                                # attached_shape.set_image_data(
                                #     # TODO: 실제로 여기서 서버로부터 계산 받은 값을 적용해야함
                                #     self.pre_drawed_image_instance.get_pre_draw_number_image(hp_number))

                                attached_shape.set_image_data(
                                    self.pre_drawed_image_instance.get_pre_draw_unit_hp(hp_number))

                                if your_actor_extra_ability:
                                    self.opponent_field_unit_repository.apply_harmful_status(
                                        opponent_field_unit.get_index(), your_actor_extra_ability)

                    if remove_from_field:
                        def remove_field_unit(_opponent_field_unit):

                            card_id = _opponent_field_unit.get_card_number()
                            card_index = _opponent_field_unit.get_index()
                            print('remove field unit',card_index)

                            self.opponent_field_unit_repository.remove_current_field_unit_card(card_index)

                            self.opponent_field_unit_repository.remove_harmful_status_by_index(card_index)
                            self.opponent_tomb_repository.create_opponent_tomb_card(card_id)
                            self.opponent_field_unit_repository.replace_opponent_field_unit_card_position()
                            print(self.opponent_field_unit_repository.get_current_field_unit_card_object_list())

                        self.create_effect_animation_to_opponent_unit_and_play_animation_and_call_function_with_param(
                            'death', opponent_field_unit.get_index(), remove_field_unit, opponent_field_unit
                        )

                else:
                    print(
                        f"{Fore.RED}opponent 메인 캐릭터 공격 -> is_attack_main_character(True): {Fore.GREEN}{is_attack_main_character}{Style.RESET_ALL}")

                    self.opponent_hp_repository.take_damage(targeting_damage)

                # opponent_field_unit_list = self.opponent_field_unit_repository.get_current_field_unit_card_object_list()
                # opponent_field_unit_list_length = len(
                #     self.opponent_field_unit_repository.get_current_field_unit_card_object_list())
                #
                # your_actor_damage = attack_animation_object.get_animation_actor_damage()
                # your_actor_extra_ability = attack_animation_object.get_extra_ability()
                #
                # for index in range(
                #         opponent_field_unit_list_length - 1,
                #         -1,
                #         -1):
                #     opponent_field_unit = opponent_field_unit_list[index]
                #
                #     if opponent_field_unit is None:
                #         continue
                #
                #     remove_from_field = False
                #
                #     fixed_card_base = opponent_field_unit.get_fixed_card_base()
                #     attached_shape_list = fixed_card_base.get_attached_shapes()
                #
                #     # TODO: 가만 보면 이 부분이 은근히 많이 사용되고 있음 (중복 많이 발생함)
                #     for attached_shape in attached_shape_list:
                #         if isinstance(attached_shape, NonBackgroundNumberImage):
                #             if attached_shape.get_circle_kinds() is CircleKinds.HP:
                #                 hp_number = attached_shape.get_number()
                #                 hp_number -= your_actor_damage
                #
                #                 # opponent_field_hp_list = attack_animation_object.get_wide_attack_opponent_field_hp_list()
                #                 # hp_number = opponent_field_hp_list[index]
                #                 print(f"{Fore.RED}hp_number: {Fore.GREEN}{hp_number}{Style.RESET_ALL}")
                #
                #                 # TODO: n 턴간 불사 특성을 검사해야하므로 사실 이것도 summary 방식으로 빼는 것이 맞으나 우선은 진행한다.
                #                 if hp_number <= 0:
                #                     remove_from_field = True
                #                     break
                #
                #                 # print(f"hp_number: {hp_number}")
                #                 attached_shape.set_number(hp_number)
                #
                #                 # attached_shape.set_image_data(
                #                 #     # TODO: 실제로 여기서 서버로부터 계산 받은 값을 적용해야함
                #                 #     self.pre_drawed_image_instance.get_pre_draw_number_image(hp_number))
                #
                #                 attached_shape.set_image_data(
                #                     self.pre_drawed_image_instance.get_pre_draw_unit_hp(hp_number))
                #
                #                 if your_actor_extra_ability:
                #                     self.opponent_field_unit_repository.apply_harmful_status(opponent_field_unit.get_index(), your_actor_extra_ability)
                #
                #     if remove_from_field:
                #         card_id = opponent_field_unit.get_card_number()
                #
                #         self.opponent_field_unit_repository.remove_current_field_unit_card(index)
                #
                #         self.opponent_field_unit_repository.remove_harmful_status_by_index(index)
                #         self.opponent_tomb_repository.create_opponent_tomb_card(card_id)

                # self.opponent_field_unit_repository.replace_opponent_field_unit_card_position()
                self.field_area_inside_handler.clear_field_area_action()
                self.opponent_fixed_unit_card_inside_handler.clear_opponent_field_area_action()

                self.opponent_fixed_unit_card_inside_handler.set_action_to_apply_opponent(ActionToApplyOpponent.Dummy)

        move_to_origin_location(1)
        self.timer_repository.set_check_nether_blade_turn_start_second_passive_targeting_animation(False)

    def finish_nether_blade_turn_start_second_passive_targeting_animation_timeout(self, attack_animation_object):
        animation_actor = attack_animation_object.get_animation_actor()
        your_fixed_card_base = animation_actor.get_fixed_card_base()
        your_actor_extra_ability = attack_animation_object.get_extra_ability()

        current_your_attacker_unit_vertices = your_fixed_card_base.get_vertices()
        current_your_attacker_unit_local_translation = your_fixed_card_base.get_local_translation()

        your_attacker_unit_moving_x = attack_animation_object.get_your_attacker_unit_moving_x()

        new_y_value = current_your_attacker_unit_local_translation[1] + 270
        your_attacker_unit_destination_local_translation = (0, new_y_value)

        steps = 15
        step_x = your_attacker_unit_moving_x / steps
        step_y = (your_attacker_unit_destination_local_translation[1] - current_your_attacker_unit_local_translation[1]) / steps
        # step_y *= -1

        is_attack_main_character = False
        opponent_field_unit = None
        # targeting_damage = self.attack_animation_object.get_animation_actor_damage()
        opponent_main_character = self.attack_animation_object.get_opponent_main_character()
        if opponent_main_character is not None:
            is_attack_main_character = True
        else:
            opponent_field_unit = self.attack_animation_object.get_opponent_field_unit()

        def move_to_origin_location(step_count):
            new_vertices = [
                (vx - step_x * step_count, vy - step_y * step_count) for vx, vy in current_your_attacker_unit_vertices
            ]
            your_fixed_card_base.update_vertices(new_vertices)


            for attached_shape in your_fixed_card_base.get_attached_shapes():
                new_attached_shape_vertices = [
                    (vx - step_x, vy - step_y) for vx, vy in attached_shape.vertices
                ]
                attached_shape.update_vertices(new_attached_shape_vertices)
                # print(f"{Fore.RED}new_attached_shape_vertices: {Fore.GREEN}{new_attached_shape_vertices}{Style.RESET_ALL}")

            if step_count < steps:

                self.master.after(20, move_to_origin_location, step_count + 1)
            else:
                self.is_playing_action_animation = False
                # targeting_damage = 20
                # if is_attack_main_character is False:
                #     print(f"{Fore.RED}필드 유닛 공격 -> is_attack_main_character(False): {Fore.GREEN}{is_attack_main_character}{Style.RESET_ALL}")
                #
                #     fixed_card_base = opponent_field_unit.get_fixed_card_base()
                #     tool_card = opponent_field_unit.get_tool_card()
                #     attached_shape_list = fixed_card_base.get_attached_shapes()
                #
                #     remove_from_field = False
                #     for attached_shape in attached_shape_list:
                #         if isinstance(attached_shape, NonBackgroundNumberImage):
                #             if attached_shape.get_circle_kinds() is CircleKinds.HP:
                #                 hp_number = attached_shape.get_number()
                #                 print(f"{Fore.RED}current hp_number: {Fore.GREEN}{hp_number}{Style.RESET_ALL}")
                #
                #                 hp_number -= targeting_damage
                #                 print(f"{Fore.RED}hp_number: {Fore.GREEN}{hp_number}{Style.RESET_ALL}")
                #
                #                 # TODO: n 턴간 불사 특성을 검사해야하므로 사실 이것도 summary 방식으로 빼는 것이 맞으나 우선은 진행한다.
                #                 if hp_number <= 0:
                #                     remove_from_field = True
                #                     break
                #
                #                 attached_shape.set_number(hp_number)
                #
                #                 # attached_shape.set_image_data(
                #                 #     # TODO: 실제로 여기서 서버로부터 계산 받은 값을 적용해야함
                #                 #     self.pre_drawed_image_instance.get_pre_draw_number_image(hp_number))
                #
                #                 attached_shape.set_image_data(
                #                     self.pre_drawed_image_instance.get_pre_draw_unit_hp(hp_number))
                #
                #                 if your_actor_extra_ability:
                #                     self.opponent_field_unit_repository.apply_harmful_status(
                #                         opponent_field_unit.get_index(), your_actor_extra_ability)
                #
                #     if remove_from_field:
                #         def remove_field_unit(_opponent_field_unit):
                #
                #             card_id = _opponent_field_unit.get_card_number()
                #             card_index = _opponent_field_unit.get_index()
                #             print('remove field unit',card_index)
                #
                #             self.opponent_field_unit_repository.remove_current_field_unit_card(card_index)
                #
                #             self.opponent_field_unit_repository.remove_harmful_status_by_index(card_index)
                #             self.opponent_tomb_repository.create_opponent_tomb_card(card_id)
                #             self.opponent_field_unit_repository.replace_opponent_field_unit_card_position()
                #             print(self.opponent_field_unit_repository.get_current_field_unit_card_object_list())
                #
                #         self.create_effect_animation_to_opponent_unit_and_play_animation_and_call_function_with_param(
                #             'death', opponent_field_unit.get_index(), remove_field_unit, opponent_field_unit
                #         )
                #
                # else:
                #     print(
                #         f"{Fore.RED}opponent 메인 캐릭터 공격 -> is_attack_main_character(True): {Fore.GREEN}{is_attack_main_character}{Style.RESET_ALL}")
                #
                #     self.opponent_hp_repository.take_damage(targeting_damage)

                self.field_area_inside_handler.clear_field_area_action()
                self.opponent_fixed_unit_card_inside_handler.clear_opponent_field_area_action()

                self.opponent_fixed_unit_card_inside_handler.set_action_to_apply_opponent(ActionToApplyOpponent.Dummy)

        move_to_origin_location(1)
        self.timer_repository.set_check_nether_blade_turn_start_second_passive_targeting_animation(False)

    def valrn_ready_to_use_shadow_ball_to_opponent_unit_animation(self):
        self.is_playing_action_animation = True
        self.reset_every_selected_action()
        # self.opponent_fixed_unit_card_inside_handler.clear_opponent_field_area_action()
        # self.targeting_enemy_select_using_your_field_card_index = None
        # self.targeting_enemy_select_support_lightning_border_list = []
        # self.opponent_you_selected_lightning_border_list = []
        #
        # self.selected_object = None
        # self.active_panel_rectangle = None
        # self.current_fixed_details_card = None
        # self.your_active_panel.clear_all_your_active_panel()

        steps = 10
        attack_animation_object = AttackAnimation.getInstance()
        animation_actor = attack_animation_object.get_animation_actor()

        your_fixed_card_base = animation_actor.get_fixed_card_base()
        current_your_attacker_unit_vertices = your_fixed_card_base.get_vertices()
        current_your_attacker_unit_local_translation = your_fixed_card_base.get_local_translation()

        new_y_value = current_your_attacker_unit_local_translation[1] - 270
        new_x_value = attack_animation_object.get_total_width() / 2 - 52.5
        # your_attacker_unit_destination_local_translation = (current_your_attacker_unit_local_translation[0], new_y_value)
        your_attacker_unit_destination_local_translation = (new_x_value, new_y_value)

        attack_animation_object.set_your_attacker_unit_moving_x(
            your_attacker_unit_destination_local_translation[0] - current_your_attacker_unit_local_translation[0])

        step_x = (your_attacker_unit_destination_local_translation[0] - current_your_attacker_unit_local_translation[0]) / steps
        step_y = (your_attacker_unit_destination_local_translation[1] - current_your_attacker_unit_local_translation[1]) / steps
        step_y *= -1

        # S = 0.5 * a * t^2
        # S = 0.5 * 100 * a
        # S = 50 * a
        staff_accel_x = 1

        # S = 0.5 * a * 100
        # S = 50 * a = -150=
        staff_accel_y = -3

        def update_position(step_count):
            print(f"{Fore.RED}step_count: {Fore.GREEN}{step_count}{Style.RESET_ALL}")

            new_vertices = [
                (vx + step_x * step_count, vy + step_y * step_count) for vx, vy in current_your_attacker_unit_vertices
            ]
            your_fixed_card_base.update_vertices(new_vertices)

            # tool_card = self.selected_object.get_tool_card()
            # if tool_card is not None:
            #     new_tool_card_vertices = [
            #         (vx + new_x, vy + new_y) for vx, vy in tool_card.vertices
            #     ]
            #     tool_card.update_vertices(new_tool_card_vertices)

            for attached_shape in your_fixed_card_base.get_attached_shapes():
                # theta = w0 * t + 0.5 * alpha * t^2
                # theta = 0.5 * alpha * t^2 => step_count = 10
                # theta = 0.5 * alpha * 100 = 10 / 50 = 0.2
                omega_accel_alpha = -0.2

                if isinstance(attached_shape, NonBackgroundNumberImage):
                    if attached_shape.get_circle_kinds() is CircleKinds.ATTACK:
                        accel_x_dist = staff_accel_x * step_count
                        accel_y_dist = staff_accel_y * step_count
                        # x: 236 / 1920, y: -367 / 1043
                        new_attached_shape_vertices = [
                            (vx + accel_x_dist, vy + accel_y_dist) for vx, vy in attached_shape.vertices
                        ]
                        attached_shape.update_vertices(new_attached_shape_vertices)
                        attached_shape.update_rotation_angle(omega_accel_alpha * step_count * step_count)

                        if step_count == 10:
                            attack_animation_object.set_your_weapon_shape(attached_shape)

                new_attached_shape_vertices = [
                    (vx + step_x, vy + step_y) for vx, vy in attached_shape.vertices
                ]
                attached_shape.update_vertices(new_attached_shape_vertices)
                # print(f"{Fore.RED}new_attached_shape_vertices: {Fore.GREEN}{new_attached_shape_vertices}{Style.RESET_ALL}")

            if step_count < steps:
                self.master.after(20, update_position, step_count + 1)
            else:
                self.valrn_shoot_shadow_ball_to_opponent_unit_animation(attack_animation_object)

        update_position(1)

    def valrn_shoot_shadow_ball_to_opponent_unit_animation(self, attack_animation_object):
        effect_animation = EffectAnimation()
        effect_animation.set_animation_name('moving_shadow_ball')
        effect_animation.set_total_window_size(self.width, self.height)

        opponent_field_unit_object = attack_animation_object.get_opponent_field_unit()
        opponent_field_unit_fixed_card_base = opponent_field_unit_object.get_fixed_card_base()

        opponent_field_unit_fixed_card_base_vertices = opponent_field_unit_fixed_card_base.get_vertices()
        print(f"{Fore.RED}valrn_shoot_shadow_ball_animation() -> opponent_field_unit_fixed_card_base_vertices: {Fore.GREEN}{opponent_field_unit_fixed_card_base_vertices}{Style.RESET_ALL}")
        opponent_field_unit_fixed_card_base_local_translation = opponent_field_unit_fixed_card_base.get_local_translation()
        print(f"{Fore.RED}valrn_shoot_shadow_ball_animation() -> opponent_field_unit_fixed_card_base_local_translation: {Fore.GREEN}{opponent_field_unit_fixed_card_base_local_translation}{Style.RESET_ALL}")

        valrn_staff = attack_animation_object.get_your_weapon_shape()
        valrn_staff_local_translation = valrn_staff.get_local_translation()
        valrn_staff_vertices = valrn_staff.get_vertices()
        moving_shadow_ball_vertices = [
            (vx, vy - 100) for vx, vy in valrn_staff_vertices
        ]
        print(f"{Fore.RED}valrn_shoot_shadow_ball_animation() -> valrn_staff_local_translation: {Fore.GREEN}{valrn_staff_local_translation}{Style.RESET_ALL}")
        print(f"{Fore.RED}valrn_shoot_shadow_ball_animation() -> valrn_staff_vertices: {Fore.GREEN}{valrn_staff_vertices}{Style.RESET_ALL}")
        print(f"{Fore.RED}valrn_shoot_shadow_ball_animation() -> moving_shadow_ball_vertices: {Fore.GREEN}{moving_shadow_ball_vertices}{Style.RESET_ALL}")

        opponent_main_character_panel_vertices = self.opponent_main_character_panel.get_vertices()
        opponent_main_character_panel_local_translation = self.opponent_main_character_panel.get_local_translation()

        # print(effect_animation_panel)
        # self.effect_animation_repository.save_effect_animation_at_dictionary_with_index(
        #     your_field_card_index, effect_animation)
        #
        # self.effect_animation_repository.save_effect_animation_panel_at_dictionary_with_index(
        #     your_field_card_index, effect_animation_panel)

        your_field_actor_card = attack_animation_object.get_animation_actor()
        your_field_card_index = your_field_actor_card.get_index()

        effect_animation.change_local_translation(opponent_field_unit_fixed_card_base.get_local_translation())
        effect_animation.draw_animation_panel()
        effect_animation_panel = effect_animation.get_animation_panel()

        self.effect_animation_repository.save_effect_animation_at_dictionary_with_index(
            your_field_card_index, effect_animation)

        self.effect_animation_repository.save_effect_animation_panel_at_dictionary_with_index(
            your_field_card_index, effect_animation_panel)

        self.targeting_enemy_select_support_lightning_border_list = []
        self.opponent_you_selected_lightning_border_list = []

        effect_animation_panel_vertices = effect_animation_panel.get_vertices()
        print(f"{Fore.RED}valrn_shoot_shadow_ball_animation() -> before effect_animation_panel_vertices: {Fore.GREEN}{effect_animation_panel_vertices}{Style.RESET_ALL}")

        effect_animation_panel_local_translation = effect_animation_panel.get_local_translation()
        print(f"{Fore.RED}valrn_shoot_shadow_ball_animation() -> before effect_animation_panel_local_translation: {Fore.GREEN}{effect_animation_panel_local_translation}{Style.RESET_ALL}")

        # 대략적인 쉐도우 볼 중점 -> x: 1089, y: -639
        # 대략적인 첫 번째 상대 유닛 위치 -> x: 319, y: -346
        # need_to_move_distance = valrn_staff_local_translation[0] + valrn_staff_vertices[0][0] - effect_animation_panel_vertices[0][0]
        # need_to_x_move_distance = valrn_staff_local_translation[0] + valrn_staff_vertices[0][0] - opponent_field_unit_fixed_card_base_local_translation[0]
        need_to_x_move_distance = valrn_staff_local_translation[0] + valrn_staff_vertices[0][0] + 50
        print(f"{Fore.RED}valrn_shoot_shadow_ball_animation() -> need_to_x_move_distance: {Fore.GREEN}{need_to_x_move_distance}{Style.RESET_ALL}")

        need_to_y_move_distance = valrn_staff_local_translation[1] + 50
        print(f"{Fore.RED}valrn_shoot_shadow_ball_animation() -> need_to_y_move_distance: {Fore.GREEN}{need_to_y_move_distance}{Style.RESET_ALL}")

        effect_animation_panel.local_translate((need_to_x_move_distance, need_to_y_move_distance))
        effect_animation_panel_local_translation = effect_animation_panel.get_local_translation()
        print(f"{Fore.RED}valrn_shoot_shadow_ball_animation() -> after change effect_animation_panel_local_translation: {Fore.GREEN}{effect_animation_panel_local_translation}{Style.RESET_ALL}")

        need_to_move_x_distance_with_acceleration = valrn_staff_local_translation[0] + valrn_staff_vertices[0][0] - \
                                                    opponent_field_unit_fixed_card_base_local_translation[0] + 50
        need_to_move_y_distance_with_acceleration = valrn_staff_local_translation[1] + valrn_staff_vertices[0][1] - \
                                                    opponent_field_unit_fixed_card_base_local_translation[1] - 100
        need_to_move_distance_with_acceleration = (need_to_move_x_distance_with_acceleration, need_to_move_y_distance_with_acceleration)
        # moving_shadow_ball_vertices: [(730.4999999999999, 58.587999999999994), (810.4999999999999, 58.587999999999994),
        #                               (810.4999999999999, 213.41200000000003), (730.4999999999999, 213.41200000000003)]
        # effect_animation_panel_vertices: [(844.9055999999999, 44.9072), (1007.1600000000001, 44.9072), (1007.1600000000001, 216.5096), (844.9055999999999, 216.5096)]
        after_effect_animation_panel_vertices = effect_animation_panel.get_vertices()
        print(f"{Fore.RED}valrn_shoot_shadow_ball_animation() -> effect_animation_panel_vertices: {Fore.GREEN}{effect_animation_panel_vertices}{Style.RESET_ALL}")

        step_count = [0]

        def burst_shadow_ball_animation():
            step_count[0] += 1
            print(f"{Fore.RED}burst_shadow_ball_animation() -> step_count: {step_count}{Style.RESET_ALL}")

            effect_animation.set_animation_name('burst_shadow_ball')
            effect_animation.set_total_window_size(self.width, self.height)
            # vertices = opponent_field_unit_fixed_card_base.get_vertices()
            # effect_animation.draw_animation_panel_with_vertices(opponent_field_unit_fixed_card_base_vertices)
            effect_animation.change_local_translation(opponent_field_unit_fixed_card_base.get_local_translation())
            effect_animation.draw_animation_panel()
            effect_animation_panel = effect_animation.get_animation_panel()

            self.effect_animation_repository.save_effect_animation_at_dictionary_with_index(
                your_field_card_index, effect_animation)

            self.effect_animation_repository.save_effect_animation_panel_at_dictionary_with_index(
                your_field_card_index, effect_animation_panel)

            self.play_effect_animation_by_index_and_call_function(your_field_card_index,
                                                                  self.calculate_shadow_ball_to_opponent_unit)

            # self.play_effect_animation_by_index_and_call_function(your_field_card_index,
            #                                                       burst_shadow_ball_animation)

        # self.play_effect_animation_by_index_and_call_function(your_field_card_index,
        #                                                       burst_shadow_ball_animation)
        self.__music_player_repository.play_sound_effect_with_event_name('valrn_active_skill_1')
        self.play_effect_animation_with_acceleration_by_index_and_call_function(
            your_field_card_index,
            burst_shadow_ball_animation,
            need_to_move_distance_with_acceleration)

    def calculate_shadow_ball_to_opponent_unit(self):
        self.shadow_ball_explosion_opponent_unit_post_animation(self.attack_animation_object)

    def shadow_ball_explosion_opponent_unit_post_animation(self, attack_animation_object):
        steps = 30

        opponent_field_unit_object = attack_animation_object.get_opponent_field_unit()
        fixed_card_base = opponent_field_unit_object.get_fixed_card_base()
        tool_card = opponent_field_unit_object.get_tool_card()
        attached_shape_list = fixed_card_base.get_attached_shapes()

        def vibration(step_count):
            if step_count % 2 == 1:
                vibration_factor = 10
                random_translation = (random.uniform(-vibration_factor, vibration_factor),
                                      random.uniform(-vibration_factor, vibration_factor))

                new_fixed_card_base_vertices = [
                    (vx + random_translation[0], vy + random_translation[1]) for vx, vy in
                    fixed_card_base.get_vertices()
                ]
                fixed_card_base.update_vertices(new_fixed_card_base_vertices)

                if tool_card is not None:
                    new_tool_card_vertices = [
                        (vx + random_translation[0], vy + random_translation[1]) for vx, vy in
                        tool_card.get_vertices()
                    ]
                    tool_card.update_vertices(new_tool_card_vertices)

                for attached_shape in attached_shape_list:
                    new_attached_shape_vertices = [
                        (vx + random_translation[0], vy + random_translation[1]) for vx, vy in
                        attached_shape.get_vertices()
                    ]
                    attached_shape.update_vertices(new_attached_shape_vertices)

            else:
                fixed_card_base.update_vertices(fixed_card_base.get_initial_vertices())
                if tool_card is not None:
                    tool_card.update_vertices(tool_card.get_initial_vertices())
                for attached_shape in attached_shape_list:
                    attached_shape.update_vertices(attached_shape.get_initial_vertices())

            if step_count < steps:
                self.master.after(20, vibration, step_count + 1)
            else:
                self.finish_shadow_ball_explosion_opponent_unit_animation(attack_animation_object)
                pass

        vibration(1)

    def finish_shadow_ball_explosion_opponent_unit_animation(self, attack_animation_object):
        animation_actor = attack_animation_object.get_animation_actor()
        your_fixed_card_base = animation_actor.get_fixed_card_base()
        tool_card = animation_actor.get_tool_card()
        attached_shape_list = your_fixed_card_base.get_attached_shapes()

        current_your_attacker_unit_vertices = your_fixed_card_base.get_vertices()
        current_your_attacker_unit_local_translation = your_fixed_card_base.get_local_translation()

        your_attacker_unit_moving_x = attack_animation_object.get_your_attacker_unit_moving_x()

        new_y_value = current_your_attacker_unit_local_translation[1] + 270
        your_attacker_unit_destination_local_translation = (0, new_y_value)
        print(
            f"{Fore.RED}your_attacker_unit_destination_local_translation{Fore.GREEN} {your_attacker_unit_destination_local_translation}{Style.RESET_ALL}")

        steps = 15
        step_x = your_attacker_unit_moving_x / steps
        step_y = (your_attacker_unit_destination_local_translation[1] - current_your_attacker_unit_local_translation[1]) / steps

        staff_shape = attack_animation_object.get_your_weapon_shape()

        # S = 0.5 * a * t^2
        # S = 0.5 * 225 * a
        # S = 112.5 * a = -50
        # a =
        staff_accel_x = -0.44444

        # S = 0.5 * a * 225
        # S = 112.5 * a = 150
        staff_accel_y = 1.33333

        def move_to_origin_location(step_count):
            new_y = current_your_attacker_unit_local_translation[1] + step_y * step_count

            new_vertices = [
                (vx - step_x * step_count, vy - step_y * step_count) for vx, vy in current_your_attacker_unit_vertices
            ]
            your_fixed_card_base.update_vertices(new_vertices)

            # tool_card = self.selected_object.get_tool_card()
            # if tool_card is not None:
            #     new_tool_card_vertices = [
            #         (vx + new_x, vy + new_y) for vx, vy in tool_card.vertices
            #     ]
            #     tool_card.update_vertices(new_tool_card_vertices)

            for attached_shape in your_fixed_card_base.get_attached_shapes():
                # theta = w0 * t + 0.5 * alpha * t^2
                # theta = 0.5 * alpha * t^2 => step_count = 15
                # theta = 0.5 * alpha * 225 = 10 / 112.5 = 0.2
                omega_accel_alpha = 0.08888

                if isinstance(attached_shape, NonBackgroundNumberImage):
                    if attached_shape.get_circle_kinds() is CircleKinds.ATTACK:
                        accel_x_dist = staff_accel_x * step_count
                        accel_y_dist = staff_accel_y * step_count

                        new_attached_shape_vertices = [
                            (vx + accel_x_dist, vy + accel_y_dist) for vx, vy in attached_shape.vertices
                        ]
                        attached_shape.update_vertices(new_attached_shape_vertices)
                        current_rotation_angle = attached_shape.get_rotation_angle()
                        attached_shape.update_rotation_angle(current_rotation_angle + omega_accel_alpha * step_count)

            for attached_shape in your_fixed_card_base.get_attached_shapes():
                new_attached_shape_vertices = [
                    (vx - step_x, vy - step_y) for vx, vy in attached_shape.vertices
                ]
                attached_shape.update_vertices(new_attached_shape_vertices)

            if step_count < steps:

                self.master.after(20, move_to_origin_location, step_count + 1)
            else:
                self.is_playing_action_animation = False
                your_fixed_card_base.update_vertices(your_fixed_card_base.get_initial_vertices())
                if tool_card is not None:
                    tool_card.update_vertices(tool_card.get_initial_vertices())
                for attached_shape in attached_shape_list:
                    if isinstance(attached_shape, NonBackgroundNumberImage):
                        if attached_shape.get_circle_kinds() is CircleKinds.ATTACK:
                            attached_shape.update_rotation_angle(0)

                    attached_shape.update_vertices(attached_shape.get_initial_vertices())

                animation_actor_card_id = animation_actor.get_card_number()
                animation_actor_skill_damage = self.card_info_repository.getCardSkillFirstDamageForCardNumber(animation_actor_card_id)
                print(f"animation_actor_skill_damage: {animation_actor_skill_damage}")

                opponent_field_unit_object = attack_animation_object.get_opponent_field_unit()
                opponent_fixed_card_base = opponent_field_unit_object.get_fixed_card_base()
                opponent_tool_card = opponent_field_unit_object.get_tool_card()
                opponent_attached_shape_list = opponent_fixed_card_base.get_attached_shapes()

                are_opponent_field_unit_death = False
                opponent_field_card_index = opponent_field_unit_object.get_index()
                opponent_field_card_id = opponent_field_unit_object.get_card_number()
                your_field_card_index = self.targeting_enemy_select_using_your_field_card_index
                your_extra_ability = self.your_field_unit_repository.get_your_unit_extra_ability_at_index(your_field_card_index)

                for opponent_attached_shape in opponent_attached_shape_list:
                    if isinstance(opponent_attached_shape, NonBackgroundNumberImage):
                        if opponent_attached_shape.get_circle_kinds() is CircleKinds.HP:
                            current_opponent_hp_number = opponent_attached_shape.get_number()
                            current_opponent_hp_number -= animation_actor_skill_damage

                            if current_opponent_hp_number <= 0:
                                are_opponent_field_unit_death = True

                                break

                            print(f"공격 후 opponent unit 체력 -> hp_number: {current_opponent_hp_number}")
                            opponent_attached_shape.set_number(current_opponent_hp_number)

                            # opponent_fixed_card_attached_shape.set_image_data(
                            #     # TODO: 실제로 여기서 서버로부터 계산 받은 값을 적용해야함
                            #     self.pre_drawed_image_instance.get_pre_draw_number_image(opponent_hp_number))

                            opponent_attached_shape.set_image_data(
                                self.pre_drawed_image_instance.get_pre_draw_unit_hp(current_opponent_hp_number))

                            if your_extra_ability:
                                self.opponent_field_unit_repository.apply_harmful_status(opponent_field_card_index, your_extra_ability)

                print(f"opponent_field_card_index: {opponent_field_card_index}")

                if are_opponent_field_unit_death is True:
                    
                    def remove_field_unit_by_index():
                    
                        self.opponent_field_unit_repository.remove_card_by_multiple_index(
                            [opponent_field_card_index])
                        self.opponent_tomb_repository.create_opponent_tomb_card(
                            opponent_field_card_id)
                        self.opponent_field_unit_repository.remove_harmful_status_by_index(opponent_field_card_index)
    
                        self.opponent_field_unit_repository.replace_opponent_field_unit_card_position()
                        
                    self.create_effect_animation_to_opponent_unit_and_play_animation_and_call_function('death', opponent_field_card_index, remove_field_unit_by_index)

                # self.opponent_fixed_unit_card_inside_handler.clear_opponent_field_area_action()
                # self.targeting_enemy_select_using_your_field_card_index = None
                # self.targeting_enemy_select_using_your_field_card_id = None
                # self.targeting_enemy_select_support_lightning_border_list = []
                # self.opponent_you_selected_lightning_border_list = []
                #
                # self.selected_object = None
                # self.active_panel_rectangle = None
                # self.current_fixed_details_card = None
                # self.your_active_panel.clear_all_your_active_panel()
                self.reset_every_selected_action()
                self.targeting_enemy_select_using_your_field_card_id = None

                self.field_area_inside_handler.clear_field_area_action()

        move_to_origin_location(1)

    def valrn_ready_to_use_shadow_ball_to_opponent_main_character_animation(self):
        self.is_playing_action_animation = True
        self.reset_every_selected_action()
        # self.opponent_fixed_unit_card_inside_handler.clear_opponent_field_area_action()
        # self.targeting_enemy_select_using_your_field_card_index = None
        # self.targeting_enemy_select_support_lightning_border_list = []
        # self.opponent_you_selected_lightning_border_list = []
        #
        # self.selected_object = None
        # self.active_panel_rectangle = None
        # self.current_fixed_details_card = None
        # self.your_active_panel.clear_all_your_active_panel()

        steps = 10
        attack_animation_object = AttackAnimation.getInstance()
        animation_actor = attack_animation_object.get_animation_actor()

        your_fixed_card_base = animation_actor.get_fixed_card_base()
        current_your_attacker_unit_vertices = your_fixed_card_base.get_vertices()
        current_your_attacker_unit_local_translation = your_fixed_card_base.get_local_translation()

        new_y_value = current_your_attacker_unit_local_translation[1] - 270
        new_x_value = attack_animation_object.get_total_width() / 2 - 52.5
        # your_attacker_unit_destination_local_translation = (current_your_attacker_unit_local_translation[0], new_y_value)
        your_attacker_unit_destination_local_translation = (new_x_value, new_y_value)

        attack_animation_object.set_your_attacker_unit_moving_x(your_attacker_unit_destination_local_translation[0] - current_your_attacker_unit_local_translation[0])

        step_x = (your_attacker_unit_destination_local_translation[0] - current_your_attacker_unit_local_translation[0]) / steps
        step_y = (your_attacker_unit_destination_local_translation[1] - current_your_attacker_unit_local_translation[1]) / steps
        step_y *= -1

        # S = 0.5 * a * t^2
        # S = 0.5 * 100 * a
        # S = 50 * a
        staff_accel_x = 1

        # S = 0.5 * a * 100
        # S = 50 * a = -150=
        staff_accel_y = -3

        def update_position(step_count):
            print(f"{Fore.RED}step_count: {Fore.GREEN}{step_count}{Style.RESET_ALL}")

            new_vertices = [
                (vx + step_x * step_count, vy + step_y * step_count) for vx, vy in current_your_attacker_unit_vertices
            ]
            your_fixed_card_base.update_vertices(new_vertices)

            # tool_card = self.selected_object.get_tool_card()
            # if tool_card is not None:
            #     new_tool_card_vertices = [
            #         (vx + new_x, vy + new_y) for vx, vy in tool_card.vertices
            #     ]
            #     tool_card.update_vertices(new_tool_card_vertices)

            for attached_shape in your_fixed_card_base.get_attached_shapes():
                # theta = w0 * t + 0.5 * alpha * t^2
                # theta = 0.5 * alpha * t^2 => step_count = 10
                # theta = 0.5 * alpha * 100 = 10 / 50 = 0.2
                omega_accel_alpha = -0.2

                if isinstance(attached_shape, NonBackgroundNumberImage):
                    if attached_shape.get_circle_kinds() is CircleKinds.ATTACK:
                        accel_x_dist = staff_accel_x * step_count
                        accel_y_dist = staff_accel_y * step_count
                        # x: 236 / 1920, y: -367 / 1043
                        new_attached_shape_vertices = [
                            (vx + accel_x_dist, vy + accel_y_dist) for vx, vy in attached_shape.vertices
                        ]
                        attached_shape.update_vertices(new_attached_shape_vertices)
                        attached_shape.update_rotation_angle(omega_accel_alpha * step_count * step_count)
                        # print(f"{Fore.RED}sword new_attached_shape_vertices{Fore.GREEN} {new_attached_shape_vertices}{Style.RESET_ALL}")

                        if step_count == 10:
                            attack_animation_object.set_your_weapon_shape(attached_shape)

                new_attached_shape_vertices = [
                    (vx + step_x, vy + step_y) for vx, vy in attached_shape.vertices
                ]
                attached_shape.update_vertices(new_attached_shape_vertices)
                # print(f"{Fore.RED}new_attached_shape_vertices: {Fore.GREEN}{new_attached_shape_vertices}{Style.RESET_ALL}")

            if step_count < steps:
                self.master.after(20, update_position, step_count + 1)
            else:
                self.valrn_shoot_shadow_ball_to_opponent_main_character_animation(attack_animation_object)
                # self.is_attack_motion_finished = True
                # attack_animation_object.set_is_finished(True)
                # attack_animation_object.set_need_post_process(True)

        update_position(1)

    def valrn_shoot_shadow_ball_to_opponent_main_character_animation(self, attack_animation_object):
        # effect_animation = EffectAnimation()
        # effect_animation.set_animation_name('moving_shadow_ball')
        # effect_animation.set_total_window_size(self.width, self.height)
        #
        # opponent_main_character_panel_vertices = self.opponent_main_character_panel.get_vertices()
        #
        # valrn_staff = attack_animation_object.get_your_weapon_shape()
        # valrn_staff_vertices = valrn_staff.get_vertices()
        # moving_shadow_ball_vertices = [
        #     (vx, vy - 100) for vx, vy in valrn_staff_vertices
        # ]
        #
        # print(f"{Fore.RED}valrn_shoot_shadow_ball_animation() -> moving_shadow_ball_vertices: {Fore.GREEN}{moving_shadow_ball_vertices}{Style.RESET_ALL}")
        # effect_animation.draw_animation_panel_with_vertices(moving_shadow_ball_vertices)
        # effect_animation_panel = effect_animation.get_animation_panel()
        #
        # def animate():
        #     effect_animation.update_effect_animation_panel()
        #     if not effect_animation.is_finished:
        #         self.master.after(17, animate)
        #     else:
        #         effect_animation.set_animation_name('moving_shadow_ball')
        #         effect_animation.reset_animation_count()
        #         self.master.after(0, animate)
        #         print("finish animation")
        #
        # effect_animation.reset_animation_count()
        #
        # self.master.after(0, animate)

        steps = 10

        effect_animation = EffectAnimation()
        effect_animation.set_animation_name('moving_shadow_ball')
        effect_animation.set_total_window_size(self.width, self.height)

        opponent_main_character_panel_vertices = self.opponent_main_character_panel.get_vertices()
        print(f"{Fore.RED}valrn_shoot_shadow_ball_animation() -> opponent_main_character_panel_vertices: {Fore.GREEN}{opponent_main_character_panel_vertices}{Style.RESET_ALL}")
        opponent_main_character_panel_local_translation = self.opponent_main_character_panel.get_local_translation()
        print(f"{Fore.RED}valrn_shoot_shadow_ball_animation() -> opponent_main_character_panel_local_translation: {Fore.GREEN}{opponent_main_character_panel_local_translation}{Style.RESET_ALL}")

        valrn_staff = attack_animation_object.get_your_weapon_shape()
        valrn_staff_local_translation = valrn_staff.get_local_translation()
        valrn_staff_vertices = valrn_staff.get_vertices()
        moving_shadow_ball_vertices = [
            (vx, vy - 100) for vx, vy in valrn_staff_vertices
        ]
        print(f"{Fore.RED}valrn_shoot_shadow_ball_animation() -> valrn_staff_local_translation: {Fore.GREEN}{valrn_staff_local_translation}{Style.RESET_ALL}")
        print(f"{Fore.RED}valrn_shoot_shadow_ball_animation() -> valrn_staff_vertices: {Fore.GREEN}{valrn_staff_vertices}{Style.RESET_ALL}")
        print(f"{Fore.RED}valrn_shoot_shadow_ball_animation() -> moving_shadow_ball_vertices: {Fore.GREEN}{moving_shadow_ball_vertices}{Style.RESET_ALL}")

        effect_animation.draw_animation_panel_with_vertices(opponent_main_character_panel_vertices)
        effect_animation_panel = effect_animation.get_animation_panel()

        your_field_actor_card = attack_animation_object.get_animation_actor()
        your_field_card_index = your_field_actor_card.get_index()

        self.effect_animation_repository.save_effect_animation_at_dictionary_with_index(
            your_field_card_index, effect_animation)

        self.effect_animation_repository.save_effect_animation_panel_at_dictionary_with_index(
            your_field_card_index, effect_animation_panel)

        self.targeting_enemy_select_support_lightning_border_list = []
        self.opponent_you_selected_lightning_border_list = []

        effect_animation_panel_local_translation = effect_animation_panel.get_local_translation()
        print(f"{Fore.RED}valrn_shoot_shadow_ball_animation() -> effect_animation_panel_local_translation: {Fore.GREEN}{effect_animation_panel_local_translation}{Style.RESET_ALL}")

        # 지팡이 자리 대략적인 좌표 (x: 1069, y: -647)
        effect_animation_panel.local_translate((170, 490))
        effect_animation_panel_local_translation = effect_animation_panel.get_local_translation()
        print(f"{Fore.RED}valrn_shoot_shadow_ball_animation() -> after change effect_animation_panel_local_translation: {Fore.GREEN}{effect_animation_panel_local_translation}{Style.RESET_ALL}")

        # moving_shadow_ball_vertices: [(730.4999999999999, 58.587999999999994), (810.4999999999999, 58.587999999999994),
        #                               (810.4999999999999, 213.41200000000003), (730.4999999999999, 213.41200000000003)]
        # effect_animation_panel_vertices: [(844.9055999999999, 44.9072), (1007.1600000000001, 44.9072), (1007.1600000000001, 216.5096), (844.9055999999999, 216.5096)]
        effect_animation_panel_vertices = effect_animation_panel.get_vertices()
        print(f"{Fore.RED}valrn_shoot_shadow_ball_animation() -> effect_animation_panel_vertices: {Fore.GREEN}{effect_animation_panel_vertices}{Style.RESET_ALL}")

        # 50 * a = 170
        x_accel = -3.4
        # 50 * a = -490
        y_accel = -9.8

        need_to_move_with_acceleration = (x_accel, y_accel)
        step_count = [0]

        def burst_shadow_ball_animation():
            step_count[0] += 1
            print(f"{Fore.RED}burst_shadow_ball_animation() -> step_count: {step_count}{Style.RESET_ALL}")

            effect_animation.set_animation_name('burst_shadow_ball')
            effect_animation.set_total_window_size(self.width, self.height)
            vertices = self.opponent_main_character_panel.get_vertices()
            effect_animation.draw_animation_panel_with_vertices(vertices)
            effect_animation_panel = effect_animation.get_animation_panel()

            self.effect_animation_repository.save_effect_animation_at_dictionary_with_index(
                your_field_card_index, effect_animation)

            self.effect_animation_repository.save_effect_animation_panel_at_dictionary_with_index(
                your_field_card_index, effect_animation_panel)

            self.play_effect_animation_by_index_and_call_function(your_field_card_index,
                                                                  self.calculate_shadow_ball_to_main_character)

        # self.play_effect_animation_by_index_and_call_function(your_field_card_index,
        #                                                       burst_shadow_ball_animation)
        self.__music_player_repository.play_sound_effect_with_event_name('valrn_active_skill_1')
        self.play_effect_animation_with_acceleration_by_index_and_call_function(
            your_field_card_index,
            burst_shadow_ball_animation,
            (170, 490))

    def calculate_shadow_ball_to_main_character(self):
        self.shadow_ball_explosion_opponent_main_character_post_animation(self.attack_animation_object)

    def shadow_ball_explosion_opponent_main_character_post_animation(self, attack_animation_object):
        steps = 30

        def vibration(step_count):
            if step_count % 2 == 1:
                vibration_factor = 10
                random_translation = (random.uniform(-vibration_factor, vibration_factor),
                                      random.uniform(-vibration_factor, vibration_factor))

                for battle_field_background_shape in self.battle_field_background_shape_list:
                    battle_field_background_shape.global_translate((random_translation[0], random_translation[1]))

            else:
                for battle_field_background_shape in self.battle_field_background_shape_list:
                    battle_field_background_shape.global_translate((0, 0))

            if step_count < steps:
                self.master.after(20, vibration, step_count + 1)
            else:
                self.finish_shadow_ball_explosion_opponent_main_character_animation(attack_animation_object)
                pass

        vibration(1)
        
    def finish_shadow_ball_explosion_opponent_main_character_animation(self, attack_animation_object):
        animation_actor = attack_animation_object.get_animation_actor()
        your_fixed_card_base = animation_actor.get_fixed_card_base()
        tool_card = animation_actor.get_tool_card()
        attached_shape_list = your_fixed_card_base.get_attached_shapes()

        current_your_attacker_unit_vertices = your_fixed_card_base.get_vertices()
        current_your_attacker_unit_local_translation = your_fixed_card_base.get_local_translation()

        your_attacker_unit_moving_x = attack_animation_object.get_your_attacker_unit_moving_x()

        new_y_value = current_your_attacker_unit_local_translation[1] + 270
        your_attacker_unit_destination_local_translation = (0, new_y_value)
        print(f"{Fore.RED}your_attacker_unit_destination_local_translation{Fore.GREEN} {your_attacker_unit_destination_local_translation}{Style.RESET_ALL}")

        steps = 15
        step_x = your_attacker_unit_moving_x / steps
        step_y = (your_attacker_unit_destination_local_translation[1] - current_your_attacker_unit_local_translation[1]) / steps

        staff_shape = attack_animation_object.get_your_weapon_shape()

        # S = 0.5 * a * t^2
        # S = 0.5 * 225 * a
        # S = 112.5 * a = -50
        # a =
        staff_accel_x = -0.44444

        # S = 0.5 * a * 225
        # S = 112.5 * a = 150
        staff_accel_y = 1.33333

        def move_to_origin_location(step_count):
            new_y = current_your_attacker_unit_local_translation[1] + step_y * step_count

            new_vertices = [
                (vx - step_x * step_count, vy - step_y * step_count) for vx, vy in current_your_attacker_unit_vertices
            ]
            your_fixed_card_base.update_vertices(new_vertices)

            # tool_card = self.selected_object.get_tool_card()
            # if tool_card is not None:
            #     new_tool_card_vertices = [
            #         (vx + new_x, vy + new_y) for vx, vy in tool_card.vertices
            #     ]
            #     tool_card.update_vertices(new_tool_card_vertices)

            for attached_shape in your_fixed_card_base.get_attached_shapes():
                # theta = w0 * t + 0.5 * alpha * t^2
                # theta = 0.5 * alpha * t^2 => step_count = 15
                # theta = 0.5 * alpha * 225 = 10 / 112.5 = 0.2
                omega_accel_alpha = 0.08888

                if isinstance(attached_shape, NonBackgroundNumberImage):
                    if attached_shape.get_circle_kinds() is CircleKinds.ATTACK:
                        accel_x_dist = staff_accel_x * step_count
                        accel_y_dist = staff_accel_y * step_count

                        new_attached_shape_vertices = [
                            (vx + accel_x_dist, vy + accel_y_dist) for vx, vy in attached_shape.vertices
                        ]
                        attached_shape.update_vertices(new_attached_shape_vertices)
                        current_rotation_angle = attached_shape.get_rotation_angle()
                        attached_shape.update_rotation_angle(current_rotation_angle + omega_accel_alpha * step_count)

            for attached_shape in your_fixed_card_base.get_attached_shapes():
                new_attached_shape_vertices = [
                    (vx - step_x, vy - step_y) for vx, vy in attached_shape.vertices
                ]
                attached_shape.update_vertices(new_attached_shape_vertices)

            if step_count < steps:

                self.master.after(20, move_to_origin_location, step_count + 1)
            else:
                self.is_playing_action_animation = False
                your_fixed_card_base.update_vertices(your_fixed_card_base.get_initial_vertices())
                if tool_card is not None:
                    tool_card.update_vertices(tool_card.get_initial_vertices())
                for attached_shape in attached_shape_list:
                    if isinstance(attached_shape, NonBackgroundNumberImage):
                        if attached_shape.get_circle_kinds() is CircleKinds.ATTACK:
                            attached_shape.update_rotation_angle(0)

                    attached_shape.update_vertices(attached_shape.get_initial_vertices())

                # self.targeting_enemy_select_using_your_field_card_id
                your_field_card_id = animation_actor.get_card_number()
                your_damage = self.card_info_repository.getCardSkillFirstDamageForCardNumber(your_field_card_id)
                print(f"your_damage: {your_damage}")
                self.opponent_hp_repository.take_damage(your_damage)

                if self.opponent_hp_repository.get_current_opponent_hp() <= 0:
                    print('Fake opponent is dead!')
                    self.opponent_hp_repository.opponent_character_die()
                    self.timer.stop_timer()

                self.targeting_enemy_select_using_your_field_card_id = None

                self.field_area_inside_handler.clear_field_area_action()

        move_to_origin_location(1)

    def opponent_valrn_shadow_ball_to_your_main_character_animation(self):
        self.is_playing_action_animation = True
        self.reset_every_selected_action()

        steps = 10
        attack_animation_object = AttackAnimation.getInstance()
        opponent_animation_actor = attack_animation_object.get_opponent_animation_actor()

        opponent_fixed_card_base = opponent_animation_actor.get_fixed_card_base()
        current_opponent_attacker_unit_vertices = opponent_fixed_card_base.get_vertices()
        current_opponent_attacker_unit_local_translation = opponent_fixed_card_base.get_local_translation()

        new_y_value = current_opponent_attacker_unit_local_translation[1] + 240
        new_x_value = attack_animation_object.get_total_width() / 2 - 52.5
        # your_attacker_unit_destination_local_translation = (current_your_attacker_unit_local_translation[0], new_y_value)
        opponent_attacker_unit_destination_local_translation = (new_x_value, new_y_value)

        attack_animation_object.set_opponent_attacker_unit_moving_x(
            opponent_attacker_unit_destination_local_translation[0] - current_opponent_attacker_unit_local_translation[0])

        step_x = (opponent_attacker_unit_destination_local_translation[0] -
                  current_opponent_attacker_unit_local_translation[0]) / steps
        step_y = (opponent_attacker_unit_destination_local_translation[1] -
                  current_opponent_attacker_unit_local_translation[1]) / steps
        step_y *= -1

        # S = 0.5 * a * t^2
        # S = 0.5 * 100 * a
        # S = 50 * a
        staff_accel_x = 1

        # S = 0.5 * a * 100
        # S = 50 * a = -150=
        staff_accel_y = 0.4

        def update_position(step_count):
            new_vertices = [
                (vx + step_x * step_count, vy + step_y * step_count) for vx, vy in
                current_opponent_attacker_unit_vertices
            ]
            opponent_fixed_card_base.update_vertices(new_vertices)

            # tool_card = self.selected_object.get_tool_card()
            # if tool_card is not None:
            #     new_tool_card_vertices = [
            #         (vx + new_x, vy + new_y) for vx, vy in tool_card.vertices
            #     ]
            #     tool_card.update_vertices(new_tool_card_vertices)

            for attached_shape in opponent_fixed_card_base.get_attached_shapes():
                # theta = w0 * t + 0.5 * alpha * t^2
                # theta = 0.5 * alpha * t^2 => step_count = 10
                # theta = 0.5 * alpha * 100 = 10 / 50 = 0.2
                omega_accel_alpha = -0.2

                if isinstance(attached_shape, NonBackgroundNumberImage):
                    if attached_shape.get_circle_kinds() is CircleKinds.ATTACK:
                        accel_x_dist = staff_accel_x * step_count
                        accel_y_dist = staff_accel_y * step_count
                        # x: 236 / 1920, y: -367 / 1043
                        new_attached_shape_vertices = [
                            (vx + accel_x_dist, vy + accel_y_dist) for vx, vy in attached_shape.vertices
                        ]
                        attached_shape.update_vertices(new_attached_shape_vertices)
                        attached_shape.update_rotation_angle(omega_accel_alpha * step_count * step_count)

                        if step_count == 10:
                            attack_animation_object.set_opponent_weapon_shape(attached_shape)

                new_attached_shape_vertices = [
                    (vx + step_x, vy + step_y) for vx, vy in attached_shape.vertices
                ]
                attached_shape.update_vertices(new_attached_shape_vertices)
                # print(f"{Fore.RED}new_attached_shape_vertices: {Fore.GREEN}{new_attached_shape_vertices}{Style.RESET_ALL}")

            if step_count < steps:
                self.master.after(20, update_position, step_count + 1)
            else:
                self.valrn_shoot_shadow_ball_to_your_main_character_animation(attack_animation_object)

        update_position(1)

    def valrn_shoot_shadow_ball_to_your_main_character_animation(self, attack_animation_object):
        steps = 10

        effect_animation = EffectAnimation()
        effect_animation.set_animation_name('moving_shadow_ball')
        effect_animation.set_total_window_size(self.width, self.height)

        your_main_character_panel_vertices = self.your_main_character_panel.get_vertices()
        print(f"{Fore.RED}valrn_shoot_shadow_ball_animation() -> your_main_character_panel_vertices: {Fore.GREEN}{your_main_character_panel_vertices}{Style.RESET_ALL}")
        your_main_character_panel_local_translation = self.your_main_character_panel.get_local_translation()
        print(f"{Fore.RED}valrn_shoot_shadow_ball_animation() -> your_main_character_panel_local_translation: {Fore.GREEN}{your_main_character_panel_local_translation}{Style.RESET_ALL}")

        valrn_staff = attack_animation_object.get_opponent_weapon_shape()
        valrn_staff_local_translation = valrn_staff.get_local_translation()
        valrn_staff_vertices = valrn_staff.get_vertices()
        moving_shadow_ball_vertices = [
            (vx, vy - 100) for vx, vy in valrn_staff_vertices
        ]
        print(f"{Fore.RED}valrn_shoot_shadow_ball_animation() -> valrn_staff_local_translation: {Fore.GREEN}{valrn_staff_local_translation}{Style.RESET_ALL}")
        print(f"{Fore.RED}valrn_shoot_shadow_ball_animation() -> valrn_staff_vertices: {Fore.GREEN}{valrn_staff_vertices}{Style.RESET_ALL}")
        print(f"{Fore.RED}valrn_shoot_shadow_ball_animation() -> moving_shadow_ball_vertices: {Fore.GREEN}{moving_shadow_ball_vertices}{Style.RESET_ALL}")

        effect_animation.draw_animation_panel_with_vertices(your_main_character_panel_vertices)
        effect_animation_panel = effect_animation.get_animation_panel()

        opponent_field_actor_card = attack_animation_object.get_opponent_animation_actor()
        opponent_field_card_index = opponent_field_actor_card.get_index()

        self.effect_animation_repository.save_effect_animation_at_dictionary_with_index(
            opponent_field_card_index, effect_animation)

        self.effect_animation_repository.save_effect_animation_panel_at_dictionary_with_index(
            opponent_field_card_index, effect_animation_panel)

        self.targeting_enemy_select_support_lightning_border_list = []
        # self.opponent_you_selected_lightning_border_list = []

        effect_animation_panel_local_translation = effect_animation_panel.get_local_translation()
        print(f"{Fore.RED}valrn_shoot_shadow_ball_animation() -> effect_animation_panel_local_translation: {Fore.GREEN}{effect_animation_panel_local_translation}{Style.RESET_ALL}")

        # 지팡이 자리 대략적인 좌표 (x: 1069, y: -647)
        effect_animation_panel.local_translate((170, -490))
        effect_animation_panel_local_translation = effect_animation_panel.get_local_translation()
        print(f"{Fore.RED}valrn_shoot_shadow_ball_animation() -> after change effect_animation_panel_local_translation: {Fore.GREEN}{effect_animation_panel_local_translation}{Style.RESET_ALL}")

        # moving_shadow_ball_vertices: [(730.4999999999999, 58.587999999999994), (810.4999999999999, 58.587999999999994),
        #                               (810.4999999999999, 213.41200000000003), (730.4999999999999, 213.41200000000003)]
        # effect_animation_panel_vertices: [(844.9055999999999, 44.9072), (1007.1600000000001, 44.9072), (1007.1600000000001, 216.5096), (844.9055999999999, 216.5096)]
        effect_animation_panel_vertices = effect_animation_panel.get_vertices()
        print(f"{Fore.RED}valrn_shoot_shadow_ball_animation() -> effect_animation_panel_vertices: {Fore.GREEN}{effect_animation_panel_vertices}{Style.RESET_ALL}")

        # 50 * a = 170
        x_accel = -3.4
        # 50 * a = -490
        y_accel = -9.8

        need_to_move_with_acceleration = (x_accel, y_accel)
        step_count = [0]

        def burst_shadow_ball_animation():
            step_count[0] += 1
            print(f"{Fore.RED}burst_shadow_ball_animation() -> step_count: {step_count}{Style.RESET_ALL}")

            effect_animation.set_animation_name('burst_shadow_ball')
            effect_animation.set_total_window_size(self.width, self.height)
            vertices = self.your_main_character_panel.get_vertices()
            effect_animation.draw_animation_panel_with_vertices(vertices)
            effect_animation_panel = effect_animation.get_animation_panel()

            self.effect_animation_repository.save_effect_animation_at_dictionary_with_index(
                opponent_field_card_index, effect_animation)

            self.effect_animation_repository.save_effect_animation_panel_at_dictionary_with_index(
                opponent_field_card_index, effect_animation_panel)

            self.play_effect_animation_by_index_and_call_function(opponent_field_card_index,
                                                                  self.calculate_shadow_ball_to_your_main_character)

        # self.play_effect_animation_by_index_and_call_function(your_field_card_index,
        #                                                       burst_shadow_ball_animation)
        self.__music_player_repository.play_sound_effect_with_event_name('valrn_active_skill_1')
        self.play_effect_animation_with_acceleration_by_index_and_call_function(
            opponent_field_card_index,
            burst_shadow_ball_animation,
            (170, -490))

    def calculate_shadow_ball_to_your_main_character(self):
        self.shadow_ball_explosion_your_main_character_post_animation(self.attack_animation_object)

    def shadow_ball_explosion_your_main_character_post_animation(self, attack_animation_object):
        steps = 30

        def vibration(step_count):
            if step_count % 2 == 1:
                vibration_factor = 10
                random_translation = (random.uniform(-vibration_factor, vibration_factor),
                                      random.uniform(-vibration_factor, vibration_factor))

                for battle_field_background_shape in self.battle_field_background_shape_list:
                    battle_field_background_shape.global_translate((random_translation[0], random_translation[1]))

            else:
                for battle_field_background_shape in self.battle_field_background_shape_list:
                    battle_field_background_shape.global_translate((0, 0))

            if step_count < steps:
                self.master.after(20, vibration, step_count + 1)
            else:
                self.finish_shadow_ball_explosion_your_main_character_animation(attack_animation_object)

        vibration(1)

    def finish_shadow_ball_explosion_your_main_character_animation(self, attack_animation_object):
        opponent_animation_actor = attack_animation_object.get_opponent_animation_actor()
        opponent_fixed_card_base = opponent_animation_actor.get_fixed_card_base()
        tool_card = opponent_animation_actor.get_tool_card()
        attached_shape_list = opponent_fixed_card_base.get_attached_shapes()

        current_opponent_attacker_unit_vertices = opponent_fixed_card_base.get_vertices()
        current_opponent_attacker_unit_local_translation = opponent_fixed_card_base.get_local_translation()

        opponent_attacker_unit_moving_x = attack_animation_object.get_opponent_attacker_unit_moving_x()

        new_y_value = current_opponent_attacker_unit_local_translation[1] - 240
        opponent_attacker_unit_destination_local_translation = (0, new_y_value)
        print(f"{Fore.RED}opponent_attacker_unit_destination_local_translation{Fore.GREEN} {opponent_attacker_unit_destination_local_translation}{Style.RESET_ALL}")

        steps = 15
        step_x = opponent_attacker_unit_moving_x / steps
        step_y = (opponent_attacker_unit_destination_local_translation[1] - current_opponent_attacker_unit_local_translation[1]) / steps

        staff_shape = attack_animation_object.get_opponent_weapon_shape()

        # S = 0.5 * a * t^2
        # S = 0.5 * 225 * a
        # S = 112.5 * a = -50
        # a =
        staff_accel_x = -0.44444

        # S = 0.5 * a * 225
        # S = 112.5 * a = 150
        staff_accel_y = 1.33333

        def move_to_origin_location(step_count):
            new_y = current_opponent_attacker_unit_local_translation[1] + step_y * step_count

            new_vertices = [
                (vx - step_x * step_count, vy - step_y * step_count) for vx, vy in current_opponent_attacker_unit_vertices
            ]
            opponent_fixed_card_base.update_vertices(new_vertices)

            # tool_card = self.selected_object.get_tool_card()
            # if tool_card is not None:
            #     new_tool_card_vertices = [
            #         (vx + new_x, vy + new_y) for vx, vy in tool_card.vertices
            #     ]
            #     tool_card.update_vertices(new_tool_card_vertices)

            for attached_shape in opponent_fixed_card_base.get_attached_shapes():
                # theta = w0 * t + 0.5 * alpha * t^2
                # theta = 0.5 * alpha * t^2 => step_count = 15
                # theta = 0.5 * alpha * 225 = 10 / 112.5 = 0.2
                omega_accel_alpha = 0.08888

                if isinstance(attached_shape, NonBackgroundNumberImage):
                    if attached_shape.get_circle_kinds() is CircleKinds.ATTACK:
                        accel_x_dist = staff_accel_x * step_count
                        accel_y_dist = staff_accel_y * step_count

                        new_attached_shape_vertices = [
                            (vx + accel_x_dist, vy + accel_y_dist) for vx, vy in attached_shape.vertices
                        ]
                        attached_shape.update_vertices(new_attached_shape_vertices)
                        current_rotation_angle = attached_shape.get_rotation_angle()
                        attached_shape.update_rotation_angle(current_rotation_angle + omega_accel_alpha * step_count)

            for attached_shape in opponent_fixed_card_base.get_attached_shapes():
                new_attached_shape_vertices = [
                    (vx - step_x, vy - step_y) for vx, vy in attached_shape.vertices
                ]
                attached_shape.update_vertices(new_attached_shape_vertices)

            if step_count < steps:

                self.master.after(20, move_to_origin_location, step_count + 1)
            else:
                self.is_playing_action_animation = False
                opponent_fixed_card_base.update_vertices(opponent_fixed_card_base.get_initial_vertices())
                if tool_card is not None:
                    tool_card.update_vertices(tool_card.get_initial_vertices())
                for attached_shape in attached_shape_list:
                    if isinstance(attached_shape, NonBackgroundNumberImage):
                        if attached_shape.get_circle_kinds() is CircleKinds.ATTACK:
                            attached_shape.update_rotation_angle(0)

                    attached_shape.update_vertices(attached_shape.get_initial_vertices())

                # self.targeting_enemy_select_using_your_field_card_id
                opponent_field_card_id = opponent_animation_actor.get_card_number()
                opponent_damage = self.card_info_repository.getCardSkillFirstDamageForCardNumber(opponent_field_card_id)
                # print(f"your_damage: {opponent_damage}")
                # self.opponent_hp_repository.take_damage(opponent_damage)

                notify_data = self.attack_animation_object.get_notify_data()
                remain_hp = notify_data['player_main_character_health_point_map']['You']

                self.your_hp_repository.change_hp(remain_hp)
                your_character_survival_state = notify_data['player_main_character_survival_map']['You']

                self.targeting_enemy_select_using_your_field_card_id = None
                # self.field_area_inside_handler.clear_field_area_action()
                
                self.opponent_field_area_inside_handler.set_active_field_area_action(OpponentFieldAreaActionProcess.Dummy)
                self.attack_animation_object.set_opponent_animation_actor(None)

                if your_character_survival_state != 'Survival':
                    print('죽었습니다!!')
                    self.timer.stop_timer()
                    self.battle_field_repository.lose()

        move_to_origin_location(1)

    def opponent_valrn_shadow_ball_to_your_unit_animation(self):
        self.is_playing_action_animation = True
        self.reset_every_selected_action()
        # self.opponent_fixed_unit_card_inside_handler.clear_opponent_field_area_action()
        # self.targeting_enemy_select_using_your_field_card_index = None
        # self.targeting_enemy_select_support_lightning_border_list = []
        # self.opponent_you_selected_lightning_border_list = []
        #
        # self.selected_object = None
        # self.active_panel_rectangle = None
        # self.current_fixed_details_card = None
        # self.your_active_panel.clear_all_your_active_panel()

        steps = 10
        attack_animation_object = AttackAnimation.getInstance()
        opponent_animation_actor = attack_animation_object.get_opponent_animation_actor()

        opponent_fixed_card_base = opponent_animation_actor.get_fixed_card_base()
        current_opponent_attacker_unit_vertices = opponent_fixed_card_base.get_vertices()
        current_opponent_attacker_unit_local_translation = opponent_fixed_card_base.get_local_translation()

        new_y_value = current_opponent_attacker_unit_local_translation[1] + 240
        new_x_value = attack_animation_object.get_total_width() / 2 - 52.5
        # your_attacker_unit_destination_local_translation = (current_your_attacker_unit_local_translation[0], new_y_value)
        opponent_attacker_unit_destination_local_translation = (new_x_value, new_y_value)

        attack_animation_object.set_opponent_attacker_unit_moving_x(
            opponent_attacker_unit_destination_local_translation[0] - current_opponent_attacker_unit_local_translation[0])

        step_x = (opponent_attacker_unit_destination_local_translation[0] - current_opponent_attacker_unit_local_translation[0]) / steps
        step_y = (opponent_attacker_unit_destination_local_translation[1] - current_opponent_attacker_unit_local_translation[1]) / steps
        step_y *= -1

        # S = 0.5 * a * t^2
        # S = 0.5 * 100 * a
        # S = 50 * a
        staff_accel_x = 1

        # S = 0.5 * a * 100
        # S = 50 * a = -150=
        staff_accel_y = 0.4

        def update_position(step_count):
            # print(f"{Fore.RED}step_count: {Fore.GREEN}{step_count}{Style.RESET_ALL}")

            new_vertices = [
                (vx + step_x * step_count, vy + step_y * step_count) for vx, vy in current_opponent_attacker_unit_vertices
            ]
            opponent_fixed_card_base.update_vertices(new_vertices)

            # tool_card = self.selected_object.get_tool_card()
            # if tool_card is not None:
            #     new_tool_card_vertices = [
            #         (vx + new_x, vy + new_y) for vx, vy in tool_card.vertices
            #     ]
            #     tool_card.update_vertices(new_tool_card_vertices)

            for attached_shape in opponent_fixed_card_base.get_attached_shapes():
                # theta = w0 * t + 0.5 * alpha * t^2
                # theta = 0.5 * alpha * t^2 => step_count = 10
                # theta = 0.5 * alpha * 100 = 10 / 50 = 0.2
                omega_accel_alpha = -0.2

                if isinstance(attached_shape, NonBackgroundNumberImage):
                    if attached_shape.get_circle_kinds() is CircleKinds.ATTACK:
                        accel_x_dist = staff_accel_x * step_count
                        accel_y_dist = staff_accel_y * step_count
                        # x: 236 / 1920, y: -367 / 1043
                        new_attached_shape_vertices = [
                            (vx + accel_x_dist, vy + accel_y_dist) for vx, vy in attached_shape.vertices
                        ]
                        attached_shape.update_vertices(new_attached_shape_vertices)
                        attached_shape.update_rotation_angle(omega_accel_alpha * step_count * step_count)

                        if step_count == 10:
                            attack_animation_object.set_opponent_weapon_shape(attached_shape)

                new_attached_shape_vertices = [
                    (vx + step_x, vy + step_y) for vx, vy in attached_shape.vertices
                ]
                attached_shape.update_vertices(new_attached_shape_vertices)
                # print(f"{Fore.RED}new_attached_shape_vertices: {Fore.GREEN}{new_attached_shape_vertices}{Style.RESET_ALL}")

            if step_count < steps:
                self.master.after(20, update_position, step_count + 1)
            else:
                self.opponent_valrn_shoot_shadow_ball_to_your_unit_animation(attack_animation_object)
                pass

        update_position(1)

    def opponent_valrn_shoot_shadow_ball_to_your_unit_animation(self, attack_animation_object):
        effect_animation = EffectAnimation()
        effect_animation.set_animation_name('moving_shadow_ball')
        effect_animation.set_total_window_size(self.width, self.height)

        your_field_unit_object = attack_animation_object.get_your_field_unit()
        your_field_unit_fixed_card_base = your_field_unit_object.get_fixed_card_base()

        your_field_unit_fixed_card_base_vertices = your_field_unit_fixed_card_base.get_vertices()
        print(f"{Fore.RED}valrn_shoot_shadow_ball_animation() -> your_field_unit_fixed_card_base_vertices: {Fore.GREEN}{your_field_unit_fixed_card_base_vertices}{Style.RESET_ALL}")
        your_field_unit_fixed_card_base_local_translation = your_field_unit_fixed_card_base.get_local_translation()
        print(f"{Fore.RED}valrn_shoot_shadow_ball_animation() -> your_field_unit_fixed_card_base_local_translation: {Fore.GREEN}{your_field_unit_fixed_card_base_local_translation}{Style.RESET_ALL}")

        valrn_staff = attack_animation_object.get_opponent_weapon_shape()
        valrn_staff_local_translation = valrn_staff.get_local_translation()
        valrn_staff_vertices = valrn_staff.get_vertices()
        moving_shadow_ball_vertices = [
            (vx, vy - 100) for vx, vy in valrn_staff_vertices
        ]
        print(f"{Fore.RED}valrn_shoot_shadow_ball_animation() -> valrn_staff_local_translation: {Fore.GREEN}{valrn_staff_local_translation}{Style.RESET_ALL}")
        print(f"{Fore.RED}valrn_shoot_shadow_ball_animation() -> valrn_staff_vertices: {Fore.GREEN}{valrn_staff_vertices}{Style.RESET_ALL}")
        print(f"{Fore.RED}valrn_shoot_shadow_ball_animation() -> moving_shadow_ball_vertices: {Fore.GREEN}{moving_shadow_ball_vertices}{Style.RESET_ALL}")

        your_main_character_panel_vertices = self.your_main_character_panel.get_vertices()
        your_main_character_panel_local_translation = self.your_main_character_panel.get_local_translation()

        # print(effect_animation_panel)
        # self.effect_animation_repository.save_effect_animation_at_dictionary_with_index(
        #     your_field_card_index, effect_animation)
        #
        # self.effect_animation_repository.save_effect_animation_panel_at_dictionary_with_index(
        #     your_field_card_index, effect_animation_panel)

        opponent_field_actor_card = attack_animation_object.get_opponent_animation_actor()
        opponent_field_card_index = opponent_field_actor_card.get_index()

        effect_animation.change_local_translation(your_field_unit_fixed_card_base.get_local_translation())
        effect_animation.draw_animation_panel()
        effect_animation_panel = effect_animation.get_animation_panel()

        self.effect_animation_repository.save_effect_animation_at_dictionary_with_index(
            opponent_field_card_index, effect_animation)

        self.effect_animation_repository.save_effect_animation_panel_at_dictionary_with_index(
            opponent_field_card_index, effect_animation_panel)

        self.targeting_enemy_select_support_lightning_border_list = []
        self.opponent_you_selected_lightning_border_list = []

        effect_animation_panel_vertices = effect_animation_panel.get_vertices()
        print(f"{Fore.RED}valrn_shoot_shadow_ball_animation() -> before effect_animation_panel_vertices: {Fore.GREEN}{effect_animation_panel_vertices}{Style.RESET_ALL}")

        effect_animation_panel_local_translation = effect_animation_panel.get_local_translation()
        print(f"{Fore.RED}valrn_shoot_shadow_ball_animation() -> before effect_animation_panel_local_translation: {Fore.GREEN}{effect_animation_panel_local_translation}{Style.RESET_ALL}")

        # 대략적인 쉐도우 볼 중점 -> x: 1089, y: -639
        # 대략적인 첫 번째 상대 유닛 위치 -> x: 319, y: -346
        # need_to_move_distance = valrn_staff_local_translation[0] + valrn_staff_vertices[0][0] - effect_animation_panel_vertices[0][0]
        # need_to_x_move_distance = valrn_staff_local_translation[0] + valrn_staff_vertices[0][0] - opponent_field_unit_fixed_card_base_local_translation[0]
        need_to_x_move_distance = valrn_staff_local_translation[0] + valrn_staff_vertices[0][0] + 50
        print(f"{Fore.RED}valrn_shoot_shadow_ball_animation() -> need_to_x_move_distance: {Fore.GREEN}{need_to_x_move_distance}{Style.RESET_ALL}")

        need_to_y_move_distance = valrn_staff_local_translation[1] - 50
        print(f"{Fore.RED}valrn_shoot_shadow_ball_animation() -> need_to_y_move_distance: {Fore.GREEN}{need_to_y_move_distance}{Style.RESET_ALL}")

        effect_animation_panel.local_translate((need_to_x_move_distance, need_to_y_move_distance))
        effect_animation_panel_local_translation = effect_animation_panel.get_local_translation()
        print(f"{Fore.RED}valrn_shoot_shadow_ball_animation() -> after change effect_animation_panel_local_translation: {Fore.GREEN}{effect_animation_panel_local_translation}{Style.RESET_ALL}")

        need_to_move_x_distance_with_acceleration = valrn_staff_local_translation[0] + valrn_staff_vertices[0][0] - \
                                                    your_field_unit_fixed_card_base_local_translation[0] + 50
        need_to_move_y_distance_with_acceleration = valrn_staff_local_translation[1] + valrn_staff_vertices[0][1] - \
                                                    your_field_unit_fixed_card_base_local_translation[1] + 100
        need_to_move_distance_with_acceleration = (need_to_move_x_distance_with_acceleration, need_to_move_y_distance_with_acceleration)
        # moving_shadow_ball_vertices: [(730.4999999999999, 58.587999999999994), (810.4999999999999, 58.587999999999994),
        #                               (810.4999999999999, 213.41200000000003), (730.4999999999999, 213.41200000000003)]
        # effect_animation_panel_vertices: [(844.9055999999999, 44.9072), (1007.1600000000001, 44.9072), (1007.1600000000001, 216.5096), (844.9055999999999, 216.5096)]
        after_effect_animation_panel_vertices = effect_animation_panel.get_vertices()
        print(f"{Fore.RED}valrn_shoot_shadow_ball_animation() -> effect_animation_panel_vertices: {Fore.GREEN}{effect_animation_panel_vertices}{Style.RESET_ALL}")

        step_count = [0]

        def burst_shadow_ball_animation():
            step_count[0] += 1
            print(f"{Fore.RED}burst_shadow_ball_animation() -> step_count: {step_count}{Style.RESET_ALL}")

            effect_animation.set_animation_name('burst_shadow_ball')
            effect_animation.set_total_window_size(self.width, self.height)
            # vertices = opponent_field_unit_fixed_card_base.get_vertices()
            #effect_animation.draw_animation_panel_with_vertices(your_field_unit_fixed_card_base_vertices)
            effect_animation.change_local_translation(
                your_field_unit_fixed_card_base.get_local_translation()
            )
            effect_animation.draw_animation_panel()
            effect_animation_panel = effect_animation.get_animation_panel()

            self.effect_animation_repository.save_effect_animation_at_dictionary_with_index(
                opponent_field_card_index, effect_animation)

            self.effect_animation_repository.save_effect_animation_panel_at_dictionary_with_index(
                opponent_field_card_index, effect_animation_panel)

            self.play_effect_animation_by_index_and_call_function(opponent_field_card_index,
                                                                  self.calculate_opponent_shadow_ball_to_your_unit)

            # self.play_effect_animation_by_index_and_call_function(your_field_card_index,
            #                                                       burst_shadow_ball_animation)

        # self.play_effect_animation_by_index_and_call_function(your_field_card_index,
        #                                                       burst_shadow_ball_animation)
        self.__music_player_repository.play_sound_effect_with_event_name('valrn_active_skill_1')
        self.play_effect_animation_with_acceleration_by_index_and_call_function(
            opponent_field_card_index,
            burst_shadow_ball_animation,
            need_to_move_distance_with_acceleration)

    def calculate_opponent_shadow_ball_to_your_unit(self):
        self.opponent_shadow_ball_explosion_your_unit_post_animation(self.attack_animation_object)

    def opponent_shadow_ball_explosion_your_unit_post_animation(self, attack_animation_object):
        steps = 30

        your_field_unit_object = attack_animation_object.get_your_field_unit()
        fixed_card_base = your_field_unit_object.get_fixed_card_base()
        tool_card = your_field_unit_object.get_tool_card()
        attached_shape_list = fixed_card_base.get_attached_shapes()

        def vibration(step_count):
            if step_count % 2 == 1:
                vibration_factor = 10
                random_translation = (random.uniform(-vibration_factor, vibration_factor),
                                      random.uniform(-vibration_factor, vibration_factor))

                new_fixed_card_base_vertices = [
                    (vx + random_translation[0], vy + random_translation[1]) for vx, vy in
                    fixed_card_base.get_vertices()
                ]
                fixed_card_base.update_vertices(new_fixed_card_base_vertices)

                if tool_card is not None:
                    new_tool_card_vertices = [
                        (vx + random_translation[0], vy + random_translation[1]) for vx, vy in
                        tool_card.get_vertices()
                    ]
                    tool_card.update_vertices(new_tool_card_vertices)

                for attached_shape in attached_shape_list:
                    new_attached_shape_vertices = [
                        (vx + random_translation[0], vy + random_translation[1]) for vx, vy in
                        attached_shape.get_vertices()
                    ]
                    attached_shape.update_vertices(new_attached_shape_vertices)

            else:
                fixed_card_base.update_vertices(fixed_card_base.get_initial_vertices())
                if tool_card is not None:
                    tool_card.update_vertices(tool_card.get_initial_vertices())
                for attached_shape in attached_shape_list:
                    attached_shape.update_vertices(attached_shape.get_initial_vertices())

            if step_count < steps:
                self.master.after(20, vibration, step_count + 1)
            else:
                self.finish_opponent_shadow_ball_explosion_your_unit_animation(attack_animation_object)

        vibration(1)

    def finish_opponent_shadow_ball_explosion_your_unit_animation(self, attack_animation_object):
        opponent_animation_actor = attack_animation_object.get_opponent_animation_actor()
        opponent_fixed_card_base = opponent_animation_actor.get_fixed_card_base()
        tool_card = opponent_animation_actor.get_tool_card()
        attached_shape_list = opponent_fixed_card_base.get_attached_shapes()

        current_opponent_attacker_unit_vertices = opponent_fixed_card_base.get_vertices()
        current_opponent_attacker_unit_local_translation = opponent_fixed_card_base.get_local_translation()

        opponent_attacker_unit_moving_x = attack_animation_object.get_opponent_attacker_unit_moving_x()

        new_y_value = current_opponent_attacker_unit_local_translation[1] - 240
        opponent_attacker_unit_destination_local_translation = (0, new_y_value)
        print(f"{Fore.RED}opponent_attacker_unit_destination_local_translation{Fore.GREEN} {opponent_attacker_unit_destination_local_translation}{Style.RESET_ALL}")

        steps = 15
        step_x = opponent_attacker_unit_moving_x / steps
        step_y = (opponent_attacker_unit_destination_local_translation[1] - current_opponent_attacker_unit_local_translation[1]) / steps

        staff_shape = attack_animation_object.get_opponent_weapon_shape()

        # S = 0.5 * a * t^2
        # S = 0.5 * 225 * a
        # S = 112.5 * a = -50
        # a =
        staff_accel_x = -0.44444

        # S = 0.5 * a * 225
        # S = 112.5 * a = 150
        staff_accel_y = 1.33333

        def move_to_origin_location(step_count):
            new_y = current_opponent_attacker_unit_local_translation[1] + step_y * step_count

            new_vertices = [
                (vx - step_x * step_count, vy - step_y * step_count) for vx, vy in current_opponent_attacker_unit_vertices
            ]
            opponent_fixed_card_base.update_vertices(new_vertices)

            # tool_card = self.selected_object.get_tool_card()
            # if tool_card is not None:
            #     new_tool_card_vertices = [
            #         (vx + new_x, vy + new_y) for vx, vy in tool_card.vertices
            #     ]
            #     tool_card.update_vertices(new_tool_card_vertices)

            for attached_shape in opponent_fixed_card_base.get_attached_shapes():
                # theta = w0 * t + 0.5 * alpha * t^2
                # theta = 0.5 * alpha * t^2 => step_count = 15
                # theta = 0.5 * alpha * 225 = 10 / 112.5 = 0.2
                omega_accel_alpha = 0.08888

                if isinstance(attached_shape, NonBackgroundNumberImage):
                    if attached_shape.get_circle_kinds() is CircleKinds.ATTACK:
                        accel_x_dist = staff_accel_x * step_count
                        accel_y_dist = staff_accel_y * step_count

                        new_attached_shape_vertices = [
                            (vx + accel_x_dist, vy + accel_y_dist) for vx, vy in attached_shape.vertices
                        ]
                        attached_shape.update_vertices(new_attached_shape_vertices)
                        current_rotation_angle = attached_shape.get_rotation_angle()
                        attached_shape.update_rotation_angle(current_rotation_angle + omega_accel_alpha * step_count)

            for attached_shape in opponent_fixed_card_base.get_attached_shapes():
                new_attached_shape_vertices = [
                    (vx - step_x, vy - step_y) for vx, vy in attached_shape.vertices
                ]
                attached_shape.update_vertices(new_attached_shape_vertices)

            if step_count < steps:

                self.master.after(20, move_to_origin_location, step_count + 1)
            else:
                self.is_playing_action_animation = False
                opponent_fixed_card_base.update_vertices(opponent_fixed_card_base.get_initial_vertices())
                if tool_card is not None:
                    tool_card.update_vertices(tool_card.get_initial_vertices())
                for attached_shape in attached_shape_list:
                    if isinstance(attached_shape, NonBackgroundNumberImage):
                        if attached_shape.get_circle_kinds() is CircleKinds.ATTACK:
                            attached_shape.update_rotation_angle(0)

                    attached_shape.update_vertices(attached_shape.get_initial_vertices())

                animation_actor_card_id = opponent_animation_actor.get_card_number()
                animation_actor_skill_damage = self.card_info_repository.getCardSkillFirstDamageForCardNumber(animation_actor_card_id)
                print(f"animation_actor_skill_damage: {animation_actor_skill_damage}")


                notify_data = self.attack_animation_object.get_notify_data()

                your_field_unit_health_point_map = (notify_data)['player_field_unit_health_point_map']['You']['field_unit_health_point_map']
                your_field_unit_harmful_effect_list = (notify_data)['player_field_unit_harmful_effect_map']['You']['field_unit_harmful_status_map']
                your_dead_field_unit_index_list = (notify_data)['player_field_unit_death_map']['You']['dead_field_unit_index_list']

                for unit_index, remaining_health_point in your_field_unit_health_point_map.items():
                    your_field_unit = self.your_field_unit_repository.find_field_unit_by_index(int(unit_index))
                    your_fixed_card_base = your_field_unit.get_fixed_card_base()
                    your_fixed_card_attached_shape_list = your_fixed_card_base.get_attached_shapes()

                    if remaining_health_point <= 0:
                        continue

                    for your_fixed_card_attached_shape in your_fixed_card_attached_shape_list:
                        if isinstance(your_fixed_card_attached_shape, NonBackgroundNumberImage):
                            if your_fixed_card_attached_shape.get_circle_kinds() is CircleKinds.HP:
                                your_fixed_card_attached_shape.set_number(int(remaining_health_point))

                                your_fixed_card_attached_shape.set_image_data(
                                    self.pre_drawed_image_instance.get_pre_draw_unit_hp(int(remaining_health_point)))

                for unit_index, harmful_effect_info in your_field_unit_harmful_effect_list.items():
                    harmful_effect_list = harmful_effect_info['harmful_status_list']
                    self.your_field_unit_repository.apply_harmful_status(int(unit_index), harmful_effect_list)

                # 죽은 유닛들 묘지에 배치 및 Replacing
                for dead_unit_index in your_dead_field_unit_index_list:
                    def remove_field_unit(unit_index):
                        field_unit_id = self.your_field_unit_repository.get_card_id_by_index(unit_index)
                        self.your_tomb_repository.create_tomb_card(field_unit_id)
                        self.your_field_unit_repository.remove_card_by_index(unit_index)
                        self.your_field_unit_repository.remove_harmful_status_by_index(unit_index)
                        self.your_field_unit_repository.replace_field_card_position()
                    self.create_effect_animation_to_your_unit_and_play_animation_and_call_function_with_param(
                        'death', dead_unit_index, remove_field_unit, dead_unit_index)

                # opponent_field_unit_object = attack_animation_object.get_opponent_field_unit()
                # opponent_fixed_card_base = opponent_field_unit_object.get_fixed_card_base()
                # opponent_tool_card = opponent_field_unit_object.get_tool_card()
                # opponent_attached_shape_list = opponent_fixed_card_base.get_attached_shapes()
                #
                # are_opponent_field_unit_death = False
                # opponent_field_card_index = opponent_field_unit_object.get_index()
                # opponent_field_card_id = opponent_field_unit_object.get_card_number()
                # your_field_card_index = self.targeting_enemy_select_using_your_field_card_index
                # your_extra_ability = self.your_field_unit_repository.get_your_unit_extra_ability_at_index(
                #     your_field_card_index)
                #
                # for opponent_attached_shape in opponent_attached_shape_list:
                #     if isinstance(opponent_attached_shape, NonBackgroundNumberImage):
                #         if opponent_attached_shape.get_circle_kinds() is CircleKinds.HP:
                #             current_opponent_hp_number = opponent_attached_shape.get_number()
                #             current_opponent_hp_number -= animation_actor_skill_damage
                #
                #             if current_opponent_hp_number <= 0:
                #                 are_opponent_field_unit_death = True
                #
                #                 break
                #
                #             print(f"공격 후 opponent unit 체력 -> hp_number: {current_opponent_hp_number}")
                #             opponent_attached_shape.set_number(current_opponent_hp_number)
                #
                #             # opponent_fixed_card_attached_shape.set_image_data(
                #             #     # TODO: 실제로 여기서 서버로부터 계산 받은 값을 적용해야함
                #             #     self.pre_drawed_image_instance.get_pre_draw_number_image(opponent_hp_number))
                #
                #             opponent_attached_shape.set_image_data(
                #                 self.pre_drawed_image_instance.get_pre_draw_unit_hp(current_opponent_hp_number))
                #
                #             if your_extra_ability:
                #                 self.opponent_field_unit_repository.apply_harmful_status(opponent_field_card_index,
                #                                                                          your_extra_ability)
                #
                # print(f"opponent_field_card_index: {opponent_field_card_index}")
                #
                # if are_opponent_field_unit_death is True:
                #     def remove_field_unit_by_index():
                #         self.opponent_field_unit_repository.remove_card_by_multiple_index(
                #             [opponent_field_card_index])
                #         self.opponent_tomb_repository.create_opponent_tomb_card(
                #             opponent_field_card_id)
                #         self.opponent_field_unit_repository.remove_harmful_status_by_index(opponent_field_card_index)
                #
                #         self.opponent_field_unit_repository.replace_opponent_field_unit_card_position()
                #
                #     self.create_effect_animation_to_opponent_unit_and_play_animation_and_call_function('death',
                #                                                                                        opponent_field_card_index,
                #                                                                                        remove_field_unit_by_index)
                #
                # # self.opponent_fixed_unit_card_inside_handler.clear_opponent_field_area_action()
                # # self.targeting_enemy_select_using_your_field_card_index = None
                # # self.targeting_enemy_select_using_your_field_card_id = None
                # # self.targeting_enemy_select_support_lightning_border_list = []
                # # self.opponent_you_selected_lightning_border_list = []
                # #
                # # self.selected_object = None
                # # self.active_panel_rectangle = None
                # # self.current_fixed_details_card = None
                # # self.your_active_panel.clear_all_your_active_panel()
                self.reset_every_selected_action()
                self.targeting_enemy_select_using_your_field_card_id = None

                self.field_area_inside_handler.clear_field_area_action()

        move_to_origin_location(1)

    def opponent_attack_main_character_animation(self):
        self.is_playing_action_animation = True
        steps = 20
        attack_animation_object = AttackAnimation.getInstance()

        notify_data = attack_animation_object.get_notify_data()
        print(f"{Fore.RED}notify_data: {Fore.GREEN} {notify_data}{Style.RESET_ALL}")

        # opponent_animation_actor = notify_data['player_field_unit_attack_map']['Opponent']['field_unit_attack_map']['1']
        opponent_animation_actor_index = int(next(iter(notify_data['player_field_unit_attack_map']['Opponent']['field_unit_attack_map'])))
        # field_unit_attack = notify_data['player_field_unit_attack_map']['Opponent']['field_unit_attack_map'][str(opponent_animation_actor_index)]

        # opponent_animation_actor_index = next(iter(notify_data['player_field_unit_attack_map']['Opponent']['field_unit_attack_map'].values()))
        opponent_animation_actor = self.opponent_field_unit_repository.find_opponent_field_unit_by_index(opponent_animation_actor_index)
        attack_animation_object.set_opponent_animation_actor(opponent_animation_actor)

        opponent_animation_actor = attack_animation_object.get_opponent_animation_actor()
        animation_actor_card_id = opponent_animation_actor.get_card_number()

        opponent_fixed_card_base = opponent_animation_actor.get_fixed_card_base()
        current_opponent_attacker_unit_vertices = opponent_fixed_card_base.get_vertices()
        current_opponent_attacker_unit_local_translation = opponent_fixed_card_base.get_local_translation()
        print(f"{Fore.RED}current_opponent_attacker_unit_local_translation{Fore.GREEN} {current_opponent_attacker_unit_local_translation}{Style.RESET_ALL}")

        new_y_value = current_opponent_attacker_unit_local_translation[1] + 30
        opponent_attacker_unit_destination_local_translation = (current_opponent_attacker_unit_local_translation[0], new_y_value)

        step_x = (opponent_attacker_unit_destination_local_translation[0] - current_opponent_attacker_unit_local_translation[0]) / steps
        step_y = (opponent_attacker_unit_destination_local_translation[1] - current_opponent_attacker_unit_local_translation[1]) / steps
        step_y *= -1

        # new_y_value = current_opponent_attacker_unit_local_translation[1] + 30
        # opponent_attacker_unit_destination_local_translation = (current_opponent_attacker_unit_local_translation[0], new_y_value)

        your_main_character = attack_animation_object.get_your_main_character()
        your_main_character_vertices = your_main_character.get_vertices()
        print(f"{Fore.RED}your_main_character_vertices: {Fore.GREEN}{your_main_character_vertices}{Style.RESET_ALL}")

        angle_radians = math.radians(-65)
        bias_result = 85 * math.cos(angle_radians)

        your_main_character_destination_y = your_main_character_vertices[0][1]
        your_main_character_destination_x = your_main_character_vertices[0][0] - 105 - bias_result
        opponent_biased_local_translation = 0

        # S = v0 * t + 0.5 * a * t^2
        # S = 0.5 * a * t^2 => step = 20
        # S = 0.5 * a * 400 => a = xxx / 200
        sword_accel_y = (current_opponent_attacker_unit_local_translation[1] - your_main_character_destination_y) / 200
        print(f"{Fore.RED}sword_accel_y: {Fore.GREEN}{sword_accel_y}{Style.RESET_ALL}")
        # sword_accel_y *= -1

        # 370 - 215 = 155 -> 310 / 225
        sword_accel_x = (your_main_character_destination_x - current_opponent_attacker_unit_local_translation[0]) / 200
        print(f"{Fore.RED}sword_accel_x: {Fore.GREEN}{sword_accel_x}{Style.RESET_ALL}")

        def update_position(step_count):
            new_x = current_opponent_attacker_unit_local_translation[0] + step_x * step_count
            new_y = current_opponent_attacker_unit_local_translation[1] + step_y * step_count

            new_vertices = [
                (vx + step_x * step_count, vy + step_y * step_count) for vx, vy in current_opponent_attacker_unit_vertices
            ]
            opponent_fixed_card_base.update_vertices(new_vertices)

            # tool_card = self.selected_object.get_tool_card()
            # if tool_card is not None:
            #     new_tool_card_vertices = [
            #         (vx + new_x, vy + new_y) for vx, vy in tool_card.vertices
            #     ]
            #     tool_card.update_vertices(new_tool_card_vertices)

            for attached_shape in opponent_fixed_card_base.get_attached_shapes():
                # theta = w0 * t + 0.5 * alpha * t^2
                # theta = 0.5 * alpha * t^2 => step_count = 15
                # theta = 0.5 * alpha * 225 = 65 / 225 = 0.28888
                # theta = 0.5 * alpha * 400 = 65 / 400 = 0.1625
                omega_accel_alpha = -0.1625

                if isinstance(attached_shape, NonBackgroundNumberImage):
                    if attached_shape.get_circle_kinds() is CircleKinds.ATTACK:
                        accel_y_dist = sword_accel_y * step_count
                        accel_y_dist *= -1

                        accel_x_dist = sword_accel_x * step_count
                        # x: 236 / 1920, y: -367 / 1043
                        new_attached_shape_vertices = [
                            (vx + accel_x_dist, vy + accel_y_dist) for vx, vy in attached_shape.vertices
                        ]
                        attached_shape.update_vertices(new_attached_shape_vertices)
                        attached_shape.update_rotation_angle(omega_accel_alpha * step_count * step_count)
                        print(f"{Fore.RED}sword new_attached_shape_vertices{Fore.GREEN} {new_attached_shape_vertices}{Style.RESET_ALL}")

                        if step_count == 20:
                            attack_animation_object.set_opponent_weapon_shape(attached_shape)

                        continue

                new_attached_shape_vertices = [
                    (vx + step_x, vy + step_y) for vx, vy in attached_shape.vertices
                ]
                attached_shape.update_vertices(new_attached_shape_vertices)
                # print(f"{Fore.RED}new_attached_shape_vertices: {Fore.GREEN}{new_attached_shape_vertices}{Style.RESET_ALL}")

            if step_count < steps:
                self.master.after(20, update_position, step_count + 1)
                if step_count == 8 and self.card_info_repository.getCardJobForCardNumber(animation_actor_card_id) == 2:
                    self.__music_player_repository.play_sound_effect_with_event_name('magician_basic_attack')
            else:
                self.start_opponent_attack_main_character_post_animation(attack_animation_object)

        update_position(1)

    def start_opponent_attack_main_character_post_animation(self, attack_animation_object):
        sword_shape = attack_animation_object.get_opponent_weapon_shape()
        your_main_character = attack_animation_object.get_your_main_character()
        your_main_character_vertices = your_main_character.get_vertices()

        opponent_animation_actor = attack_animation_object.get_opponent_animation_actor()
        animation_actor_card_id = opponent_animation_actor.get_card_number()

        steps = 30
        # (390 - 153) / 1848 = 0.1282
        sword_shape_vertices = sword_shape.get_vertices()
        need_to_moving_distance_x = your_main_character_vertices[1][0] - your_main_character_vertices[0][0]
        # sword_target_x = 0.1282 * attack_animation_object.get_total_width()
        print(f"{Fore.RED}need_to_moving_distance_x:{Fore.GREEN} {need_to_moving_distance_x}{Style.RESET_ALL}")

        # S = v0 * t + 0.5 * a * t^2
        # S = 0.5 * a * t^2 => step = 10
        # S = 0.5 * a * 100 = sword_target_x / 50
        sword_accel_x = need_to_moving_distance_x / 50
        print(f"{Fore.RED}sword_accel_x{Fore.GREEN} {sword_accel_x}{Style.RESET_ALL}")

        # theta = w0 * t + 0.5 * alpha * t^2
        # theta = 0.5 * alpha * t^2 => step_count = 10
        # theta = 0.5 * alpha * 100 = 30 / 50 = 0.6
        omega_accel_alpha = 0.3

        opponent_field_unit = self.attack_animation_object.get_opponent_animation_actor()

        def moving_action(step_count):
            if step_count == 1:
                if self.card_info_repository.getCardJobForCardNumber(animation_actor_card_id) == 1:
                    self.__music_player_repository.play_sound_effect_with_event_name('warrior_basic_attack')
                # elif self.card_info_repository.getCardJobForCardNumber(animation_actor_card_id) == 2:
                #     self.__music_player_repository.play_sound_effect_with_event_name_for_wav('magician_basic_attack')
            if step_count < 11:
                sword_accel_x_dist = sword_accel_x * step_count

                new_attached_shape_vertices = [
                    (vx + sword_accel_x_dist, vy) for vx, vy in sword_shape.vertices
                ]
                sword_shape.update_vertices(new_attached_shape_vertices)

                current_angle = sword_shape.get_rotation_angle()
                sword_shape.update_rotation_angle(current_angle + omega_accel_alpha * step_count * step_count)

            if step_count > 2:
                if step_count % 2 == 1:
                    vibration_factor = 10
                    random_translation = (random.uniform(-vibration_factor, vibration_factor),
                                          random.uniform(-vibration_factor, vibration_factor))

                    for battle_field_background_shape in self.battle_field_background_shape_list:
                        battle_field_background_shape.global_translate((random_translation[0], random_translation[1]))

                else:
                    for battle_field_background_shape in self.battle_field_background_shape_list:
                        battle_field_background_shape.global_translate((0, 0))

            if step_count < steps:
                self.master.after(20, moving_action, step_count + 1)
            else:


                self.finish_opponent_attack_main_character_post_animation(attack_animation_object)

        # self.play_effect_animation_by_index(attack_animation_object.get_opponent_animation_actor().get_index())
        opponent_field_card_id = opponent_field_unit.get_card_number()
        opponent_field_unit_job_number = self.card_info_repository.getCardJobForCardNumber(opponent_field_card_id)
        effect_animation_name = ''
        for attack_type in AttackType:
            if attack_type.value == opponent_field_unit_job_number:
                effect_animation_name = attack_type.name
                print('effect animation name: ', effect_animation_name)
                break

        effect_animation = EffectAnimation()
        effect_animation.set_animation_name(effect_animation_name)
        effect_animation.set_total_window_size(self.width, self.height)
        vertices = self.your_main_character_panel.get_vertices()
        effect_animation.draw_animation_panel_with_vertices(vertices)
        effect_animation_panel = effect_animation.get_animation_panel()

        animation_index = self.effect_animation_repository.save_effect_animation_at_dictionary_without_index_and_return_index(
            effect_animation)

        self.effect_animation_repository.save_effect_animation_panel_at_dictionary_with_index(
            animation_index, effect_animation_panel)

        self.play_effect_animation_by_index(animation_index)
        moving_action(1)

    def finish_opponent_attack_main_character_post_animation(self, attack_animation_object):
        sword_shape = attack_animation_object.get_opponent_weapon_shape()

        animation_actor = attack_animation_object.get_opponent_animation_actor()
        opponent_fixed_card_base = animation_actor.get_fixed_card_base()
        tool_card = animation_actor.get_tool_card()
        attached_shape_list = opponent_fixed_card_base.get_attached_shapes()

        current_opponent_attacker_unit_vertices = opponent_fixed_card_base.get_vertices()
        current_opponent_attacker_unit_local_translation = opponent_fixed_card_base.get_local_translation()

        new_y_value = current_opponent_attacker_unit_local_translation[1] + 30
        opponent_attacker_unit_destination_local_translation = (
        current_opponent_attacker_unit_local_translation[0], new_y_value)

        steps = 15
        step_y = (opponent_attacker_unit_destination_local_translation[1] - current_opponent_attacker_unit_local_translation[1]) / steps
        step_y *= -1

        # (390 - 153) / 1848 = 0.1282
        current_sword_shape = attack_animation_object.get_opponent_weapon_shape()
        current_sword_shape_target = current_sword_shape.get_initial_vertices()

        current_sword_shape_target_x = current_sword_shape_target[0][0]
        current_sword_shape_target_y = current_sword_shape_target[0][1]

        # theta = w0 * t + 0.5 * alpha * t^2
        # theta = 0.5 * alpha * t^2 => step_count = 15
        # theta = 0.5 * alpha * 225 = angle / 112.5
        target_rotation_angle = sword_shape.get_rotation_angle()
        return_omega_accel_alpha = target_rotation_angle / 112.5

        current_sword_shape_vertices = current_sword_shape.get_vertices()
        current_sword_shape_x_vertex = current_sword_shape_vertices[0][0]
        current_sword_shape_y_vertex = current_sword_shape_vertices[0][1]

        sword_accel_x = (current_sword_shape_x_vertex - current_sword_shape_target_x - 52.5 + 15) / 112.5
        sword_accel_y = (current_sword_shape_y_vertex - current_sword_shape_target_y + 85 - 60) / 112.5

        def move_to_origin_location(step_count):
            new_y = current_opponent_attacker_unit_local_translation[1] + step_y * step_count
            print(f"{Fore.RED}step ->{Fore.GREEN}new_y: {new_y}{Style.RESET_ALL}")

            new_vertices = [
                (vx, vy - step_y * step_count) for vx, vy in current_opponent_attacker_unit_vertices
            ]
            opponent_fixed_card_base.update_vertices(new_vertices)
            print(f"{Fore.RED}new_vertices{Fore.GREEN} {new_vertices}{Style.RESET_ALL}")

            # tool_card = self.selected_object.get_tool_card()
            # if tool_card is not None:
            #     new_tool_card_vertices = [
            #         (vx + new_x, vy + new_y) for vx, vy in tool_card.vertices
            #     ]
            #     tool_card.update_vertices(new_tool_card_vertices)

            for attached_shape in opponent_fixed_card_base.get_attached_shapes():
                # theta = w0 * t + 0.5 * alpha * t^2
                # theta = 0.5 * alpha * t^2 => step_count = 15
                # theta = 0.5 * alpha * 225 = 65 / 225 = 0.28888
                omega_accel_alpha = -0.28888

                if isinstance(attached_shape, NonBackgroundNumberImage):
                    if attached_shape.get_circle_kinds() is CircleKinds.ATTACK:
                        current_sword_shape_vertices = current_sword_shape.get_vertices()

                        current_sword_shape_x_vertex = current_sword_shape_vertices[0][0]
                        current_sword_shape_y_vertex = current_sword_shape_vertices[0][1]

                        # S = v0 * t + 0.5 * a * t^2
                        # S = 0.5 * a * t^2 => step = 15
                        # S = 0.5 * a * 225 = distance / 112.5
                        # 225 = (steps * steps)

                        # difference_x: 11.434448575145638, difference_y: 94.0313609929536

                        # sword_accel_x = (current_sword_shape_target_x - current_sword_shape_x_vertex - 195) / 112.5
                        # sword_accel_x = (current_sword_shape_x_vertex - current_sword_shape_target_x) / 112.5
                        # sword_accel_y = (current_sword_shape_target_y - current_sword_shape_y_vertex + 124.732391723) / 112.5
                        print(f"{Fore.RED}sword_accel -> {Fore.GREEN}x: {sword_accel_x}, y: {sword_accel_y}{Style.RESET_ALL}")

                        sword_accel_x_dist = sword_accel_x * step_count
                        sword_accel_y_dist = sword_accel_y * step_count

                        new_attached_shape_vertices = [
                            (vx - sword_accel_x_dist, vy - sword_accel_y_dist) for vx, vy in sword_shape.vertices
                        ]
                        sword_shape.update_vertices(new_attached_shape_vertices)
                        # print(f"{Fore.RED}new_attached_shape_vertices: {Fore.GREEN}{new_attached_shape_vertices}{Style.RESET_ALL}")

                        current_angle = sword_shape.get_rotation_angle()
                        sword_shape.update_rotation_angle(current_angle - return_omega_accel_alpha * step_count)

                        continue

                new_attached_shape_vertices = [
                    (vx, vy - step_y) for vx, vy in attached_shape.vertices
                ]
                attached_shape.update_vertices(new_attached_shape_vertices)

            if step_count < steps:
                self.master.after(20, move_to_origin_location, step_count + 1)
            else:
                self.is_playing_action_animation = False
                opponent_fixed_card_base.update_vertices(opponent_fixed_card_base.get_initial_vertices())
                if tool_card is not None:
                    tool_card.update_vertices(tool_card.get_initial_vertices())
                for attached_shape in attached_shape_list:
                    attached_shape.update_vertices(attached_shape.get_initial_vertices())

                self.is_attack_motion_finished = True
                attack_animation_object.set_is_finished(True)
                self.opponent_field_area_inside_handler.set_active_field_area_action(OpponentFieldAreaActionProcess.Dummy)

                notify_data = attack_animation_object.get_notify_data()

                # opponent_damage = attack_animation_object.get_opponent_animation_actor_damage()
                health_point = notify_data['player_main_character_health_point_map']['You']
                self.your_hp_repository.change_hp(int(health_point))
                if self.your_hp_repository.get_your_character_survival_info() == SurvivalType.DEATH:
                    self.battle_field_repository.lose()

                self.attack_animation_object.set_opponent_animation_actor(None)


        move_to_origin_location(1)

    def apply_response_data_of_field_unit_hp(self, player_field_unit_health_point_data):
        print('apply notify data of field unit hp!! : ', player_field_unit_health_point_data)

        for player, hp_map in player_field_unit_health_point_data.items():
            for unit_index, remain_hp in hp_map['field_unit_health_point_map'].items():
                if remain_hp <= 0:
                    continue
                print(unit_index)
                if player == 'You':
                    field_unit = self.your_field_unit_repository.find_field_unit_by_index(int(unit_index))
                    if field_unit == None:
                        continue
                    fixed_card_base = field_unit.get_fixed_card_base()
                    fixed_card_attached_shape_list = fixed_card_base.get_attached_shapes()

                    for fixed_card_attached_shape in fixed_card_attached_shape_list:
                        if isinstance(fixed_card_attached_shape, NonBackgroundNumberImage):
                            if fixed_card_attached_shape.get_circle_kinds() is CircleKinds.HP:
                                fixed_card_attached_shape.set_number(remain_hp)
                                fixed_card_attached_shape.set_image_data(
                                    self.pre_drawed_image_instance.get_pre_draw_unit_hp(remain_hp))

                elif player == 'Opponent':
                    field_unit = self.opponent_field_unit_repository.find_opponent_field_unit_by_index(int(unit_index))
                    if field_unit == None:
                        continue
                    fixed_card_base = field_unit.get_fixed_card_base()
                    fixed_card_attached_shape_list = fixed_card_base.get_attached_shapes()

                    for fixed_card_attached_shape in fixed_card_attached_shape_list:
                        if isinstance(fixed_card_attached_shape, NonBackgroundNumberImage):
                            if fixed_card_attached_shape.get_circle_kinds() is CircleKinds.HP:
                                fixed_card_attached_shape.set_number(remain_hp)
                                fixed_card_attached_shape.set_image_data(
                                    self.pre_drawed_image_instance.get_pre_draw_unit_hp(remain_hp))



    def apply_response_data_of_dead_unit(self, player_field_unit_death_data):

        for player, dead_field_unit_index_list_map in player_field_unit_death_data.items():
            dead_field_unit_index_list = dead_field_unit_index_list_map.get('dead_field_unit_index_list', [])
            if len(dead_field_unit_index_list) == 0:
                continue

            if player == 'You':
                for unit_index in dead_field_unit_index_list:
                    card_id = self.your_field_unit_repository.get_card_id_by_index(unit_index)
                    self.your_tomb_repository.create_tomb_card(card_id)
                    self.your_field_unit_repository.remove_card_by_index(unit_index)
                    self.your_field_unit_repository.remove_harmful_status_by_index(unit_index)
                self.your_field_unit_repository.replace_field_card_position()
            elif player == 'Opponent':
                for unit_index in dead_field_unit_index_list:
                    card_id = self.opponent_field_unit_repository.get_opponent_card_id_by_index(unit_index)
                    self.opponent_tomb_repository.create_opponent_tomb_card(card_id)
                    self.opponent_field_unit_repository.remove_current_field_unit_card(unit_index)
                    self.opponent_field_unit_repository.remove_harmful_status_by_index(unit_index)

                self.opponent_field_unit_repository.replace_opponent_field_unit_card_position()

            else:
                print(f'apply_notify_data_of_dead_unit error : unknown player {player}')

    def apply_response_data_of_harmful_status(self, player_field_unit_harmful_effect_data):

        try:
            for player, field_data in player_field_unit_harmful_effect_data.items():
                for unit_index, harmful_status_value in field_data.get('field_unit_harmful_status_map', {}).items():
                    harmful_status_list = harmful_status_value.get('harmful_status_list', [])
                    if len(harmful_status_list) == 0:
                        continue

                    if player == 'Opponent':
                        self.opponent_field_unit_repository.apply_harmful_status(int(unit_index), harmful_status_list)
                    elif player == 'You':
                        self.your_field_unit_repository.apply_harmful_status(int(unit_index), harmful_status_list)
        except Exception as e:
            print('An error occurred while applying harmful status data:', e)

    def play_harmful_effect_animation(self, repository,index, harmful_effect_animation):

        def animate():
            if repository.get_is_index_in_harmful_status(index):
                harmful_effect_animation.update_harmful_effect_animation_panel()

            else:
                harmful_effect_animation.is_finished = True

            if not harmful_effect_animation.is_finished:
                self.master.after(17, animate)
            else:
                print("harmful_effect_animation finish")

        harmful_effect_animation.reset_animation_count()
        self.master.after(0, animate)


    def play_effect_animation(self):
        if self.is_effect_animation_playing:
            return

        def animate():
            self.is_effect_animation_playing = True
            finish_list = []
            is_all_finished = False
            for effect_animation in self.effect_animation_repository.get_effect_animation_list():
                effect_animation.update_effect_animation_panel()
                finish_list.append(effect_animation.is_finished)

            for finish in finish_list:
                if finish == False:
                    is_all_finished = False
                    break
                else:
                    is_all_finished = True

            if not is_all_finished:
                self.master.after(17, animate)
            else:
                self.effect_animation_repository.reset_all_effect_animation()
                self.is_effect_animation_playing = False
                print("finish animation")

        for effect_animation in self.effect_animation_repository.get_effect_animation_list():
            print(f"animation count: {effect_animation}")
            effect_animation.reset_animation_count()

        self.master.after(0, animate)

    def play_effect_animation_by_index(self, index):

        def animate():
            effect_animation = self.effect_animation_repository.get_effect_animation_by_index(index)
            effect_animation.update_effect_animation_panel()
            print('is finished?? ',effect_animation.is_finished)
            if not effect_animation.is_finished:
                self.master.after(17, animate)
            else:
                self.effect_animation_repository.remove_effect_animation_by_index(index)
                print("finish animation")



        print(f"animation playing at index : {index}")
        effect_animation = self.effect_animation_repository.get_effect_animation_by_index(index)
        print(f"effect_animation : {effect_animation}")
        effect_animation.reset_animation_count()

        self.master.after(0, animate)

    def play_effect_animation_with_acceleration_by_index_and_call_function(self, index, function, need_to_move_acceleration_distance):
        step_count = [0]

        def animate():
            effect_animation = self.effect_animation_repository.get_effect_animation_by_index(index)
            effect_animation.update_effect_animation_panel_with_acceleration(need_to_move_acceleration_distance, step_count[0])

            if not effect_animation.is_finished:
                step_count[0] += 1
                self.master.after(17, animate)
            else:
                self.effect_animation_repository.remove_effect_animation_by_index(index)
                function()
                print("finish animation")

        print(f"animation playing at index : {index}")
        effect_animation = self.effect_animation_repository.get_effect_animation_by_index(index)
        print(f"effect_animation : {effect_animation}")
        effect_animation.reset_animation_count()

        self.master.after(0, animate)

    def play_effect_animation_by_index_and_call_function(self, index, function):

        def animate():
            effect_animation = self.effect_animation_repository.get_effect_animation_by_index(index)
            effect_animation.update_effect_animation_panel()
            if not effect_animation.is_finished:
                self.master.after(17, animate)
            else:
                self.effect_animation_repository.remove_effect_animation_by_index(index)
                if function:
                    function()
                print("finish animation")

        print(f"animation playing at index : {index}")
        effect_animation = self.effect_animation_repository.get_effect_animation_by_index(index)
        print(f"effect_animation : {effect_animation}")
        effect_animation.reset_animation_count()

        self.master.after(0, animate)


    def play_effect_animation_by_index_and_call_function_with_param(self, index, function, param, need_delay = False):

        def animate():
            effect_animation = self.effect_animation_repository.get_effect_animation_by_index(index)
            effect_animation.update_effect_animation_panel()
            if not effect_animation.is_finished:
                self.master.after(17, animate)
            else:

                self.effect_animation_repository.remove_effect_animation_by_index(index)
                function(param)
                print("finish animation")

        print(f"animation playing at index : {index}")
        effect_animation = self.effect_animation_repository.get_effect_animation_by_index(index)
        print(f"effect_animation : {effect_animation}")
        effect_animation.reset_animation_count()

        if need_delay:
            self.master.after(2000, animate)
        else:
            self.master.after(0, animate)
        
        
    def create_effect_animation_to_opponent_unit_and_play_animation_and_call_function(self, effect_name, index, function):
        effect_animation = EffectAnimation()
        effect_animation.set_animation_name(effect_name)
        effect_animation.set_total_window_size(self.width, self.height)
        effect_animation.change_local_translation(self.opponent_field_unit_repository.find_opponent_field_unit_by_index(
            index).get_fixed_card_base().get_local_translation())
        effect_animation.draw_animation_panel()
        effect_animation_panel = effect_animation.get_animation_panel()

        animation_index = self.effect_animation_repository.save_effect_animation_at_dictionary_without_index_and_return_index(
            effect_animation)

        self.effect_animation_repository.save_effect_animation_panel_at_dictionary_with_index(
            animation_index, effect_animation_panel)

        self.__music_player_repository.play_sound_effect_of_card_execution(effect_name)

        self.play_effect_animation_by_index_and_call_function(animation_index, function)


    def create_effect_animation_to_opponent_unit_and_play_animation_and_call_function_with_param(self, effect_name, index, function, param):
        effect_animation = EffectAnimation()
        effect_animation.set_animation_name(effect_name)
        effect_animation.set_total_window_size(self.width, self.height)
        effect_animation.change_local_translation(self.opponent_field_unit_repository.find_opponent_field_unit_by_index(
            index).get_fixed_card_base().get_local_translation())
        effect_animation.draw_animation_panel()
        effect_animation_panel = effect_animation.get_animation_panel()

        animation_index = self.effect_animation_repository.save_effect_animation_at_dictionary_without_index_and_return_index(
            effect_animation)

        self.effect_animation_repository.save_effect_animation_panel_at_dictionary_with_index(
            animation_index, effect_animation_panel)


        self.play_effect_animation_by_index_and_call_function_with_param(animation_index, function, param)

    def create_effect_animation_to_full_screen_and_play_animation_and_call_function_with_param(self, effect_name, function, param):
        effect_animation = EffectAnimation()
        effect_animation.set_animation_name(effect_name)
        effect_animation.set_total_window_size(self.width, self.height)

        effect_animation.draw_full_screen_animation_panel()
        effect_animation_panel = effect_animation.get_animation_panel()
        animation_index = self.effect_animation_repository.save_effect_animation_at_dictionary_without_index_and_return_index(
            effect_animation)
        self.effect_animation_repository.save_effect_animation_panel_at_dictionary_with_index(
            animation_index, effect_animation_panel)

        self.play_effect_animation_by_index_and_call_function_with_param(animation_index, function, param)

    # def create_effect_animation_to_opponent_field_and_play_animation_and_call_function_with_param_full_transparency(self, effect_name, function, param):
    #     effect_animation = EffectAnimation()
    #     effect_animation.set_animation_name(effect_name)
    #     effect_animation.set_total_window_size(self.width, self.height)
    #     field_vertices = self.opponent_field_panel.get_vertices()
    #     main_character_vertices = self.opponent_main_character_panel.get_vertices()
    #     vertices = [(field_vertices[0][0], main_character_vertices[0][1]),
    #                 (field_vertices[2][0], main_character_vertices[1][1]),
    #                 field_vertices[3], field_vertices[0]]
    #
    #     effect_animation.draw_animation_panel_with_vertices(vertices)
    #     effect_animation_panel = effect_animation.get_animation_panel()
    #     effect_animation_panel.set_alpha(1.0)
    #     animation_index = self.effect_animation_repository.save_effect_animation_at_dictionary_without_index_and_return_index(
    #         effect_animation)
    #     self.effect_animation_repository.save_effect_animation_panel_at_dictionary_with_index(
    #         animation_index, effect_animation_panel)
    #
    #     self.play_effect_animation_by_index_and_call_function_with_param(animation_index, function, param)

    def create_effect_animation_to_opponent_field_and_play_animation_and_call_function_with_param(self, effect_name, function, param):
        effect_animation = EffectAnimation()
        effect_animation.set_animation_name(effect_name)
        effect_animation.set_total_window_size(self.width, self.height)
        field_vertices = self.opponent_field_panel.get_vertices()
        main_character_vertices = self.opponent_main_character_panel.get_vertices()
        vertices = [(field_vertices[0][0], main_character_vertices[0][1]),
                    (field_vertices[2][0], main_character_vertices[1][1]),
                    field_vertices[3], field_vertices[0]]

        effect_animation.draw_animation_panel_with_vertices(vertices)
        effect_animation_panel = effect_animation.get_animation_panel()
        animation_index = self.effect_animation_repository.save_effect_animation_at_dictionary_without_index_and_return_index(
            effect_animation)
        self.effect_animation_repository.save_effect_animation_panel_at_dictionary_with_index(
            animation_index, effect_animation_panel)

        self.play_effect_animation_by_index_and_call_function_with_param(animation_index, function, param)

    def reset_every_selected_action(self):
        self.opponent_fixed_unit_card_inside_handler.clear_opponent_field_area_action()
        self.targeting_enemy_select_using_your_field_card_index = None
        self.targeting_enemy_select_using_your_field_card_id = None
        self.targeting_enemy_select_support_lightning_border_list = []
        self.opponent_you_selected_lightning_border_list = []

        self.selected_object = None
        self.active_panel_rectangle = None
        self.current_fixed_details_card = None
        self.opponent_selected_object = None
        self.your_active_panel.clear_all_your_active_panel()

        self.field_area_inside_handler.clear_lightning_border_list()
        self.your_field_unit_lightning_border_list.clear()
        self.opponent_fixed_unit_card_inside_handler.clear_lightning_border_list()

        self.opponent_details_panel_rectangle = None
        self.opponent_details_panel.clear_all_opponent_details_panel()

        self.your_hand_details_panel_rectangle = None
        self.your_hand_details_panel.clear_all_your_hand_details_panel()

        # self.lightning_border.remove_lightning_border()

    def create_effect_animation_with_vertices_and_play_animation_and_call_function(self, effect_name, vertices, function):
        effect_animation = EffectAnimation()
        effect_animation.set_animation_name(effect_name)
        effect_animation.set_total_window_size(self.width, self.height)
        effect_animation.draw_animation_panel_with_vertices(vertices)
        effect_animation_panel = effect_animation.get_animation_panel()

        animation_index = self.effect_animation_repository.save_effect_animation_at_dictionary_without_index_and_return_index(
            effect_animation)

        self.effect_animation_repository.save_effect_animation_panel_at_dictionary_with_index(
            animation_index, effect_animation_panel)

        self.__music_player_repository.play_sound_effect_of_card_execution(effect_name)

        self.play_effect_animation_by_index_and_call_function(animation_index, function)

    def create_effect_animation_with_vertices_and_play_animation_and_call_function_with_param(self, effect_name, vertices, function, param):
        effect_animation = EffectAnimation()
        effect_animation.set_animation_name(effect_name)
        effect_animation.set_total_window_size(self.width, self.height)
        effect_animation.draw_animation_panel_with_vertices(vertices)
        effect_animation_panel = effect_animation.get_animation_panel()

        animation_index = self.effect_animation_repository.save_effect_animation_at_dictionary_without_index_and_return_index(
            effect_animation)

        self.effect_animation_repository.save_effect_animation_panel_at_dictionary_with_index(
            animation_index, effect_animation_panel)

        self.play_effect_animation_by_index_and_call_function_with_param(animation_index, function, param)



    def create_effect_animation_to_your_unit_and_play_animation_and_call_function(self, effect_name, index, function):
        effect_animation = EffectAnimation()
        effect_animation.set_animation_name(effect_name)
        effect_animation.set_total_window_size(self.width, self.height)
        effect_animation.change_local_translation(self.your_field_unit_repository.find_field_unit_by_index(
            index).get_fixed_card_base().get_local_translation())
        effect_animation.draw_animation_panel()
        effect_animation_panel = effect_animation.get_animation_panel()

        animation_index = self.effect_animation_repository.save_effect_animation_at_dictionary_without_index_and_return_index(
            effect_animation)

        self.effect_animation_repository.save_effect_animation_panel_at_dictionary_with_index(
            animation_index, effect_animation_panel)

        if effect_name == 'dark_blast':
            self.__music_player_repository.play_sound_effect_of_card_execution('energy_burn')

        self.play_effect_animation_by_index_and_call_function(animation_index, function)

    def create_effect_animation_to_your_unit_and_play_animation_and_call_function_with_param(self, effect_name, index, function, param):
        effect_animation = EffectAnimation()
        effect_animation.set_animation_name(effect_name)
        effect_animation.set_total_window_size(self.width, self.height)
        effect_animation.change_local_translation(self.your_field_unit_repository.find_field_unit_by_index(
            index).get_fixed_card_base().get_local_translation())
        effect_animation.draw_animation_panel()
        effect_animation_panel = effect_animation.get_animation_panel()

        animation_index = self.effect_animation_repository.save_effect_animation_at_dictionary_without_index_and_return_index(
            effect_animation)

        self.effect_animation_repository.save_effect_animation_panel_at_dictionary_with_index(
            animation_index, effect_animation_panel)

        self.play_effect_animation_by_index_and_call_function_with_param(animation_index, function, param)

    def create_effect_animation_to_your_field_and_play_animation_and_call_function_with_param(self, effect_name, function, param):
        effect_animation = EffectAnimation()
        effect_animation.set_animation_name(effect_name)
        effect_animation.set_total_window_size(self.width, self.height)
        field_vertices = self.your_field_panel.get_vertices()
        main_character_vertices = self.your_main_character_panel.get_vertices()
        vertices = [field_vertices[1], field_vertices[2],
                    (field_vertices[3][0], main_character_vertices[2][1]),
                    (field_vertices[0][0], main_character_vertices[3][1])]

        effect_animation.draw_animation_panel_with_vertices(vertices)
        effect_animation_panel = effect_animation.get_animation_panel()
        animation_index = self.effect_animation_repository.save_effect_animation_at_dictionary_without_index_and_return_index(
            effect_animation)
        self.effect_animation_repository.save_effect_animation_panel_at_dictionary_with_index(
            animation_index, effect_animation_panel)

        self.play_effect_animation_by_index_and_call_function_with_param(animation_index, function, param)

    def start_first_turn(self):
        whose_turn = self.__notify_reader_repository.get_is_your_turn_for_check_fake_process()
        if whose_turn is True:
            self.timer_repository.set_function(self.call_turn_end)
            self.timer_repository.set_unit_timeout_function(self.targeting_skill_timeout)
            self.timer_repository.set_timer(60)
            self.timer.get_timer()
            self.timer.start_timer()
            self.message_on_the_screen.create_message_on_the_battle_screen(MessageNumber.YOUR_TURN.value)

        #     return
        #
        # def whose_turn_is_false():
        #     self.timer.stop_timer()
        #
        # self.timer_repository.set_function(whose_turn_is_false())
        # self.timer_repository.set_timer(60)
        # self.timer.get_timer()
        # self.timer.start_timer()

    def targeting_skill_timeout(self):
        print("패시브 타임아웃 확인")
        my_turn = self.__notify_reader_repository.get_is_your_turn_for_check_fake_process()
        if my_turn is False:
            return
        print("내 턴에만 되는지 확인용")
        if self.timer_repository.get_check_nether_blade_second_passive_targeting_animation() is True:
            print("전함 2차 네더 패시브")
            self.finish_nether_blade_second_passive_targeting_animation_timeout(self.attack_animation_object)
            self.reset_every_selected_action()

        if self.timer_repository.get_check_nether_blade_turn_start_second_passive_targeting_animation() is True:
            print("턴 시작 시 네더 패시브")
            self.finish_nether_blade_turn_start_second_passive_targeting_animation_timeout(self.attack_animation_object)
            self.reset_every_selected_action()
        else:
            self.reset_every_selected_action()

    def fake_opponent_turn_end(self):
        print("Opponent Turn을 종료합니다")
        turn_end_request_result = self.round_repository.request_turn_end(
            TurnEndRequest(
                self.__session_repository.get_second_fake_session_info()))
        print(f"turn_end_request_result: {turn_end_request_result}")
        # your_main_character_survival_state = (
        #     data)['player_main_character_survival_map']['You']

        if turn_end_request_result.get('player_main_character_survival_map', {}).get('Opponent', None) == 'Death':
            print(f"{Fore.RED}Fake Opponent win!{Style.RESET_ALL}")
            # self.your_hp_repository.your_character_die()
            self.timer.stop_timer()
            # self.battle_field_repository.win()
            return

        self.__notify_reader_repository.set_is_your_turn_for_check_fake_process(True)
        self.timer.stop_timer()
        self.timer_repository.set_timer(60)
        self.timer_repository.set_function(self.call_turn_end)
        self.timer.get_timer()
        self.timer.start_timer()

    def check_opponent_turn_end(self):
        my_turn = self.__notify_reader_repository.get_is_your_turn_for_check_fake_process()
        if my_turn is False:
            return
        print("Opponent Turn을 종료합니다")
        turn_end_request_result = self.round_repository.request_turn_end(
            TurnEndRequest(
                self.__session_repository.get_second_fake_session_info()))
        print(f"turn_end_request_result: {turn_end_request_result}")
        # your_main_character_survival_state = (
        #     data)['player_main_character_survival_map']['You']

        if turn_end_request_result.get('player_main_character_survival_map', {}).get('Opponent', None) == 'Death':
            print(f"{Fore.RED}Fake Opponent win!{Style.RESET_ALL}")
            # self.your_hp_repository.your_character_die()
            self.timer.stop_timer()
            # self.battle_field_repository.win()
            return

        if turn_end_request_result.get('is_success', False) == False:
            return

        if turn_end_request_result.get('is_success') is True:
            self.__notify_reader_repository.set_is_your_turn_for_check_fake_process(True)
            self.timer.stop_timer()
            self.timer_repository.set_timer(60)
            self.timer_repository.set_function(self.call_turn_end)
            self.timer.get_timer()
            self.timer.start_timer()

    def death_scythe_animation(self):

        data = self.attack_animation_object.get_notify_data()
        player_who_use_card = None
        player_who_targeted = None
        player_who_dead_unit = None
        for player_who_use_card_index in data['player_hand_use_map'].keys():
            player_who_use_card = player_who_use_card_index
            used_card_id = data['player_hand_use_map'][player_who_use_card]['card_id']

            # 카드를 사용 하고, 묘지로 보냄
            if player_who_use_card == "Opponent":
                self.opponent_tomb_repository.create_opponent_tomb_card(used_card_id)
            elif player_who_use_card == "You":
                self.your_tomb_repository.create_tomb_card(used_card_id)

            self.battle_field_repository.set_current_use_card_id(used_card_id)

        for player_who_targeted_index in data['player_field_unit_health_point_map'].keys():
            player_who_targeted = player_who_targeted_index

            for player_who_dead_unit_index in data['player_field_unit_death_map'].keys():
                player_who_dead_unit = player_who_dead_unit_index

                field_unit_health_point_map = (
                    data)['player_field_unit_health_point_map'][player_who_targeted]
                dead_field_unit_index_list_map = (
                    data)['player_field_unit_death_map'][player_who_dead_unit]
                dead_card_index_list = dead_field_unit_index_list_map["dead_field_unit_index_list"]

                # 필드 유닛 체력 맵 갱신
                if player_who_dead_unit == "Opponent":
                    def calculate_death_scythe_notify_data():

                        for unit_index, remaining_health_point in field_unit_health_point_map[
                            "field_unit_health_point_map"].items():

                            opponent_field_unit = self.opponent_field_unit_repository.find_opponent_field_unit_by_index(
                                int(unit_index))
                            opponent_fixed_card_base = opponent_field_unit.get_fixed_card_base()
                            opponent_fixed_card_attached_shape_list = opponent_fixed_card_base.get_attached_shapes()

                            if remaining_health_point <= 0:
                                continue

                            for opponent_fixed_card_attached_shape in opponent_fixed_card_attached_shape_list:
                                if isinstance(opponent_fixed_card_attached_shape, NonBackgroundNumberImage):
                                    if opponent_fixed_card_attached_shape.get_circle_kinds() is CircleKinds.HP:
                                        opponent_fixed_card_attached_shape.set_number(remaining_health_point)

                                        opponent_fixed_card_attached_shape.set_image_data(
                                            self.pre_drawed_image_instance.get_pre_draw_unit_hp(
                                                remaining_health_point))

                        for dead_unit_index in dead_card_index_list:
                            def remove_field_unit_by_index():
                                field_unit_id = self.opponent_field_unit_repository.get_opponent_card_id_by_index(
                                    dead_unit_index)
                                self.opponent_tomb_repository.create_opponent_tomb_card(field_unit_id)
                                self.opponent_field_unit_repository.remove_current_field_unit_card(dead_unit_index)
                                self.opponent_field_unit_repository.remove_harmful_status_by_index(dead_unit_index)
                                self.opponent_field_unit_repository.replace_opponent_field_unit_card_position()

                            self.create_effect_animation_to_opponent_unit_and_play_animation_and_call_function(
                                'death', dead_unit_index, remove_field_unit_by_index)
                            # effect_animation = EffectAnimation()
                            # effect_animation.set_animation_name('death')
                            # effect_animation.change_local_translation(
                            #     self.opponent_field_unit_repository.find_opponent_field_unit_by_index(
                            #         dead_unit_index).get_fixed_card_base().get_local_translation()
                            # )
                            # effect_animation.draw_animation_panel()
                            #
                            # self.__notify_reader_repository.save_notify_effect_animation_request(
                            #     EffectAnimationRequest(
                            #         effect_animation=effect_animation,
                            #         target_player=player_who_dead_unit,
                            #         target_index=dead_unit_index,
                            #         target_type=TargetType.UNIT,
                            #         call_function=remove_field_unit_by_index
                            #     )
                            # )

                    def vibration_death_scythe_opponent():
                        unit_index = int(list(field_unit_health_point_map["field_unit_health_point_map"].keys())[0])
                        steps = 30

                        field_unit_object = self.opponent_field_unit_repository.find_opponent_field_unit_by_index(unit_index)
                        fixed_card_base = field_unit_object.get_fixed_card_base()
                        tool_card = field_unit_object.get_tool_card()
                        attached_shape_list = fixed_card_base.get_attached_shapes()

                        def vibration(step_count):
                            if step_count % 2 == 1:
                                vibration_factor = 10
                                random_translation = (random.uniform(-vibration_factor, vibration_factor),
                                                      random.uniform(-vibration_factor, vibration_factor))

                                new_fixed_card_base_vertices = [
                                    (vx + random_translation[0], vy + random_translation[1]) for vx, vy in
                                    fixed_card_base.get_vertices()
                                ]
                                fixed_card_base.update_vertices(new_fixed_card_base_vertices)

                                if tool_card is not None:
                                    new_tool_card_vertices = [
                                        (vx + random_translation[0], vy + random_translation[1]) for vx, vy in
                                        tool_card.get_vertices()
                                    ]
                                    tool_card.update_vertices(new_tool_card_vertices)

                                for attached_shape in attached_shape_list:
                                    new_attached_shape_vertices = [
                                        (vx + random_translation[0], vy + random_translation[1]) for vx, vy in
                                        attached_shape.get_vertices()
                                    ]
                                    attached_shape.update_vertices(new_attached_shape_vertices)

                            else:
                                fixed_card_base.update_vertices(fixed_card_base.get_initial_vertices())
                                if tool_card is not None:
                                    tool_card.update_vertices(tool_card.get_initial_vertices())
                                for attached_shape in attached_shape_list:
                                    attached_shape.update_vertices(attached_shape.get_initial_vertices())

                            if step_count < steps:
                                self.master.after(20, vibration, step_count + 1)
                            else:
                                calculate_death_scythe_notify_data()

                        vibration(1)

                    unit_index = list(field_unit_health_point_map["field_unit_health_point_map"].keys())[0]

                    self.create_effect_animation_to_opponent_unit_and_play_animation_and_call_function(
                        'death_scythe', int(unit_index), vibration_death_scythe_opponent)

                    # effect_animation = EffectAnimation()
                    # effect_animation.set_animation_name('death_scythe')
                    # effect_animation.change_local_translation(
                    #     self.opponent_field_unit_repository.find_opponent_field_unit_by_index(
                    #         int(unit_index)).get_fixed_card_base().get_local_translation()
                    # )
                    # effect_animation.draw_animation_panel()
                    #
                    # self.__notify_reader_repository.save_notify_effect_animation_request(
                    #     EffectAnimationRequest(
                    #         effect_animation=effect_animation,
                    #         target_player=player_who_dead_unit,
                    #         target_index=int(unit_index),
                    #         target_type=TargetType.UNIT,
                    #         call_function=calculate_death_scythe_notify_data
                    #     )
                    # )



                elif player_who_dead_unit == "You":
                    def calculate_death_scythe_notify_data():
                        print('calculate_death_scythe_notify_data called!!')
                        for unit_index, remaining_health_point in field_unit_health_point_map[
                            "field_unit_health_point_map"].items():
                            your_field_unit = self.your_field_unit_repository.find_field_unit_by_index(
                                int(unit_index))
                            your_fixed_card_base = your_field_unit.get_fixed_card_base()
                            your_fixed_card_attached_shape_list = your_fixed_card_base.get_attached_shapes()

                            if remaining_health_point <= 0:
                                continue

                            for your_fixed_card_attached_shape in your_fixed_card_attached_shape_list:
                                if isinstance(your_fixed_card_attached_shape, NonBackgroundNumberImage):
                                    if your_fixed_card_attached_shape.get_circle_kinds() is CircleKinds.HP:
                                        your_fixed_card_attached_shape.set_number(remaining_health_point)

                                        your_fixed_card_attached_shape.set_image_data(
                                            self.pre_drawed_image_instance.get_pre_draw_unit_hp(
                                                remaining_health_point))

                        for dead_unit_index in dead_card_index_list:
                            def remove_field_unit_by_index(unit_index):
                                field_unit_id = self.your_field_unit_repository.get_card_id_by_index(unit_index)
                                self.your_tomb_repository.create_tomb_card(field_unit_id)
                                self.your_field_unit_repository.remove_card_by_index(unit_index)
                                self.your_field_unit_repository.remove_harmful_status_by_index(unit_index)
                                self.your_field_unit_repository.replace_field_card_position()

                            self.create_effect_animation_to_your_unit_and_play_animation_and_call_function_with_param(
                                'death', dead_unit_index, remove_field_unit_by_index, dead_unit_index)

                    def vibration_death_scythe_you():
                        unit_index = int(list(field_unit_health_point_map["field_unit_health_point_map"].keys())[0])
                        steps = 30

                        field_unit_object = self.your_field_unit_repository.find_field_unit_by_index(unit_index)
                        fixed_card_base = field_unit_object.get_fixed_card_base()
                        tool_card = field_unit_object.get_tool_card()
                        attached_shape_list = fixed_card_base.get_attached_shapes()

                        def vibration(step_count):
                            if step_count % 2 == 1:
                                vibration_factor = 10
                                random_translation = (random.uniform(-vibration_factor, vibration_factor),
                                                      random.uniform(-vibration_factor, vibration_factor))

                                new_fixed_card_base_vertices = [
                                    (vx + random_translation[0], vy + random_translation[1]) for vx, vy in
                                    fixed_card_base.get_vertices()
                                ]
                                fixed_card_base.update_vertices(new_fixed_card_base_vertices)

                                if tool_card is not None:
                                    new_tool_card_vertices = [
                                        (vx + random_translation[0], vy + random_translation[1]) for vx, vy in
                                        tool_card.get_vertices()
                                    ]
                                    tool_card.update_vertices(new_tool_card_vertices)

                                for attached_shape in attached_shape_list:
                                    new_attached_shape_vertices = [
                                        (vx + random_translation[0], vy + random_translation[1]) for vx, vy in
                                        attached_shape.get_vertices()
                                    ]
                                    attached_shape.update_vertices(new_attached_shape_vertices)

                            else:
                                fixed_card_base.update_vertices(fixed_card_base.get_initial_vertices())
                                if tool_card is not None:
                                    tool_card.update_vertices(tool_card.get_initial_vertices())
                                for attached_shape in attached_shape_list:
                                    attached_shape.update_vertices(attached_shape.get_initial_vertices())

                            if step_count < steps:
                                self.master.after(20, vibration, step_count + 1)
                            else:
                                calculate_death_scythe_notify_data()

                        vibration(1)

                    unit_index = list(field_unit_health_point_map["field_unit_health_point_map"].keys())[0]

                    self.create_effect_animation_to_your_unit_and_play_animation_and_call_function(
                        'death_scythe', int(unit_index), vibration_death_scythe_you)

    def energy_burn_animation(self):
        notify_dict_data = self.attack_animation_object.get_notify_data()

        hand_use_card_id = int(notify_dict_data.get("player_hand_use_map", {})
                               .get("Opponent", {})
                               .get("card_id", None))

        if notify_dict_data.get("player_field_unit_energy_map") != {}:
            # attach_energy_race_type = 0
            attach_race_energy_count = 0

            field_unit_index = list(notify_dict_data.get("player_field_unit_energy_map", {})
                                    .get("You", {})
                                    .get("field_unit_energy_map", {}).keys())[0]

            updated_total_energy_count = int(notify_dict_data.get("player_field_unit_energy_map", {})
                                             .get("You", {})
                                             .get("field_unit_energy_map", {})[field_unit_index]
                                             .get("total_energy_count"))

            if updated_total_energy_count != 0:
                # attach_total_energy_count = int(updated_total_energy_count)
                attach_energy_race = list(notify_dict_data.get("player_field_unit_energy_map", {})
                                          .get("You", {})
                                          .get("field_unit_energy_map", {})[field_unit_index]
                                          .get("attached_energy_map", {}).keys())[0]

                updated_race_energy_count = (notify_dict_data.get("player_field_unit_energy_map", {})
                .get("You", {})
                .get("field_unit_energy_map", {})[field_unit_index]
                .get("attached_energy_map", {})[attach_energy_race])

                # print(attach_race_energy_count)

                # attach_energy_race_type = int(attach_energy_race)
                attach_race_energy_count = int(updated_race_energy_count)
                print(f"attach_race_energy_count: {attach_race_energy_count}")

            field_unit_index = int(field_unit_index)

            self.battle_field_repository.set_current_use_card_id(hand_use_card_id)
            print("detach undead energy")

            def calculate_unit_energy_remove_item_card():

                before_attach_energy_count = self.your_field_unit_repository.get_your_field_unit_race_energy(
                    field_unit_index, EnergyType.Undead)

                difference_energy_count = before_attach_energy_count - attach_race_energy_count
                print(f"difference_energy_count: {difference_energy_count}")

                self.your_field_unit_repository.detach_race_energy(
                    field_unit_index,
                    EnergyType.Undead,
                    difference_energy_count)

                your_field_unit = self.your_field_unit_repository.find_field_unit_by_index(field_unit_index)
                total_attached_energy_count = self.your_field_unit_repository.get_total_energy_at_index(
                    field_unit_index)

                your_fixed_card_base = your_field_unit.get_fixed_card_base()
                your_fixed_card_attached_shape_list = your_fixed_card_base.get_attached_shapes()

                for your_fixed_card_attached_shape in your_fixed_card_attached_shape_list:
                    if isinstance(your_fixed_card_attached_shape, NonBackgroundNumberImage):
                        if your_fixed_card_attached_shape.get_circle_kinds() is CircleKinds.ENERGY:
                            your_fixed_card_attached_shape.set_image_data(
                                self.pre_drawed_image_instance.get_pre_draw_unit_energy(
                                    total_attached_energy_count))



            def vibration_energy_burn():
                steps = 30

                field_unit_object = self.your_field_unit_repository.find_field_unit_by_index(field_unit_index)
                fixed_card_base = field_unit_object.get_fixed_card_base()
                tool_card = field_unit_object.get_tool_card()
                attached_shape_list = fixed_card_base.get_attached_shapes()

                def vibration(step_count):
                    if step_count % 2 == 1:
                        vibration_factor = 10
                        random_translation = (random.uniform(-vibration_factor, vibration_factor),
                                              random.uniform(-vibration_factor, vibration_factor))

                        new_fixed_card_base_vertices = [
                            (vx + random_translation[0], vy + random_translation[1]) for vx, vy in
                            fixed_card_base.get_vertices()
                        ]
                        fixed_card_base.update_vertices(new_fixed_card_base_vertices)

                        if tool_card is not None:
                            new_tool_card_vertices = [
                                (vx + random_translation[0], vy + random_translation[1]) for vx, vy in
                                tool_card.get_vertices()
                            ]
                            tool_card.update_vertices(new_tool_card_vertices)

                        for attached_shape in attached_shape_list:
                            new_attached_shape_vertices = [
                                (vx + random_translation[0], vy + random_translation[1]) for vx, vy in
                                attached_shape.get_vertices()
                            ]
                            attached_shape.update_vertices(new_attached_shape_vertices)

                    else:
                        fixed_card_base.update_vertices(fixed_card_base.get_initial_vertices())
                        if tool_card is not None:
                            tool_card.update_vertices(tool_card.get_initial_vertices())
                        for attached_shape in attached_shape_list:
                            attached_shape.update_vertices(attached_shape.get_initial_vertices())

                    if step_count < steps:
                        self.master.after(20, vibration, step_count + 1)
                    else:
                        calculate_unit_energy_remove_item_card()

                vibration(1)

            self.create_effect_animation_to_your_unit_and_play_animation_and_call_function(
                'dark_blast', field_unit_index, vibration_energy_burn)


        else:
            field_unit_index = int(list(notify_dict_data.get("player_field_unit_health_point_map", {})
                                        .get("You", {})
                                        .get("field_unit_health_point_map", {}).keys())[0])

            field_unit_hp = int(list(notify_dict_data.get("player_field_unit_health_point_map", {})
                                     .get("You", {})
                                     .get("field_unit_health_point_map", {}).values())[0])

            dead_field_unit_index_list = list(notify_dict_data.get("player_field_unit_death_map", {})
                                              .get("You", {})
                                              .get("dead_field_unit_index_list", []))



            self.battle_field_repository.set_current_use_card_id(hand_use_card_id)

            def calculate_unit_energy_remove_item_card():

                for dead_field_unit_index in dead_field_unit_index_list:
                    def remove_field_unit_by_index(index):
                        self.your_tomb_repository.create_tomb_card(
                            self.your_field_unit_repository.find_field_unit_by_index(index).get_card_number())
                        self.your_field_unit_repository.remove_card_by_index(index)
                        self.your_field_unit_repository.remove_harmful_status_by_index(index)
                        self.your_field_unit_repository.replace_field_card_position()

                    self.create_effect_animation_to_your_unit_and_play_animation_and_call_function_with_param(
                        'death', dead_field_unit_index, remove_field_unit_by_index, dead_field_unit_index)

                    # effect_animation = EffectAnimation()
                    # effect_animation.set_animation_name('death')
                    # effect_animation.change_local_translation(
                    #     self.your_field_unit_repository.find_field_unit_by_index(
                    #         dead_field_unit_index).get_fixed_card_base().get_local_translation()
                    # )
                    # effect_animation.draw_animation_panel()
                    #
                    # self.__notify_reader_repository.save_notify_effect_animation_request(
                    #     EffectAnimationRequest(
                    #         effect_animation=effect_animation,
                    #         target_player='You',
                    #         target_index=dead_field_unit_index,
                    #         target_type=TargetType.UNIT,
                    #         call_function=remove_field_unit_by_index,
                    #         function_need_param=True,
                    #         param=dead_field_unit_index
                    #     )
                    # )

                try:
                    your_field_unit = self.your_field_unit_repository.find_field_unit_by_index(field_unit_index)

                    your_fixed_card_base = your_field_unit.get_fixed_card_base()
                    your_fixed_card_attached_shape_list = your_fixed_card_base.get_attached_shapes()

                    for your_fixed_card_attached_shape in your_fixed_card_attached_shape_list:
                        if isinstance(your_fixed_card_attached_shape, NonBackgroundNumberImage):
                            if your_fixed_card_attached_shape.get_circle_kinds() is CircleKinds.HP:
                                hp_number = your_fixed_card_attached_shape.get_number()
                                hp_number -= 10

                                if hp_number <= 0:
                                    break

                                your_fixed_card_attached_shape.set_number(hp_number)

                                your_fixed_card_attached_shape.set_image_data(
                                    self.pre_drawed_image_instance.get_pre_draw_unit_hp(
                                        hp_number))

                                print(f"changed hp: {your_fixed_card_attached_shape.get_circle_kinds()}")
                except Exception as e:
                    print(f"error occured!! : {e}")

            def vibration_energy_burn():
                steps = 30

                field_unit_object = self.your_field_unit_repository.find_field_unit_by_index(field_unit_index)
                fixed_card_base = field_unit_object.get_fixed_card_base()
                tool_card = field_unit_object.get_tool_card()
                attached_shape_list = fixed_card_base.get_attached_shapes()

                def vibration(step_count):
                    if step_count % 2 == 1:
                        vibration_factor = 10
                        random_translation = (random.uniform(-vibration_factor, vibration_factor),
                                              random.uniform(-vibration_factor, vibration_factor))

                        new_fixed_card_base_vertices = [
                            (vx + random_translation[0], vy + random_translation[1]) for vx, vy in
                            fixed_card_base.get_vertices()
                        ]
                        fixed_card_base.update_vertices(new_fixed_card_base_vertices)

                        if tool_card is not None:
                            new_tool_card_vertices = [
                                (vx + random_translation[0], vy + random_translation[1]) for vx, vy in
                                tool_card.get_vertices()
                            ]
                            tool_card.update_vertices(new_tool_card_vertices)

                        for attached_shape in attached_shape_list:
                            new_attached_shape_vertices = [
                                (vx + random_translation[0], vy + random_translation[1]) for vx, vy in
                                attached_shape.get_vertices()
                            ]
                            attached_shape.update_vertices(new_attached_shape_vertices)

                    else:
                        fixed_card_base.update_vertices(fixed_card_base.get_initial_vertices())
                        if tool_card is not None:
                            tool_card.update_vertices(tool_card.get_initial_vertices())
                        for attached_shape in attached_shape_list:
                            attached_shape.update_vertices(attached_shape.get_initial_vertices())

                    if step_count < steps:
                        self.master.after(20, vibration, step_count + 1)
                    else:
                        calculate_unit_energy_remove_item_card()

                vibration(1)

            self.create_effect_animation_to_your_unit_and_play_animation_and_call_function(
                'dark_blast', field_unit_index,  vibration_energy_burn)



    def repository_clear(self):
        self.your_deck_repository.clear_every_resource()
        self.your_hand_repository.clear_every_resource()
        self.opponent_hand_repository.clear_every_resource()
        self.your_field_unit_repository.clear_every_resource()
        self.opponent_field_unit_repository.clear_every_resource()
        self.your_tomb_repository.clear_every_resource()
        self.opponent_tomb_repository.clear_every_resource()
        self.your_hp_repository.clear_every_resource()
        self.opponent_hp_repository.clear_every_resource()
        self.your_field_energy_repository.clear_every_resource()
        self.opponent_field_energy_repository.clear_every_resource()
        self.your_lost_zone_repository.clear_every_resource()
        self.opponent_lost_zone_repository.clear_every_resource()
        self.round_repository.clear_every_resource()
        self.your_field_unit_action_repository.clear_every_resource()
        self.timer_repository.clear_every_resource()
        self.effect_animation_repository.clear_every_resource()
        
        del self.timer
        self.game_end_sound_call = False
        # self.battle_field_repository.clear_every_resource()

    def corpse_explosion_animation(self):
        data = self.attack_animation_object.get_notify_data()
        your_field_unit_health_point_map = data['player_field_unit_health_point_map']['You']['field_unit_health_point_map']
        your_dead_field_unit_index_list = data['player_field_unit_death_map']['You']['dead_field_unit_index_list']
        opponent_sacrificed_field_unit_index_list = data['player_field_unit_death_map']['Opponent']['dead_field_unit_index_list']

        # 사용된 카드 묘지로 보냄


        def calculate_your_field_unit_hp(param):
            print('calculate your field unit hp!!')
            # 체력 정보 Update
            your_field_unit_health_point_map = param[0]
            opponent_sacrificed_field_unit_index_list = param[1]
            for unit_index, remaining_health_point in your_field_unit_health_point_map.items():
                your_field_unit = self.your_field_unit_repository.find_field_unit_by_index(int(unit_index))
                your_fixed_card_base = your_field_unit.get_fixed_card_base()
                your_fixed_card_attached_shape_list = your_fixed_card_base.get_attached_shapes()

                if remaining_health_point <= 0:
                    continue

                for your_fixed_card_attached_shape in your_fixed_card_attached_shape_list:
                    if isinstance(your_fixed_card_attached_shape, NonBackgroundNumberImage):
                        if your_fixed_card_attached_shape.get_circle_kinds() is CircleKinds.HP:
                            def set_hp(param):
                                _your_fixed_card_attached_shape = param[0]
                                _remaining_health_point = param[1]
                                _your_fixed_card_attached_shape.set_number(int(_remaining_health_point))
                                _your_fixed_card_attached_shape.set_image_data(
                                    self.pre_drawed_image_instance.get_pre_draw_unit_hp(int(_remaining_health_point)))



                            self.create_effect_animation_to_your_unit_and_play_animation_and_call_function_with_param(
                                'dark_blast', int(unit_index), set_hp, (your_fixed_card_attached_shape, remaining_health_point)
                            )



                            # effect_animation = EffectAnimation()
                            # effect_animation.set_animation_name('dark_blast')
                            # effect_animation.change_local_translation(
                            #     self.your_field_unit_repository.find_field_unit_by_index(int(unit_index))
                            #     .get_fixed_card_base().get_local_translation())
                            # effect_animation.draw_animation_panel()
                            #
                            # self.__notify_reader_repository.save_notify_effect_animation_request(
                            #     EffectAnimationRequest(
                            #         effect_animation=effect_animation,
                            #         target_player='You',
                            #         target_index=int(unit_index),
                            #         target_type=TargetType.UNIT,
                            #         call_function=set_hp,
                            #         function_need_param=True,
                            #         param=(your_fixed_card_attached_shape, remaining_health_point)
                            #
                            #     )
                            # )

            # 죽은 유닛들 묘지에 배치 및 Replacing
            if your_dead_field_unit_index_list:
                for dead_unit_index in your_dead_field_unit_index_list:
                    unit_index = dead_unit_index

                    def remove_your_unit(unit_index):
                        # unit_index = dead_unit_index
                        print('index??? : ', unit_index)
                        field_unit_id = self.your_field_unit_repository.get_card_id_by_index(unit_index)
                        self.your_tomb_repository.create_tomb_card(field_unit_id)
                        self.your_field_unit_repository.remove_card_by_index(unit_index)
                        self.your_field_unit_repository.remove_harmful_status_by_index(unit_index)
                        self.your_field_unit_repository.replace_field_card_position()

                    self.create_effect_animation_to_your_unit_and_play_animation_and_call_function_with_param(
                        'death', dead_unit_index, remove_your_unit, dead_unit_index)

                    # effect_animation = EffectAnimation()
                    # effect_animation.set_unit_index(dead_unit_index)
                    # effect_animation.set_animation_name('death')
                    # effect_animation.change_local_translation(
                    #     self.your_field_unit_repository.find_field_unit_by_index(int(dead_unit_index))
                    #     .get_fixed_card_base().get_local_translation())
                    # effect_animation.draw_animation_panel()
                    #
                    # self.__notify_reader_repository.save_notify_effect_animation_request(
                    #     EffectAnimationRequest(
                    #         effect_animation=effect_animation,
                    #         target_player='You',
                    #         target_index=dead_unit_index,
                    #         target_type=TargetType.UNIT,
                    #         call_function=remove_your_unit,
                    #         function_need_param=True,
                    #         param=dead_unit_index
                    #     )
                    # )

            if opponent_sacrificed_field_unit_index_list:
                for dead_unit_index in opponent_sacrificed_field_unit_index_list:
                    def remove_field_unit(unit_index):
                        field_unit_id = self.opponent_field_unit_repository.get_opponent_card_id_by_index(unit_index)
                        self.opponent_tomb_repository.create_opponent_tomb_card(field_unit_id)
                        self.opponent_field_unit_repository.remove_current_field_unit_card(unit_index)
                        self.opponent_field_unit_repository.remove_harmful_status_by_index(unit_index)
                        self.opponent_field_unit_repository.replace_opponent_field_unit_card_position()

                    self.create_effect_animation_to_opponent_unit_and_play_animation_and_call_function_with_param(
                        'death', dead_unit_index, remove_field_unit, dead_unit_index)

                    # effect_animation = EffectAnimation()
                    # effect_animation.set_animation_name('death')
                    # effect_animation.change_local_translation(
                    #     self.__opponent_field_unit_repository.find_opponent_field_unit_by_index(int(dead_unit_index))
                    #     .get_fixed_card_base().get_local_translation())
                    # effect_animation.draw_animation_panel()
                    #
                    # self.__notify_reader_repository.save_notify_effect_animation_request(
                    #     EffectAnimationRequest(
                    #         effect_animation=effect_animation,
                    #         target_player='Opponent',
                    #         target_index=dead_unit_index,
                    #         target_type=TargetType.UNIT,
                    #         call_function=remove_field_unit,
                    #         function_need_param=True,
                    #         param=int(dead_unit_index)
                    #     )
                    # )

        def vibration_corpse_explosion(param):
            your_field_unit_health_point_map = param[0]
            opponent_sacrificed_field_unit_index_list = param[1]
            your_unit_index_list = list(your_field_unit_health_point_map.keys())
            opponent_unit_index_list = opponent_sacrificed_field_unit_index_list
            self.corpse_explosion_vibration_finish_count = len(your_unit_index_list) + len(opponent_unit_index_list)
            self.corpse_explosion_vibration_current_count = 0

            for unit_index in your_unit_index_list:
                steps = 30

                field_unit_object = self.your_field_unit_repository.find_field_unit_by_index(int(unit_index))

                def vibration(field_unit_object, step_count):
                    fixed_card_base = field_unit_object.get_fixed_card_base()
                    tool_card = field_unit_object.get_tool_card()
                    attached_shape_list = fixed_card_base.get_attached_shapes()

                    if step_count % 2 == 1:
                        vibration_factor = 10
                        random_translation = (random.uniform(-vibration_factor, vibration_factor),
                                              random.uniform(-vibration_factor, vibration_factor))

                        new_fixed_card_base_vertices = [
                            (vx + random_translation[0], vy + random_translation[1]) for vx, vy in
                            fixed_card_base.get_vertices()
                        ]
                        fixed_card_base.update_vertices(new_fixed_card_base_vertices)

                        if tool_card is not None:
                            new_tool_card_vertices = [
                                (vx + random_translation[0], vy + random_translation[1]) for vx, vy in
                                tool_card.get_vertices()
                            ]
                            tool_card.update_vertices(new_tool_card_vertices)

                        for attached_shape in attached_shape_list:
                            new_attached_shape_vertices = [
                                (vx + random_translation[0], vy + random_translation[1]) for vx, vy in
                                attached_shape.get_vertices()
                            ]
                            attached_shape.update_vertices(new_attached_shape_vertices)

                    else:
                        fixed_card_base.update_vertices(fixed_card_base.get_initial_vertices())
                        if tool_card is not None:
                            tool_card.update_vertices(tool_card.get_initial_vertices())
                        for attached_shape in attached_shape_list:
                            attached_shape.update_vertices(attached_shape.get_initial_vertices())

                    if step_count < steps:
                        self.master.after(20, vibration, field_unit_object, step_count + 1)
                    else:
                        self.corpse_explosion_vibration_current_count += 1
                        if self.corpse_explosion_vibration_finish_count == self.corpse_explosion_vibration_current_count:
                            calculate_your_field_unit_hp(param)

                vibration(field_unit_object, 1)

            for unit_index in opponent_unit_index_list:
                steps = 30

                field_unit_object = self.opponent_field_unit_repository.find_opponent_field_unit_by_index(unit_index)


                def vibration(field_unit_object, step_count):

                    fixed_card_base = field_unit_object.get_fixed_card_base()
                    tool_card = field_unit_object.get_tool_card()
                    attached_shape_list = fixed_card_base.get_attached_shapes()

                    if step_count % 2 == 1:
                        vibration_factor = 10
                        random_translation = (random.uniform(-vibration_factor, vibration_factor),
                                              random.uniform(-vibration_factor, vibration_factor))

                        new_fixed_card_base_vertices = [
                            (vx + random_translation[0], vy + random_translation[1]) for vx, vy in
                            fixed_card_base.get_vertices()
                        ]
                        fixed_card_base.update_vertices(new_fixed_card_base_vertices)

                        if tool_card is not None:
                            new_tool_card_vertices = [
                                (vx + random_translation[0], vy + random_translation[1]) for vx, vy in
                                tool_card.get_vertices()
                            ]
                            tool_card.update_vertices(new_tool_card_vertices)

                        for attached_shape in attached_shape_list:
                            new_attached_shape_vertices = [
                                (vx + random_translation[0], vy + random_translation[1]) for vx, vy in
                                attached_shape.get_vertices()
                            ]
                            attached_shape.update_vertices(new_attached_shape_vertices)

                    else:
                        fixed_card_base.update_vertices(fixed_card_base.get_initial_vertices())
                        if tool_card is not None:
                            tool_card.update_vertices(tool_card.get_initial_vertices())
                        for attached_shape in attached_shape_list:
                            attached_shape.update_vertices(attached_shape.get_initial_vertices())

                    if step_count < steps:
                        self.master.after(20, vibration, field_unit_object, step_count + 1)
                    else:
                        self.corpse_explosion_vibration_current_count += 1
                        if self.corpse_explosion_vibration_finish_count == self.corpse_explosion_vibration_current_count:
                            calculate_your_field_unit_hp(param)

                vibration(field_unit_object, 1)

        self.create_effect_animation_to_your_field_and_play_animation_and_call_function_with_param(
            'corpse_explosion', vibration_corpse_explosion, (your_field_unit_health_point_map ,opponent_sacrificed_field_unit_index_list)
        )

        # effect_animation = EffectAnimation()
        # effect_animation.set_animation_name('corpse_explosion')
        #
        # self.__notify_reader_repository.save_notify_effect_animation_request(
        #     EffectAnimationRequest(
        #         effect_animation=effect_animation,
        #         target_player='You',
        #         target_index=1000,
        #         target_type=TargetType.AREA,
        #         call_function=calculate_your_field_unit_hp
        #     )
        # )

    def play_loading_effect_animation(self):
        loading_animation = EffectAnimation()
        loading_animation.set_animation_name('loading_screen')
        loading_animation.draw_full_screen_animation_panel()
        loading_animation_panel = loading_animation.get_animation_panel()

        def animate():
            loading_animation.update_loading_animation_panel()
            loading_animation_panel.draw()

            if not self.is_loading_finished:
                self.master.after(17, animate)
            else:
                print("harmful_effect_animation finish")

        self.master.after(0, animate)