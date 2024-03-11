from OpenGL.GL import *
from OpenGL.GLU import *
from colorama import Fore, Style
from pyopengltk import OpenGLFrame
from screeninfo import get_monitors
from shapely import Polygon, Point

from battle_field_muligun.infra.muligun_your_hand_repository import MuligunYourHandRepository
from battle_field_muligun.entity.scene.battle_field_muligun_scene import BattleFieldMuligunScene
from battle_field_muligun.service.request.check_opponent_muligun_request import CheckOpponentMuligunRequest
from battle_field_muligun.service.request.muligun_request import MuligunRequest
from battle_field_muligun_timer.battle_field_muligun_timer import BattleFieldMuligunTimer
from image_shape.non_background_image import NonBackgroundImage
from image_shape.rectangle_image import RectangleImage
from opengl_battle_field_pickable_card.pickable_card import PickableCard
from opengl_rectangle_lightning_border.lightning_border import LightningBorder
from opengl_shape.image_rectangle_element import ImageRectangleElement
from opengl_shape.rectangle import Rectangle
from pre_drawed_image_manager.pre_drawed_image import PreDrawedImage
from session.repository.session_repository_impl import SessionRepositoryImpl


class BattleFieldMuligunFrame(OpenGLFrame):
    sessionRepository = SessionRepositoryImpl.getInstance()
    __pre_drawed_image_instance = PreDrawedImage.getInstance()

    def __init__(self,  master=None, switchFrameWithMenuName=None, **kwargs):
        super().__init__(master, **kwargs)
        self.__switchFrameWithMenuName = switchFrameWithMenuName
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
        self.prev_selected_object = None
        self.execute_pick_card_effect = True
        self.ok_button_visible = True
        self.ok_button_clicked = False

        self.click_card_effect_rectangles = []
        self.selected_object_list_for_muligun = []
        self.checking_draw_effect = {}
        self.change_card_object_list = {}

        self.lightning_border = LightningBorder()

        self.battle_field_muligun_scene = BattleFieldMuligunScene()
        self.battle_field_muligun_scene.create_battle_field_muligun_scene(self.width, self.height)
        self.battle_field_muligun_background_shape_list = self.battle_field_muligun_scene.get_battle_field_muligun_background()

        self.alpha_background = self.create_opengl_alpha_background()
        self.ok_button = self.create_ok_button()

        self.your_hand_repository = MuligunYourHandRepository.getInstance()
        # print(f"your_hand_repo: {self.your_hand_repository.get_current_hand_state()}")
        # self.your_hand_repository.save_current_hand_state([6, 8, 19, 20, 151])
        print("Call Muligun Frame Constructor")

        self.hand_card_list = None
        self.hand_card_state = None

        self.button_click_processing = False
        self.message_visible = False

        self.timer_visible = True
        # self.select_card_id = self.your_hand_repository.select_card_id_list()
        # self.delete_select_card = self.your_hand_repository.delete_select_card()

        self.bind("<Configure>", self.on_resize)
        self.bind("<Button-1>", self.on_canvas_left_click)
        self.bind("<Button-3>", self.on_canvas_ok_button_click)

        self.timer_panel = None
        self.timer = BattleFieldMuligunTimer()

        self.is_doing_mulligan = True

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

        self.timer.set_total_window_size(self.width, self.height)
        self.timer.draw_current_timer_panel()
        self.timer_panel = self.timer.get_timer_panel()
        self.timer.set_function(self.muligunTimeOut)
        self.timer.set_timer(30)
        self.timer.start_timer()

        self.hand_card_list = self.your_hand_repository.get_current_hand_card_list()
        # self.hand_card_state = self.your_hand_repository.get_current_hand_state()
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
        self.after(17, self.draw_muligun_timer)
        self.after(17, self.redraw)

    def on_resize(self, event):
        self.reshape(event.width, event.height)

    def draw_base(self):
        for battle_field_muligun_background_shape in self.battle_field_muligun_background_shape_list:
            battle_field_muligun_background_shape.draw()

    def redraw(self):
        if self.is_doing_mulligan == False:
            return
        # print("redrawing")
        if self.is_reshape_not_complete:
            return

        self.tkMakeCurrent()
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

        self.draw_base()
        self.alpha_background.draw()
        # glDisable(GL_BLEND)
        if self.your_hand_repository.get_is_my_mulligan():
            if self.your_hand_repository.get_is_opponent_mulligan():
              #  print(f"check opponent muligun responseData:{mulligan_done}")

               # if mulligan_done is True:
                self.message_visible = False
                self.timer.stop_timer()
                print("사용자 둘 다 멀리건 선택 완료")
                # TODO: 배틀 필드 화면으로 넘어가야 함.
                self.timer_visible = False
                # self.master.after(self.__switchFrameWithMenuName('fake-battle-field'))
                self.is_doing_mulligan = False
                self.__switchFrameWithMenuName('fake-battle-field')
            else:
                self.message_visible = True

        if self.ok_button_visible is True:
            self.ok_button.draw()

        if self.timer_visible is True:
            self.draw_muligun_timer()


        # self.hand_card_list = self.your_hand_repository.get_current_hand_card_list()
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

        if self.your_hand_repository.get_is_opponent_mulligan() is False:
            if self.message_visible is True:
                self.waiting_message().draw()

        self.tkSwapBuffers()

    def draw_pick_card_effect(self):
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

    # def remove_selected_card_is_already_selected(self, hand_card_object):
    #     if hand_card_object in self.selected_object_list_for_muligun:
    #         print(f"remove_selected_card_is_already_selected: {hand_card_object}")
    #         self.selected_object_list_for_muligun.remove(hand_card_object)
    #     else:
    #         print(f"The specified object is not in the list.")

    def remove_selected_card_is_already_selected(self, hand_card_object):
        if hand_card_object in self.selected_object_list_for_muligun:
            if id(hand_card_object) in self.checking_draw_effect.keys():
                print(f"카드 클릭 했었니?{id(hand_card_object)}, 딕셔너리는 뭐니?: {self.checking_draw_effect}")
                del self.checking_draw_effect[id(hand_card_object)]

            print(f"카드 효과 잘 삭제 되었니?{self.checking_draw_effect}")

            print(f"remove_selected_card_is_already_selected: {hand_card_object}")
            self.selected_object_list_for_muligun.remove(hand_card_object)
        else:
            print(f"The specified object is not in the list.")
            fixed_x, fixed_y = hand_card_object.get_pickable_card_base().get_local_translation()
            new_rectangle = self.create_change_card_expression((fixed_x, fixed_y))
            self.checking_draw_effect[id(hand_card_object)] = new_rectangle
            self.selected_object_list_for_muligun.append(hand_card_object)

    def extract_card_id_list_in_hand_card_list(self, muligun_list, origin_list):
        card_id_list = []

        for muligun_object in muligun_list:
            try:
                origin_object = next(obj for obj in origin_list if obj == muligun_object)
                card_number = origin_object.get_card_number()
                card_id_list.append(card_number)
                # origin_list.remove(origin_object)
            except StopIteration:
                pass

        return card_id_list

    def extract_card_index_list_in_hand_card_list(self, muligun_list, origin_list):
        card_index_list = []

        for muligun_object in muligun_list:
            try:
                origin_object = next(obj for obj in origin_list if obj == muligun_object)
                card_index = origin_list.index(origin_object)
                card_index_list.append(card_index)
            except StopIteration:
                pass

        return card_index_list

    def on_canvas_left_click(self, event):
        try:
            x, y = event.x, event.y
            y = self.winfo_reqheight() - y

            for hand_card in self.hand_card_list:
                if isinstance(hand_card, PickableCard):
                    hand_card.selected = False

            self.selected_object = None
            print(f"self.hand_card_list = {self.hand_card_list}")
            print(f"self.your_hand_repository.get_current_hand_card_list() = {self.your_hand_repository.get_current_hand_card_list()}")

            # Selection | Deselection
            for hand_card in reversed(self.hand_card_list):
                pickable_card_base = hand_card.get_pickable_card_base()
                are_you_select_pickable_card = pickable_card_base.is_point_inside((x, y))

                if are_you_select_pickable_card:
                    print("Selection Pickable Rectangle")
                    hand_card.selected = not hand_card.selected
                    self.selected_object = hand_card

                    # 이미 선택 되어 있으면 카드 오브젝트 리스트에서 삭제. 아니면 카드 오브젝트에 추가
                    self.remove_selected_card_is_already_selected(hand_card)
                    # self.selected_object_list_for_muligun.append(hand_card)

                    print(f"self.selected_object_list_for_muligun: {self.selected_object_list_for_muligun}")

                    break

            # for hand_card in reversed(self.hand_card_list):
            #     pickable_card_base = hand_card.get_pickable_card_base()
            #
            #     if pickable_card_base.is_point_inside((x, y)):
            #         hand_card.selected = not hand_card.selected
            #         self.selected_object = hand_card
            #         hand_card_index = self.hand_card_list.index(hand_card)
            #         self.change_card_object_list[hand_card_index] = hand_card
            #
            #         fixed_x, fixed_y = pickable_card_base.get_local_translation()
            #         new_rectangle = self.create_change_card_expression((fixed_x, fixed_y))
            #         self.click_card_effect_rectangles.append(new_rectangle)
            #
            #         # 교체할 카드 선택 취소 기능)
            #         if hand_card_index in self.checking_draw_effect:
            #             del self.checking_draw_effect[hand_card_index]
            #
            #             # 선택한 카드 리스트에 담긴 것을 다시 지워야 함.
            #             if hand_card_index in self.change_card_object_list:
            #                 del self.change_card_object_list[self.hand_card_list.index(hand_card)]
            #
            #         else:
            #             fixed_x, fixed_y = pickable_card_base.get_local_translation()
            #             new_rectangle = self.create_change_card_expression((fixed_x, fixed_y))
            #             self.checking_draw_effect[hand_card_index] = new_rectangle
            #             print(self.checking_draw_effect)
            #             print(list(self.checking_draw_effect.keys()))

            # 확인 버튼 기능
            # if self.ok_button.is_point_inside((x, y)):
            #     self.on_canvas_ok_button_click(event)

            if self.is_point_inside_rectangle((x, y), self.ok_button):
                self.on_canvas_ok_button_click(event)

        except Exception as e:
            print(f"Exception in on_canvas_click: {e}")

    def on_canvas_ok_button_click(self, event):
        if not self.ok_button_clicked:
            # self.your_hand_repository.select_card_id_list(self.change_card_object_list)# 서버에 보내줄 카드 아이디 리스트로 저장.
            # print(f"your_hand select_card: {self.change_card_object_list}")
            print("on_canvas_ok_button_click()")
            print(f"{Fore.RED}len(self.current_hand_card_list):{Fore.GREEN} {len(self.your_hand_repository.get_current_hand_card_list())}{Style.RESET_ALL}")

            will_be_change_card_index_list = self.extract_card_index_list_in_hand_card_list(
                self.selected_object_list_for_muligun,
                self.hand_card_list)
            print(f"will_be_change_card_index_list: {will_be_change_card_index_list}")

            will_be_change_card_id_list = self.extract_card_id_list_in_hand_card_list(
                self.selected_object_list_for_muligun,
                self.hand_card_list)
            print(f"will_be_change_card_id_list: {will_be_change_card_id_list}")

            will_be_change_card_id_list_str = list(map(str, will_be_change_card_id_list))
            print(f"will_be_change_card_id_list_str: {will_be_change_card_id_list_str}")

            # card_id_list = []
            # change_card_object_list_length = len(self.change_card_object_list)
            # print(f"change_card_object_list_length: {change_card_object_list_length}")
            #
            # for index in range(change_card_object_list_length):
            #     card_id_list.append(self.change_card_object_list[index])

            # card_id_list = [str(card.get_card_number()) for card in self.change_card_object_list.values()]
            # change_card_object_list_length = len(card_id_list)

            # 제거는 인덱스로 해야함
            self.your_hand_repository.remove_card_by_multiple_index(will_be_change_card_index_list)

            print(f"{Fore.RED}len(self.current_hand_card_list):{Fore.GREEN} {len(self.hand_card_list)}{Style.RESET_ALL}")

            # self.your_hand_repository.delete_select_card(self.change_card_object_list)# 처음 드로우한 5장의 카드 리스트에서 교체할 카드 삭제.
            self.your_hand_repository.replace_hand_card_position()

            responseData = self.your_hand_repository.requestMuligun(
                MuligunRequest(self.sessionRepository.get_session_info(),
                               will_be_change_card_id_list_str))

            print("muligun responseData:", responseData)

            redrawn_hand_card_list = responseData['redrawn_hand_card_list']
            print(f"{Fore.RED}redrawn_hand_card_list:{Fore.GREEN} {redrawn_hand_card_list}{Style.RESET_ALL}")

            for redrawn_hand_card_id in redrawn_hand_card_list:
                print(f"redrawn_hand_card_id: {redrawn_hand_card_id}")
                self.your_hand_repository.create_muligun_hand_unit_card(redrawn_hand_card_id)

            self.hand_card_list = self.your_hand_repository.get_current_hand_card_list()
            print(f"{Fore.RED}self.hand_card_list:{Fore.GREEN} {self.hand_card_list}{Style.RESET_ALL}")

            # TODO: 새로 받을 카드 임의로 지정. 나중에는 서버에서 받아야 함. 임의로 넣었기 때문에 현재 2개만 교체 가능
            # self.redraw_card()

            # 그려져 있는 카드 선택 효과, 그려져 있는 버튼은 지워야 함.
            self.click_card_effect_rectangles = []
            self.checking_draw_effect = {}
            self.ok_button_visible = False
            self.execute_pick_card_effect = False
            self.ok_button_clicked = True

            self.your_hand_repository.set_is_my_mulligan(True)


            # try:
            #     #     # responseData = self.your_hand_repository.requestCheckOpponentMuligun(
            #     #     #     CheckOpponentMuligunRequest(self.sessionRepository.get_session_info()))
            #     mulligan_done = self.your_hand_repository.get_is_mulligan_done()
            #     print(f"check opponent muligun responseData:{mulligan_done}")
            #
            #     if mulligan_done is True:
            #         self.message_visible = False
            #         self.timer.stop_timer()
            #         print("사용자 둘 다 멀리건 선택 완료")
            #         # TODO: 배틀 필드 화면으로 넘어가야 함.
            #         self.timer_visible = False
            #         # self.master.after(self.__switchFrameWithMenuName('fake-battle-field'))
            #         self.__switchFrameWithMenuName('fake-battle-field')
            #     else:
            #         self.message_visible = True
            #
            # except Exception as e:
            #     print(f"멀리건 에러: {e}")

        else:
            #self.master.after(self.__switchFrameWithMenuName('decision-first'))
            #self.master.after(self.__switchFrameWithMenuName('rock-paper-scissors'))
            self.master.after(self.__switchFrameWithMenuName('fake-battle-field'))


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

        print(f"사각형 안 만들어 지는 거니?:{new_rectangle}")
        return new_rectangle

    # 검정 투명 배경 화면
    def create_opengl_alpha_background(self):
        rectangle_color = (0.0, 0.0, 0.0, 0.65)

        new_rectangle = Rectangle(rectangle_color,
                                  [(0, 0), (self.width, 0), (self.width, self.height), (0, self.height)])
        return new_rectangle


    def waiting_message(self):
            self.__pre_drawed_image_instance.pre_draw_waiting_message()
            data = self.__pre_drawed_image_instance.get_pre_draw_waiting_message()
            vertices = [(300, 300), (1600, 300), (1600, 650), (300, 650)]
            waiting_message_image = NonBackgroundImage(
                image_data=data,
                vertices=vertices)
            return waiting_message_image

    # 확인 버튼
    # def create_ok_button(self):
    #     rectangle_size = 100
    #     rectangle_color = (0.8314, 0.7686, 0.6588, 1.0)
    #
    #     start_point = (850, 900)  # 확인 버튼 위치는 고정.
    #     end_point = (start_point[0] + rectangle_size * 2.0, start_point[1] + rectangle_size * 0.55)
    #
    #     new_rectangle = PickableRectangle(rectangle_color, [
    #         (start_point[0], start_point[1]),
    #         (end_point[0], start_point[1]),
    #         (end_point[0], end_point[1]),
    #         (start_point[0], end_point[1])
    #     ])
    #     return new_rectangle

    def create_ok_button(self):
        rectangle_size = 100
        # rectangle_color = (0.8314, 0.7686, 0.6588, 1.0)

        start_point = (850, 800)  # 확인 버튼 위치는 고정.
        end_point = (start_point[0] + rectangle_size * 2.0, start_point[1] + rectangle_size * 0.55)

        new_rectangle = ImageRectangleElement("local_storage/button_image/ok_button.png",[
            (start_point[0], start_point[1]),
            (end_point[0], start_point[1]),
            (end_point[0], end_point[1]),
            (start_point[0], end_point[1]),
        ])
        return new_rectangle

    def is_point_inside_rectangle(self, point, rectangle):
        x, y = point
        y *= -1

        rectangle_vertices = rectangle.get_vertices()

        ratio_applied_valid_your_field = [(x * self.width_ratio, y * self.height_ratio) for x, y in rectangle_vertices]
        print(f"ratio_applied_valid_your_field: {ratio_applied_valid_your_field}")
        print(f"x: {x * self.width_ratio}, y: {y * self.height_ratio}")

        poly = Polygon(ratio_applied_valid_your_field)
        point = Point(x, y)

        return point.within(poly)


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
    # def redraw_card(self):
    #     # self.your_hand_repository.save_current_hand_state(new_card_number_list)
    #     # print(f"현재 카드 뭐 있니?: {self.hand_card_state}")
    #     self.your_hand_repository.create_hand_card_list()
    #     return self.hand_card_list

    def draw_muligun_timer(self):
        if self.is_doing_mulligan == True:
            self.timer.set_width_ratio(self.width_ratio)
            self.timer.set_height_ratio(self.height_ratio)
            self.timer.update_current_timer_panel()
            self.timer_panel.set_width_ratio(self.width_ratio)
            self.timer_panel.set_height_ratio(self.height_ratio)
            self.timer_panel.draw()
            self.master.after(17, self.draw_muligun_timer)

    def muligunTimeOut(self):
        print("muligunTimeOut")
        self.timer.stop_timer()
        self.master.after(self.__switchFrameWithMenuName('fake-battle-field'))
