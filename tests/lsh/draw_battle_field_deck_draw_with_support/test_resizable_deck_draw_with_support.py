from screeninfo import get_monitors

from battle_field.components.field_area_inside.field_area_action import FieldAreaAction
from battle_field.components.field_area_inside.legacy.circle_image_legacy_field_area_inside_handler import CircleImageLegacyFieldAreaInsideHandler

import tkinter
import unittest

from OpenGL.GL import *
from OpenGL.GLU import *
from pyopengltk import OpenGLFrame

from battle_field.handler.legacy.circle_image_legacy_support_card_handler import CircleImageLegacySupportCardHandler
from battle_field.infra.legacy.circle_image_legacy_opponent_field_unit_repository import CircleImageLegacyOpponentFieldUnitRepository
from battle_field.infra.your_deck_repository import YourDeckRepository
from battle_field.infra.legacy.circle_image_legacy_your_field_unit_repository import CircleImageLegacyYourFieldUnitRepository
from battle_field.infra.legacy.circle_image_legacy_your_hand_repository import CircleImageLegacyYourHandRepository
from battle_field.infra.legacy.circle_image_legacy_your_tomb_repository import CircleImageLegacyYourTombRepository
from battle_field_fixed_card.legacy.circle_image_legacy_fixed_field_card import LegacyFixedFieldCard
from battle_field_muligun.entity.scene.battle_field_muligun_scene import BattleFieldMuligunScene
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

        self.your_deck_repository = YourDeckRepository.getInstance()
        self.your_deck_list = None

        self.your_field_unit_repository = CircleImageLegacyYourFieldUnitRepository.getInstance()

        self.card_info_repository = CardInfoFromCsvRepositoryImpl.getInstance()

        self.pre_drawed_image_instance = PreDrawedImage.getInstance()

        self.your_field_unit_lightning_border_list = []
        self.boost_selection = False

        self.support_card_handler = CircleImageLegacySupportCardHandler.getInstance()
        self.current_process_card_id = 0

        self.your_tomb_repository = CircleImageLegacyYourTombRepository.getInstance()

        self.opponent_field_unit_repository = CircleImageLegacyOpponentFieldUnitRepository.getInstance()
        # self.opponent_fixed_unit_card_inside_handler = OpponentFixedUnitCardInsideHandler.getInstance()
        self.field_area_inside_handler = CircleImageLegacyFieldAreaInsideHandler.getInstance()

        self.bind("<Configure>", self.on_resize)
        self.bind("<B1-Motion>", self.on_canvas_drag)
        self.bind("<ButtonRelease-1>", self.on_canvas_release)
        self.bind("<Button-1>", self.on_canvas_left_click)
        self.bind("<Button-3>", self.on_canvas_right_click)

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

        # 1848 기준 -> 1848 - (105 * 5 + 170 * 4) = 643
        # 643 / 2 = 321.5
        # 321.5 / 1848 = 17.4% => 0.174
        # 위 수식은 적합하지 않음 (0.286 포함)
        # 실제로 카드 좌측 하단 기준으로 170 이동이였음 (그러므로 카드간 간격은 65)
        # 1920 기준 -> 1920 - (105 * 5 + 65 * 4) = 1135
        # 1135 / 2 = 567.5
        self.your_hand_repository.set_x_base(567.5)
        self.your_hand_repository.save_current_hand_state([8, 20, 19, 151, 93])
        # self.your_hand_repository.save_current_hand_state([151])
        self.your_hand_repository.create_hand_card_list()

        self.your_deck_repository.save_deck_state([93, 93, 93, 5])

        self.opponent_field_unit_repository.create_field_unit_card(33)
        self.opponent_field_unit_repository.create_field_unit_card(35)
        self.opponent_field_unit_repository.create_field_unit_card(36)
        self.opponent_field_unit_repository.create_field_unit_card(25)
        self.opponent_field_unit_repository.create_field_unit_card(26)
        self.opponent_field_unit_repository.create_field_unit_card(27)

        self.hand_card_list = self.your_hand_repository.get_current_hand_card_list()

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
            current_field_unit_list = self.your_field_unit_repository.get_current_field_unit_list()
            current_field_unit_list_length = len(current_field_unit_list)

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

                        elif card_type == CardType.ENERGY.value:
                            print("에너지를 붙입니다!")
                            # self.selected_object = None
                            self.your_hand_repository.remove_card_by_index(placed_index)
                            self.your_field_unit_repository.get_attached_energy_info().add_energy_at_index(unit_index, 1)

                            your_fixed_field_unit = self.your_field_unit_repository.find_field_unit_by_index(unit_index)
                            fixed_card_base = your_fixed_field_unit.get_fixed_card_base()
                            fixed_card_attached_shape_list = fixed_card_base.get_attached_shapes()
                            placed_card_id = self.selected_object.get_card_number()
                            print(f"placed_card_id : {placed_card_id}")
                            print(f"card grade : {self.card_info_repository.getCardGradeForCardNumber(placed_card_id)}")

                            attached_energy_count = self.your_field_unit_repository.get_attached_energy_info().get_energy_at_index(unit_index)
                            self.your_hand_repository.replace_hand_card_position()
                            # TODO: attached_energy 값 UI에 표현 (이미지 작업 미완료)

                            # TODO: 특수 에너지 붙인 것을 어떻게 표현 할 것인가 ? (아직 미정)
                            for fixed_card_attached_shape in fixed_card_attached_shape_list:
                                if isinstance(fixed_card_attached_shape, CircleNumberImage):
                                    if fixed_card_attached_shape.get_circle_kinds() is CircleKinds.ENERGY:
                                        fixed_card_attached_shape.set_image_data(
                                            self.pre_drawed_image_instance.get_pre_draw_number_image(
                                                attached_energy_count))
                                        print(f"changed energy: {fixed_card_attached_shape.get_circle_kinds()}")

                            card_race = self.card_info_repository.getCardRaceForCardNumber(placed_card_id)
                            if card_race == CardRace.UNDEAD.value:
                                card_race_circle = your_fixed_field_unit.creat_fixed_card_energy_race_circle(
                                    color=(0, 0, 0, 1),
                                    vertices=(0, (attached_energy_count * 10) + 20),
                                    local_translation=fixed_card_base.get_local_translation())
                                fixed_card_base.set_attached_shapes(card_race_circle)

                            self.selected_object = None

                            return
                        else:
                            self.return_to_initial_location()
                            return

            y *= -1

            # if self.is_drop_location_valid_battle_field_panel(x, y):
            #     placed_card_id = self.selected_object.get_card_number()
            #     print(f"on_canvas_release -> placed_card_id: {placed_card_id}")
            #
            #     card_type = self.card_info_repository.getCardTypeForCardNumber(placed_card_id)
            #     if card_type == CardType.UNIT.value:
            #         # TODO: Memory Leak 발생하지 않도록 좀 더 꼼꼼하게 리소스 해제 하는지 확인해야함
            #         self.your_hand_repository.remove_card_by_id(placed_card_id)
            #         self.your_field_unit_repository.create_field_unit_card(placed_card_id)
            #         self.your_field_unit_repository.save_current_field_unit_state(placed_card_id)
            #
            #         # 카드 구성하는 모든 도형에 local_translation 적용
            #         self.your_hand_repository.replace_hand_card_position()
            #
            #         self.selected_object = None
            #         return
            #
            #     if card_type == CardType.SUPPORT.value:
            #         print("서포트 카드 사용 감지!")
            #         self.selected_object = None
            #         self.prev_selected_object = None
            #
            #         # 현재 필드에 존재하는 모든 유닛에 Lightning Border
            #         for fixed_field_unit_card in self.your_field_unit_repository.get_current_field_unit_list():
            #             print("에너지 부스팅 준비")
            #             card_base = fixed_field_unit_card.get_fixed_card_base()
            #             self.your_field_unit_lightning_border_list.append(card_base)
            #             self.current_process_card_id = placed_card_id
            #
            #         self.your_hand_repository.remove_card_by_id(placed_card_id)
            #
            #         tomb_state = self.your_tomb_repository.current_tomb_state
            #         tomb_state.place_unit_to_tomb(placed_card_id)
            #         self.your_hand_repository.replace_hand_card_position()
            #
            #         self.boost_selection = True
            #
            #         return
            #
            #     self.return_to_initial_location()
            # else:
            #     self.return_to_initial_location()

            # 당신(Your) Field에 던진 카드
            self.field_area_inside_handler.set_width_ratio(self.width_ratio)
            self.field_area_inside_handler.set_height_ratio(self.height_ratio)

            drop_action_result = self.field_area_inside_handler.handle_card_drop(x, y, self.selected_object, self.battle_field_unit_place_panel)
            if drop_action_result is None or drop_action_result is FieldAreaAction.Dummy:
                print("self.field_area_inside_handler.get_field_area_action() = None")
                self.return_to_initial_location()
            else:
                print("self.field_area_inside_handler.get_field_area_action() = Some Action")
                self.selected_object = None

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


class TestResizableDeckDrawWithSupport(unittest.TestCase):

    def test_resizable_deck_draw_with_support(self):
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
