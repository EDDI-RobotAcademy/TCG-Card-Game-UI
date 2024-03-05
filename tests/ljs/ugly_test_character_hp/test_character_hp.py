import multiprocessing

from screeninfo import get_monitors

from battle_field.components.field_area_inside.field_area_action import FieldAreaAction
from battle_field.components.field_area_inside.legacy.circle_image_legacy_field_area_inside_handler import CircleImageLegacyFieldAreaInsideHandler

import tkinter
import unittest

from OpenGL.GL import *
from OpenGL.GLU import *
from pyopengltk import OpenGLFrame

from battle_field.components.mouse_left_click.left_click_detector import LeftClickDetector
from battle_field.components.opponent_fixed_unit_card_inside.opponent_field_area_action import OpponentFieldAreaAction
from battle_field.components.opponent_fixed_unit_card_inside.opponent_fixed_unit_card_inside_handler import \
    OpponentFixedUnitCardInsideHandler
from battle_field.entity.opponent_tomb import OpponentTomb
from battle_field.entity.tomb_type import TombType
from battle_field.entity.your_tomb import YourTomb
from battle_field.handler.legacy.circle_image_legacy_support_card_handler import CircleImageLegacySupportCardHandler
from battle_field.infra.legacy.circle_image_legacy_opponent_field_unit_repository import CircleImageLegacyOpponentFieldUnitRepository
from battle_field.infra.legacy.circle_image_legacy_opponent_tomb_repository import CircleImageLegacyOpponentTombRepository
from battle_field.infra.legacy.circle_image_legacy_your_deck_repository import CircleImageLegacyYourDeckRepository
from battle_field.infra.your_field_energy_repository import YourFieldEnergyRepository
from battle_field.infra.legacy.circle_image_legacy_your_field_unit_repository import CircleImageLegacyYourFieldUnitRepository
from battle_field.infra.legacy.circle_image_legacy_your_hand_repository import CircleImageLegacyYourHandRepository
from battle_field.infra.legacy.circle_image_legacy_your_tomb_repository import CircleImageLegacyYourTombRepository
from battle_field.state.energy_type import EnergyType
from battle_field_fixed_card.legacy.circle_image_legacy_fixed_field_card import LegacyFixedFieldCard
from battle_field_muligun.entity.scene.battle_field_muligun_scene import BattleFieldMuligunScene
from card_info_from_csv.repository.card_info_from_csv_repository_impl import CardInfoFromCsvRepositoryImpl
from common.card_race import CardRace
from common.card_type import CardType
from image_shape.circle_image import CircleImage
from image_shape.circle_kinds import CircleKinds
from image_shape.circle_number_image import CircleNumberImage
from initializer.init_domain import DomainInitializer
from battle_field_function.service.battle_field_function_service_impl import \
    BattleFieldFunctionServiceImpl
from notify_reader.controller.notify_reader_controller_impl import NotifyReaderControllerImpl
from opengl_battle_field_pickable_card.legacy.pickable_card import LegacyPickableCard
from opengl_rectangle_lightning_border.lightning_border import LightningBorder
from opengl_shape.circle import Circle
from opengl_shape.rectangle import Rectangle
from pre_drawed_image_manager.pre_drawed_image import PreDrawedImage
from notify_reader.repository.notify_reader_repository_impl import \
    NotifyReaderRepositoryImpl
from tests.ljs.ugly_test_character_hp.entity.opponent_hp import OpponentHp
from tests.ljs.ugly_test_character_hp.entity.your_hp import YourHp
from tests.ljs.ugly_test_character_hp.repository.opponent_hp_repository import OpponentHpRepository
from tests.ljs.ugly_test_character_hp.repository.your_hp_repository import YourHpRepository


class PreDrawedBattleFieldFrameRefactor(OpenGLFrame):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)

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

        self.battle_field_muligun_background_shape_list = None
        self.battle_field_unit_place_panel = None

        self.battle_field_opponent_unit_place_panel = None

        self.active_panel_rectangle = None
        self.selected_object = None
        self.prev_selected_object = None
        self.drag_start = None

        self.lightning_border = LightningBorder()

        self.your_hand_repository = CircleImageLegacyYourHandRepository.getInstance()
        self.hand_card_list = None

        self.your_deck_repository = CircleImageLegacyYourDeckRepository.getInstance()
        self.your_deck_list = None

        self.your_field_unit_repository = CircleImageLegacyYourFieldUnitRepository.getInstance()

        self.card_info_repository = CardInfoFromCsvRepositoryImpl.getInstance()

        self.pre_drawed_image_instance = PreDrawedImage.getInstance()

        self.your_field_unit_lightning_border_list = []
        self.boost_selection = False

        self.support_card_handler = CircleImageLegacySupportCardHandler.getInstance()
        self.current_process_card_id = 0

        self.your_tomb_repository = CircleImageLegacyYourTombRepository.getInstance()
        self.your_tomb_panel = None
        self.your_tomb = YourTomb()
        self.tomb_panel_popup_rectangle = None
        self.tomb_panel_selected = False

        self.opponent_tomb_repository = CircleImageLegacyOpponentTombRepository.getInstance()
        self.opponent_tomb_panel = None
        self.opponent_tomb = OpponentTomb()
        self.opponent_tomb_popup_rectangle_panel = None
        self.opponent_tomb_panel_selected = False

        self.selected_tomb = TombType.Dummy

        self.opponent_field_unit_repository = CircleImageLegacyOpponentFieldUnitRepository.getInstance()
        # self.opponent_fixed_unit_card_inside_handler = OpponentFixedUnitCardInsideHandler.getInstance()
        self.field_area_inside_handler = CircleImageLegacyFieldAreaInsideHandler.getInstance()
        # TODO: Your 카드에 집어넣는 경우도 이것으로 감지하는 것이 더 좋을 것임
        self.your_fixed_unit_card_inside_handler = None
        self.opponent_fixed_unit_card_inside_handler = OpponentFixedUnitCardInsideHandler.getInstance()
        # self.your_tomb_repository = YourTombRepository.getInstance()

        self.left_click_detector = LeftClickDetector.getInstance()

        self.selected_object_for_check_required_energy = []
        self.selected_object_index_for_check_required_energy = []
        self.required_energy_select_lightning_border_list = []

        self.your_field_energy_repository = YourFieldEnergyRepository.getInstance()

        self.your_hp_panel = None
        self.your_hp = YourHp()
        self.your_hp_repository = YourHpRepository.getInstance()

        self.opponent_hp_panel = None
        self.opponent_hp = OpponentHp()
        self.opponent_hp_repository = OpponentHpRepository.getInstance()


        self.bind("<Configure>", self.on_resize)
        self.bind("<B1-Motion>", self.on_canvas_drag)
        self.bind("<ButtonRelease-1>", self.on_canvas_release)
        self.bind("<Button-1>", self.on_canvas_left_click)
        self.bind("<Button-3>", self.on_canvas_right_click)

        self.focus_set()
        self.bind("<Key>", self.on_key_press)

        def get_notify():
            NotifyReaderControllerImpl.getInstance().requestToReadNotifyCommand()
            self.master.after(17, get_notify)
        self.master.after(0,get_notify)


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

        battle_field_muligun_scene = BattleFieldMuligunScene()
        battle_field_muligun_scene.create_battle_field_muligun_scene(self.width, self.height)
        self.battle_field_muligun_background_shape_list = battle_field_muligun_scene.get_battle_field_muligun_background()

        self.battle_field_unit_place_panel = Rectangle(
            (0.0, 0.0, 0.0, 0.1),
            [(245, 470), (245, 700), (1675, 700), (1675, 470)],
            (0, 0),
            (0, 0))
        self.battle_field_unit_place_panel.set_draw_border(False)

        self.battle_field_opponent_unit_place_panel = Rectangle(
            (0.0, 0.0, 0.0, 0.1),
            [(245, 230), (245, 460), (1675, 460), (1675, 230)],
            (0, 0),
            (0, 0))
        self.battle_field_opponent_unit_place_panel.set_draw_border(False)

        # (257, 969)
        # (415, 971)
        # (332, 791)
        self.your_tomb.set_total_window_size(self.width, self.height)
        self.your_tomb.create_your_tomb_panel()
        self.your_tomb_panel = self.your_tomb.get_your_tomb_panel()

        self.opponent_tomb.set_total_window_size(self.width, self.height)
        self.opponent_tomb.create_opponent_tomb_panel()
        self.opponent_tomb_panel = self.opponent_tomb.get_opponent_tomb_panel()

        # 1848 기준 -> 1848 - (105 * 5 + 170 * 4) = 643
        # 643 / 2 = 321.5
        # 321.5 / 1848 = 17.4% => 0.174
        # 위 수식은 적합하지 않음 (0.286 포함)
        # 실제로 카드 좌측 하단 기준으로 170 이동이였음 (그러므로 카드간 간격은 65)
        # 1920 기준 -> 1920 - (105 * 5 + 65 * 4) = 1135
        # 1135 / 2 = 567.5
        self.your_hand_repository.set_x_base(567.5)
        self.your_hand_repository.save_current_hand_state([8, 20, 31, 151, 93])
        # self.your_hand_repository.save_current_hand_state([151])
        self.your_hand_repository.create_hand_card_list()

        self.your_deck_repository.save_deck_state([93, 35, 93, 5])

        # self.opponent_field_unit_repository.create_field_unit_card(33)
        # self.opponent_field_unit_repository.create_field_unit_card(35)
        # self.opponent_field_unit_repository.create_field_unit_card(36)
        # self.opponent_field_unit_repository.create_field_unit_card(25)
        # self.opponent_field_unit_repository.create_field_unit_card(26)
        self.opponent_field_unit_repository.create_field_unit_card(27)

        self.hand_card_list = self.your_hand_repository.get_current_hand_card_list()

        self.your_hp.set_total_window_size(self.width, self.height)
        self.your_hp_repository.set_first_hp_state()
        self.your_hp.draw_current_your_hp_panel()
        self.your_hp_panel = self.your_hp.get_your_hp_panel()

        self.opponent_hp.set_total_window_size(self.width, self.height)
        self.opponent_hp_repository.set_first_hp_state()
        self.opponent_hp.draw_current_opponent_hp_panel()
        self.opponent_hp_panel = self.opponent_hp.get_opponent_hp_panel()

        # self.your_tomb_repository.create_tomb_card(93)
        # self.your_tomb_repository.create_tomb_card(31)
        # self.your_tomb_repository.create_tomb_card(32)
        # self.your_tomb_repository.create_tomb_card_list()

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

        if key.lower() == 'd':
            self.your_hp_repository.take_damage()

        if key.lower() == 'o':
            self.opponent_hp_repository.take_damage()


        if key.lower() == 'a':
            notify_raw_data = '''{
                "NOTIFY_UNIT_SPAWN":
                    {"player_spawn_unit_map":
                        {"Opponent" : "26"}
                    }
            }'''
            NotifyReaderRepositoryImpl.getInstance().getNoWaitIpcChannel().put(notify_raw_data)
            #self.opponent_field_unit_repository.create_field_unit_card(26)

        if key.lower() == 'e':
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
            #NotifyReaderControllerImpl.getInstance().requestToReadNotifyCommand()
            # from battle_field_function.service.battle_field_function_service_impl import BattleFieldFunctionServiceImpl
            # attach_energy_data = BattleFieldFunctionServiceImpl.getInstance().attachFieldUnitEnergy(notify_dict)
            # print("attach_energy_count : ",attach_energy_data)
            # self.attach_energy(attach_energy_data)

    def on_resize(self, event):
        self.reshape(event.width, event.height)

    def draw_base(self):
        for battle_field_muligun_background_shape in self.battle_field_muligun_background_shape_list:
            battle_field_muligun_background_shape.set_width_ratio(self.width_ratio)
            battle_field_muligun_background_shape.set_height_ratio(self.height_ratio)
            battle_field_muligun_background_shape.draw()

        # TODO: 메인 로직에선 제거해야함 (현재는 개발 편의상 배치)
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

        self.battle_field_unit_place_panel.set_width_ratio(self.width_ratio)
        self.battle_field_unit_place_panel.set_height_ratio(self.height_ratio)
        self.battle_field_unit_place_panel.draw()

        self.battle_field_opponent_unit_place_panel.set_width_ratio(self.width_ratio)
        self.battle_field_opponent_unit_place_panel.set_height_ratio(self.height_ratio)
        self.battle_field_opponent_unit_place_panel.draw()

        self.your_tomb.set_width_ratio(self.width_ratio)
        self.your_tomb.set_height_ratio(self.height_ratio)
        self.your_tomb_panel.set_draw_border(False)
        self.your_tomb_panel.draw()

        self.opponent_tomb.set_width_ratio(self.width_ratio)
        self.opponent_tomb.set_height_ratio(self.height_ratio)
        self.opponent_tomb_panel.set_draw_border(False)
        self.opponent_tomb_panel.draw()

        self.your_hp.set_width_ratio(self.width_ratio)
        self.your_hp.set_height_ratio(self.height_ratio)
        self.your_hp.draw_current_your_hp_panel()

        self.opponent_hp.set_width_ratio(self.width_ratio)
        self.opponent_hp.set_height_ratio(self.height_ratio)
        self.opponent_hp.draw_current_opponent_hp_panel()

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

    def on_canvas_release(self, event):
        x, y = event.x, event.y
        y = self.winfo_reqheight() - y

        if isinstance(self.selected_object, LegacyPickableCard):
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

                        elif card_type == CardType.ITEM.value:
                            print("아군에게 아이템 사용")

                            # 우선 '사기 전환'이라 가정
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
                            total_attached_energy_count = self.your_field_unit_repository.get_total_energy_at_index(
                                unit_index)
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

            drop_action_result = self.field_area_inside_handler.handle_card_drop(x, y, self.selected_object,
                                                                                 self.battle_field_unit_place_panel)
            if drop_action_result is None or drop_action_result is FieldAreaAction.Dummy:
                print("self.field_area_inside_handler.get_field_area_action() = None")
                self.return_to_initial_location()
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
        valid_area_vertices = self.battle_field_unit_place_panel.get_vertices()
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

            self.tomb_panel_selected = False
            self.opponent_tomb_panel_selected = False

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
                print(f"type(field_unit) = {type(your_field_unit)}")
                fixed_card_base = your_field_unit.get_fixed_card_base()
                print(f"type(fixed_card_base) = {type(fixed_card_base)}")

                if fixed_card_base.is_point_inside((x, y)):
                    if self.boost_selection:
                        self.your_field_unit_lightning_border_list = []
                        print("덱에서 에너지 검색해서 부스팅 진행")

                        proper_handler = self.support_card_handler.getSupportCardHandler(self.current_process_card_id)
                        proper_handler(your_field_unit.get_index())

                        self.boost_selection = False
                        break

                    your_field_unit.selected = not your_field_unit.selected
                    self.selected_object = your_field_unit
                    self.drag_start = (x, y)

                    if self.selected_object != self.prev_selected_object:
                        self.active_panel_rectangle = None
                        self.prev_selected_object = self.selected_object

                    break

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
                return

            self.tomb_panel_selected = False
            self.opponent_tomb_panel_selected = False

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

    def attach_energy(self, attach_energy_data):

        # TODO: Change it to ENUM Value (Not just integer)
        # card_race = self.card_info_repository.getCardRaceForCardNumber(93)
        card_race = attach_energy_data['energy_race']
        print(f"card_race: {card_race}")

        attach_energy_count = attach_energy_data['race_energy_count']
        opponent_unit_index = attach_energy_data['target_unit_index']

        before_attach_energy_count = self.opponent_field_unit_repository.get_opponent_field_unit_race_energy(
            0, EnergyType.Undead)

        self.opponent_field_unit_repository.attach_race_energy(
            opponent_unit_index,
            EnergyType.Undead,
            attach_energy_count)
        opponent_field_unit = self.opponent_field_unit_repository.find_opponent_field_unit_by_index(opponent_unit_index)

        # after_attach_energy_count = self.opponent_field_unit_repository.get_opponent_field_unit_race_energy(
        #     0, EnergyType.Undead)
        total_attached_energy_count = attach_energy_data[
            'total_energy_count']  # self.opponent_field_unit_repository.get_total_energy_at_index(0)
        total_attached_energy_count = self.opponent_field_unit_repository.get_total_energy_at_index(opponent_unit_index)
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


        every_energy = self.opponent_field_unit_repository.get_energy_info_at_index(opponent_unit_index)
        print(f"every_energy: {every_energy}")

        if card_race == CardRace.UNDEAD.value:
            for energy_count in range(0, attach_energy_count):
                card_race_circle = opponent_field_unit.creat_fixed_card_energy_race_circle(
                    color=(0, 0, 0, 1),
                    vertices=(0, ((total_attached_energy_count - energy_count) * 10) + 20),
                    local_translation=opponent_fixed_card_base.get_local_translation())
                opponent_fixed_card_base.set_attached_shapes(card_race_circle)


class TestCharacterHp(unittest.TestCase):

    def setUp(self):

        pass

    def test_character_hp(self):
        DomainInitializer.initEachDomain()
        root = tkinter.Tk()
        root.geometry(f"{root.winfo_screenwidth()}x{root.winfo_screenheight()}-0-0")
        root.deiconify()

        pre_drawed_battle_field_frame = PreDrawedBattleFieldFrameRefactor(root)
        BattleFieldFunctionServiceImpl.getInstance().saveFrame(pre_drawed_battle_field_frame)
        pre_drawed_battle_field_frame.pack(fill=tkinter.BOTH, expand=1)
        root.update_idletasks()

        self.noWaitIpcChannel = multiprocessing.Queue()
        notifyReaderController = NotifyReaderControllerImpl.getInstance()
        notifyReaderController.requestToMappingNoticeWithFunction()
        notifyReaderController.requestToInjectNoWaitIpcChannel(self.noWaitIpcChannel)

        # taskWorkerService = TaskWorkerServiceImpl.getInstance()
        # taskWorkerService.createTaskWorker("NotifyReader", notifyReaderController.requestToReadNotifyCommand)
        # taskWorkerService.executeTaskWorker("NotifyReader")

        def animate():
            pre_drawed_battle_field_frame.redraw()
            root.after(17, animate)

        root.after(0, animate)

        root.mainloop()


if __name__ == '__main__':
    unittest.main()
