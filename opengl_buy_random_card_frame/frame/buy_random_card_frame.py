import os
import tkinter as tk

import pandas
from pyopengltk import OpenGLFrame
from OpenGL.GL import *
from OpenGL.GLUT import *

from common.utility import get_project_root
from opengl_buy_random_card_frame.entity.buy_random_card_scene import BuyRandomCardScene


from opengl_battle_field_pickable_card.pickable_card import PickableCard
from opengl_buy_random_card_frame.renderer.buy_random_card_frame_renderer import BuyRandomCardFrameRenderer
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

        self.random_card_number = [2, 5, 8, 9, 10, 11, 13, 14, 15, 16]



    def initgl(self):
        print("initgl 입니다.")
        glClearColor(0, 0, 0, 0)
        glOrtho(0, self.width, self.height, 0, -1, 1)

        self.make_card_main_frame()
        self.render = BuyRandomCardFrameRenderer(self.buy_random_card_scene, self)
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

        # 덱 생성 버튼
        button_rectangle = Rectangle(color=(1.0, 0.0, 0.0, 1.0),
                                     local_translation=(0, 0),
                                     vertices=[(0.75 * self.width, 0.85 * self.height + 90),
                                               (self.width - 50, 0.85 * self.height + 90),
                                               (self.width - 50, self.height - 10),
                                               (0.75 * self.width, self.height - 10)])

        self.buy_random_card_scene.add_button_list(button_rectangle)
        print(f"버튼 도형 잘 들어갔니?:{self.buy_random_card_scene.get_button_list()}")

        # 뒤로가기 버튼
        go_to_back_button = Rectangle(color=(0.0, 1.0, 0.0, 1.0),
                                      local_translation=(0, 0),
                                      vertices=[(0.85 * self.width, 0.85 * self.height + 90),
                                                (self.width - 50, 0.85 * self.height + 90),
                                                (self.width - 50, self.height - 10),
                                                (0.85 * self.width, self.height - 10)])

        self.buy_random_card_scene.add_button_list(go_to_back_button)
        print(f"버튼 도형 잘 들어갔니?:{self.buy_random_card_scene.get_button_list()}")

        response_card_number = self.getRandomCardNumber()

        x = 50
        y = 50

        for i, number in enumerate(response_card_number):
            try:
                print(f"index: {i}, card number: {number}")
                card = PickableCard(local_translation=(x, y), scale=250)
                card.init_card(number)
                self.buy_random_card_scene.add_card_list(card)
                print(f"카드 리스트: {self.buy_random_card_scene.get_card_list()}")

                x += 240

                if (i + 1) % 5 == 0:
                    y = 400
                    x = 50
                    if (i + 1) % 10 == 0:
                        x = 50
                        y = 50

                if (i + 1) % 8 == 0:
                    continue

            except Exception as e:
                print(f"Error creating card: {e}")
                pass

    def redraw(self):
            self.make_card_main_frame()
            self.render_after = BuyRandomCardFrameRenderer(self.buy_random_card_scene, self)
            self.render_after.render()

    def setRandomCardNumber(self, random_card_number):
        self.random_card_number = random_card_number

    def getRandomCardNumber(self):
        return self.random_card_number

