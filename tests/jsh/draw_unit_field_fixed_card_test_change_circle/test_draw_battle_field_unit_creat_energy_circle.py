from battle_field.components.field_area_inside.field_area_action import FieldAreaAction
from battle_field.components.field_area_inside.field_area_inside_handler import FieldAreaInsideHandler
from battle_field.components.fixed_unit_card_inside.fixed_unit_card_inside_handler import FixedUnitCardInsideHandler
from battle_field.components.init_location.location_initializer import LocationInitializer
from battle_field.components.mouse_drag.drag_handler import DragHandler
from battle_field.components.mouse_left_click.left_click_detector import LeftClickDetector
from battle_field.components.opponent_fixed_unit_card_inside.opponent_field_area_action import OpponentFieldAreaAction
from battle_field.components.opponent_fixed_unit_card_inside.opponent_fixed_unit_card_inside_handler import \
    OpponentFixedUnitCardInsideHandler
from battle_field.entity.legacy.battle_field_scene_legacy import BattleFieldSceneLegacy

import tkinter
import unittest

from OpenGL.GL import *
from OpenGL.GLU import *
from pyopengltk import OpenGLFrame

from battle_field.handler.support_card_handler import SupportCardHandler
from battle_field.infra.opponent_field_unit_repository import OpponentFieldUnitRepository
from battle_field.infra.your_deck_repository import YourDeckRepository
from battle_field.infra.your_field_unit_repository import YourFieldUnitRepository
from battle_field.infra.legacy.circle_image_legacy_your_hand_repository import CircleImageLegacyYourHandRepository
from battle_field.infra.your_tomb_repository import YourTombRepository
from battle_field_fixed_card.legacy.fixed_field_card import LegacyFixedFieldCard
from card_info_from_csv.repository.card_info_from_csv_repository_impl import CardInfoFromCsvRepositoryImpl
from common.card_type import CardType

from initializer.init_domain import DomainInitializer

from opengl_battle_field_pickable_card.legacy.pickable_card import LegacyPickableCard
from opengl_rectangle_lightning_border.lightning_border import LightningBorder
from opengl_shape.rectangle import Rectangle


class PreDrawedBattleFieldFrameVer(OpenGLFrame):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)

        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        self.width = screen_width
        self.height = screen_height

        self.active_panel_rectangle = None
        self.selected_object = None
        self.prev_selected_object = None
        self.drag_start = None

        self.lightning_border = LightningBorder()

        self.battle_field_scene = BattleFieldSceneLegacy()
        self.battle_field_scene.create_battle_field_scene()

        self.opponent_tomb_shapes = self.battle_field_scene.get_opponent_tomb()
        self.opponent_lost_zone_shapes = self.battle_field_scene.get_opponent_lost_zone()
        self.opponent_trap_shapes = self.battle_field_scene.get_opponent_trap()
        self.opponent_deck_shapes = self.battle_field_scene.get_opponent_deck()
        self.opponent_main_character_shapes = self.battle_field_scene.get_opponent_main_character()
        self.opponent_hand_panel_shapes = self.battle_field_scene.get_opponent_hand_panel()
        self.opponent_unit_field_shapes = self.battle_field_scene.get_opponent_unit_field()

        self.your_tomb_shapes = self.battle_field_scene.get_your_tomb()
        self.your_lost_zone_shapes = self.battle_field_scene.get_your_lost_zone()
        self.your_trap_shapes = self.battle_field_scene.get_your_trap()
        self.your_deck_shapes = self.battle_field_scene.get_your_deck()
        self.your_main_character_shapes = self.battle_field_scene.get_your_main_character()
        self.your_hand_panel_shapes = self.battle_field_scene.get_your_hand_panel()
        self.your_unit_field_shapes = self.battle_field_scene.get_your_unit_field()

        self.battle_field_environment_shapes = self.battle_field_scene.get_battle_field_environment()

        self.your_hand_repository = CircleImageLegacyYourHandRepository.getInstance()
        self.your_hand_repository.save_current_hand_state([8, 19, 151, 93, 9, 20, 30, 93])
        self.your_hand_repository.create_hand_card_list()

        self.your_deck_repository = YourDeckRepository.getInstance()
        self.your_deck_repository.save_deck_state([93, 93, 93, 5])

        # 실제로 상대는 하나씩 낼 것이고 이에 대한 서버의 Notify로 렌더링이 진행 될 것이다.
        self.opponent_field_unit_repository = OpponentFieldUnitRepository.getInstance()
        self.opponent_field_unit_repository.create_field_unit_card(33)
        self.opponent_field_unit_repository.create_field_unit_card(35)
        self.opponent_field_unit_repository.create_field_unit_card(36)
        self.opponent_field_unit_repository.create_field_unit_card(25)
        self.opponent_field_unit_repository.create_field_unit_card(26)
        self.opponent_field_unit_repository.create_field_unit_card(27)

        self.hand_card_list = self.your_hand_repository.get_current_hand_card_list()

        self.your_field_unit_repository = YourFieldUnitRepository.getInstance()

        self.your_tomb_repository = YourTombRepository.getInstance()
        # TODO: Naming Issue
        self.card_info_repository = CardInfoFromCsvRepositoryImpl.getInstance()

        self.your_lightning_border_list = []
        self.boost_selection = False

        self.support_card_handler = SupportCardHandler.getInstance()
        self.current_process_card_id = 0

        self.left_click_detector = LeftClickDetector.getInstance()
        self.fixed_unit_card_inside_handler = FixedUnitCardInsideHandler.getInstance(
            self.your_hand_repository,
            self.your_field_unit_repository,
            self.card_info_repository)

        self.field_area_inside_handler = FieldAreaInsideHandler.getInstance(
            self.your_hand_repository,
            self.your_field_unit_repository,
            self.your_deck_repository,
            self.card_info_repository,
            self.your_tomb_repository)

        self.opponent_fixed_unit_card_inside_handler = OpponentFixedUnitCardInsideHandler.getInstance(
            self.your_hand_repository,
            self.opponent_field_unit_repository,
            self.card_info_repository)

        self.selected_object_for_check_required_energy = []
        self.selected_object_index_for_check_required_energy = []
        self.required_energy_select_lightning_border_list = []

        self.bind("<Configure>", self.on_resize)
        self.bind("<B1-Motion>", self.on_canvas_drag)
        self.bind("<ButtonRelease-1>", self.on_canvas_release)
        self.bind("<Button-1>", self.on_canvas_left_click)
        self.bind("<Button-3>", self.on_canvas_right_click)

    def initgl(self):
        glClearColor(1.0, 1.0, 1.0, 0.0)
        glOrtho(0, self.width, self.height, 0, -1, 1)

        self.tkMakeCurrent()

    def reshape(self, width, height):
        print(f"Reshaping window to width={width}, height={height}")
        glViewport(0, 0, width, height)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluOrtho2D(0, width, height, 0)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

    def on_resize(self, event):
        self.reshape(event.width, event.height)

    def draw_base(self):
        for opponent_tomb_shape in self.opponent_tomb_shapes:
            opponent_tomb_shape.draw()

        for opponent_lost_zone_shape in self.opponent_lost_zone_shapes:
            opponent_lost_zone_shape.draw()

        for opponent_trap_shape in self.opponent_trap_shapes:
            opponent_trap_shape.draw()

        for opponent_card_deck_shape in self.opponent_deck_shapes:
            opponent_card_deck_shape.draw()

        for opponent_main_character_shape in self.opponent_main_character_shapes:
            opponent_main_character_shape.draw()

        for opponent_hand_panel_shape in self.opponent_hand_panel_shapes:
            opponent_hand_panel_shape.draw()

        for opponent_unit_field_shape in self.opponent_unit_field_shapes:
            opponent_unit_field_shape.draw()

        for your_tomb_shape in self.your_tomb_shapes:
            your_tomb_shape.draw()

        for your_lost_zone_shape in self.your_lost_zone_shapes:
            your_lost_zone_shape.draw()

        for your_trap_shape in self.your_trap_shapes:
            your_trap_shape.draw()

        for your_card_deck_shape in self.your_deck_shapes:
            your_card_deck_shape.draw()

        for your_main_character_shape in self.your_main_character_shapes:
            your_main_character_shape.draw()

        for your_hand_panel_shape in self.your_hand_panel_shapes:
            your_hand_panel_shape.draw()

        for your_unit_field_shape in self.your_unit_field_shapes:
            your_unit_field_shape.draw()

        for battle_field_environment_shape in self.battle_field_environment_shapes:
            battle_field_environment_shape.draw()

    def redraw(self):
        self.tkMakeCurrent()
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        self.draw_base()

        # 상대 필드 유닛 배치 시작
        for opponent_field_unit in self.opponent_field_unit_repository.get_current_field_unit_card_object_list():
            fixed_card_base = opponent_field_unit.get_fixed_card_base()
            fixed_card_base.draw()

            attached_shape_list = fixed_card_base.get_attached_shapes()

            for attached_shape in attached_shape_list:
                attached_shape.draw()
        # 상대 필드 유닛 배치 끝

        # 필드 배치 유닛 시작
        for your_field_unit in self.your_field_unit_repository.get_current_field_unit_list():
            fixed_card_base = your_field_unit.get_fixed_card_base()
            fixed_card_base.draw()

            attached_shape_list = fixed_card_base.get_attached_shapes()

            for attached_shape in attached_shape_list:
                attached_shape.draw()

        # 필드 배치 유닛 끝
        for hand_card in self.hand_card_list:
            pickable_card_base = hand_card.get_pickable_card_base()
            pickable_card_base.draw()

            attached_shape_list = pickable_card_base.get_attached_shapes()

            for attached_shape in attached_shape_list:
                attached_shape.draw()

        if self.selected_object:
            card_base = None

            # TODO: Ugly -> Need to Refactor
            if isinstance(self.selected_object, LegacyFixedFieldCard):
                card_base = self.selected_object.get_fixed_card_base()
            elif isinstance(self.selected_object, LegacyPickableCard):
                card_base = self.selected_object.get_pickable_card_base()

            self.lightning_border.set_padding(50)
            self.lightning_border.update_shape(card_base)
            self.lightning_border.draw_lightning_border()

        if self.active_panel_rectangle:
            self.active_panel_rectangle.draw()

        for your_field_lightning_border in self.field_area_inside_handler.get_lightning_border_list():
            self.lightning_border.set_padding(20)
            self.lightning_border.update_shape(your_field_lightning_border)
            self.lightning_border.draw_lightning_border()

        for your_hand_lightning_border in self.opponent_fixed_unit_card_inside_handler.get_lightning_border_list():
            self.lightning_border.set_padding(20)
            self.lightning_border.update_shape(your_hand_lightning_border)
            self.lightning_border.draw_lightning_border()

        for required_energy_selection_border in self.required_energy_select_lightning_border_list:
            self.lightning_border.set_padding(20)
            self.lightning_border.update_shape(required_energy_selection_border)
            self.lightning_border.draw_lightning_border()

        self.tkSwapBuffers()

    def on_canvas_drag(self, event):
        x, y = event.x, event.y
        y = self.winfo_reqheight() - y

        if self.selected_object and self.drag_start:
            drag_handler = DragHandler(self.selected_object, self.drag_start)

            dx = x - self.drag_start[0]
            dy = y - self.drag_start[1]
            dy *= -1

            drag_handler.update_selected_object_vertices_with_drag(dx, dy)

            self.drag_start = (x, y)

    def return_to_initial_location(self):
        LocationInitializer.return_to_initial_location(self.selected_object)
        self.drag_start = None

    def on_canvas_release(self, event):
        if isinstance(self.selected_object, LegacyFixedFieldCard):
            return

        x, y = event.x, event.y
        y = self.winfo_reqheight() - y

        if isinstance(self.selected_object, LegacyPickableCard):
            # Opponent에 적용하는 카드 시작
            current_opponent_field_unit_list = self.opponent_field_unit_repository.get_current_field_unit_card_object_list()
            current_opponent_field_unit_list_length = len(current_opponent_field_unit_list)

            if current_opponent_field_unit_list_length > 0:
                is_pickable_card_inside_unit = self.opponent_fixed_unit_card_inside_handler.handle_pickable_card_inside_unit(
                    self.selected_object, x, y)

                if is_pickable_card_inside_unit:
                    self.selected_object = None
                    return
            # Opponent에 적용하는 카드 끝

            current_your_field_unit_list = self.your_field_unit_repository.get_current_field_unit_list()
            current_your_field_unit_list_length = len(current_your_field_unit_list)

            # 현재 Your Field Unit에게 에너지 부착 및 도구 부착
            if current_your_field_unit_list_length > 0:
                is_pickable_card_inside_unit = self.fixed_unit_card_inside_handler.handle_pickable_card_inside_unit(
                    self.selected_object, x, y)

                if is_pickable_card_inside_unit:
                    self.selected_object = None

            y *= -1

            # 당신(Your) Field에 던진 카드
            drop_action_result = self.field_area_inside_handler.handle_card_drop(x, y, self.selected_object)
            if drop_action_result is None or drop_action_result is FieldAreaAction.Dummy:
                print("self.field_area_inside_handler.get_field_area_action() = None")
                self.return_to_initial_location()
            else:
                print("self.field_area_inside_handler.get_field_area_action() = Some Action")
                self.selected_object = None

    def on_canvas_left_click(self, event):
        try:
            x, y = event.x, event.y
            y = self.winfo_reqheight() - y

            # PickableCard (Hand Card List)
            for card in self.hand_card_list:
                card.selected = False

            self.selected_object = None

            selected_object = self.left_click_detector.which_one_select_is_in_your_hand_list_area((x, y),
                                                                                                  self.hand_card_list,
                                                                                                  self.winfo_reqheight())

            if selected_object:
                selected_object.selected = not selected_object.selected
                self.selected_object = selected_object
                self.drag_start = (x, y)

                if self.selected_object != self.prev_selected_object:
                    self.active_panel_rectangle = None
                    self.prev_selected_object = self.selected_object

            # 상대에게 어떤 카드 사용 시 에너지가 필요하다면
            if self.opponent_fixed_unit_card_inside_handler.get_opponent_field_area_action() is OpponentFieldAreaAction.REQUIRE_ENERGY_TO_USAGE:
                print("카드를 사용하기 위해 에너지가 필요합니다!")

                selected_card_id = self.selected_object.get_card_number()

                if self.card_info_repository.getCardTypeForCardNumber(selected_card_id) is not CardType.ENERGY.value:
                    return

                required_energy_race = self.opponent_fixed_unit_card_inside_handler.get_required_energy_race()
                if self.card_info_repository.getCardRaceForCardNumber(selected_card_id) is not required_energy_race.value:
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
                    usage_card_index = self.opponent_fixed_unit_card_inside_handler.get_action_set_card_index()

                    self.your_hand_repository.remove_card_by_multiple_index(
                        [
                            usage_card_index,
                            self.selected_object_index_for_check_required_energy[0],
                            self.selected_object_index_for_check_required_energy[1]
                        ])

                    self.opponent_field_unit_repository.remove_current_field_unit_card(
                        self.opponent_fixed_unit_card_inside_handler.get_opponent_unit_index())

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

                    self.selected_object = None
                    return

            # FixedFieldCard (Field Unit Card List)
            for your_field_unit in self.your_field_unit_repository.get_current_field_unit_list():
                your_field_unit.selected = False

            selected_your_field_unit = (self.left_click_detector
                                   .which_one_select_is_in_your_field_unit_list_area((x, y),
                                                                                self.your_field_unit_repository.get_current_field_unit_list(),
                                                                                self.winfo_reqheight()))

            if selected_your_field_unit:
                selected_your_field_unit.selected = not selected_your_field_unit.selected
                self.selected_object = selected_your_field_unit
                self.drag_start = (x, y)

                if self.field_area_inside_handler.get_field_area_action() is FieldAreaAction.ENERGY_BOOST:
                    self.field_area_inside_handler.clear_lightning_border_list()
                    self.field_area_inside_handler.clear_field_area_action()

                    print(f"덱에서 에너지 검색해서 부스팅 진행 -> current_process_card_id: {self.field_area_inside_handler.get_action_set_card_id()}")

                    proper_handler = self.support_card_handler.getSupportCardHandler(
                        self.field_area_inside_handler.get_action_set_card_id())
                    print(f"proper_handler: {proper_handler}")
                    proper_handler(selected_your_field_unit.get_index())

                if self.selected_object != self.prev_selected_object:
                    self.active_panel_rectangle = None
                    self.prev_selected_object = self.selected_object

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
        rectangle_size = 50
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


class TestDrawBattleFieldUnitChangeCircleNumber(unittest.TestCase):

    def test_draw_battle_field_unit_change_circle_number(self):
        DomainInitializer.initEachDomain()

        root = tkinter.Tk()
        root.geometry(f"{root.winfo_screenwidth()}x{root.winfo_screenheight()}-0-0")
        root.deiconify()

        pre_drawed_battle_field_frame = PreDrawedBattleFieldFrameVer(root)
        pre_drawed_battle_field_frame.pack(fill=tkinter.BOTH, expand=1)
        root.update_idletasks()

        def animate():
            pre_drawed_battle_field_frame.redraw()
            root.after(17, animate)

        root.after(0, animate)

        root.mainloop()


if __name__ == '__main__':
    unittest.main()
