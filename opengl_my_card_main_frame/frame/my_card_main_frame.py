import tkinter as tk

import pandas
from pyopengltk import OpenGLFrame
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from screeninfo import get_monitors

from common.utility import get_project_root
from image_shape.non_background_image import NonBackgroundImage
from image_shape.rectangle_image import RectangleImage
from lobby_frame.service.lobby_menu_frame_service_impl import LobbyMenuFrameServiceImpl
from opengl_my_card_main_frame.entity.my_card_main_scene import MyCardMainScene
from opengl_my_card_main_frame.entity.my_deck_register_scene import MyDeckRegisterScene

from opengl_battle_field_pickable_card.pickable_card import PickableCard
from opengl_my_card_main_frame.renderer.fifth_page_card_renerer import FifthPageCardRenderer
from opengl_my_card_main_frame.renderer.fourth_page_card_renderer import FourthPageCardRenderer
from opengl_my_card_main_frame.renderer.my_card_main_frame_renderer import MyCardMainFrameRenderer
from opengl_my_card_main_frame.renderer.my_deck_register_frame_renderer import MyDeckRegisterFrameRenderer
from opengl_my_card_main_frame.renderer.second_page_card_renderer import SecondPageCardRenderer
from opengl_my_card_main_frame.renderer.third_page_card_renderer import ThirdPageCardRenderer
from opengl_shape.image_rectangle_element import ImageRectangleElement
from opengl_shape.rectangle import Rectangle
from pre_drawed_image_manager.pre_drawed_image import PreDrawedImage


class MyCardMainFrame(OpenGLFrame):
    __pre_drawed_image_instance = PreDrawedImage.getInstance()
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)

        self.init_monitor_specification()

        self.my_card_main_scene = MyCardMainScene()
        self.my_deck_register_scene = MyDeckRegisterScene()
        self.lobby_service = LobbyMenuFrameServiceImpl()
        self.current_rely = 0.20

        self.textbox_string = tk.StringVar()
        self.entry = None

        # 덱 생성 버튼 누르기 전 까지는 안 나타남.
        self.show_my_deck_register_screen = False

        # 다음 페이지 혹은 이전 페이지 누르기 전 까지는 안 나타남.
        self.show_first_page_card_screen = False
        self.show_second_page_card_screen = False
        self.show_third_page_card_screen = False
        self.show_fourth_page_card_screen = False
        self.show_fifth_page_card_screen = False

        self.bind("<Configure>", self.on_resize)
        # self.bind("<Button-1>", self.on_canvas_left_click)

    def init_monitor_specification(self):
        print(f"init_monitor_specification()")

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
        print("initgl 입니다.")
        glClearColor(0.0, 0.0, 0.0, 0)
        glOrtho(0, self.width, self.height, 0, -1, 1)

        # self.tkMakeCurrent()
        #
        # self.make_card_main_frame()
        # self.render = MyCardMainFrameRenderer(self.my_card_main_scene, self)
        #
        # self.render.render()

    def init_first_window(self, width, height):
        print(f"Operate Only Once -> width: {width}, height: {height}")
        self.width = width
        self.height = height

        self.current_width = self.width
        self.current_height = self.height

        self.prev_width = self.width
        self.prev_height = self.height
        self.is_reshape_not_complete = False

        self.make_card_main_frame()
        self.render = MyCardMainFrameRenderer(self.my_card_main_scene, self)



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

    def redraw(self):
        if self.is_reshape_not_complete:
            return

        self.tkMakeCurrent()
        self.render.render()

        if self.show_my_deck_register_screen is True:
            glEnable(GL_BLEND)
            if glIsEnabled(GL_BLEND):
                print("Blending is enabled.")
            else:
                print("Blending is not enabled.")
            glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

            self.make_my_deck_register_frame()
            self.render_after = MyDeckRegisterFrameRenderer(self.my_deck_register_scene, self)
            self.render_after.render()

    def make_card_main_frame(self):
        # project_root = get_project_root()
        # glClearColor(1.0, 1.0, 1.0, 0.0)
        # glClear(GL_COLOR_BUFFER_BIT)

        # 나의 카드 배경 화면
        # background_rectangle = ImageRectangleElement(image_path=os.path.join(project_root, "local_storage", "my_card_frame", "my_card_background.png"),
        #                                              local_translation=(0, 0),
        #                                              vertices=[(0, 0), (self.width, 0), (self.width, self.height), (0, self.height)])
        # self.my_card_main_scene.add_my_card_background(background_rectangle)
        #print(f"카드 배경 잘 들어갔니?:{self.my_card_main_scene.get_my_card_background()}")

        self.__pre_drawed_image_instance.pre_draw_my_card_background(self.width, self.height)
        background_data = self.__pre_drawed_image_instance.get_pre_draw_my_card_background()
        my_card_background = RectangleImage(image_data=background_data,
                                            vertices=[(0, 0), (self.width, 0), (self.width, self.height), (0, self.height)])
        self.my_card_main_scene.add_my_card_background(my_card_background)

        # 나의 덱 화면
        # my_deck_rectangle = Rectangle(color=(0.5137, 0.3608, 0.2314, 1.0),
        #                               local_translation=(0, 0),
        #                               vertices=[(0.84 * self.width, 0), (self.width, 0), (self.width, self.height),
        #                                         (0.84 * self.width, self.height)])
        #
        # self.my_card_main_scene.add_my_card_background(my_deck_rectangle)
        #print(f"덱 화면 잘 들어갔니?:{self.my_card_main_scene.get_my_card_background()}")

        # 덱 생성 버튼
        # button_rectangle = Rectangle(color=(1.0, 0.0, 0.0, 1.0),
        #                              local_translation=(0, 0),
        #                              vertices=[(0.85 * self.width, 0.85 * self.height),
        #                                        (self.width - 50, 0.85 * self.height),
        #                                        (self.width - 50, self.height - 100),
        #                                        (0.85 * self.width, self.height - 100)])
        #
        # self.my_card_main_scene.add_button_list(button_rectangle)
        #print(f"버튼 도형 잘 들어갔니?:{self.my_card_main_scene.get_button_list()}")

        # width: 1920, height: 1080
        # 1508, 793
        # 1508, 874
        # 1803, 874
        # 1803, 793

        # 1508 / 1848 -> 0.78541
        # 1803 / 1848 -> 0.93906
        # 793 / 1016 -> 0.73426
        # 874 / 1016 -> 0.80926

        left_x_point = self.width * 0.81601
        right_x_point = self.width * 0.97564
        top_y_point = self.height * 0.78051
        bottom_y_point = self.height * 0.86023

        # rectangle_size = 130
        # start_point = (1569, 746)
        # end_point = (start_point[0] + rectangle_size * 2.3, start_point[1] + rectangle_size * 0.55)

        create_deck_button_vertices = [
            (left_x_point, top_y_point),
            (right_x_point, top_y_point),
            (right_x_point, bottom_y_point),
            (left_x_point, bottom_y_point),
        ]

        create_deck_button_image = self.__pre_drawed_image_instance.get_pre_draw_create_deck_button()
        create_deck_button = RectangleImage(image_data=create_deck_button_image,
                                            vertices=create_deck_button_vertices)

        self.my_card_main_scene.add_button_list(create_deck_button)

        # 뒤로가기 버튼
        # go_to_back_button = Rectangle(color=(0.0, 1.0, 0.0, 1.0),
        #                               local_translation=(0, 0),
        #                               vertices=[(0.85 * self.width, 0.85 * self.height + 90),
        #                                         (self.width - 50, 0.85 * self.height + 90),
        #                                         (self.width - 50, self.height - 10),
        #                                         (0.85 * self.width, self.height - 10)])
        #
        # self.my_card_main_scene.add_button_list(go_to_back_button)
        #print(f"버튼 도형 잘 들어갔니?:{self.my_card_main_scene.get_button_list()}")

        # 1508 / 1848 -> 0.78541
        # 1803 / 1848 -> 0.93906
        # 900 / 1016 -> 0.73426
        # 982 / 1016 -> 0.80926

        go_back_left_x_point = self.width * 0.81601
        go_back_right_x_point = self.width * 0.97564
        go_back_top_y_point = self.height * 0.88582
        go_back_bottom_y_point = self.height * 0.96653

        go_to_back_button_vertices = [
            (go_back_left_x_point, go_back_top_y_point),
            (go_back_right_x_point, go_back_top_y_point),
            (go_back_right_x_point, go_back_bottom_y_point),
            (go_back_left_x_point, go_back_bottom_y_point),
        ]

        go_to_back_button_image = self.__pre_drawed_image_instance.get_pre_draw_go_back_button()
        go_to_back_button = RectangleImage(image_data=go_to_back_button_image,
                                           vertices=go_to_back_button_vertices)

        self.my_card_main_scene.add_button_list(go_to_back_button)


        # 다음 페이지 버튼
        # next_page_button_rectangle = Rectangle(color=(1.0, 1.0, 0.0, 1.0),
        #                                        local_translation=(0, 0),
        #                                        vertices=[(0.85 * self.width - self.width * 0.25, 0.85 * self.height + 90),
        #                                                  (self.width - 50 - self.width * 0.25, 0.85 * self.height + 90),
        #                                                  (self.width - 50 - self.width * 0.25, self.height - 100 + 90),
        #                                                  (0.85 * self.width - self.width * 0.25, self.height - 100 + 90)])
        #
        # self.my_card_main_scene.add_button_list(next_page_button_rectangle)

        # 1508 / 1848 -> 0.78541
        # 1803 / 1848 -> 0.93906
        # 900 / 1016 -> 0.73426
        # 982 / 1016 -> 0.80926

        # 1850, 1016 (academy pc)
        # x: 108, y: 572
        # x: 136, y: 571
        # difference -> 0.01513

        # 다음 페이지 버튼 도형으로 만든 것.
        next_left_x_point = self.width * 0.730
        next_right_x_point = self.width * 0.786
        next_top_y_point = self.height * 0.483
        next_bottom_y_point = self.height * 0.553
        next_gold_button_image_data = self.__pre_drawed_image_instance.get_pre_draw_next_gold_button()
        next_page_button = NonBackgroundImage(image_data=next_gold_button_image_data,
                                              vertices=[
                                                  (next_left_x_point, next_top_y_point),
                                                  (next_right_x_point, next_top_y_point),
                                                  (next_right_x_point, next_bottom_y_point),
                                                  (next_left_x_point, next_bottom_y_point)
                                              ])
        self.my_card_main_scene.add_button_list(next_page_button)
        print(f"버튼들 다 담김?: {self.my_card_main_scene.get_button_list()}")

        # 이전 페이지 버튼
        # before_page_button_rectangle = Rectangle(color=(0.0, 0.0, 1.0, 1.0),
        #                                          local_translation=(0, 0),
        #                                          vertices=[(50, 0.85 * self.height + 90),
        #                                                    (0.15 * self.width, 0.85 * self.height + 90),
        #                                                    (0.15 * self.width, self.height - 100 + 90),
        #                                                    (50, self.height - 100 + 90)])
        #
        # self.my_card_main_scene.add_button_list(before_page_button_rectangle)

        # 이전 페이지 버튼 도형으로 만든 것.
        prev_left_x_point = self.width * 0.002
        prev_right_x_point = self.width * 0.058
        prev_top_y_point = self.height * 0.483
        prev_bottom_y_point = self.height * 0.553
        prev_gold_button_image_data = self.__pre_drawed_image_instance.get_pre_draw_prev_gold_button()
        pre_page_button = NonBackgroundImage(image_data=prev_gold_button_image_data,
                                               vertices=[
                                                   (prev_left_x_point, prev_top_y_point),
                                                   (prev_right_x_point, prev_top_y_point),
                                                   (prev_right_x_point, prev_bottom_y_point),
                                                   (prev_left_x_point, prev_bottom_y_point)
                                               ])
        self.my_card_main_scene.add_button_list(pre_page_button)

        # TODO: 카드 갯수 표기 배치 (이건 한 개만 테스트 한 것)
        # 가로 길이 비율 0.036, 세로 길이 비율 0.056
        # number_left_x_point = self.width * 0.130 # 첫 번째 카드는 이 위치로 고정
        # number_right_x_point = self.width * 0.166
        # number_top_y_point = self.height * 0.450 # 첫 번째줄은 이 높이로 고정하면 될 듯
        # number_bottom_y_point = self.height * 0.506
        # number_of_cards_data = self.__pre_drawed_image_instance.get_pre_draw_number_of_cards(2)
        # number_of_cards_text = NonBackgroundImage(image_data=number_of_cards_data,
        #                                            vertices=[
        #                                                (number_left_x_point, number_top_y_point),
        #                                                (number_right_x_point, number_top_y_point),
        #                                                (number_right_x_point, number_bottom_y_point),
        #                                                (number_left_x_point, number_bottom_y_point)
        #                                            ])
        # self.my_card_main_scene.add_text_list(number_of_cards_text)
        #
        #
        # number_left_x_point = self.width * 0.130  # 첫 번째 카드는 이 위치로 고정
        # number_right_x_point = self.width * 0.166
        # number_top_y_point = self.height * 0.940  # 두 번째 줄 높이 고정
        # number_bottom_y_point = self.height * 0.996
        # number_of_cards_data2 = self.__pre_drawed_image_instance.get_pre_draw_number_of_cards(3)
        # number_of_cards_text2 = NonBackgroundImage(image_data=number_of_cards_data2,
        #                                               vertices=[
        #                                                   (number_left_x_point, number_top_y_point),
        #                                                   (number_right_x_point, number_top_y_point),
        #                                                   (number_right_x_point, number_bottom_y_point),
        #                                                   (number_left_x_point, number_bottom_y_point)
        #                                               ])
        # self.my_card_main_scene.add_text_list(number_of_cards_text2)
        #
        # number_left_x_point = self.width * 0.130  # 두 번째 카드의 위치는
        # number_right_x_point = self.width * 0.166
        # number_top_y_point = self.height * 0.940  # 두 번째 줄 높이 고정
        # number_bottom_y_point = self.height * 0.996
        # x_increase = self.width * 0.164 # 간격 고정
        # number_of_cards_data3 = self.__pre_drawed_image_instance.get_pre_draw_number_of_cards(4)
        # number_of_cards_text3 = NonBackgroundImage(image_data=number_of_cards_data3,
        #                                            vertices=[
        #                                                (number_left_x_point + x_increase, number_top_y_point),
        #                                                (number_right_x_point + x_increase, number_top_y_point),
        #                                                (number_right_x_point + x_increase, number_bottom_y_point),
        #                                                (number_left_x_point + x_increase, number_bottom_y_point)
        #                                            ])
        # self.my_card_main_scene.add_text_list(number_of_cards_text3)

        # 모든 카드
        print(f"서버로 부터 가져온 카드 리스트: {self.lobby_service.get_card_data_list()}")
        #all_card_number = self.card_data_read().tolist()
        all_card_number = self.lobby_service.get_card_data_list()
        number_of_cards = self.lobby_service.get_number_of_cards_list()
        print(f"카드 갯수 리스트: {number_of_cards}")
        # print(f"카드 번호 리스트: {all_card_number}")
        # print(f"카드 번호 길이: {len(all_card_number)}")

        x = 165
        y = 30

        for i, number in enumerate(all_card_number):
            try:
                #print(f"index: {i}, card number: {number}")
                card = PickableCard(local_translation=(x, y))
                card.init_card_in_my_card_frame(number)
                self.my_card_main_scene.add_card_list(card)
                #print(f"카드 리스트: {self.my_card_main_scene.get_card_list()}")

                x += 315

                if (i + 1) % 4 == 0:  # 4개씩
                    y = 500
                    x = 165
                    if (i + 1) % 8 == 0:
                        x = 165
                        y = 30

                if (i + 1) % 8 == 0:
                    continue

            except Exception as e:
                print(f"Error creating card: {e}")
                pass


        # 카드 갯수 표기
        #TODO: 갯수가 1개인 경우에는 표기 안 함.
        number_left_x_point = self.width * 0.130  # 첫 번째 카드는 이 위치로 고정
        number_right_x_point = self.width * 0.166
        number_top_y_point = self.height * 0.450  # 첫 번째줄은 이 높이로 고정하면 될 듯
        number_bottom_y_point = self.height * 0.506
        for i, number in enumerate(number_of_cards):
            try:
                if number == 1:
                    # number_of_cards_data = self.__pre_drawed_image_instance.get_pre_draw_number_of_cards(9)
                    self.my_card_main_scene.add_text_list(None)
                else:
                    number_of_cards_data = self.__pre_drawed_image_instance.get_pre_draw_number_of_cards(number)

                    number_of_cards_text = NonBackgroundImage(image_data=number_of_cards_data,
                                                               vertices=[
                                                                   (number_left_x_point, number_top_y_point),
                                                                   (number_right_x_point, number_top_y_point),
                                                                   (number_right_x_point, number_bottom_y_point),
                                                                   (number_left_x_point, number_bottom_y_point)
                                                               ])
                    self.my_card_main_scene.add_text_list(number_of_cards_text)

                number_left_x_point += self.width * 0.164
                number_right_x_point += self.width * 0.164

                if (i + 1) % 4 == 0:
                    number_top_y_point = self.height * 0.940  # 두 번째 줄 부턴 위치 바뀜
                    number_bottom_y_point = self.height * 0.996
                    number_left_x_point = self.width * 0.130
                    number_right_x_point = self.width * 0.166

                    if (i + 1) % 8 == 0:
                        number_left_x_point = self.width * 0.130
                        number_right_x_point = self.width * 0.166
                        number_top_y_point = self.height * 0.450
                        number_bottom_y_point = self.height * 0.506

                if (i + 1) % 8 == 0:
                    continue

            except Exception as e:
                print(f"Error number text: {e}")
                pass



    def make_my_deck_register_frame(self):
        # glEnable(GL_BLEND)
        # glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

        # 검정 투명 화면
        alpha_rectangle = Rectangle(color=(0.0, 0.0, 0.0, 0.7),
                                    local_translation=(0, 0),
                                    vertices=[(0, 0), (self.width, 0), (self.width, self.height), (0, self.height)])

        self.my_deck_register_scene.add_alpha_rectangle(alpha_rectangle)

        # 덱 생성 사각형
        center_x = 0.5 * self.width
        center_y = 0.5 * self.height
        deck_register_rectangle = Rectangle(color=(0.5137, 0.3608, 0.2314, 1.0),
                                            local_translation=(0, 0),
                                            vertices=[(center_x - 0.5 * 0.5 * self.width, center_y - 0.5 * 0.5 * self.height),
                                                      (center_x + 0.5 * 0.5 * self.width, center_y - 0.5 * 0.5 * self.height),
                                                      (center_x + 0.5 * 0.5 * self.width, center_y + 0.5 * 0.5 * self.height),
                                                      (center_x - 0.5 * 0.5 * self.width, center_y + 0.5 * 0.5 * self.height)])

        self.my_deck_register_scene.add_my_deck_background(deck_register_rectangle)

        # 텍스트 박스
        self.entry = tk.Entry(self.master, textvariable=self.textbox_string)
        self.entry.place(relx=0.5, rely=0.4, width=300, height=50, anchor="center")
        # self.my_deck_register_scene.add_deck_name_list(self.textbox_string.get()) # 생성한 덱의 이름을 리스트에 저장

        # 확인 버튼 사각형
        button_width = 0.15 * self.width
        button_height = 0.06 * self.height
        ok_button_y_offset = 0.8 * 0.5 * self.height
        ok_button_x_offset = 0.25 * 0.5 * self.width
        ok_button_rectangle = Rectangle(color=(1.0, 0.0, 0.0, 1.0),
                                        local_translation=(0, 0),
                                        vertices=[(center_x - 0.5 * button_width + ok_button_x_offset,
                                                   center_y - 0.5 * 0.5 * self.height - button_height + ok_button_y_offset),
                                                  (center_x + 0.5 * button_width + ok_button_x_offset,
                                                   center_y - 0.5 * 0.5 * self.height - button_height + ok_button_y_offset),
                                                  (center_x + 0.5 * button_width + ok_button_x_offset,
                                                   center_y - 0.5 * 0.5 * self.height + ok_button_y_offset),
                                                  (center_x - 0.5 * button_width + ok_button_x_offset,
                                                   center_y - 0.5 * 0.5 * self.height + ok_button_y_offset)])

        self.my_deck_register_scene.add_button_list(ok_button_rectangle)

        # 되돌아 가기 버튼 사각형
        go_to_back_button_rectangle = Rectangle(color=(0.0, 1.0, 0.0, 1.0),
                                                local_translation=(0, 0),
                                                vertices=[(center_x - 0.5 * button_width - ok_button_x_offset,
                                                           center_y - 0.5 * 0.5 * self.height - button_height + ok_button_y_offset),
                                                          (center_x + 0.5 * button_width - ok_button_x_offset,
                                                           center_y - 0.5 * 0.5 * self.height - button_height + ok_button_y_offset),
                                                          (center_x + 0.5 * button_width - ok_button_x_offset,
                                                           center_y - 0.5 * 0.5 * self.height + ok_button_y_offset),
                                                          (center_x - 0.5 * button_width - ok_button_x_offset,
                                                           center_y - 0.5 * 0.5 * self.height + ok_button_y_offset)])
        self.my_deck_register_scene.add_button_list(go_to_back_button_rectangle)

    def getMyDeckRegisterScene(self):
        return self.my_deck_register_scene

    # csv 파일 읽어오기
    def card_data_read(self):
        currentLocation = os.getcwd()
        #print(f"currentLocation: {currentLocation}")

        data_card = pandas.read_csv('local_storage/card/data.csv')
        data_card_number = data_card['카드번호']

        return data_card_number

    # 1) 확인 버튼을 눌렀을 때 화면을 지우기 위함
    def clear_screen(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    # 2) 다시 그려야 함.
    def drawMyCardMainFrame(self):
        if self.show_first_page_card_screen is True:
            self.render = MyCardMainFrameRenderer(self.my_card_main_scene, self)
            self.render.render()

    # 텍스트 박스 지우기 위한 텍스트 박스 객체 가져오는 함수
    def getTextBox(self):
        return self.entry

    # 텍스트 박스에 적은 텍스트 가져오기
    def getString(self):
        return self.textbox_string.get()

    def second_page_card_draw(self):
        if self.show_second_page_card_screen is True:
            self.render = SecondPageCardRenderer(self.my_card_main_scene, self)
            self.render.render()

    def third_page_card_draw(self):
        if self.show_third_page_card_screen is True:
            self.render = ThirdPageCardRenderer(self.my_card_main_scene, self)
            self.render.render()

    def fourth_page_card_draw(self):
        if self.show_fourth_page_card_screen is True:
            self.render = FourthPageCardRenderer(self.my_card_main_scene, self)
            self.render.render()

    def fifth_page_card_draw(self):
        if self.show_fifth_page_card_screen is True:
            self.render = FifthPageCardRenderer(self.my_card_main_scene, self)
            self.render.render()