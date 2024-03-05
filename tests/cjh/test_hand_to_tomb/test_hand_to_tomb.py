from battle_field.components.mouse_left_click.left_click_detector import LeftClickDetector
from battle_field.entity.legacy.battle_field_scene_legacy import BattleFieldSceneLegacy

import tkinter
import unittest

from OpenGL.GL import *
from OpenGL.GLU import *
from pyopengltk import OpenGLFrame

from battle_field.entity.legacy.your_tomb import YourTomb
from battle_field.handler.support_card_handler import SupportCardHandler
from battle_field.infra.battle_field_repository import BattleFieldRepository
from battle_field.infra.your_deck_repository import YourDeckRepository
from battle_field.infra.legacy.circle_image_legacy_your_field_unit_repository import CircleImageLegacyYourFieldUnitRepository
from battle_field.infra.legacy.circle_image_legacy_your_hand_repository import CircleImageLegacyYourHandRepository
from battle_field.infra.your_tomb_repository import YourTombRepository
from battle_field.state.current_tomb import CurrentTombState
from battle_field_fixed_card.legacy.fixed_field_card import LegacyFixedFieldCard
from card_info_from_csv.repository.card_info_from_csv_repository_impl import CardInfoFromCsvRepositoryImpl
from common.card_type import CardType
from image_shape.circle_image import CircleImage
from image_shape.circle_number_image import CircleNumberImage
from initializer.init_domain import DomainInitializer
from opengl_battle_field_pickable_card.legacy.pickable_card import LegacyPickableCard
from opengl_rectangle_lightning_border.lightning_border import LightningBorder
from opengl_shape.rectangle import Rectangle


class HandToTomb(OpenGLFrame):
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
        self.your_tomb = YourTomb()
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
        self.your_hand_repository.save_current_hand_state([8, 19, 151, 2, 9, 20, 30, 6])
        self.your_hand_repository.create_hand_card_list()

        self.your_deck_repository = YourDeckRepository.getInstance()
        self.your_deck_repository.save_deck_state([93, 93, 93, 5])

        self.hand_card_list = self.your_hand_repository.get_current_hand_card_list()

        self.your_field_unit_repository = CircleImageLegacyYourFieldUnitRepository.getInstance()

        self.your_tomb_repository = YourTombRepository.getInstance()
        self.tomb_card_list = self.your_tomb_repository.get_current_tomb_state()
        # TODO: Naming Issue
        self.card_info = CardInfoFromCsvRepositoryImpl.getInstance()

        self.your_lightning_border_list = []
        self.boost_selection = False

        self.support_card_handler = SupportCardHandler.getInstance()
        self.current_process_card_id = 0

        self.bind("<Configure>", self.on_resize)
        self.bind("<B1-Motion>", self.on_canvas_drag)
        self.bind("<ButtonRelease-1>", self.on_canvas_release)
        self.bind("<Button-1>", self.on_canvas_left_click)
        self.bind("<Button-3>", self.on_canvas_right_click)

        self.left_click_detector = LeftClickDetector.getInstance()
        self.battle_field_repository = BattleFieldRepository.getInstance()
        self.tomb_panel_rectangle = []
        self.current_tomb_state = CurrentTombState()

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
            if isinstance(self.selected_object, LegacyFixedFieldCard):
                card_base = self.selected_object.get_fixed_card_base()
            elif isinstance(self.selected_object, LegacyPickableCard):
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

        if self.tomb_panel_rectangle:

            glEnable(GL_BLEND)
            glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

            for rectangle in self.tomb_panel_rectangle:
                rectangle.draw()

                for tomb_card in self.your_tomb_repository.current_tomb_unit_list:
                    print(f"tomb_card_number_redraw: {tomb_card}")
                    tomb_card_base = tomb_card.get_fixed_card_base()
                    print(f"tomb_card_base:: {tomb_card_base}")
                    tomb_card_base.draw()

        self.tkSwapBuffers()


    def on_canvas_drag(self, event):
        x, y = event.x, event.y
        y = self.winfo_reqheight() - y

        if self.selected_object and self.drag_start:
            pickable_card = self.selected_object.get_pickable_card_base()

            dx = x - self.drag_start[0]
            dy = y - self.drag_start[1]
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

            for attached_shape in pickable_card.get_attached_shapes():
                new_attached_shape_vertices = [
                    (vx + dx, vy + dy) for vx, vy in attached_shape.vertices
                ]
                attached_shape.update_vertices(new_attached_shape_vertices)

            self.drag_start = (x, y)

    def return_to_initial_location(self):
        pickable_card_base = self.selected_object.get_pickable_card_base()
        initial_vertices = pickable_card_base.get_initial_vertices()

        pickable_card_base.update_vertices(initial_vertices)

        tool_card = self.selected_object.get_tool_card()
        if tool_card is not None:
            tool_initial_vertices = tool_card.get_initial_vertices()
            tool_card.update_vertices(tool_initial_vertices)

        for attached_shape in pickable_card_base.get_attached_shapes():
            if isinstance(attached_shape, CircleImage):
                attached_circle_shape_initial_center = attached_shape.get_initial_center()
                # print(f"attached_circle_image_shape: {attached_circle_shape_initial_center}")
                attached_shape.update_circle_vertices(attached_circle_shape_initial_center)
                continue

            if isinstance(attached_shape, CircleNumberImage):
                attached_circle_shape_initial_center = attached_shape.get_initial_center()
                # print(f"attached_circle_image_shape: {attached_circle_shape_initial_center}")
                attached_shape.update_circle_vertices(attached_circle_shape_initial_center)
                continue

            attached_shape_initial_vertices = attached_shape.get_initial_vertices()
            attached_shape.update_vertices(attached_shape_initial_vertices)

        self.drag_start = None

    def on_canvas_release(self, event):
        x, y = event.x, event.y
        y = self.winfo_reqheight() - y

        # if self.boost_selection:

        if isinstance(self.selected_object, LegacyPickableCard):
            # print("I'm PickableCard")
            current_field_unit_list = self.your_field_unit_repository.get_current_field_unit_list()
            current_field_unit_list_length = len(current_field_unit_list)
            print(f"current_field_unit_list_length: {current_field_unit_list_length}")

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
                            self.your_field_unit_repository.get_attached_energy_info().add_energy_at_index(unit_index, 1)
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
                            assert isinstance(card_base, object)
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

            for hand_card in self.hand_card_list:
                if isinstance(hand_card, LegacyPickableCard):
                    hand_card.selected = False

            self.selected_object = None

            for hand_card in reversed(self.hand_card_list):
                # print(f"hand_card: {hand_card}")
                pickable_card_base = hand_card.get_pickable_card_base()

                if pickable_card_base.is_point_inside((x, y)):
                    hand_card.selected = not hand_card.selected
                    self.selected_object = hand_card
                    self.drag_start = (x, y)

                    if self.selected_object != self.prev_selected_object:
                        self.active_panel_rectangle = None
                        self.prev_selected_object = self.selected_object

                    break

            # Field Unit
            for field_unit in self.your_field_unit_repository.get_current_field_unit_list():
                if isinstance(field_unit, LegacyFixedFieldCard):
                    field_unit.selected = False

            for field_unit in self.your_field_unit_repository.get_current_field_unit_list():
                print(f"field_unit{field_unit}")
                fixed_card_base = field_unit.get_fixed_card_base()
                print(f"fixed_card_base{fixed_card_base}")
                placed_card_id = field_unit.get_card_number()
                print(f"placed_card_id {placed_card_id}")

                if fixed_card_base.is_point_inside((x, y)):
                    if self.boost_selection:
                        self.your_lightning_border_list = []
                        print("덱에서 에너지 검색해서 부스팅 진행")

                        proper_handler = self.support_card_handler.getSupportCardHandler(self.current_process_card_id)
                        # def energy_boost_from_deck_as_possible(self, target_unit_index)
                        proper_handler(field_unit.get_index())
                        break

                    field_unit.selected = not field_unit.selected
                    self.selected_object = field_unit
                    self.drag_start = (x, y)

                    if self.selected_object != self.prev_selected_object:
                        self.active_panel_rectangle = None
                        self.prev_selected_object = self.selected_object

                    self.your_field_unit_repository.remove_card_by_id(placed_card_id)
                    self.your_tomb_repository.create_tomb_card(placed_card_id)
                    self.your_tomb_repository.save_current_tomb_state(placed_card_id)
                    self.your_field_unit_repository.replace_field_card_position()
                    print(f"current_tomb_unit_list{self.your_tomb_repository.get_current_tomb_state()}")

            selected_button = self.left_click_detector.which_one_select_is_in_extra_area((x, y),
                                                                                         self.battle_field_repository.get_battle_field_button_list(),
                                                                                         self.winfo_reqheight())
            print(f"selected_button: {selected_button}")
            # print(f"current_tomb_unit_list test: {self.your_tomb_repository.get_current_tomb_state()}")
            if selected_button:
                print(f"current_tomb_unit_list test: {self.your_tomb_repository.current_tomb_unit_list}")
                tomb_background_rectangle = self.create_opengl_tomb_rectangle((100, 100))
                print(f"tomb_background_rectangle: {tomb_background_rectangle}")
                self.tomb_panel_rectangle.append(tomb_background_rectangle)


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
        rectangle_size = 100
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
    def create_opengl_tomb_rectangle(self, start_point):
        rectangle_size = 800
        rectangle_color = (1.0, 0.0, 0.0, 1.0)

        end_point = (start_point[0] + rectangle_size, start_point[1] + rectangle_size)

        new_rectangle = Rectangle(rectangle_color, [
            (start_point[0], start_point[1]),
            (end_point[0], start_point[1]),
            (end_point[0], end_point[1]),
            (start_point[0], end_point[1])
        ])

        new_rectangle.created_by_left_click = True

        return new_rectangle
    def handle_dead_button_click(self, rectangle):
        pass


class TestHandCardToTomb(unittest.TestCase):

    def test_hand_card_to_tomb(self):
        DomainInitializer.initEachDomain()

        root = tkinter.Tk()
        root.geometry(f"{root.winfo_screenwidth()}x{root.winfo_screenheight()}-0-0")
        root.deiconify()

        pre_drawed_battle_field_frame = HandToTomb(root)
        pre_drawed_battle_field_frame.pack(fill=tkinter.BOTH, expand=1)
        root.update_idletasks()

        def animate():
            pre_drawed_battle_field_frame.redraw()
            root.after(17, animate)

        root.after(0, animate)

        root.mainloop()


if __name__ == '__main__':
    unittest.main()
