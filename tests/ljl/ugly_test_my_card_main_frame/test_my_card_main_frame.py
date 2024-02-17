import os

import pandas
from OpenGL.GL import *
from OpenGL.GLU import *
import tkinter as tk

from pyopengltk import OpenGLFrame

from opengl_battle_field_pickable_card.pickable_card import PickableCard
from PIL import Image, ImageTk

from tkinter_shape.shape import Shape
from tests.ugly_test_card.renderer.card_frame_renderer import CardFrameRenderer


class CardFrame(OpenGLFrame):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)

        self.card_list = []
        self.images = []

        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        self.width = screen_width
        self.height = screen_height

        self.canvas = tk.Canvas(self, width=self.width, height=self.height)
        self.canvas.pack()

        self.create_alpha_rectangle(0, 0, self.width, self.height, fill='#835C3B')


        data_card_number = self.test_ugly_data_csv_read().tolist()
        print(f"data_csv: {data_card_number}")
        x = 10
        y = 20
        for number in data_card_number:
            try:
                card = PickableCard(local_translation=(x, y))
                card.init_card(int(number))
                self.card_list.append(card)
                print(f"카드 리스트: {self.card_list}")
                print(number)
                x += 390
                if len(self.card_list) > 3:
                    x = 10
                    y = 620
                if len(self.card_list) == 6:
                    break
            except:
                pass
        # positions = [(10, 20), (400, 20), (790, 20)]  # 예시 위치
        # for position in positions:
        #     print(position)
        #     card = Card(local_translation=position)
        #     card.init_card(8)  # 카드 번호 설정 (예시)
        #     self.card_list.append(card)

        #self.renderer = CardFrameRenderer(self.card_list, self)
        print(len(self.card_list))
        self.redraw()

    def initgl(self):
        glClearColor(1.0, 1.0, 1.0, 0.0)
        glOrtho(0, self.width, self.height, 0, -1, 1)

    def create_alpha_rectangle(self, x1, y1, x2, y2, **kwargs):
        if 'alpha' in kwargs:
            alpha = int(kwargs.pop('alpha') * 255)
            fill = kwargs.pop('fill')
            fill = self.master.winfo_rgb(fill) + (alpha,)
            image = Image.new('RGBA', (x2 - x1, y2 - y1), fill)
            self.images.append(ImageTk.PhotoImage(image))
            self.canvas.create_image(x1, y1, image=self.images[-1], anchor='nw')
        self.canvas.create_rectangle(x1, y1, x2, y2, **kwargs)

    def redraw(self):
        self.tkMakeCurrent()
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        for card in self.card_list:
            attached_tool_card = card.get_tool_card()
            attached_tool_card.draw()

            pickable_card_base = card.get_pickable_card_base()
            pickable_card_base.draw()

            attached_shape_list = pickable_card_base.get_attached_shapes()
            for attached_shape in attached_shape_list:
                attached_shape.draw()

        self.tkSwapBuffers()


    def test_ugly_data_csv_read(self):
        currentLocation = os.getcwd()
        print(f"currentLocation: {currentLocation}")

        data_card = pandas.read_csv('../../../local_storage/card/data.csv')
        data_card_number = data_card['카드번호']

        print(data_card_number)

        return data_card_number


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Card Frame")
    root.geometry(f"{root.winfo_screenwidth()}x{root.winfo_screenheight()}-0-0")

    card_frame = CardFrame(root)
    card_frame.pack(fill=tk.BOTH, expand=tk.YES)

    root.mainloop()
