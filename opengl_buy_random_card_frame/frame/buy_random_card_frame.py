import os
import tkinter as tk

import pandas
from pyopengltk import OpenGLFrame
from OpenGL.GL import *
from OpenGL.GLUT import *

from common.utility import get_project_root
from opengl_buy_random_card_frame.entity.buy_random_card_scene import BuyRandomCardScene


from opengl_battle_field_card.card import Card
from opengl_my_card_main_frame.renderer.fifth_page_card_renerer import FifthPageCardRenderer
from opengl_my_card_main_frame.renderer.fourth_page_card_renderer import FourthPageCardRenderer
from opengl_my_card_main_frame.renderer.my_card_main_frame_renderer import MyCardMainFrameRenderer
from opengl_my_card_main_frame.renderer.my_deck_register_frame_renderer import MyDeckRegisterFrameRenderer
from opengl_my_card_main_frame.renderer.second_page_card_renderer import SecondPageCardRenderer
from opengl_my_card_main_frame.renderer.third_page_card_renderer import ThirdPageCardRenderer
from opengl_shape.image_rectangle_element import ImageRectangleElement
from opengl_shape.rectangle import Rectangle


class BuyRandomCardFrame(OpenGLFrame):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self.buy_random_card_scene = BuyRandomCardScene()
        self.current_rely = 0.20

        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        self.width = screen_width
        self.height = screen_height



    def initgl(self):
        print("initgl 입니다.")
        glClearColor(0, 0, 0, 0)
        glOrtho(0, self.width, self.height, 0, -1, 1)

        self.make_card_main_frame()
        self.render = MyCardMainFrameRenderer(self.buy_random_card_scene, self)
        self.render.render()


    def make_card_main_frame(self):
        project_root = get_project_root()
        glClearColor(0.0, 1.0, 0.0,0.0)
        glClear(GL_COLOR_BUFFER_BIT)

        # 나의 카드 배경 화면
        background_rectangle = ImageRectangleElement(image_path=os.path.join(project_root, "local_storage", "image", "battle_lobby", "background.png"),
                                                     local_translation=(0, 0),
                                                     vertices=[(0, 0), (self.width, 0), (self.width, self.height), (0, self.height)])
        self.buy_random_card_scene.add_my_card_background(background_rectangle)
        print(f"카드 배경 잘 들어갔니?:{self.buy_random_card_scene.get_my_card_background()}")


        self.my_card_main_scene.add_my_card_background(my_deck_rectangle)
        print(f"덱 화면 잘 들어갔니?:{self.my_card_main_scene.get_my_card_background()}")

        # 덱 생성 버튼
        button_rectangle = Rectangle(color=(1.0, 0.0, 0.0, 1.0),
                                     local_translation=(0, 0),
                                     vertices=[(0.85 * self.width, 0.85 * self.height),
                                               (self.width - 50, 0.85 * self.height),
                                               (self.width - 50, self.height - 100),
                                               (0.85 * self.width, self.height - 100)])

        self.my_card_main_scene.add_button_list(button_rectangle)
        print(f"버튼 도형 잘 들어갔니?:{self.my_card_main_scene.get_button_list()}")

        # 뒤로가기 버튼
        go_to_back_button = Rectangle(color=(0.0, 1.0, 0.0, 1.0),
                                      local_translation=(0, 0),
                                      vertices=[(0.85 * self.width, 0.85 * self.height + 90),
                                                (self.width - 50, 0.85 * self.height + 90),
                                                (self.width - 50, self.height - 10),
                                                (0.85 * self.width, self.height - 10)])

        self.my_card_main_scene.add_button_list(go_to_back_button)
        print(f"버튼 도형 잘 들어갔니?:{self.my_card_main_scene.get_button_list()}")



        # 모든 카드
        all_card_number = self.card_data_read().tolist()
        print(f"카드 번호 리스트: {all_card_number}")
        print(f"카드 번호 길이: {len(all_card_number)}")

        x = 50
        y = 50

        for i, number in enumerate(all_card_number):
            try:
                print(f"index: {i}, card number: {number}")
                card = Card(local_translation=(x, y), scale=350)
                card.init_card(number)
                self.my_card_main_scene.add_card_list(card)
                print(f"카드 리스트: {self.my_card_main_scene.get_card_list()}")

                x += 360

                if (i + 1) % 4 == 0:  # 4개씩
                    print(f"index(4단위로 나와야 정상임):{i}")
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





    # csv 파일 읽어오기
    def card_data_read(self):
        currentLocation = os.getcwd()
        print(f"currentLocation: {currentLocation}")

        data_card = pandas.read_csv('local_storage/card/data.csv')
        data_card_number = data_card['카드번호']

        return data_card_number
