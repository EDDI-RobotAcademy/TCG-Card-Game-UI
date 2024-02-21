import tkinter
import unittest

from image_shape.rectangle_image import RectangleImage
from initializer.init_domain import DomainInitializer
from tests.ljs.ugly_test_battle_field_functions.pre_drawed_battle_field_frame.PreDrawedBattleFieldFrameRefactorLJS import \
    PreDrawedBattleFieldFrameRefactorLJS


from battle_field_function.controller.battle_field_function_controller_impl import BattleFieldFunctionControllerImpl
from battle_field_ui_button.battle_field_button import BattleFieldButton
from pre_drawed_image_manager.pre_drawed_image import PreDrawedImage

from battle_field.components.init_location.location_initializer import LocationInitializer
from battle_field.components.mouse_drag.drag_handler import DragHandler
from battle_field.components.mouse_left_click.left_click_detector import LeftClickDetector
from battle_field.entity.battle_field_scene import BattleFieldScene

import tkinter
import unittest

from OpenGL.GL import *
from OpenGL.GLU import *
from pyopengltk import OpenGLFrame

from battle_field.handler.support_card_handler import SupportCardHandler
from battle_field.infra.battle_field_repository import BattleFieldRepository
from battle_field.infra.your_deck_repository import YourDeckRepository
from battle_field.infra.your_field_unit_repository import YourFieldUnitRepository
from battle_field.infra.your_hand_repository import YourHandRepository
from battle_field.infra.your_tomb_repository import YourTombRepository
from battle_field_fixed_card.fixed_field_card import FixedFieldCard
from card_info_from_csv.repository.card_info_from_csv_repository_impl import CardInfoFromCsvRepositoryImpl
from common.card_type import CardType
from image_shape.circle_image import CircleImage
from image_shape.circle_number_image import CircleNumberImage
from initializer.init_domain import DomainInitializer
from opengl_battle_field_pickable_card.pickable_card import PickableCard
from opengl_rectangle_lightning_border.lightning_border import LightningBorder
from opengl_shape.rectangle import Rectangle

from battle_field.entity.battle_field_environment import BattleFieldEnvironment
from battle_field.entity.opponent_deck import OpponentDeck
from battle_field.entity.opponent_hand_panel import OpponentHandPanel
from battle_field.entity.opponent_lost_zone import OpponentLostZone
from battle_field.entity.opponent_main_character import OpponentMainCharacter
from battle_field.entity.opponent_tomb import OpponentTomb
from battle_field.entity.opponent_trap import OpponentTrap
from battle_field.entity.opponent_unit_field import OpponentUnitField
from battle_field.entity.turn_end_button import TurnEndButton
from battle_field.entity.your_deck import YourDeck
from battle_field.entity.your_hand_panel import YourHandPanel
from battle_field.entity.your_lost_zone import YourLostZone
from battle_field.entity.your_main_character import YourMainCharacter
from battle_field.entity.your_tomb import YourTomb
from battle_field.entity.your_trap import YourTrap
from battle_field.entity.your_unit_field import YourUnitField
from battle_field.infra.battle_field_repository import BattleFieldRepository


class BattleFieldSceneForWinTest:
    __battle_field_repository = BattleFieldRepository.getInstance()
    def __init__(self):
        self.opponent_tomb = None
        self.opponent_lost_zone = None
        self.opponent_trap = None
        self.opponent_deck = None
        self.opponent_main_character = None
        self.opponent_hand_panel = None

        self.your_tomb = None
        self.your_lost_zone = None
        self.your_trap = None
        self.your_deck = None
        self.your_main_character = None
        self.your_hand_panel = None
        self.win_panel = None

        self.battle_field_environment = None
        self.turn_end_button = None

    def create_battle_field_scene(self):
        self.create_opponent_tomb()
        self.create_opponent_lost_zone()
        self.create_opponent_trap()
        self.create_opponent_deck()
        self.create_opponent_main_character()
        self.create_opponent_hand_panel()
        self.create_opponent_unit_field()

        self.create_your_tomb()
        self.create_your_lost_zone()
        self.create_your_trap()
        self.create_your_deck()
        self.create_your_main_character()
        self.create_your_hand_panel()
        self.create_your_unit_field()

        self.create_battle_field_environment()
        self.create_turn_end_button()
        #self.create_win_panel()

    def create_opponent_tomb(self):
        self.opponent_tomb = OpponentTomb()
        self.opponent_tomb.init_shapes()

    def create_opponent_lost_zone(self):
        self.opponent_lost_zone = OpponentLostZone()
        self.opponent_lost_zone.init_shapes()

    def create_opponent_trap(self):
        self.opponent_trap = OpponentTrap()
        self.opponent_trap.init_shapes()

    def create_opponent_deck(self):
        self.opponent_deck = OpponentDeck()
        self.opponent_deck.init_shapes()

    def create_opponent_main_character(self):
        self.opponent_main_character = OpponentMainCharacter()
        self.opponent_main_character.init_opponent_main_character_shapes()

    def create_opponent_hand_panel(self):
        self.opponent_hand_panel = OpponentHandPanel()
        self.opponent_hand_panel.init_shapes()

    def create_opponent_unit_field(self):
        self.opponent_unit_field = OpponentUnitField()
        self.opponent_unit_field.init_shapes()

    def create_your_tomb(self):
        self.your_tomb = YourTomb()
        self.your_tomb.init_shapes()

    def create_your_lost_zone(self):
        self.your_lost_zone = YourLostZone()
        self.your_lost_zone.init_shapes()

    def create_your_trap(self):
        self.your_trap = YourTrap()
        self.your_trap.init_shapes()

    def create_your_deck(self):
        self.your_deck = YourDeck()
        self.your_deck.init_shapes()

    def create_your_main_character(self):
        self.your_main_character = YourMainCharacter()
        self.your_main_character.init_your_main_character_shapes()

    def create_your_hand_panel(self):
        self.your_hand_panel = YourHandPanel()
        self.your_hand_panel.init_shapes()

    def create_your_unit_field(self):
        self.your_unit_field = YourUnitField()
        self.your_unit_field.init_shapes()

    def create_battle_field_environment(self):
        self.battle_field_environment = BattleFieldEnvironment()
        self.battle_field_environment.init_shapes()

    def create_turn_end_button(self):
        self.turn_end_button = TurnEndButton()
        self.turn_end_button.init_shapes()
        self.__battle_field_repository.add_battle_field_button(button=self.turn_end_button)

    def create_win_panel(self):
        self.win_panel = WinPanel()
        self.win_panel.init_shapes()

    def get_win_panel(self):
        return self.win_panel.get_win_panel_shapes()


    def get_opponent_tomb(self):
        return self.opponent_tomb.get_tomb_shapes()

    def get_opponent_lost_zone(self):
        return self.opponent_lost_zone.get_lost_zone_shapes()

    def get_opponent_trap(self):
        return self.opponent_trap.get_trap_shapes()

    def get_opponent_deck(self):
        return self.opponent_deck.get_opponent_deck_shapes()

    def get_opponent_main_character(self):
        return self.opponent_main_character.get_main_character_shapes()

    def get_opponent_hand_panel(self):
        return self.opponent_hand_panel.get_opponent_hand_panel_shapes()

    def get_opponent_unit_field(self):
        return self.opponent_unit_field.get_opponent_unit_field_shapes()

    def get_your_tomb(self):
        return self.your_tomb.get_tomb_shapes()

    def get_your_lost_zone(self):
        return self.your_lost_zone.get_lost_zone_shapes()

    def get_your_trap(self):
        return self.your_trap.get_trap_shapes()

    def get_your_deck(self):
        return self.your_deck.get_your_deck_shapes()

    def get_your_main_character(self):
        return self.your_main_character.get_main_character_shapes()

    def get_your_hand_panel(self):
        return self.your_hand_panel.get_your_hand_panel_shapes()

    def get_your_unit_field(self):
        return self.your_unit_field.get_your_unit_field_shapes()

    def get_battle_field_environment(self):
        return self.battle_field_environment.get_environment_shapes()

    def get_turn_end_button(self):
        return self.turn_end_button.get_turn_end_button_shapes()



class PreDrawedBattleFieldFrameRefactorForWinTest(OpenGLFrame):

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

        self.battle_field_scene = BattleFieldSceneForWinTest()
        self.battle_field_scene.create_battle_field_scene()

        self.alpha_background = self.create_opengl_alpha_background()

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
        self.turn_end_button_shapes = self.battle_field_scene.get_turn_end_button()


        self.your_hand_repository = YourHandRepository.getInstance()
        self.your_hand_repository.save_current_hand_state([8, 19, 151, 2, 9, 20, 30, 6])
        self.your_hand_repository.create_hand_card_list()

        self.your_deck_repository = YourDeckRepository.getInstance()
        self.your_deck_repository.save_deck_state([93, 93, 93, 5])

        self.battle_field_repository = BattleFieldRepository.getInstance()

        self.hand_card_list = self.your_hand_repository.get_current_hand_card_list()

        self.your_field_unit_repository = YourFieldUnitRepository.getInstance()

        self.your_tomb_repository = YourTombRepository.getInstance()
        # TODO: Naming Issue
        self.card_info = CardInfoFromCsvRepositoryImpl.getInstance()

        self.your_lightning_border_list = []
        self.boost_selection = False

        self.support_card_handler = SupportCardHandler.getInstance()
        self.current_process_card_id = 0

        self.left_click_detector = LeftClickDetector.getInstance()

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

        for turn_end_button_shape in self.turn_end_button_shapes:
            turn_end_button_shape.draw()




    def redraw(self):
        self.tkMakeCurrent()
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

        self.draw_base()



        # 필드 배치 유닛 시작
        for field_unit in self.your_field_unit_repository.get_current_field_unit_list():
            fixed_card_base = field_unit.get_fixed_card_base()
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
                # if isinstance(attached_shape, CircleImage):
                # print(f"attached_shape: {attached_shape.vertices}")
                # print(f"attached_shape: {attached_shape.center}")
                attached_shape.draw()

        if self.selected_object:
            card_base = None

            # TODO: Ugly -> Need to Refactor
            if isinstance(self.selected_object, FixedFieldCard):
                card_base = self.selected_object.get_fixed_card_base()
            elif isinstance(self.selected_object, PickableCard):
                card_base = self.selected_object.get_pickable_card_base()

            self.lightning_border.set_padding(50)
            self.lightning_border.update_shape(card_base)
            self.lightning_border.draw_lightning_border()

        if self.active_panel_rectangle:
            self.active_panel_rectangle.draw()

        for your_lightning_border in self.your_lightning_border_list:
            self.lightning_border.set_padding(20)
            self.lightning_border.update_shape(your_lightning_border)
            self.lightning_border.draw_lightning_border()

        if self.battle_field_repository.is_game_over:
            self.alpha_background.draw()
            self.battle_field_scene.create_win_panel()
            for win_panel_shape in self.battle_field_scene.get_win_panel():
                win_panel_shape.draw()

        self.tkSwapBuffers()

    def create_opengl_alpha_background(self):
        rectangle_color = (0.0, 0.0, 0.0, 0.65)

        new_rectangle = Rectangle(rectangle_color,
                                  [(0, 0), (self.width, 0), (self.width, self.height), (0, self.height)])
        return new_rectangle

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

        # if self.selected_object and self.drag_start:
        #     pickable_card = self.selected_object.get_pickable_card_base()
        #
        #     dx = x - self.drag_start[0]
        #     dy = y - self.drag_start[1]
        #     dy *= -1
        #
        #     new_vertices = [
        #         (vx + dx, vy + dy) for vx, vy in pickable_card.vertices
        #     ]
        #     pickable_card.update_vertices(new_vertices)
        #
        #     tool_card = self.selected_object.get_tool_card()
        #     if tool_card is not None:
        #         new_tool_card_vertices = [
        #             (vx + dx, vy + dy) for vx, vy in tool_card.vertices
        #         ]
        #         tool_card.update_vertices(new_tool_card_vertices)
        #
        #     for attached_shape in pickable_card.get_attached_shapes():
        #         new_attached_shape_vertices = [
        #             (vx + dx, vy + dy) for vx, vy in attached_shape.vertices
        #         ]
        #         attached_shape.update_vertices(new_attached_shape_vertices)
        #
        #     self.drag_start = (x, y)

    def return_to_initial_location(self):
        # pickable_card_base = self.selected_object.get_pickable_card_base()
        # intiial_vertices = pickable_card_base.get_initial_vertices()
        #
        # pickable_card_base.update_vertices(intiial_vertices)
        #
        # tool_card = self.selected_object.get_tool_card()
        # if tool_card is not None:
        #     tool_intiial_vertices = tool_card.get_initial_vertices()
        #     tool_card.update_vertices(tool_intiial_vertices)
        #
        # for attached_shape in pickable_card_base.get_attached_shapes():
        #     if isinstance(attached_shape, CircleImage):
        #         attached_circle_shape_initial_center = attached_shape.get_initial_center()
        #         # print(f"attached_circle_image_shape: {attached_circle_shape_initial_center}")
        #         attached_shape.update_circle_vertices(attached_circle_shape_initial_center)
        #         continue
        #
        #     if isinstance(attached_shape, CircleNumberImage):
        #         attached_circle_shape_initial_center = attached_shape.get_initial_center()
        #         # print(f"attached_circle_image_shape: {attached_circle_shape_initial_center}")
        #         attached_shape.update_circle_vertices(attached_circle_shape_initial_center)
        #         continue
        #
        #     attached_shape_intiial_vertices = attached_shape.get_initial_vertices()
        #     attached_shape.update_vertices(attached_shape_intiial_vertices)

        LocationInitializer.return_to_initial_location(self.selected_object)

        self.drag_start = None

    def on_canvas_release(self, event):
        x, y = event.x, event.y
        y = self.winfo_reqheight() - y

        # if self.boost_selection:

        # release_handler = ReleaseHandler(self.selected_object, self.your_hand_repository,
        #                                  self.your_field_unit_repository, self.card_info)
        # release_handler.handle_release(x, y)

        if isinstance(self.selected_object, PickableCard):
            # print("I'm PickableCard")
            current_field_unit_list = self.your_field_unit_repository.get_current_field_unit_list()
            current_field_unit_list_length = len(current_field_unit_list)

            # 현재 Your Field Unit에게 에너지 부착 및 도구 부착
            if current_field_unit_list_length > 0:
                for unit_index, current_field_unit in enumerate(current_field_unit_list):
                    # print(f"type(current_field_unit): {type(current_field_unit)}")
                    fixed_card_base = current_field_unit.get_fixed_card_base()
                    if fixed_card_base.is_point_inside((x, y)):
                        print("fixed field unit detect something comes inside!")

                        placed_card_id = self.selected_object.get_card_number()
                        card_type = self.card_info.getCardTypeForCardNumber(placed_card_id)

                        if card_type == CardType.TOOL.value:
                            self.selected_object = None

                            # TODO: 배포덱에서는 도구를 사용하지 않음
                            print("도구를 붙입니다!")
                            self.your_hand_repository.remove_card_by_id(placed_card_id)
                            self.your_hand_repository.replace_hand_card_position()

                            return
                        elif card_type == CardType.ENERGY.value:
                            self.selected_object = None

                            print("에너지를 붙입니다!")
                            self.your_hand_repository.remove_card_by_id(placed_card_id)
                            self.your_field_unit_repository.get_attached_energy_info().add_energy_at_index(unit_index,
                                                                                                           1)
                            self.your_hand_repository.replace_hand_card_position()
                            # TODO: attached_energy 값 UI에 표현 (이미지 작업 미완료)

                            # TODO: 특수 에너지 붙인 것을 어떻게 표현 할 것인가 ? (아직 미정)
                            return
                        # else:
                        #     self.return_to_initial_location()

                        # self.your_field_unit_repository.create_field_unit_card(placed_card_id)
                        # self.your_field_unit_repository.save_current_field_unit_state(placed_card_id)

                        # self.selected_object = None

            y *= -1

            # TODO: 현재 마우스 포인트(점)로 감지하나 추후 면으로 감지하도록 만들어야 함
            if self.is_drop_location_valid_your_unit_field(x, y):
                if self.selected_object:
                    placed_card_id = self.selected_object.get_card_number()
                    print(f"my card number is {placed_card_id}")
                    card_type = self.card_info.getCardTypeForCardNumber(placed_card_id)
                    print(f"my card type is {card_type}")

                    if card_type == CardType.UNIT.value:
                        # TODO: Memory Leak 발생하지 않도록 좀 더 꼼꼼하게 리소스 해제 하는지 확인해야함
                        self.your_hand_repository.remove_card_by_id(placed_card_id)
                        self.your_field_unit_repository.create_field_unit_card(placed_card_id)
                        self.your_field_unit_repository.save_current_field_unit_state(placed_card_id)

                        # 카드 구성하는 모든 도형에 local_translation 적용
                        self.your_hand_repository.replace_hand_card_position()

                        self.selected_object = None
                        return

                    if card_type == CardType.SUPPORT.value:
                        print("서포트 카드 사용 감지!")
                        self.selected_object = None
                        self.prev_selected_object = None

                        # 현재 필드에 존재하는 모든 유닛에 Lightning Border
                        for fixed_field_unit_card in self.your_field_unit_repository.get_current_field_unit_list():
                            print("에너지 부스팅 준비")
                            card_base = fixed_field_unit_card.get_fixed_card_base()
                            self.your_lightning_border_list.append(card_base)

                        self.current_process_card_id = placed_card_id
                        self.your_hand_repository.remove_card_by_id(placed_card_id)

                        tomb_state = self.your_tomb_repository.current_tomb_state
                        tomb_state.place_unit_to_tomb(placed_card_id)
                        self.your_hand_repository.replace_hand_card_position()

                        self.boost_selection = True

                        return

                    self.return_to_initial_location()

            else:
                self.return_to_initial_location()

    def is_drop_location_valid_your_unit_field(self, x, y):
        valid_area_vertices = [(300, 580), (1600, 580), (1600, 730), (300, 730)]

        return self.point_inside_polygon(x, y, valid_area_vertices)

    def point_inside_polygon(self, x, y, poly):
        n = len(poly)
        inside = False

        p1x, p1y = poly[0]
        for i in range(1, n + 1):
            p2x, p2y = poly[i % n]
            if y > min(p1y, p2y):
                if y <= max(p1y, p2y):
                    if x <= max(p1x, p2x):
                        if p1y != p2y:
                            xinters = (y - p1y) * (p2x - p1x) / (p2y - p1y) + p1x
                        if p1x == p2x or x <= xinters:
                            inside = not inside
            p1x, p1y = p2x, p2y

        return inside

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

            # FixedFieldCard (Field Unit Card List)
            for field_unit in self.your_field_unit_repository.get_current_field_unit_list():
                field_unit.selected = False

            # for field_unit in self.your_field_unit_repository.get_current_field_unit_list():
            #     fixed_card_base = field_unit.get_fixed_card_base()
            #
            #     if fixed_card_base.is_point_inside((x, y)):
            #         field_unit.selected = not field_unit.selected
            #         self.selected_object = field_unit
            #         self.drag_start = (x, y)
            #
            #         if self.selected_object != self.prev_selected_object:
            #             self.active_panel_rectangle = None
            #             self.prev_selected_object = self.selected_object
            #
            #             if self.boost_selection:
            #                 self.your_lightning_border_list = []
            #                 print("덱에서 에너지 검색해서 부스팅 진행")
            #
            #                 proper_handler = self.support_card_handler.getSupportCardHandler(
            #                     self.current_process_card_id)
            #                 # def energy_boost_from_deck_as_possible(self, target_unit_index)
            #                 proper_handler(field_unit.get_index())
            #                 self.boost_selection = False
            #
            #         break

            selected_field_unit = (self.left_click_detector
                                   .which_one_select_is_in_your_field_unit_list_area((x, y),
                                                                                     self.your_field_unit_repository.get_current_field_unit_list(),
                                                                                     self.winfo_reqheight()))

            if selected_field_unit:
                selected_field_unit.selected = not selected_field_unit.selected
                self.selected_object = selected_field_unit
                self.drag_start = (x, y)

                if self.selected_object != self.prev_selected_object:
                    self.active_panel_rectangle = None
                    self.prev_selected_object = self.selected_object

                    if self.boost_selection:
                        self.your_lightning_border_list = []
                        print("덱에서 에너지 검색해서 부스팅 진행")

                        proper_handler = self.support_card_handler.getSupportCardHandler(
                            self.current_process_card_id)
                        proper_handler(selected_field_unit.get_index())
                        self.boost_selection = False


            selected_button = self.left_click_detector.which_one_select_is_in_extra_area((x, y),
                                                                                         self.battle_field_repository.get_battle_field_button_list(),
                                                                                         self.winfo_reqheight())
            if selected_button:
                selected_button.invoke_click_event()


        except Exception as e:
            print(f"Exception in on_canvas_click: {e}")

    def on_canvas_right_click(self, event):
        x, y = event.x, event.y

        if self.selected_object and isinstance(self.selected_object, FixedFieldCard):
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

class WinPanel:
    __pre_drawed_image_instance = PreDrawedImage.getInstance()
    __battle_field_repository = BattleFieldRepository.getInstance()
    __battle_field_function_controller = BattleFieldFunctionControllerImpl.getInstance()

    def __init__(self, local_translation=(0, 0), scale=1):
        self.shapes = []
        self.local_translation = local_translation
        self.scale = scale

    def get_win_panel_shapes(self):
        return self.shapes

    def add_shape(self, shape):
        shape.local_translate(self.local_translation)
        self.shapes.append(shape)

    def create_win_panel(self, is_win):
        win_panel = RectangleImage(self.__pre_drawed_image_instance.get_pre_draw_your_card_deck(),
                                                vertices=[(750, 300), (1150, 300), (1150,600), (750,600)])
        self.add_shape(win_panel)


        text_vertices = [(850,380),(1050, 380), (1050, 530), (850,530)]
        if is_win:
            text_image = RectangleImage(
                image_data=self.__pre_drawed_image_instance.get_pre_draw_win_text(),
                vertices=text_vertices
            )
        else:
            text_image = RectangleImage(
                image_data=self.__pre_drawed_image_instance.get_pre_draw_lose_text(),
                vertices=text_vertices
            )
        self.add_shape(text_image)




    def init_shapes(self):
            self.create_win_panel(
                              is_win=self.__battle_field_repository.is_win)


class UglyTestWin(unittest.TestCase):
    def test_win_ugly(self):
        DomainInitializer.initEachDomain()

        root = tkinter.Tk()
        root.geometry(f"{root.winfo_screenwidth()}x{root.winfo_screenheight()}-0-0")
        root.deiconify()

        root.title("Win Test")


        pre_drawed_battle_field_frame = PreDrawedBattleFieldFrameRefactorForWinTest(root)
        pre_drawed_battle_field_frame.pack(fill=tkinter.BOTH, expand=1)
        root.update_idletasks()

        def animate():
            pre_drawed_battle_field_frame.redraw()
            root.after(17, animate)

        root.after(0, animate)
        win_button = tkinter.Button(master=root, text="win!!")
        win_button.place(relx=0.3, rely=0.5, anchor="center")

        lose_button = tkinter.Button(master=root, text="loseTT")
        lose_button.place(relx=0.7, rely=0.5, anchor="center")

        close_button = tkinter.Button(master=root, text="close")
        close_button.place(relx=0.5, rely=0.5, anchor="center")
        def win(event):
            BattleFieldRepository.getInstance().is_game_over=True
            BattleFieldRepository.getInstance().is_win=True

        def lose(event):
            BattleFieldRepository.getInstance().is_game_over=True
            BattleFieldRepository.getInstance().is_win = False

        def close(event):
            BattleFieldRepository.getInstance().is_game_over=False

        win_button.bind("<Button-1>", win)
        lose_button.bind("<Button-1>", lose)
        close_button.bind("<Button-1>", close)

        root.mainloop()




if __name__ == '__main__':
    unittest.main()