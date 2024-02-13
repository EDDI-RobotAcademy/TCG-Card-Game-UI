import os
import tkinter as tk

import pandas
from pyopengltk import OpenGLFrame
from OpenGL.GL import *
from OpenGL.GLUT import *

from common.utility import get_project_root
from opengl_my_card_main_frame.entity.my_card_main_scene import MyCardMainScene
from opengl_my_card_main_frame.entity.my_deck_register_scene import MyDeckRegisterScene

from opengl_battle_field_card.card import Card
from opengl_my_card_main_frame.renderer.my_card_main_frame_renderer import MyCardMainFrameRenderer
from opengl_shape.image_rectangle_element import ImageRectangleElement
from opengl_shape.rectangle import Rectangle
from text_field.text_box import TextBox


class MyCardMainFrame(OpenGLFrame):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self.my_card_main_scene = MyCardMainScene()
        self.my_deck_register_scene = MyDeckRegisterScene()
        self.current_rely = 0.20

        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        self.width = screen_width
        self.height = screen_height

        self.textbox_string = tk.StringVar()

        # 덱 생성 버튼 누르기 전 화면 그리기
        # self.make_card_main_frame()
        # self.renderer = MyCardMainFrameRenderer(self.my_card_main_scene, self)

    def initgl(self):
        print("initgl 입니다.")
        glClearColor(0, 0, 0, 0)
        glOrtho(0, self.width, self.height, 0, -1, 1)


    def make_card_main_frame(self):
        project_root = get_project_root()
        glClearColor(0.0, 1.0, 0.0,0.0)
        glClear(GL_COLOR_BUFFER_BIT)

        # 나의 카드 배경 화면
        background_rectangle = ImageRectangleElement(image_path=os.path.join(project_root, "local_storage", "image", "battle_lobby", "background.png"),
                                                     local_translation=(0, 0),
                                                     vertices=[(0, 0), (self.width, 0), (self.width, self.height), (0, self.height)])
        self.my_card_main_scene.add_my_card_background(background_rectangle)
        print(f"카드 배경 잘 들어갔니?:{self.my_card_main_scene.get_my_card_background()}")

        # 나의 덱 화면
        my_deck_rectangle = Rectangle(color=(0.5137, 0.3608, 0.2314, 1.0),
                                      local_translation=(0, 0),
                                      vertices=[(0.75 * self.width, 0), (self.width, 0), (self.width, self.height),
                                                (0.75 * self.width, self.height)])

        self.my_card_main_scene.add_my_card_background(my_deck_rectangle)
        print(f"덱 화면 잘 들어갔니?:{self.my_card_main_scene.get_my_card_background()}")

        # 덱 생성 버튼
        button_rectangle = Rectangle(color=(1.0, 0.0, 0.0, 1.0),
                                     local_translation=(0, 0),
                                     vertices=[(0.85 * self.width, 0.85 * self.height),
                                               (self.width, 0.85 * self.height),
                                               (self.width, self.height),
                                               (0.85 * self.width, self.height)])

        self.my_card_main_scene.add_button_list(button_rectangle)
        print(f"버튼 도형 잘 들어갔니?:{self.my_card_main_scene.get_button_list()}")


        #모든 카드
        all_card_number = self.card_data_read().tolist()
        print(f"카드 번호 리스트: {all_card_number}")
        x = 10
        y = 20
        for number in all_card_number:
            try:
                card = Card(local_translation=(x, y))
                card.init_card(int(number))
                self.my_card_main_scene.add_card_list(card)
                print(f"카드 리스트: {self.my_card_main_scene.get_card_list()}")
                print(number)
                x += 390
                if len(self.my_card_main_scene.get_card_list()) == 4:
                    print(f"카드 리스트 안에 몇 개 있니?: {len(self.my_card_main_scene.get_card_list())}")
                    x = 10
                    y = 620

                if len(self.my_card_main_scene.get_card_list()) == 5:
                    print(f"카드 리스트 안에 몇 개 있니?: {len(self.my_card_main_scene.get_card_list())}")
                    x = 10
                    x += 390

                if len(self.my_card_main_scene.get_card_list()) == 8:
                    print(f"카드 리스트 안에 몇 개 있니?: {len(self.my_card_main_scene.get_card_list())}")
                    break

            except Exception as e:
                print(f"Error creating card: {e}")
                pass
    def redraw(self):
        self.make_card_main_frame()
        self.render = MyCardMainFrameRenderer(self.my_card_main_scene, self)
        self.render.render()


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
        entry = tk.Entry(self.master, textvariable=self.textbox_string)
        entry.place(relx=0.5, rely=0.5, width=300, height=100, anchor="center")
        #self.my_deck_register_scene.add_deck_name_list(self.entry.get_textbox_string()) # 생성한 덱의 이름을 리스트에 저장

    def getScene(self):
        return self.my_deck_register_scene

    # def redraw(self):
    #     self.make_card_main_frame()
    #     self.renderer = MyCardMainFrameRenderer(self.my_card_main_scene, self)

    # csv 파일 읽어오기
    def card_data_read(self):
        currentLocation = os.getcwd()
        print(f"currentLocation: {currentLocation}")

        data_card = pandas.read_csv('local_storage/card/data.csv')
        data_card_number = data_card['카드번호']

        return data_card_number