from battle_field.entity.battle_field_environment import BattleFieldEnvironment
from battle_field.entity.battle_field_scene import BattleFieldScene
from battle_field.entity.opponent_deck import OpponentDeck
from battle_field.entity.opponent_hand_panel import OpponentHandPanel
from battle_field.entity.opponent_lost_zone import OpponentLostZone
from battle_field.entity.opponent_main_character import OpponentMainCharacter
from battle_field.entity.opponent_tomb import OpponentTomb
from battle_field.entity.opponent_trap import OpponentTrap
from battle_field.entity.opponent_unit_field import OpponentUnitField
from battle_field.entity.your_deck import YourDeck
from battle_field.entity.your_hand_panel import YourHandPanel
from battle_field.entity.your_lost_zone import YourLostZone
from battle_field.entity.your_main_character import YourMainCharacter
from battle_field.entity.your_tomb import YourTomb
from battle_field.entity.your_trap import YourTrap
from battle_field.entity.your_unit_field import YourUnitField

import tkinter
import unittest

from OpenGL.GL import *
from OpenGL.GLU import *
from pyopengltk import OpenGLFrame

from battle_field.infra.your_hand_repository import YourHandRepository
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

        self.click_card_effect_rectangle = None
        self.selected_object = None
        self.prev_selected_object = None
        self.drag_start = None

        self.click_card_effect_rectangles = []
        self.selected_objects = []
        self.checking_draw_effect = {}

        self.lightning_border = LightningBorder()

        self.battle_field_scene = BattleFieldScene()
        self.battle_field_scene.create_battle_field_scene()

        self.alpha_background = self.create_opengl_alpha_background()
        self.ok_button = self.create_ok_button()

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
        self.your_hand_repository.save_current_hand_state([6, 8, 19, 20, 151])
        #self.your_hand_repository.create_hand_card_list()
        self.your_hand_repository.create_hand_card_list_muligun()

        self.hand_card_list = self.your_hand_repository.get_current_hand_card_list()
        print(f"뭐가 나오냐?{self.hand_card_list}")

        self.bind("<Configure>", self.on_resize)
        # self.bind("<ButtonRelease-1>", self.on_canvas_release)
        self.bind("<Button-1>", self.on_canvas_left_click)
        # self.bind("<Button-3>", self.on_canvas_right_click)

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
        # glClearColor(1.0, 1.0, 1.0, 0.0)
        # glOrtho(0, self.width, self.height, 0, -1, 1)
        #
        # glViewport(0, 0, self.width, self.height)
        # glMatrixMode(GL_PROJECTION)
        # glLoadIdentity()
        # gluOrtho2D(0, self.width, self.height, 0)
        # glMatrixMode(GL_MODELVIEW)
        # glLoadIdentity()

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
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

        self.draw_base()
        self.alpha_background.draw()
        self.ok_button.draw()

        # 처음 드로우한 5장의 카드 그리는 부분
        for hand_card in self.hand_card_list:
            attached_tool_card = hand_card.get_tool_card()
            if attached_tool_card is not None:
                attached_tool_card.draw()

            pickable_card_base = hand_card.get_pickable_card_base()
            pickable_card_base.draw()

            attached_shape_list = pickable_card_base.get_attached_shapes()

            for attached_shape in attached_shape_list:
                attached_shape.draw()

        #self.draw_pick_card_effect()
        self.draw_pick_card_effect_dict()


        self.tkSwapBuffers()

    # 바꿀 카드 클릭 했을 때 효과
    # def draw_pick_card_effect(self):
    #     for hand_card, click_card_effect_rectangle in zip(self.selected_objects, self.click_card_effect_rectangles):
    #         if hand_card:
    #             pickable_card_base = hand_card.get_pickable_card_base()
    #
    #             self.lightning_border.set_padding(50)
    #             self.lightning_border.update_shape(pickable_card_base)
    #             self.lightning_border.draw_lightning_border()
    #
    #         if click_card_effect_rectangle:
    #
    #             glEnable(GL_BLEND)
    #             glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    #
    #             click_card_effect_rectangle.draw()

    def draw_pick_card_effect_dict(self):
        for hand_card_id, click_card_effect_rectangle in self.checking_draw_effect.items():
            hand_card = self.get_hand_card_by_id(hand_card_id)
            if hand_card:
                pickable_card_base = hand_card.get_pickable_card_base()

                self.lightning_border.set_padding(50)
                self.lightning_border.update_shape(pickable_card_base)
                self.lightning_border.draw_lightning_border()

            if click_card_effect_rectangle:
                glEnable(GL_BLEND)
                glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

                click_card_effect_rectangle.draw()

    def get_hand_card_by_id(self, hand_card_id):
        for hand_card in self.hand_card_list:
            if id(hand_card) == hand_card_id:
                return hand_card
        return None

    def on_canvas_left_click(self, event):
        try:
            x, y = event.x, event.y
            y = self.winfo_reqheight() - y

            for hand_card in self.hand_card_list:
                if isinstance(hand_card, PickableCard):
                    hand_card.selected = False

            self.selected_object = None

            for hand_card in reversed(self.hand_card_list):
                pickable_card_base = hand_card.get_pickable_card_base()

                if pickable_card_base.is_point_inside((x, y)):
                    hand_card.selected = not hand_card.selected
                    self.selected_object = hand_card
                    hand_card_id = id(hand_card)
                    # self.selected_objects.append(hand_card_id)
                    print(f"교체할 카드가 뭐야? : {self.selected_objects}")

                    fixed_x, fixed_y = pickable_card_base.get_local_translation()
                    new_rectangle = self.create_change_card_expression((fixed_x, fixed_y))
                    self.click_card_effect_rectangle = new_rectangle
                    # self.click_card_effect_rectangles.append(new_rectangle)

                    # 교체할 카드 이미 효과 있으면 지우기.
                    if hand_card_id in self.checking_draw_effect:
                        del self.checking_draw_effect[hand_card_id]
                        print(self.checking_draw_effect)
                        print(list(self.checking_draw_effect.keys()))

                    else:
                        fixed_x, fixed_y = pickable_card_base.get_local_translation()
                        new_rectangle = self.create_change_card_expression((fixed_x, fixed_y))
                        self.checking_draw_effect[hand_card_id] = new_rectangle
                        print(self.checking_draw_effect)
                        print(list(self.checking_draw_effect.keys()))

        except Exception as e:
            print(f"Exception in on_canvas_click: {e}")


    # def on_canvas_right_click(self, event):
    #     x, y = event.x, event.y
    #
    #     if self.selected_object:
    #         convert_y = self.winfo_reqheight() - y
    #         pickable_card_base = self.selected_object.get_pickable_card_base()
    #         print(f"내가 클릭한 카드 local: {pickable_card_base.get_local_translation()}")
    #         if pickable_card_base.is_point_inside((x, convert_y)):
    #             fixed_x, fixed_y = pickable_card_base.get_local_translation()
    #             new_rectangle = self.create_change_card_expression((fixed_x, fixed_y))
    #             self.click_card_effect_rectangle = new_rectangle



    # 멀리건 화면에서 교체하려는 카드 클릭시 나타나는 표현
    def create_change_card_expression(self, start_point):
        rectangle_size = 300
        rectangle_color = (0.0, 0.0, 0.0, 0.65)

        end_point = (start_point[0] + rectangle_size, start_point[1] + rectangle_size * 1.62)

        new_rectangle = Rectangle(rectangle_color, [
            (start_point[0], start_point[1]),
            (end_point[0], start_point[1]),
            (end_point[0], end_point[1]),
            (start_point[0], end_point[1])
        ])
        new_rectangle.created_by_right_click = True
        return new_rectangle

    def create_opengl_alpha_background(self):
        rectangle_color = (0.0, 0.0, 0.0, 0.65)

        new_rectangle = Rectangle(rectangle_color,
                                  [(0, 0), (self.width, 0), (self.width, self.height), (0, self.height)])
        return new_rectangle

    def create_ok_button(self):
        rectangle_size = 100
        rectangle_color = (0.8314, 0.7686, 0.6588, 1.0)

        start_point = (850, 900)  # 확인 버튼 위치는 고정.
        end_point = (start_point[0] + rectangle_size * 2.0, start_point[1] + rectangle_size * 0.55)

        new_rectangle = Rectangle(rectangle_color, [
            (start_point[0], start_point[1]),
            (end_point[0], start_point[1]),
            (end_point[0], end_point[1]),
            (start_point[0], end_point[1])
        ])
        new_rectangle.created_by_right_click = True
        return new_rectangle


class TestDrawBattleFieldMuligun(unittest.TestCase):

    def test_draw_battle_field_muligun(self):
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
            # root.after(33, animate)

        root.after(0, animate)

        root.mainloop()


if __name__ == '__main__':
    unittest.main()
