import random
import time

from colorama import Fore, Style
from screeninfo import get_monitors
from shapely import Polygon, Point

from battle_field.components.field_area_inside.field_area_action import FieldAreaAction

import tkinter
import unittest

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

from battle_field.infra.opponent_field_energy_repository import OpponentFieldEnergyRepository
from battle_field.infra.opponent_field_unit_repository import OpponentFieldUnitRepository
from battle_field.infra.opponent_hand_repository import OpponentHandRepository
from battle_field.infra.opponent_hp_repository import OpponentHpRepository
from battle_field.infra.opponent_lost_zone_repository import OpponentLostZoneRepository

from battle_field.infra.opponent_tomb_repository import OpponentTombRepository

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

from card_info_from_csv.repository.card_info_from_csv_repository_impl import CardInfoFromCsvRepositoryImpl
from common.card_grade import CardGrade
from common.card_race import CardRace
from common.card_type import CardType
from fake_battle_field.entity.animation_test_image import AnimationTestImage
from fake_battle_field.entity.muligun_reset_button import MuligunResetButton
from image_shape.circle_image import CircleImage
from image_shape.circle_kinds import CircleKinds
from image_shape.circle_number_image import CircleNumberImage
from image_shape.non_background_number_image import NonBackgroundNumberImage
from initializer.init_domain import DomainInitializer
from notify_reader.repository.notify_reader_repository_impl import NotifyReaderRepositoryImpl
from opengl_battle_field_pickable_card.pickable_card import PickableCard

from opengl_rectangle_lightning_border.lightning_border import LightningBorder
from opengl_shape.circle import Circle
from opengl_shape.rectangle import Rectangle
from pre_drawed_image_manager.pre_drawed_image import PreDrawedImage
from test_detector.detector import DetectorAboutTest
from tests.lsh.rotate_shape.animation_support.attack_animation import AttackAnimation


class PreDrawedBattleFieldFrameRefactor(OpenGLFrame):

    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)

        self.init_monitor_specification()

        self.current_your_attacker_unit_local_translation = None
        self.is_attack_motion_finished = False
        self.your_attacker_unit_destination_local_translation = None
        self.attack_animation_object = AttackAnimation.getInstance()

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

        self.your_field_unit_repository = YourFieldUnitRepository.getInstance()

        self.card_info_repository = CardInfoFromCsvRepositoryImpl.getInstance()

        self.pre_drawed_image_instance = PreDrawedImage.getInstance()

        self.your_field_unit_lightning_border_list = []

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

        self.bind("<Configure>", self.on_resize)
        self.bind("<B1-Motion>", self.on_canvas_drag)
        self.bind("<ButtonRelease-1>", self.on_canvas_release)
        self.bind("<Button-1>", self.on_canvas_left_click)
        self.bind("<Button-3>", self.on_canvas_right_click)

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

        self.opponent_field_unit_repository.create_field_unit_card(31)
        # self.opponent_field_unit_repository.create_field_unit_card(27)
        self.your_field_unit_repository.create_field_unit_card(31)
        # self.your_field_unit_repository.create_field_unit_card(19)
        # self.your_field_unit_repository.create_field_unit_card(27)

        self.your_active_panel = YourActivePanel()
        self.your_active_panel.set_total_window_size(self.width, self.height)

        muligun_reset_button_instance = MuligunResetButton()
        muligun_reset_button_instance.set_total_window_size(self.width, self.height)
        muligun_reset_button_instance.init_muligun_reset_button()
        self.muligun_reset_button = muligun_reset_button_instance.get_muligun_reset_button()

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

        glDisable(GL_BLEND)

    def post_draw(self):
        # glEnable(GL_BLEND)
        # glBlendFunc(GL_ONE_MINUS_SRC_ALPHA, GL_SRC_ALPHA)

        self.muligun_reset_button.set_width_ratio(self.width_ratio)
        self.muligun_reset_button.set_height_ratio(self.height_ratio)
        self.muligun_reset_button.draw()

        # glDisable(GL_BLEND)

    def redraw(self):
        if self.is_reshape_not_complete:
            return

        self.tkMakeCurrent()
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        glDisable(GL_DEPTH_TEST)

        self.draw_base()

        if self.attack_animation_object.get_need_post_process():
            print(f"{Fore.RED}애니메이션 처리 후 구동 할 코드가 있습니다!{Style.RESET_ALL}")

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
                # if isinstance(attached_shape, NonBackgroundNumberImage):
                #     if attached_shape.get_circle_kinds() == CircleKinds.ATTACK:
                #         print("검 위치")

                attached_shape.set_width_ratio(self.width_ratio)
                attached_shape.set_height_ratio(self.height_ratio)
                attached_shape.draw()

        # self.post_draw()

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

        ratio_applied_valid_your_field = [(x * self.width_ratio, y * self.height_ratio) for x, y in opponent_battle_field_area_vertices]
        print(f"ratio_applied_valid_your_field: {ratio_applied_valid_your_field}")
        print(f"x: {x * self.width_ratio}, y: {y * self.height_ratio}")

        poly = Polygon(ratio_applied_valid_your_field)
        point = Point(x, y)

        return point.within(poly)

    def on_canvas_release(self, event):
        x, y = event.x, event.y
        y = self.winfo_reqheight() - y

        if isinstance(self.selected_object, PickableCard):
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

            y *= -1

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

            if self.your_active_panel.get_your_active_panel_attack_button() is not None:
                if self.your_active_panel.is_point_inside_attack_button((x, y)):
                    your_field_unit_index = self.selected_object.get_index()

                    print("일반 공격 클릭")

                    opponent_field_unit_object_list = self.opponent_field_unit_repository.get_current_field_unit_card_object_list()
                    for opponent_field_unit_object in opponent_field_unit_object_list:
                        if opponent_field_unit_object is None:
                            continue

                        fixed_opponent_card_base = opponent_field_unit_object.get_fixed_card_base()
                        self.targeting_enemy_select_support_lightning_border_list.append(fixed_opponent_card_base)

                    self.opponent_fixed_unit_card_inside_handler.set_opponent_field_area_action(OpponentFieldAreaAction.GENERAL_ATTACK_TO_TARGETING_ENEMY)

                    your_field_unit_id = self.selected_object.get_card_number()
                    your_field_unit_index = self.selected_object.get_index()

                    # self.targeting_ememy_select_using_hand_card_id

                    self.targeting_enemy_select_using_your_field_card_index = your_field_unit_index
                    self.targeting_enemy_select_using_your_field_card_id = your_field_unit_id

                    return

            if self.your_active_panel.get_your_active_panel_first_skill_button() is not None:
                if self.your_active_panel.is_point_inside_first_skill_button((x, y)):
                    your_field_unit_index = self.selected_object.get_index()

                    print("첫 번째 스킬 클릭")

                    your_field_unit_id = self.selected_object.get_card_number()
                    your_field_unit_index = self.selected_object.get_index()
                    your_field_unit_attached_energy = self.your_field_unit_repository.get_attached_energy_info()

                    your_field_unit_total_energy = your_field_unit_attached_energy.get_total_energy_at_index(your_field_unit_index)
                    print(f"your_field_unit_total_energy: {your_field_unit_total_energy}")

                    your_field_unit_attached_energy_info = your_field_unit_attached_energy.get_energy_info_at_index(your_field_unit_index)
                    print(f"your_field_unit_attached_energy_info: {your_field_unit_attached_energy_info}")

                    your_field_unit_attached_undead_energy = your_field_unit_attached_energy.get_race_energy_at_index(your_field_unit_index, EnergyType.Undead)
                    # print(f"your_field_unit_attached_undead_energy: {your_field_unit_attached_undead_energy}")

                    your_field_unit_attached_human_energy = your_field_unit_attached_energy.get_race_energy_at_index(your_field_unit_index, EnergyType.Human)
                    # print(f"your_field_unit_attached_human_energy: {your_field_unit_attached_human_energy}")

                    your_field_unit_attached_trent_energy = your_field_unit_attached_energy.get_race_energy_at_index(your_field_unit_index, EnergyType.Trent)
                    # print(f"your_field_unit_attached_trent_energy: {your_field_unit_attached_trent_energy}")

                    your_field_unit_required_undead_energy = self.card_info_repository.getCardSkillFirstUndeadEnergyRequiredForCardNumber(your_field_unit_id)
                    your_field_unit_required_human_energy = self.card_info_repository.getCardSkillFirstHumanEnergyRequiredForCardNumber(your_field_unit_id)
                    your_field_unit_required_trent_energy = self.card_info_repository.getCardSkillFirstTrentEnergyRequiredForCardNumber(your_field_unit_id)
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

                    print("두 번째 스킬 클릭")

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

            self.tomb_panel_selected = False
            self.opponent_tomb_panel_selected = False
            self.your_lost_zone_panel_selected = False
            self.opponent_lost_zone_panel_selected = False
            self.muligun_reset_button_clicked = False

            # TODO: 메인 캐릭터 공격할 때도 이쪽 루틴을 타고 있어 Refactoring이 필요함
            if self.opponent_fixed_unit_card_inside_handler.get_opponent_field_area_action() is OpponentFieldAreaAction.GENERAL_ATTACK_TO_TARGETING_ENEMY:
                print("일반 공격 진행")

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

                    self.attack_animation_object.set_opponent_field_unit(opponent_field_unit_object)

                    if opponent_fixed_card_base.is_point_inside((x, y)):
                        your_field_card_index = self.targeting_enemy_select_using_your_field_card_index

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
                                    your_damage = self.card_info_repository.getCardAttackForCardNumber(your_field_card_id)
                                    print(f"your_damage: {your_damage}")

                                    your_field_unit = self.your_field_unit_repository.find_field_unit_by_index(your_field_card_index)
                                    your_fixed_card_base = your_field_unit.get_fixed_card_base()
                                    your_fixed_card_attached_shape_list = your_fixed_card_base.get_attached_shapes()

                                    opponent_field_card_id = opponent_field_unit_object.get_card_number()
                                    opponent_field_card_index = opponent_field_unit_object.get_index()
                                    opponent_damage = self.card_info_repository.getCardAttackForCardNumber(
                                        opponent_field_card_id)

                                    print(f"opponent_damage: {opponent_damage}")

                                    # 공격을 위해 your_field_unit 살짝 위로 올라옴
                                    current_your_attacker_unit_vertices = your_fixed_card_base.get_vertices()
                                    print(f"{Fore.RED}current_your_attacker_unit_vertices{Fore.GREEN} {current_your_attacker_unit_vertices}{Style.RESET_ALL}")
                                    current_your_attacker_unit_local_translation = your_fixed_card_base.get_local_translation()
                                    print(f"{Fore.RED}current_your_attacker_unit_local_translation{Fore.GREEN} {current_your_attacker_unit_local_translation}{Style.RESET_ALL}")

                                    new_y_value = current_your_attacker_unit_local_translation[1] + 20
                                    self.your_attacker_unit_destination_local_translation = (current_your_attacker_unit_local_translation[0], new_y_value)
                                    self.attack_animation_object.set_animation_actor(self.selected_object)

                                    self.master.after(0, self.attack_animation)

                                    # while not self.attack_animation_object.get_is_finished():
                                    #     time.sleep(1)

                                    are_your_field_unit_death = False
                                    for your_fixed_card_attached_shape in your_fixed_card_attached_shape_list:
                                        if isinstance(your_fixed_card_attached_shape, NonBackgroundNumberImage):
                                            if your_fixed_card_attached_shape.get_circle_kinds() is CircleKinds.HP:
                                                your_hp_number = your_fixed_card_attached_shape.get_number()
                                                your_hp_number -= opponent_damage
                                                print(f"your 유닛 hp number: {your_hp_number}")

                                                if your_hp_number <= 0:
                                                    are_your_field_unit_death = True
                                                    self.attack_animation_object.set_your_field_unit_death(True)

                                                    self.attack_animation_object.set_your_field_death_unit_index(
                                                        your_field_card_index)

                                                    break

                                                print(f"공격 후 your unit 체력 -> hp_number: {your_hp_number}")
                                                your_fixed_card_attached_shape.set_number(your_hp_number)

                                                self.attack_animation_object.set_your_field_hp_shape(your_fixed_card_attached_shape)
                                                self.attack_animation_object.set_your_field_unit_death(False)

                                                # your_fixed_card_attached_shape.set_image_data(
                                                #     self.pre_drawed_image_instance.get_pre_draw_unit_hp(
                                                #         your_hp_number))

                                    # if are_your_field_unit_death is True:
                                    #     self.your_field_unit_repository.remove_card_by_index(
                                    #         your_field_card_index)
                                    #
                                    #     self.your_field_unit_repository.replace_field_card_position()

                                    print("your 유닛 hp 갱신")

                                    opponent_hp_number = opponent_fixed_card_attached_shape.get_number()
                                    opponent_hp_number -= your_damage

                                    print(f"opponent_hp_number: {opponent_hp_number}")

                                    self.attack_animation_object.set_opponent_field_hp_shape(opponent_fixed_card_attached_shape)

                                    # TODO: n 턴간 불사 특성을 검사해야하므로 사실 이것도 summary 방식으로 빼는 것이 맞으나 우선은 진행한다.
                                    # (지금 당장 불사가 존재하지 않음)
                                    if opponent_hp_number <= 0:
                                        are_opponent_field_unit_death = True
                                        self.attack_animation_object.set_opponent_field_unit_death(True)

                                        self.attack_animation_object.set_opponent_field_death_unit_index(opponent_field_card_index)

                                        break

                                    print(f"공격 후 opponent unit 체력 -> hp_number: {opponent_hp_number}")
                                    opponent_fixed_card_attached_shape.set_number(opponent_hp_number)
                                    self.attack_animation_object.set_opponent_field_unit_death(False)

                                    # opponent_fixed_card_attached_shape.set_image_data(
                                    #     # TODO: 실제로 여기서 서버로부터 계산 받은 값을 적용해야함
                                    #     self.pre_drawed_image_instance.get_pre_draw_number_image(opponent_hp_number))

                                    # opponent_fixed_card_attached_shape.set_image_data(
                                    #     self.pre_drawed_image_instance.get_pre_draw_unit_hp(opponent_hp_number))

                        # opponent_field_card_index = None
                        # opponent_field_card_id = None

                        print(f"opponent_field_card_index: {opponent_field_card_index}")

                        # if are_opponent_field_unit_death is True:
                        #     self.opponent_field_unit_repository.remove_card_by_multiple_index(
                        #         [opponent_field_card_index])
                        #
                        #     self.opponent_field_unit_repository.replace_opponent_field_unit_card_position()

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

                                    your_second_passive_skill_damage = self.card_info_repository.getCardPassiveSecondDamageForCardNumber(your_field_card_id)
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
                                    your_skill_damage = self.card_info_repository.getCardSkillFirstDamageForCardNumber(your_field_card_id)
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

            self.tomb_panel_selected = False
            self.opponent_tomb_panel_selected = False
            self.your_lost_zone_panel_selected = False
            self.opponent_lost_zone_panel_selected = False
            self.muligun_reset_button_clicked = False

        except Exception as e:
            print(f"Exception in on_canvas_click: {e}")

    def is_point_inside_muligun_reset_button(self, click_point, muligun_reset_button, canvas_height):
        x, y = click_point
        y = canvas_height - y

        translated_vertices = [
            (x * self.width_ratio, y * self.height_ratio )
            for x, y in muligun_reset_button.get_vertices()
        ]
        print(f"x: {x}, y: {y}")
        print(f"translated_vertices: {translated_vertices}")

        if not (translated_vertices[0][0] <= x <= translated_vertices[2][0] and
                translated_vertices[1][1] <= y <= translated_vertices[2][1]):
            print("muligun_reset_button result -> False")
            return False

        print("muligun_reset_button result -> True")
        return True

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

    def attack_animation(self):
        attack_animation_object = AttackAnimation.getInstance()
        animation_actor = attack_animation_object.get_animation_actor()
        # print(f"{Fore.RED}animation_actor(selected_object){Fore.GREEN} {animation_actor}{Style.RESET_ALL}")

        your_fixed_card_base = animation_actor.get_fixed_card_base()
        current_your_attacker_unit_vertices = your_fixed_card_base.get_vertices()
        # print(f"{Fore.RED}current_your_attacker_unit_vertices{Fore.GREEN} {current_your_attacker_unit_vertices}{Style.RESET_ALL}")
        current_your_attacker_unit_local_translation = your_fixed_card_base.get_local_translation()
        # print(f"{Fore.RED}current_your_attacker_unit_local_translation{Fore.GREEN} {current_your_attacker_unit_local_translation}{Style.RESET_ALL}")

        new_y_value = current_your_attacker_unit_local_translation[1] + 30
        your_attacker_unit_destination_local_translation = (current_your_attacker_unit_local_translation[0], new_y_value)
        # print(f"{Fore.RED}your_attacker_unit_destination_local_translation{Fore.GREEN} {your_attacker_unit_destination_local_translation}{Style.RESET_ALL}")

        steps = 15
        step_x = (your_attacker_unit_destination_local_translation[0] - current_your_attacker_unit_local_translation[0]) / steps
        step_y = (your_attacker_unit_destination_local_translation[1] - current_your_attacker_unit_local_translation[1]) / steps
        step_y *= -1
        # print(f"{Fore.RED}step ->{Fore.GREEN}step_x: {step_x}, step_y: {step_y}{Style.RESET_ALL}")

        sword_target_x = 0.084375 * attack_animation_object.get_total_width()
        # print(f"{Fore.RED}sword_target_x: {Fore.GREEN}{sword_target_x}{Style.RESET_ALL}")

        sword_target_y = 0.278 * attack_animation_object.get_total_height()
        # print(f"{Fore.RED}sword_target_y: {Fore.GREEN}{sword_target_y}{Style.RESET_ALL}")

        # S = v0 * t + 0.5 * a * t^2
        # S = 0.5 * a * t^2 => step = 15
        # S = 0.5 * a * 225 = 580 / 225 = 2.57777

        # 670 -> 450 = 220 -> 440 / 225 = 1.9555
        # 670 -> 420 = 250 -> 500 / 225 = 2.2222
        # 670 -> 400 = 270 -> 540 / 225 = 2.4
        sword_accel_y = 2.4

        # 370 - 215 = 155 -> 310 / 225
        sword_accel_x = 1.3777

        def update_position(step_count):
            print(f"{Fore.RED}step_count: {Fore.GREEN}{step_count}{Style.RESET_ALL}")
            # your_fixed_card_base = selected_object.get_fixed_card_base()

            new_x = current_your_attacker_unit_local_translation[0] + step_x * step_count
            new_y = current_your_attacker_unit_local_translation[1] + step_y * step_count
            # dy *= -1
            print(f"{Fore.RED}step ->{Fore.GREEN}new_x: {new_x}, new_y: {new_y}{Style.RESET_ALL}")

            new_vertices = [
                (vx + step_x * step_count, vy + step_y * step_count) for vx, vy in current_your_attacker_unit_vertices
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
                # if isinstance(attached_shape, CircleImage):
                #     new_attached_shape_center = (attached_shape.vertices[0][0] + new_x, attached_shape.vertices[0][1] + new_y)
                #     attached_shape.update_circle_vertices(new_attached_shape_center)
                #     continue
                #
                # if isinstance(attached_shape, CircleNumberImage):
                #     new_attached_shape_center = (attached_shape.vertices[0][0] + new_x, attached_shape.vertices[0][1] + new_y)
                #     attached_shape.update_circle_vertices(new_attached_shape_center)
                #     continue
                #
                # if isinstance(attached_shape, Circle):
                #     new_attached_shape_center = (attached_shape.vertices[0][0] + new_x, attached_shape.vertices[0][1] + new_y)
                #     attached_shape.update_center(new_attached_shape_center)
                #     continue

                # theta = w0 * t + 0.5 * alpha * t^2
                # theta = 0.5 * alpha * t^2 => step_count = 15
                # theta = 0.5 * alpha * 225 = 65 / 225 = 0.28888
                omega_accel_alpha = -0.28888

                if isinstance(attached_shape, NonBackgroundNumberImage):
                    if attached_shape.get_circle_kinds() is CircleKinds.ATTACK:
                        accel_y_dist = sword_accel_y * step_count
                        accel_y_dist *= -1

                        accel_x_dist = sword_accel_x * step_count
                        # x: 236 / 1920, y: -367 / 1043
                        new_attached_shape_vertices = [
                            (vx - accel_x_dist, vy + accel_y_dist) for vx, vy in attached_shape.vertices
                        ]
                        attached_shape.update_vertices(new_attached_shape_vertices)
                        attached_shape.update_rotation_angle(omega_accel_alpha * step_count * step_count)

                        if step_count == 15:
                            attack_animation_object.set_your_weapon_shape(attached_shape)

                        continue

                print(
                    f"{Fore.RED}attached_shape.vertices: {Fore.GREEN}{attached_shape.vertices}{Style.RESET_ALL}")

                new_attached_shape_vertices = [
                    (vx + step_x, vy + step_y) for vx, vy in attached_shape.vertices
                ]
                attached_shape.update_vertices(new_attached_shape_vertices)
                print(f"{Fore.RED}new_attached_shape_vertices: {Fore.GREEN}{new_attached_shape_vertices}{Style.RESET_ALL}")


            # new_x = current_your_attacker_unit_local_translation[0] + step_x * step_count
            # new_y = current_your_attacker_unit_local_translation[1] + step_y * step_count
            # your_fixed_card_base.set_local_translation(new_x, new_y)
            if step_count < steps:

                self.master.after(20, update_position, step_count + 1)
            else:
                self.start_post_animation(attack_animation_object)
                self.is_attack_motion_finished = True
                attack_animation_object.set_is_finished(True)
                attack_animation_object.set_need_post_process(True)

        update_position(1)

    def start_post_animation(self, attack_animation_object):
        sword_shape = attack_animation_object.get_your_weapon_shape()

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
            if step_count < 11:
                sword_accel_x_dist = sword_accel_x * step_count

                new_attached_shape_vertices = [
                    (vx + sword_accel_x_dist, vy) for vx, vy in sword_shape.vertices
                ]
                sword_shape.update_vertices(new_attached_shape_vertices)
                print(f"{Fore.RED}new_attached_shape_vertices: {Fore.GREEN}{new_attached_shape_vertices}{Style.RESET_ALL}")

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

                self.master.after(20, slash_with_sword, step_count + 1)
            else:
                self.finish_post_animation(attack_animation_object)
                # self.is_attack_motion_finished = True
                # attack_animation_object.set_is_finished(True)
                # attack_animation_object.set_need_post_process(True)

        slash_with_sword(1)

    def finish_post_animation(self, attack_animation_object):
        sword_shape = attack_animation_object.get_your_weapon_shape()

        animation_actor = attack_animation_object.get_animation_actor()
        your_fixed_card_base = animation_actor.get_fixed_card_base()
        tool_card = animation_actor.get_tool_card()
        attached_shape_list = your_fixed_card_base.get_attached_shapes()

        current_your_attacker_unit_vertices = your_fixed_card_base.get_vertices()

        current_your_attacker_unit_local_translation = your_fixed_card_base.get_local_translation()
        print(f"{Fore.RED}current_your_attacker_unit_local_translation{Fore.GREEN} {current_your_attacker_unit_local_translation}{Style.RESET_ALL}")

        new_y_value = current_your_attacker_unit_local_translation[1] + 30
        your_attacker_unit_destination_local_translation = (
        current_your_attacker_unit_local_translation[0], new_y_value)
        print(f"{Fore.RED}your_attacker_unit_destination_local_translation{Fore.GREEN} {your_attacker_unit_destination_local_translation}{Style.RESET_ALL}")

        steps = 15
        # step_x = (your_attacker_unit_destination_local_translation[0] - current_your_attacker_unit_local_translation[0]) / steps
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

                        sword_accel_x = (current_sword_shape_target_x - current_sword_shape_x_vertex + 15.1677706645) / 112.5
                        sword_accel_y = (current_sword_shape_target_y - current_sword_shape_y_vertex + 124.732391723) / 112.5

                        sword_accel_x_dist = sword_accel_x * step_count
                        sword_accel_y_dist = sword_accel_y * step_count

                        new_attached_shape_vertices = [
                            (vx + sword_accel_x_dist, vy + sword_accel_y_dist) for vx, vy in sword_shape.vertices
                        ]
                        sword_shape.update_vertices(new_attached_shape_vertices)
                        print(
                            f"{Fore.RED}new_attached_shape_vertices: {Fore.GREEN}{new_attached_shape_vertices}{Style.RESET_ALL}")

                        current_angle = sword_shape.get_rotation_angle()
                        sword_shape.update_rotation_angle(current_angle - return_omega_accel_alpha * step_count)

                        continue

                print(
                    f"{Fore.RED}attached_shape.vertices: {Fore.GREEN}{attached_shape.vertices}{Style.RESET_ALL}")

                new_attached_shape_vertices = [
                    (vx, vy - step_y) for vx, vy in attached_shape.vertices
                ]
                attached_shape.update_vertices(new_attached_shape_vertices)
                print(
                    f"{Fore.RED}new_attached_shape_vertices: {Fore.GREEN}{new_attached_shape_vertices}{Style.RESET_ALL}")

            if step_count < steps:

                self.master.after(20, move_to_origin_location, step_count + 1)
            else:
                # print(f"{Fore.RED}current_sword_shape_target{Fore.GREEN} {current_sword_shape_target}{Style.RESET_ALL}")
                # difference_x = current_sword_shape_target[0][0] - sword_shape.vertices[0][0]
                # difference_y = current_sword_shape_target[0][1] - sword_shape.vertices[0][1]
                #
                # print(f"{Fore.RED}difference -> {Fore.GREEN}difference_x: {difference_x}, difference_y: {difference_y}{Style.RESET_ALL}")

                your_fixed_card_base.update_vertices(your_fixed_card_base.get_initial_vertices())
                if tool_card is not None:
                    tool_card.update_vertices(tool_card.get_initial_vertices())
                for attached_shape in attached_shape_list:
                    attached_shape.update_vertices(attached_shape.get_initial_vertices())

                self.is_attack_motion_finished = True
                attack_animation_object.set_is_finished(True)
                attack_animation_object.set_need_post_process(True)

                if self.attack_animation_object.get_your_field_unit_death():
                    your_field_death_unit_index = self.attack_animation_object.get_your_field_death_unit_index()
                    self.your_field_unit_repository.remove_card_by_index(your_field_death_unit_index)
                    self.your_field_unit_repository.replace_field_card_position()
                else:
                    your_field_hp_shape = self.attack_animation_object.get_your_field_hp_shape()
                    your_hp_number = your_field_hp_shape.get_number()

                    your_field_hp_shape.set_image_data(
                        self.pre_drawed_image_instance.get_pre_draw_unit_hp(
                            your_hp_number))

                if self.attack_animation_object.get_opponent_field_unit_death():
                    opponent_field_unit = self.attack_animation_object.get_opponent_field_unit()
                    opponent_field_unit_index = opponent_field_unit.get_index()
                    self.opponent_field_unit_repository.remove_card_by_multiple_index([opponent_field_unit_index])
                    self.opponent_field_unit_repository.replace_opponent_field_unit_card_position()
                else:
                    opponent_field_hp_shape = self.attack_animation_object.get()
                    opponent_hp_number = opponent_field_hp_shape.get_number()

                    opponent_field_hp_shape.set_image_data(
                        self.pre_drawed_image_instance.get_pre_draw_unit_hp(
                            opponent_hp_number))

                # your_fixed_card_attached_shape.set_image_data(
                #     self.pre_drawed_image_instance.get_pre_draw_unit_hp(
                #         your_hp_number))

                # if are_your_field_unit_death is True:
                #     self.your_field_unit_repository.remove_card_by_index(
                #         your_field_card_index)
                #
                #     self.your_field_unit_repository.replace_field_card_position()

                # opponent_fixed_card_attached_shape.set_image_data(
                #     self.pre_drawed_image_instance.get_pre_draw_unit_hp(opponent_hp_number))

                # if are_opponent_field_unit_death is True:
                #     self.opponent_field_unit_repository.remove_card_by_multiple_index(
                #         [opponent_field_card_index])
                #
                #     self.opponent_field_unit_repository.replace_opponent_field_unit_card_position()

        move_to_origin_location(1)



class TestRotationFieldUnit(unittest.TestCase):

    def test_rotate_field_unit(self):
        DomainInitializer.initEachDomain()
        detector_about_test = DetectorAboutTest.getInstance()
        detector_about_test.set_is_it_test(True)

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

