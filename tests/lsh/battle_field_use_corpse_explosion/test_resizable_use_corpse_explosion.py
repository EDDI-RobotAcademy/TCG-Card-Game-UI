from screeninfo import get_monitors
from shapely import Polygon, Point

from battle_field.components.field_area_inside.field_area_action import FieldAreaAction
from battle_field.components.field_area_inside.field_area_inside_handler import FieldAreaInsideHandler

import tkinter
import unittest

from OpenGL.GL import *
from OpenGL.GLU import *
from pyopengltk import OpenGLFrame

from battle_field.components.fixed_unit_card_inside.fixed_unit_card_inside_action import FixedUnitCardInsideAction
from battle_field.components.mouse_left_click.left_click_detector import LeftClickDetector
from battle_field.components.opponent_fixed_unit_card_inside.opponent_field_area_action import OpponentFieldAreaAction
from battle_field.components.opponent_fixed_unit_card_inside.opponent_fixed_unit_card_inside_handler import \
    OpponentFixedUnitCardInsideHandler
from battle_field.entity.battle_field_scene import BattleFieldScene
from battle_field.entity.opponent_field_panel import OpponentFieldPanel
from battle_field.entity.your_field_panel import YourFieldPanel
from battle_field.entity.opponent_lost_zone import OpponentLostZone
from battle_field.entity.opponent_tomb import OpponentTomb
from battle_field.entity.tomb_type import TombType
from battle_field.entity.your_lost_zone import YourLostZone
from battle_field.entity.your_tomb import YourTomb
from battle_field.handler.support_card_handler import SupportCardHandler
from battle_field.infra.opponent_field_unit_repository import OpponentFieldUnitRepository
from battle_field.infra.opponent_lost_zone_repository import OpponentLostZoneRepository
from battle_field.infra.opponent_tomb_repository import OpponentTombRepository
from battle_field.infra.your_deck_repository import YourDeckRepository
from battle_field.infra.your_field_energy_repository import YourFieldEnergyRepository
from battle_field.infra.your_field_unit_repository import YourFieldUnitRepository
from battle_field.infra.legacy.circle_image_legacy_your_hand_repository import CircleImageLegacyYourHandRepository
from battle_field.infra.your_lost_zone_repository import YourLostZoneRepository
from battle_field.infra.your_tomb_repository import YourTombRepository
from battle_field.state.energy_type import EnergyType
from battle_field_fixed_card.legacy.fixed_field_card import LegacyFixedFieldCard
from card_info_from_csv.repository.card_info_from_csv_repository_impl import CardInfoFromCsvRepositoryImpl
from common.card_race import CardRace
from common.card_type import CardType
from image_shape.circle_image import CircleImage
from image_shape.circle_kinds import CircleKinds
from image_shape.circle_number_image import CircleNumberImage
from initializer.init_domain import DomainInitializer
from opengl_battle_field_pickable_card.legacy.pickable_card import LegacyPickableCard
from opengl_rectangle_lightning_border.lightning_border import LightningBorder
from opengl_shape.circle import Circle
from opengl_shape.rectangle import Rectangle
from pre_drawed_image_manager.pre_drawed_image import PreDrawedImage


class PreDrawedBattleFieldFrameRefactor(OpenGLFrame):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)

        self.init_monitor_specification()

        self.battle_field_background_shape_list = None

        self.your_field_panel = None
        self.opponent_field_panel = None

        self.active_panel_rectangle = None
        self.selected_object = None
        self.prev_selected_object = None
        self.drag_start = None

        self.lightning_border = LightningBorder()

        self.your_hand_repository = CircleImageLegacyYourHandRepository.getInstance()
        self.hand_card_list = None

        self.your_deck_repository = YourDeckRepository.getInstance()
        self.your_deck_list = None

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
        self.targeting_enemy_select_count = 0

        self.opponent_you_selected_lightning_border_list = []
        self.opponent_you_selected_object_list = []

        self.your_field_energy_repository = YourFieldEnergyRepository.getInstance()

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

        self.bind("<Configure>", self.on_resize)
        self.bind("<B1-Motion>", self.on_canvas_drag)
        self.bind("<ButtonRelease-1>", self.on_canvas_release)
        self.bind("<Button-1>", self.on_canvas_left_click)
        self.bind("<Button-3>", self.on_canvas_right_click)

        # TODO: 이 부분은 임시 방편입니다 (상대방 행동 했다 가정하고 키보드 입력 받기 위함)
        self.focus_set()
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

        self.your_hand_repository.set_x_base(567.5)
        self.your_hand_repository.save_current_hand_state([25, 33, 2, 151, 93])
        # self.your_hand_repository.save_current_hand_state([151])
        self.your_hand_repository.create_hand_card_list()

        self.your_deck_repository.save_deck_state([93, 35, 93, 5])

        # self.opponent_field_unit_repository.create_field_unit_card(33)
        # self.opponent_field_unit_repository.create_field_unit_card(35)
        # self.opponent_field_unit_repository.create_field_unit_card(36)
        # self.opponent_field_unit_repository.create_field_unit_card(25)
        # self.opponent_field_unit_repository.create_field_unit_card(26)
        self.opponent_field_unit_repository.create_field_unit_card(27)
        self.your_field_unit_repository.create_field_unit_card(31)

        self.hand_card_list = self.your_hand_repository.get_current_hand_card_list()

        # self.your_tomb_repository.create_tomb_card(93)
        # self.your_tomb_repository.create_tomb_card(31)
        # self.your_tomb_repository.create_tomb_card(32)
        # self.your_tomb_repository.create_tomb_card_list()

        self.your_lost_zone.set_total_window_size(self.width, self.height)
        self.your_lost_zone.create_your_lost_zone_panel()
        self.your_lost_zone_panel = self.your_lost_zone.get_your_lost_zone_panel()

        self.opponent_lost_zone.set_total_window_size(self.width, self.height)
        self.opponent_lost_zone.create_opponent_lost_zone_panel()
        self.opponent_lost_zone_panel = self.opponent_lost_zone.get_opponent_lost_zone_panel()

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

        if key.lower() == 'a':
            self.opponent_field_unit_repository.create_field_unit_card(26)

        if key.lower() == 'q':
            self.opponent_field_unit_repository.create_field_unit_card(31)

        if key.lower() == 'n':
            self.opponent_field_unit_repository.create_field_unit_card(19)

        if key.lower() == 'e':
            print("attach undead energy")

            # TODO: Change it to ENUM Value (Not just integer)
            card_race = self.card_info_repository.getCardRaceForCardNumber(93)
            print(f"card_race: {card_race}")

            attach_energy_count = 1
            opponent_unit_index = 0

            # self.opponent_field_unit_repository.attach_race_energy(opponent_unit_index, EnergyType.Undead, attach_energy_count)
            # opponent_field_unit = self.opponent_field_unit_repository.find_opponent_field_unit_by_index(0)
            #
            # opponent_field_unit_attached_undead_energy_count = self.opponent_field_unit_repository.get_opponent_field_unit_race_energy(0, EnergyType.Undead)
            # print(f"opponent_field_unit_attached_undead_energy_count: {opponent_field_unit_attached_undead_energy_count}")

            before_attach_energy_count = self.opponent_field_unit_repository.get_opponent_field_unit_race_energy(
                0, EnergyType.Undead)

            self.opponent_field_unit_repository.attach_race_energy(
                opponent_unit_index,
                EnergyType.Undead,
                attach_energy_count)
            opponent_field_unit = self.opponent_field_unit_repository.find_opponent_field_unit_by_index(0)

            # after_attach_energy_count = self.opponent_field_unit_repository.get_opponent_field_unit_race_energy(
            #     0, EnergyType.Undead)
            total_attached_energy_count = self.opponent_field_unit_repository.get_total_energy_at_index(0)
            print(
                f"opponent_field_unit_attached_undead_energy_count: {total_attached_energy_count}")

            opponent_fixed_card_base = opponent_field_unit.get_fixed_card_base()
            opponent_fixed_card_attached_shape_list = opponent_fixed_card_base.get_attached_shapes()

            for opponent_fixed_card_attached_shape in opponent_fixed_card_attached_shape_list:
                if isinstance(opponent_fixed_card_attached_shape, CircleNumberImage):
                    if opponent_fixed_card_attached_shape.get_circle_kinds() is CircleKinds.ENERGY:
                        opponent_fixed_card_attached_shape.set_image_data(
                            self.pre_drawed_image_instance.get_pre_draw_number_image(
                                total_attached_energy_count))
                        print(f"changed energy: {opponent_fixed_card_attached_shape.get_circle_kinds()}")

            # after_attach_energy_count
            # before_attach_energy_count

            every_energy = self.opponent_field_unit_repository.get_energy_info_at_index(0)
            print(f"every_energy: {every_energy}")

            if card_race == CardRace.UNDEAD.value:
                card_race_circle = opponent_field_unit.creat_fixed_card_energy_race_circle(
                    color=(0, 0, 0, 1),
                    vertices=(0, (total_attached_energy_count * 10) + 20),
                    local_translation=opponent_fixed_card_base.get_local_translation())
                opponent_fixed_card_base.set_attached_shapes(card_race_circle)

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

        glDisable(GL_BLEND)

    def redraw(self):
        if self.is_reshape_not_complete:
            return

        self.tkMakeCurrent()
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        self.draw_base()

        for opponent_field_unit in self.opponent_field_unit_repository.get_current_field_unit_card_object_list():
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

        for hand_card in self.hand_card_list:
            attached_tool_card = hand_card.get_tool_card()
            if attached_tool_card is not None:
                attached_tool_card.set_width_ratio(self.width_ratio)
                attached_tool_card.set_height_ratio(self.height_ratio)
                attached_tool_card.draw()

            pickable_card_base = hand_card.get_pickable_card_base()
            pickable_card_base.set_width_ratio(self.width_ratio)
            pickable_card_base.set_height_ratio(self.height_ratio)
            pickable_card_base.draw()

            attached_shape_list = pickable_card_base.get_attached_shapes()

            for attached_shape in attached_shape_list:
                attached_shape.set_width_ratio(self.width_ratio)
                attached_shape.set_height_ratio(self.height_ratio)
                attached_shape.draw()

        if self.selected_object:
            card_base = None

            if isinstance(self.selected_object, LegacyFixedFieldCard):
                card_base = self.selected_object.get_fixed_card_base()
            elif isinstance(self.selected_object, LegacyPickableCard):
                card_base = self.selected_object.get_pickable_card_base()

            self.lightning_border.set_width_ratio(self.width_ratio)
            self.lightning_border.set_height_ratio(self.height_ratio)

            self.lightning_border.set_padding(50)
            self.lightning_border.update_shape(card_base)
            self.lightning_border.draw_lightning_border()

        if self.active_panel_rectangle:
            # self.active_panel_rectangle.set_width_ratio(self.width_ratio)
            # self.active_panel_rectangle.set_height_ratio(self.height_ratio)
            self.active_panel_rectangle.draw()

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

        self.tkSwapBuffers()

    def on_canvas_drag(self, event):
        x, y = event.x, event.y
        y = self.winfo_reqheight() - y
        # print(f"on_canvas_drag -> x: {x}, y: {y}")

        if self.selected_object and self.drag_start:
            if not isinstance(self.selected_object, LegacyPickableCard):
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

        ratio_applied_valid_your_field = [(x * self.width_ratio, y * self.height_ratio) for x, y in opponent_battle_field_area_vertices]
        print(f"ratio_applied_valid_your_field: {ratio_applied_valid_your_field}")
        print(f"x: {x * self.width_ratio}, y: {y * self.height_ratio}")

        poly = Polygon(ratio_applied_valid_your_field)
        point = Point(x, y)

        return point.within(poly)

    def on_canvas_release(self, event):
        x, y = event.x, event.y
        y = self.winfo_reqheight() - y

        if isinstance(self.selected_object, LegacyPickableCard):
            # Opponent Field Area 시작
            # is_pickable_card_inside_opponent_field =

            your_card_id = self.selected_object.get_card_number()
            card_type = self.card_info_repository.getCardTypeForCardNumber(your_card_id)
            print(f"opponent field area -> card_type: {card_type}")

            if card_type in [CardType.ITEM.value]:
                # opponent_field_area_vertices = self.battle_field_opponent_unit_place_panel.get_vertices()
                # print(f"opponent_field_area_vertices: {opponent_field_area_vertices}")

                # TODO: 추후 변경이 필요함
                # if opponent_field_area_vertices.is_point_inside((x, y)):
                if self.is_point_inside_opponent_field_area((x, y), self.opponent_field_panel):
                    print("파멸의 계약 사용")
                    self.__required_energy = 0

                    damage = 15

                    # TODO: 즉발이므로 대기 액션이 필요없음 (서버와의 통신을 위해 대기가 발생 할 수 있긴함) 그 때 가서 추가
                    for index in range(
                            len(self.opponent_field_unit_repository.get_current_field_unit_card_object_list()) - 1, -1,
                            -1):
                        opponent_field_unit = \
                        self.opponent_field_unit_repository.get_current_field_unit_card_object_list()[index]
                        remove_from_field = False

                        fixed_card_base = opponent_field_unit.get_fixed_card_base()
                        attached_shape_list = fixed_card_base.get_attached_shapes()

                        # TODO: 가만 보면 이 부분이 은근히 많이 사용되고 있음 (중복 많이 발생함)
                        for attached_shape in attached_shape_list:
                            if isinstance(attached_shape, CircleNumberImage):
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

                                    attached_shape.set_image_data(
                                        # TODO: 실제로 여기서 서버로부터 계산 받은 값을 적용해야함
                                        self.pre_drawed_image_instance.get_pre_draw_number_image(hp_number))

                        if remove_from_field:
                            card_id = opponent_field_unit.get_card_number()

                            self.opponent_field_unit_repository.remove_current_field_unit_card(index)
                            self.opponent_tomb_repository.create_opponent_tomb_card(card_id)

                    your_card_index = self.your_hand_repository.find_index_by_selected_object(self.selected_object)
                    self.your_hand_repository.remove_card_by_index(your_card_index)
                    self.your_tomb_repository.create_tomb_card(your_card_id)

                    self.your_hand_repository.replace_hand_card_position()
                    self.opponent_field_unit_repository.replace_opponent_field_unit_card_position()

                    # 실제 날리는 데이터의 경우 서버로부터 응답 받은 정보를 로스트 존으로 배치
                    self.opponent_lost_zone_repository.create_opponent_lost_zone_card(32)

                    self.selected_object = None
                    return

            # Opponent Field Area 끝

            current_opponent_field_unit_list = self.opponent_field_unit_repository.get_current_field_unit_card_object_list()
            current_opponent_field_unit_list_length = len(current_opponent_field_unit_list)
            print(f"current_opponent_field_unit_list_length: {current_opponent_field_unit_list_length}")

            if current_opponent_field_unit_list_length > 0:
                is_pickable_card_inside_unit = self.opponent_fixed_unit_card_inside_handler.handle_pickable_card_inside_unit(
                    self.selected_object, x, y)

                if is_pickable_card_inside_unit:
                    self.selected_object = None
                    return

            current_field_unit_list = self.your_field_unit_repository.get_current_field_unit_list()
            current_field_unit_list_length = len(current_field_unit_list)

            # TODO: 이 부분이 YourFixedFieldUnitCardInsideHandler
            # 현재 Your Field Unit에게 에너지 부착 및 도구 부착
            if current_field_unit_list_length > 0:
                for unit_index, current_field_unit in enumerate(current_field_unit_list):
                    fixed_card_base = current_field_unit.get_fixed_card_base()
                    if fixed_card_base.is_point_inside((x, y)):
                        print("fixed field unit detect something comes inside!")

                        placed_card_id = self.selected_object.get_card_number()
                        card_type = self.card_info_repository.getCardTypeForCardNumber(placed_card_id)
                        placed_index = self.your_hand_repository.find_index_by_selected_object(self.selected_object)

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

                            if placed_card_id == 35:
                                print(f"사기 전환(35) -> placed_card_id: {placed_card_id}")
                                card_id = current_field_unit.get_card_number()
                                fixed_field_unit_hp = self.card_info_repository.getCardHpForCardNumber(card_id)
                                acquire_energy = round(fixed_field_unit_hp / 5)
                                print(f"acquire_energy: {acquire_energy}")

                                self.your_field_energy_repository.increase_your_field_energy(acquire_energy)
                                self.your_hand_repository.remove_card_by_index(placed_index)
                                self.your_field_unit_repository.remove_card_by_index(unit_index)

                                self.your_hand_repository.replace_hand_card_position()

                                self.your_tomb_repository.create_tomb_card(card_id)
                                self.your_tomb_repository.create_tomb_card(placed_card_id)

                                print(f"사기 전환 이후 필드 에너지 수량: {self.your_field_energy_repository.get_your_field_energy()}")

                            if placed_card_id == 33:
                                print(f"시체 폭발(33) -> placed_card_id: {placed_card_id}")
                                card_id = current_field_unit.get_card_number()

                                opponent_field_unit_object_list = self.opponent_field_unit_repository.get_current_field_unit_card_object_list()
                                for opponent_field_unit_object in opponent_field_unit_object_list:
                                    fixed_opponent_card_base = opponent_field_unit_object.get_fixed_card_base()
                                    self.targeting_enemy_select_support_lightning_border_list.append(fixed_opponent_card_base)

                                self.fixed_unit_card_inside_action = FixedUnitCardInsideAction.TARGETING_TWO_ENEMY_AS_POSSIBLE
                                # self.targeting_enemy_select_support_lightning_border_list = []
                                self.targeting_ememy_select_using_hand_card_id = placed_card_id
                                self.targeting_ememy_select_using_hand_card_index = placed_index
                                self.targeting_enemy_select_using_your_field_card_index = unit_index
                                self.targeting_enemy_for_sacrifice_unit_id = card_id
                                self.targeting_enemy_select_count = 2

                                # self.your_hand_repository.replace_hand_card_position()
                                #
                                # self.your_tomb_repository.create_tomb_card(card_id)
                                # self.your_tomb_repository.create_tomb_card(placed_card_id)


                            self.selected_object = None
                            return


                        elif card_type == CardType.ENERGY.value:
                            print("에너지를 붙입니다!")
                            # self.selected_object = None
                            self.your_hand_repository.remove_card_by_index(placed_index)
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

                            your_fixed_field_unit = self.your_field_unit_repository.find_field_unit_by_index(unit_index)
                            fixed_card_base = your_fixed_field_unit.get_fixed_card_base()
                            fixed_card_attached_shape_list = fixed_card_base.get_attached_shapes()
                            placed_card_id = self.selected_object.get_card_number()
                            print(f"placed_card_id : {placed_card_id}")
                            print(f"card grade : {self.card_info_repository.getCardGradeForCardNumber(placed_card_id)}")

                            # attached_energy_count = self.your_field_unit_repository.get_attached_energy_info().get_energy_at_index(unit_index)
                            total_attached_energy_count = self.your_field_unit_repository.get_total_energy_at_index(unit_index)
                            print(f"total_attached_energy_count: {total_attached_energy_count}")
                            # undead_attach_energy_count = self.your_field_unit_repository.get_your_field_unit_race_energy(
                            #     unit_index, race)
                            self.your_hand_repository.replace_hand_card_position()

                            # card_id = current_field_unit.get_card_number()
                            # self.your_tomb_repository.create_tomb_card(card_id)
                            self.your_tomb_repository.create_tomb_card(placed_card_id)
                            # TODO: attached_energy 값 UI에 표현 (이미지 작업 미완료)

                            # TODO: 특수 에너지 붙인 것을 어떻게 표현 할 것인가 ? (아직 미정)
                            for fixed_card_attached_shape in fixed_card_attached_shape_list:
                                if isinstance(fixed_card_attached_shape, CircleNumberImage):
                                    if fixed_card_attached_shape.get_circle_kinds() is CircleKinds.ENERGY:
                                        fixed_card_attached_shape.set_image_data(
                                            self.pre_drawed_image_instance.get_pre_draw_number_image(
                                                total_attached_energy_count))
                                        print(f"changed energy: {fixed_card_attached_shape.get_circle_kinds()}")

                            card_race = self.card_info_repository.getCardRaceForCardNumber(placed_card_id)
                            if card_race == CardRace.UNDEAD.value:
                                card_race_circle = your_fixed_field_unit.creat_fixed_card_energy_race_circle(
                                    color=(0, 0, 0, 1),
                                    vertices=(0, (total_attached_energy_count * 10) + 20),
                                    local_translation=fixed_card_base.get_local_translation())
                                fixed_card_base.set_attached_shapes(card_race_circle)

                            self.selected_object = None

                            return
                        else:
                            self.return_to_initial_location()
                            return

            y *= -1

            # 당신(Your) Field에 던진 카드
            self.field_area_inside_handler.set_width_ratio(self.width_ratio)
            self.field_area_inside_handler.set_height_ratio(self.height_ratio)

            drop_action_result = self.field_area_inside_handler.handle_card_drop(x, y, self.selected_object, self.your_field_panel)
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

            self.tomb_panel_selected = False
            self.opponent_tomb_panel_selected = False
            self.your_lost_zone_panel_selected = False
            self.opponent_lost_zone_panel_selected = False

            for hand_card in self.hand_card_list:
                if isinstance(hand_card, LegacyPickableCard):
                    hand_card.selected = False

            self.selected_object = None

            for hand_card in reversed(self.hand_card_list):
                pickable_card_base = hand_card.get_pickable_card_base()
                pickable_card_base.set_width_ratio(self.width_ratio)
                pickable_card_base.set_height_ratio(self.height_ratio)

                if pickable_card_base.is_point_inside((x, y)):
                    hand_card.selected = not hand_card.selected
                    self.selected_object = hand_card
                    self.drag_start = (x, y)

                    if self.selected_object != self.prev_selected_object:
                        self.active_panel_rectangle = None
                        self.prev_selected_object = self.selected_object

                    break

            if self.opponent_fixed_unit_card_inside_handler.get_opponent_field_area_action() is OpponentFieldAreaAction.REQUIRE_ENERGY_TO_USAGE:
                print("카드를 사용하기 위해 에너지가 필요합니다!")

                selected_card_id = self.selected_object.get_card_number()

                if self.card_info_repository.getCardTypeForCardNumber(selected_card_id) is not CardType.ENERGY.value:
                    return

                required_energy_race = self.opponent_fixed_unit_card_inside_handler.get_required_energy_race()
                if self.card_info_repository.getCardRaceForCardNumber(
                        selected_card_id) is not required_energy_race.value:
                    return

                self.selected_object_for_check_required_energy.append(self.selected_object)
                self.selected_object_index_for_check_required_energy.append(
                    self.your_hand_repository.find_index_by_selected_object(
                        self.selected_object))

                card_base = self.selected_object.get_pickable_card_base()
                self.required_energy_select_lightning_border_list.append(card_base)

                self.opponent_fixed_unit_card_inside_handler.decrease_required_energy()
                required_energy_count = self.opponent_fixed_unit_card_inside_handler.get_required_energy()

                if required_energy_count == 0:
                    print(f"required_energy_count: {required_energy_count}")
                    usage_card_index = self.opponent_fixed_unit_card_inside_handler.get_action_set_card_index()

                    selected_energy_index_list = []
                    selected_energy_index_list.append(self.selected_object_index_for_check_required_energy[0])
                    selected_energy_index_list.append(self.selected_object_index_for_check_required_energy[1])

                    selected_energy_id_list = []
                    selected_energy_id_list.append(self.selected_object_for_check_required_energy[0].get_card_number())
                    selected_energy_id_list.append(self.selected_object_for_check_required_energy[1].get_card_number())
                    # print(f"self.selected_object_for_check_required_energy[0]: {self.selected_object_for_check_required_energy[0]}")
                    # print(f"self.selected_object_for_check_required_energy[1]: {self.selected_object_for_check_required_energy[1]}")

                    self.your_hand_repository.remove_card_by_multiple_index(
                        [
                            usage_card_index,
                            selected_energy_index_list[0],
                            selected_energy_index_list[1]
                        ])

                    opponent_unit_card_index = self.opponent_fixed_unit_card_inside_handler.get_opponent_unit_index()

                    self.opponent_field_unit_repository.remove_current_field_unit_card(
                        opponent_unit_card_index)

                    # print("isn't it operate ? (Death Sice)")
                    self.your_tomb_repository.create_tomb_card(selected_energy_id_list[0])
                    self.your_tomb_repository.create_tomb_card(selected_energy_id_list[1])
                    self.your_tomb_repository.create_tomb_card(
                        self.opponent_fixed_unit_card_inside_handler.get_your_hand_card_id())
                    # TODO: 상대편은 상대 무덤으로 이동해야함
                    self.opponent_tomb_repository.create_opponent_tomb_card(
                        self.opponent_fixed_unit_card_inside_handler.get_opponent_unit_id())

                    self.your_hand_repository.replace_hand_card_position()

                    self.selected_object_for_check_required_energy = []
                    self.selected_object_index_for_check_required_energy = []
                    self.required_energy_select_lightning_border_list = []

                    self.opponent_fixed_unit_card_inside_handler.clear_opponent_unit_index()
                    self.opponent_fixed_unit_card_inside_handler.clear_action_set_card_index()
                    self.opponent_fixed_unit_card_inside_handler.clear_opponent_field_area_action()
                    self.opponent_fixed_unit_card_inside_handler.clear_required_energy_race()
                    self.opponent_fixed_unit_card_inside_handler.clear_required_energy()
                    self.opponent_fixed_unit_card_inside_handler.clear_lightning_border_list()
                    self.opponent_fixed_unit_card_inside_handler.clear_opponent_unit_id()
                    self.opponent_fixed_unit_card_inside_handler.clear_your_hand_card_id()

                    self.opponent_field_unit_repository.replace_opponent_field_unit_card_position()

                    self.selected_object = None
                    return

            your_field_unit_list = self.your_field_unit_repository.get_current_field_unit_list()
            for your_field_unit in your_field_unit_list:
                if isinstance(your_field_unit, LegacyFixedFieldCard):
                    your_field_unit.selected = False

            for your_field_unit in your_field_unit_list:
                print(f"your field unit (field_unit) = {type(your_field_unit)}")
                fixed_card_base = your_field_unit.get_fixed_card_base()
                print(f"your field unit type (fixed_card_base) = {type(fixed_card_base)}")

                if fixed_card_base.is_point_inside((x, y)):
                    if self.field_area_inside_handler.get_field_area_action() is FieldAreaAction.ENERGY_BOOST:
                        self.field_area_inside_handler.clear_lightning_border_list()
                        self.field_area_inside_handler.clear_field_area_action()
                        self.your_field_unit_lightning_border_list = []
                        print("덱에서 에너지 검색해서 부스팅 진행")

                        current_process_card_id = self.field_area_inside_handler.get_action_set_card_id()
                        proper_handler = self.support_card_handler.getSupportCardHandler(current_process_card_id)
                        proper_handler(your_field_unit.get_index())

                        self.your_tomb_repository.create_tomb_card(current_process_card_id)

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
                        self.prev_selected_object = self.selected_object

                    break

            if self.fixed_unit_card_inside_action is FixedUnitCardInsideAction.TARGETING_TWO_ENEMY_AS_POSSIBLE:
                print("적 유닛 2체까지 선택 가능")

                opponent_field_unit_object_list = self.opponent_field_unit_repository.get_current_field_unit_card_object_list()
                for opponent_field_unit_object in opponent_field_unit_object_list:
                    if isinstance(opponent_field_unit_object, LegacyFixedFieldCard):
                        opponent_field_unit_object.selected = False

                for opponent_field_unit_object in opponent_field_unit_object_list:
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
                                    if isinstance(opponent_fixed_card_attached_shape, CircleNumberImage):
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

                                            opponent_fixed_card_attached_shape.set_image_data(
                                                # TODO: 실제로 여기서 서버로부터 계산 받은 값을 적용해야함
                                                self.pre_drawed_image_instance.get_pre_draw_number_image(hp_number))

                                # if remove_from_field:
                                #     card_id = opponent_you_selected_object.get_card_number()
                                #
                                #     self.opponent_field_unit_repository.remove_current_field_unit_card(opponent_you_selected_object.get_index())
                                #     self.opponent_tomb_repository.create_opponent_tomb_card(card_id)

                            # for remove_from_field in remove_from_field_list:

                            print(f"corpse explosion index: {self.targeting_ememy_select_using_hand_card_index}")
                            self.your_hand_repository.remove_card_by_index(
                                self.targeting_ememy_select_using_hand_card_index)
                            self.your_tomb_repository.create_tomb_card(
                                self.targeting_ememy_select_using_hand_card_id)

                            self.opponent_field_unit_repository.remove_card_by_multiple_index(remove_from_field_index_list)

                            for remove_from_field_id in remove_from_field_id_list:
                                self.opponent_tomb_repository.create_opponent_tomb_card(
                                    remove_from_field_id)

                            self.your_field_unit_repository.remove_card_by_index(self.targeting_enemy_select_using_your_field_card_index)
                            self.your_tomb_repository.create_tomb_card(self.targeting_enemy_for_sacrifice_unit_id)

                            self.your_hand_repository.replace_hand_card_position()
                            self.opponent_field_unit_repository.replace_opponent_field_unit_card_position()

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

                        # 두 체가 선택되면 묻지 않고 발동합니다.
                        # if
                        #
                        # self.targeting_ememy_select_using_hand_card_id = placed_card_id
                        # self.targeting_ememy_select_using_hand_card_index = placed_index
                        # self.targeting_enemy_select_using_your_field_card_index = unit_index
                        # self.targeting_enemy_select_count = 2

                        # self.targeting_enemy_select_support_lightning_border_list = []
                        #         self.targeting_ememy_select_using_hand_card_id = -1
                        #         self.targeting_ememy_select_using_hand_card_index = -1
                        #         self.targeting_enemy_select_using_your_field_card_index = -1
                        #         self.targeting_enemy_select_count = 0
                        #
                        #         self.opponent_you_selected_lightning_border_list = []
                        #         self.opponent_you_selected_index_list = []

            self.tomb_panel_selected = self.left_click_detector.which_one_select_is_in_your_tomb_area(
                (x, y),
                self.your_tomb,
                self.winfo_reqheight())

            if self.tomb_panel_selected:
                print(f"on_canvas_left_click() -> current_tomb_unit_list: {self.your_tomb_repository.get_current_tomb_state()}")
                self.your_tomb.create_tomb_panel_popup_rectangle()
                self.tomb_panel_popup_rectangle = self.your_tomb.get_tomb_panel_popup_rectangle()

                self.opponent_tomb_panel_selected = False
                self.your_lost_zone_panel_selected = False
                self.opponent_lost_zone_panel_selected = False
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
                return

            self.tomb_panel_selected = False
            self.opponent_tomb_panel_selected = False
            self.your_lost_zone_panel_selected = False
            self.opponent_lost_zone_panel_selected = False

            # self.selected_tomb = self.left_click_detector.which_tomb_did_you_select(
            #     (x, y),
            #     self.your_tomb,
            #     self.opponent_tomb,
            #     self.winfo_reqheight())
            #
            # if self.selected_tomb is TombType.Your:
            #     self.your_tomb.create_tomb_panel_popup_rectangle()
            #     self.tomb_panel_popup_rectangle = self.your_tomb.get_tomb_panel_popup_rectangle()
            #
            # elif self.selected_tomb is TombType.Opponent:
            #     self.opponent_tomb.create_opponent_tomb_panel_popup_rectangle()
            #     self.opponent_tomb_popup_rectangle_panel = self.opponent_tomb.get_opponent_tomb_panel_popup_rectangle()

        except Exception as e:
            print(f"Exception in on_canvas_click: {e}")

    def on_canvas_right_click(self, event):
        x, y = event.x, event.y

        if self.selected_object and isinstance(self.selected_object, LegacyFixedFieldCard):
            convert_y = self.winfo_reqheight() - y
            fixed_card_base = self.selected_object.get_fixed_card_base()
            if fixed_card_base.is_point_inside((x, convert_y)):
                new_rectangle = self.create_opengl_rectangle((x, y))
                self.active_panel_rectangle = new_rectangle

    def create_opengl_rectangle(self, start_point):
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


class TestResizableUseUseCorpseExplosion(unittest.TestCase):

    def test_resizable_use_corpse_explosion(self):
        DomainInitializer.initEachDomain()

        root = tkinter.Tk()
        root.geometry(f"{root.winfo_screenwidth()}x{root.winfo_screenheight()}-0-0")
        root.deiconify()

        pre_drawed_battle_field_frame = PreDrawedBattleFieldFrameRefactor(root)
        pre_drawed_battle_field_frame.pack(fill=tkinter.BOTH, expand=1)
        root.update_idletasks()

        def animate():
            pre_drawed_battle_field_frame.redraw()
            root.after(17, animate)

        root.after(0, animate)

        root.mainloop()


if __name__ == '__main__':
    unittest.main()

