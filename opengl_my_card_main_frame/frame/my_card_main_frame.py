import os
import tkinter as tk

import pandas
from pyopengltk import OpenGLFrame
from OpenGL.GL import *
from OpenGL.GLUT import *

from common.utility import get_project_root
from lobby_frame.service.lobby_menu_frame_service_impl import LobbyMenuFrameServiceImpl
from opengl_my_card_main_frame.entity.my_card_main_scene import MyCardMainScene
from opengl_my_card_main_frame.entity.my_deck_register_scene import MyDeckRegisterScene

from opengl_battle_field_card.card import Card
from opengl_my_card_main_frame.renderer.fifth_page_card_renerer import FifthPageCardRenderer
from opengl_my_card_main_frame.renderer.fourth_page_card_renderer import FourthPageCardRenderer
from opengl_my_card_main_frame.renderer.my_card_main_frame_renderer import MyCardMainFrameRenderer
from opengl_my_card_main_frame.renderer.my_deck_register_frame_renderer import MyDeckRegisterFrameRenderer
from opengl_my_card_main_frame.renderer.second_page_card_renderer import SecondPageCardRenderer
from opengl_my_card_main_frame.renderer.third_page_card_renderer import ThirdPageCardRenderer
from opengl_shape.image_rectangle_element import ImageRectangleElement
from opengl_shape.rectangle import Rectangle


class MyCardMainFrame(OpenGLFrame):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self.my_card_main_scene = MyCardMainScene()
        self.my_deck_register_scene = MyDeckRegisterScene()
        self.lobby_service = LobbyMenuFrameServiceImpl()
        self.current_rely = 0.20

        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        self.width = screen_width
        self.height = screen_height

        self.textbox_string = tk.StringVar()


        # 덱 생성 버튼 누르기 전 까지는 안 나타남.
        self.show_my_deck_register_screen = False

        # 다음 페이지 혹은 이전 페이지 누르기 전 까지는 안 나타남.
        self.show_first_page_card_screen = False
        self.show_second_page_card_screen = False
        self.show_third_page_card_screen = False
        self.show_fourth_page_card_screen = False
        self.show_fifth_page_card_screen = False


    def initgl(self):
        print("initgl 입니다.")
        glClearColor(0, 0, 0, 0)
        glOrtho(0, self.width, self.height, 0, -1, 1)

        self.make_card_main_frame()
        self.render = MyCardMainFrameRenderer(self.my_card_main_scene, self)
        self.render.render()


    def make_card_main_frame(self):
        project_root = get_project_root()
        glClearColor(0.0, 1.0, 0.0,0.0)
        glClear(GL_COLOR_BUFFER_BIT)

        # 나의 카드 배경 화면
        background_rectangle = ImageRectangleElement(image_path=os.path.join(project_root, "local_storage", "image", "battle_lobby", "background.png"),
                                                     local_translation=(0, 0),
                                                     vertices=[(0, 0), (self.width, 0), (self.width, self.height), (0, self.height)])
        self.my_card_main_scene.add_my_card_background(background_rectangle)
        #print(f"카드 배경 잘 들어갔니?:{self.my_card_main_scene.get_my_card_background()}")

        # 나의 덱 화면
        my_deck_rectangle = Rectangle(color=(0.5137, 0.3608, 0.2314, 1.0),
                                      local_translation=(0, 0),
                                      vertices=[(0.75 * self.width, 0), (self.width, 0), (self.width, self.height),
                                                (0.75 * self.width, self.height)])

        self.my_card_main_scene.add_my_card_background(my_deck_rectangle)
        #print(f"덱 화면 잘 들어갔니?:{self.my_card_main_scene.get_my_card_background()}")

        # 덱 생성 버튼
        button_rectangle = Rectangle(color=(1.0, 0.0, 0.0, 1.0),
                                     local_translation=(0, 0),
                                     vertices=[(0.85 * self.width, 0.85 * self.height),
                                               (self.width - 50, 0.85 * self.height),
                                               (self.width - 50, self.height - 100),
                                               (0.85 * self.width, self.height - 100)])

        self.my_card_main_scene.add_button_list(button_rectangle)
        #print(f"버튼 도형 잘 들어갔니?:{self.my_card_main_scene.get_button_list()}")

        # 뒤로가기 버튼
        go_to_back_button = Rectangle(color=(0.0, 1.0, 0.0, 1.0),
                                      local_translation=(0, 0),
                                      vertices=[(0.85 * self.width, 0.85 * self.height + 90),
                                                (self.width - 50, 0.85 * self.height + 90),
                                                (self.width - 50, self.height - 10),
                                                (0.85 * self.width, self.height - 10)])

        self.my_card_main_scene.add_button_list(go_to_back_button)
        #print(f"버튼 도형 잘 들어갔니?:{self.my_card_main_scene.get_button_list()}")

        # 다음 페이지 버튼
        next_page_button_rectangle = Rectangle(color=(1.0, 1.0, 0.0, 1.0),
                                               local_translation=(0, 0),
                                               vertices=[(0.85 * self.width - self.width * 0.25, 0.85 * self.height + 90),
                                                         (self.width - 50 - self.width * 0.25, 0.85 * self.height + 90),
                                                         (self.width - 50 - self.width * 0.25, self.height - 100 + 90),
                                                         (0.85 * self.width - self.width * 0.25, self.height - 100 + 90)])

        self.my_card_main_scene.add_button_list(next_page_button_rectangle)

        # 이전 페이지 버튼
        before_page_button_rectangle = Rectangle(color=(0.0, 0.0, 1.0, 1.0),
                                                 local_translation=(0, 0),
                                                 vertices=[(50, 0.85 * self.height + 90),
                                                           (0.15 * self.width, 0.85 * self.height + 90),
                                                           (0.15 * self.width, self.height - 100 + 90),
                                                           (50, self.height - 100 + 90)])

        self.my_card_main_scene.add_button_list(before_page_button_rectangle)

        # 모든 카드
        print(f"서버로 부터 가져온 카드 리스트: {self.lobby_service.get_card_data_list()}")
        #all_card_number = self.card_data_read().tolist()
        all_card_number = self.lobby_service.get_card_data_list()
        # print(f"카드 번호 리스트: {all_card_number}")
        # print(f"카드 번호 길이: {len(all_card_number)}")

        x = 50
        y = 50

        for i, number in enumerate(all_card_number):
            try:
                #print(f"index: {i}, card number: {number}")
                card = Card(local_translation=(x, y), scale=350)
                card.init_card(number)
                self.my_card_main_scene.add_card_list(card)
                #print(f"카드 리스트: {self.my_card_main_scene.get_card_list()}")

                x += 360

                if (i + 1) % 4 == 0:  # 4개씩
                    y = 500
                    x = 50
                    if (i + 1) % 8 == 0:
                        x = 50
                        y = 50

                if (i + 1) % 8 == 0:
                    continue

            except Exception as e:
                print(f"Error creating card: {e}")
                pass

    def redraw(self):
        if self.show_my_deck_register_screen is True:
            self.make_my_deck_register_frame()
            self.render_after = MyDeckRegisterFrameRenderer(self.my_deck_register_scene, self)
            self.render_after.render()

    def make_my_deck_register_frame(self):
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

        # 검정 투명 화면
        alpha_rectangle = Rectangle(color=(0.0, 0.0, 0.0, 0.8),
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