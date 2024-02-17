from battle_field.entity.battle_field_scene import BattleFieldScene

import tkinter
import unittest

from OpenGL.GL import *
from OpenGL.GLU import *
from pyopengltk import OpenGLFrame

from battle_field.infra.your_field_unit_repository import YourFieldUnitRepository
from battle_field.infra.your_hand_repository import YourHandRepository
from battle_field_fixed_card.fixed_field_card import FixedFieldCard
from card_info_from_csv.repository.card_info_from_csv_repository_impl import CardInfoFromCsvRepositoryImpl
from common.card_type import CardType
from initializer.init_domain import DomainInitializer
from opengl_battle_field_pickable_card.pickable_card import PickableCard
from opengl_rectangle_lightning_border.lightning_border import LightningBorder
from opengl_shape.rectangle import Rectangle


class PreDrawedBattleFieldFrameRefactor(OpenGLFrame):
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

        self.battle_field_scene = BattleFieldScene()
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

        self.your_hand_repository = YourHandRepository.getInstance()
        self.your_hand_repository.save_current_hand_state([6, 8, 19, 151])
        self.your_hand_repository.create_hand_card_list()

        self.hand_card_list = self.your_hand_repository.get_current_hand_card_list()

        # # add fixed field unit
        # self.battle_field_unit = FixedFieldCard(local_translation=(300, 580))
        # self.battle_field_unit.init_card(32)

        self.your_field_unit_repository = YourFieldUnitRepository.getInstance()
        # TODO: Naming Issue
        self.card_info = CardInfoFromCsvRepositoryImpl.getInstance()

        self.bind("<Configure>", self.on_resize)
        self.bind("<B1-Motion>", self.on_canvas_drag)
        self.bind("<ButtonRelease-1>", self.on_canvas_release)
        self.bind("<Button-1>", self.on_canvas_left_click)
        self.bind("<Button-3>", self.on_canvas_right_click)

    def initgl(self):
        glClearColor(1.0, 1.0, 1.0, 0.0)
        glOrtho(0, self.width, self.height, 0, -1, 1)

        self.tkMakeCurrent()
        # self.draw_base()

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
        # attached_tool_card = self.battle_field_unit.get_tool_card()
        # if attached_tool_card is not None:
        #     attached_tool_card.draw()
        #
        # fixed_card_base = self.battle_field_unit.get_fixed_card_base()
        # fixed_card_base.draw()
        #
        # attached_shape_list = fixed_card_base.get_attached_shapes()
        #
        # for attached_shape in attached_shape_list:
        #     attached_shape.draw()

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
            # self.redraw()

    def on_canvas_release(self, event):
        x, y = event.x, event.y
        y = self.winfo_reqheight() - y

        # if self.selected_object and self.drag_start:
        if isinstance(self.selected_object, PickableCard):
            y *= -1

            if self.is_drop_location_valid(x, y):
                placed_card_id = self.selected_object.get_card_number()
                # print(f"on_canvas_release -> placed_card_id: {placed_card_id}")

                card_type = self.card_info.getCardTypeForCardNumber(placed_card_id)
                # print(f"card_type: {card_type}")
                if card_type != CardType.UNIT.value:
                    return

                # TODO: Memory Leak 발생하지 않도록 좀 더 꼼꼼하게 리소스 해제 하는지 확인해야함
                self.your_hand_repository.remove_card_by_id(placed_card_id)
                self.your_field_unit_repository.create_field_unit_card(placed_card_id)
                self.your_field_unit_repository.save_current_field_unit_state(placed_card_id)

                self.selected_object = None

    def is_drop_location_valid(self, x, y):
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
                if isinstance(hand_card, PickableCard):
                    hand_card.selected = False

            self.selected_object = None

            for hand_card in reversed(self.hand_card_list):
                print(f"type(hand_card) = {type(hand_card)}")
                pickable_card_base = hand_card.get_pickable_card_base()
                print(f"type(pickable_card_base) = {type(pickable_card_base)}")

                if pickable_card_base.is_point_inside((x, y)):
                    hand_card.selected = not hand_card.selected
                    self.selected_object = hand_card
                    self.drag_start = (x, y)

                    if self.selected_object != self.prev_selected_object:
                        self.active_panel_rectangle = None
                        self.prev_selected_object = self.selected_object

                    break

            # # Field Unit
            # print("let's find field unit")
            # if isinstance(self.battle_field_unit, FixedFieldCard):
            #     self.battle_field_unit.selected = False
            #
            # print(f"type(fixed_card_base) = {type(self.battle_field_unit)}")
            #
            # fixed_card_base = self.battle_field_unit.get_fixed_card_base()
            #
            # if fixed_card_base.is_point_inside((x, y)):
            #     # fixed_card_base.selected = not fixed_card_base.selected
            #     self.battle_field_unit.selected = not self.battle_field_unit.selected
            #     self.selected_object = self.battle_field_unit
            #     print("selected fixed field unit")
            #
            #     if self.selected_object != self.prev_selected_object:
            #         self.active_panel_rectangle = None
            #         self.prev_selected_object = self.selected_object

            for field_unit in self.your_field_unit_repository.get_current_field_unit_list():
                if isinstance(field_unit, FixedFieldCard):
                    field_unit.selected = False

            for field_unit in self.your_field_unit_repository.get_current_field_unit_list():
                print(f"type(field_unit) = {type(field_unit)}")
                fixed_card_base = field_unit.get_fixed_card_base()
                print(f"type(fixed_card_base) = {type(fixed_card_base)}")

                if fixed_card_base.is_point_inside((x, y)):
                    field_unit.selected = not field_unit.selected
                    self.selected_object = field_unit
                    self.drag_start = (x, y)

                    if self.selected_object != self.prev_selected_object:
                        self.active_panel_rectangle = None
                        self.prev_selected_object = self.selected_object

                    break

        except Exception as e:
            print(f"Exception in on_canvas_click: {e}")

    def on_canvas_right_click(self, event):
        x, y = event.x, event.y

        print(f"selected_object: {self.selected_object}")
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


class TestDrawBattleFieldHandListWithConstraint(unittest.TestCase):

    def test_draw_battle_field_hand_list_with_constraint(self):
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
