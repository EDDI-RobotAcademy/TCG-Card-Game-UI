import tkinter

from OpenGL.GL import *
from OpenGL.GLU import *
from pyopengltk import OpenGLFrame
from screeninfo import get_monitors

from battle_field_muligun.infra.your_hand_repository import YourHandRepository
from battle_field_muligun.entity.scene.battle_field_muligun_scene import BattleFieldMuligunScene
from opengl_battle_field_pickable_card.pickable_card import PickableCard
from opengl_pickable_shape.pickable_rectangle import PickableRectangle
from opengl_rectangle_lightning_border.lightning_border import LightningBorder
from opengl_shape.rectangle import Rectangle

class BattleFieldMuligunFrame(OpenGLFrame):
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

        self.click_card_effect_rectangle = None
        self.selected_object = None
        self.execute_pick_card_effect = True
        self.ok_button_visible = True

        self.click_card_effect_rectangles = []
        self.selected_objects = []
        self.checking_draw_effect = {}
        self.change_card_object_list = {}

        self.lightning_border = LightningBorder()

        self.battle_field_muligun_scene = BattleFieldMuligunScene()
        self.battle_field_muligun_scene.create_battle_field_muligun_scene(self.width, self.height)
        self.battle_field_muligun_background_shape_list = self.battle_field_muligun_scene.get_battle_field_muligun_background()

        self.alpha_background = self.create_opengl_alpha_background()
        self.ok_button = self.create_ok_button()

        self.your_hand_repository = YourHandRepository.getInstance()
        # print(f"your_hand_repo: {self.your_hand_repository.get_current_hand_state()}")
        # self.your_hand_repository.save_current_hand_state([6, 8, 19, 20, 151])
        print("Call Muligun Frame Constructor")

        self.hand_card_list = None
        self.hand_card_state = None

        # self.select_card_id = self.your_hand_repository.select_card_id_list()
        # self.delete_select_card = self.your_hand_repository.delete_select_card()

        self.bind("<Configure>", self.on_resize)
        self.bind("<Button-1>", self.on_canvas_left_click)
        self.bind("<Button-3>", self.on_canvas_ok_button_click)

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

        self.hand_card_list = self.your_hand_repository.get_current_hand_card_list()
        self.hand_card_state = self.your_hand_repository.get_current_hand_state()
        self.your_hand_repository.create_hand_card_list()

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

    def start_redraw_loop(self):
        print(f"start_redraw_loop")
        self.after(17, self.redraw)

    def on_resize(self, event):
        self.reshape(event.width, event.height)

    def draw_base(self):
        for battle_field_muligun_background_shape in self.battle_field_muligun_background_shape_list:
            battle_field_muligun_background_shape.draw()

    def redraw(self):
        print("redrawing")
        if self.is_reshape_not_complete:
            return

        self.tkMakeCurrent()
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

        self.draw_base()
        self.alpha_background.draw()

        # glDisable(GL_BLEND)

        if self.ok_button_visible is True:
            self.ok_button.draw()

        for hand_card in self.hand_card_list:
            attached_tool_card = hand_card.get_tool_card()
            if attached_tool_card is not None:
                attached_tool_card.draw()

            pickable_card_base = hand_card.get_pickable_card_base()
            pickable_card_base.draw()

            attached_shape_list = pickable_card_base.get_attached_shapes()

            for attached_shape in attached_shape_list:
                attached_shape.draw()

        if self.execute_pick_card_effect is True:
            self.draw_pick_card_effect()

        self.tkSwapBuffers()

    def draw_pick_card_effect(self):
        for hand_card_index, click_card_effect_rectangle in self.checking_draw_effect.items():
            hand_card = self.get_hand_card_by_index(hand_card_index)
            if hand_card:
                pickable_card_base = hand_card.get_pickable_card_base()

                self.lightning_border.set_padding(50)
                self.lightning_border.update_shape(pickable_card_base)
                self.lightning_border.draw_lightning_border()

            if click_card_effect_rectangle:
                glEnable(GL_BLEND)
                glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

                click_card_effect_rectangle.draw()

    def get_hand_card_by_index(self, hand_card_index):
        for hand_card in self.hand_card_list:
            if self.hand_card_list.index(hand_card) == hand_card_index:
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
                    hand_card_index = self.hand_card_list.index(hand_card)
                    self.change_card_object_list[hand_card_index] = hand_card

                    fixed_x, fixed_y = pickable_card_base.get_local_translation()
                    new_rectangle = self.create_change_card_expression((fixed_x, fixed_y))
                    self.click_card_effect_rectangles.append(new_rectangle)

                    # 교체할 카드 선택 취소 기능)
                    if hand_card_index in self.checking_draw_effect:
                        del self.checking_draw_effect[hand_card_index]

                        # 선택한 카드 리스트에 담긴 것을 다시 지워야 함.
                        if hand_card_index in self.change_card_object_list:
                            del self.change_card_object_list[self.hand_card_list.index(hand_card)]

                    else:
                        fixed_x, fixed_y = pickable_card_base.get_local_translation()
                        new_rectangle = self.create_change_card_expression((fixed_x, fixed_y))
                        self.checking_draw_effect[hand_card_index] = new_rectangle
                        print(self.checking_draw_effect)
                        print(list(self.checking_draw_effect.keys()))

            # 확인 버튼 기능
            if self.ok_button.is_point_inside((x, y)):
                self.on_canvas_ok_button_click(event)

        except Exception as e:
            print(f"Exception in on_canvas_click: {e}")

    def on_canvas_ok_button_click(self, event):
        self.your_hand_repository.select_card_id_list(self.change_card_object_list)# 서버에 보내줄 카드 아이디 리스트로 저장.
        self.your_hand_repository.delete_select_card(self.change_card_object_list)# 처음 드로우한 5장의 카드 리스트에서 교체할 카드 삭제.

        # TODO: 새로 받을 카드 임의로 지정. 나중에는 서버에서 받아야 함. 임의로 넣었기 때문에 현재 2개만 교체 가능
        self.redraw_card()

        # 그려져 있는 카드 선택 효과, 그려져 있는 버튼은 지워야 함.
        self.click_card_effect_rectangles = []
        self.checking_draw_effect = {}
        self.ok_button_visible = False
        self.execute_pick_card_effect = False


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
        return new_rectangle

    # 검정 투명 배경 화면
    def create_opengl_alpha_background(self):
        rectangle_color = (0.0, 0.0, 0.0, 0.65)

        new_rectangle = Rectangle(rectangle_color,
                                  [(0, 0), (self.width, 0), (self.width, self.height), (0, self.height)])
        return new_rectangle

    # 확인 버튼
    def create_ok_button(self):
        rectangle_size = 100
        rectangle_color = (0.8314, 0.7686, 0.6588, 1.0)

        start_point = (850, 900)  # 확인 버튼 위치는 고정.
        end_point = (start_point[0] + rectangle_size * 2.0, start_point[1] + rectangle_size * 0.55)

        new_rectangle = PickableRectangle(rectangle_color, [
            (start_point[0], start_point[1]),
            (end_point[0], start_point[1]),
            (end_point[0], end_point[1]),
            (start_point[0], end_point[1])
        ])
        return new_rectangle


    # 처음 뽑은 5장 카드 리스트에서 뽑은 카드 삭제
    # def delete_select_card(self):
    #     change_card_index_list = self.change_card_object_list
    #     # print(f"바꿀 카드 잘 들어왔냐는?: {change_card_index_list}")
    #     # print(f"before- 상태: {self.hand_card_state}, 오브젝트: {self.hand_card_list}")
    #     for index in sorted(change_card_index_list.keys(), reverse=True):
    #         self.hand_card_state.pop(index)
    #         self.hand_card_list.pop(index)
    #
    #     print(f"after- 상태: {self.hand_card_state}, 오브젝트: {self.hand_card_list}")

    # 서버로 전달 받으면 다시 그릴 카드 리스트에 담기
    def redraw_card(self):
        # self.your_hand_repository.save_current_hand_state(new_card_number_list)
        # print(f"현재 카드 뭐 있니?: {self.hand_card_state}")
        self.your_hand_repository.create_hand_card_list()
        return self.hand_card_list