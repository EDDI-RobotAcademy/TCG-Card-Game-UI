import unittest
import tkinter as tk

import pandas
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from pyopengltk import OpenGLFrame

from common.utility import get_project_root
from opengl_battle_field_card.card import Card
from opengl_shape.image_rectangle_element import ImageRectangleElement
from opengl_shape.rectangle import Rectangle


class RectDrawingApp(OpenGLFrame):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)

        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        self.width = screen_width
        self.height = screen_height

        self.card_list = []

        data_card_number = self.test_ugly_data_csv_read().tolist()
        print(f"data_csv: {data_card_number}")
        x = 10
        y = 20
        for number in data_card_number:
            try:
                card = Card(local_translation=(x, y))
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
            except Exception as e:
                print(f"Error creating card: {e}")
                pass

    def initgl(self):
        glClearColor(1.0, 1.0, 1.0, 1.0)
        #gluOrtho2D(-1.0, 1.0, -1.0, 1.0)
        glOrtho(0, self.width, self.height, 0, -1, 1)

    def redraw(self):
        project_root = get_project_root()
        glClear(GL_COLOR_BUFFER_BIT)
        glClearColor(0.0, 1.0, 0.0, 0.0)

        # 배경 이미지 도형
        background_rectangle = ImageRectangleElement(image_path=os.path.join(project_root, "local_storage", "image", "battle_lobby", "background.png"),
                                                     local_translation=(0, 0),
                                                     #vertices=[(-1, -1), (1, -1), (1, 1), (-1, 1)]
                                                     vertices=[(0, 0), (self.width, 0), (self.width, self.height), (0, self.height)])
        background_rectangle.draw()

        # 나의 덱 도형
        myDeck_rectangle= Rectangle(color=(0.5137, 0.3608, 0.2314, 1.0),
                                    local_translation=(0, 0),
                                    #vertices=[(0.45, -1), (1, -1), (1, 1), (0.45, 1)]
                                    vertices=[(0.75*self.width, 0), (self.width, 0), (self.width, self.height), (0.75*self.width, self.height)])
        myDeck_rectangle.draw()

        for card in self.card_list:
            attached_tool_card = card.get_tool_card()
            attached_tool_card.draw()

            pickable_card_base = card.get_pickable_card_base()
            pickable_card_base.draw()

            attached_shape_list = pickable_card_base.get_attached_shapes()
            for attached_shape in attached_shape_list:
                attached_shape.draw()

        self.tkSwapBuffers()

    # csv 파일 읽어오기
    def test_ugly_data_csv_read(self):
        currentLocation = os.getcwd()
        print(f"currentLocation: {currentLocation}")

        data_card = pandas.read_csv('../../local_storage/card/data.csv')
        data_card_number = data_card['카드번호']

        print(data_card_number)

        return data_card_number

class TestAppWindow(unittest.TestCase):
    def test_opengl_basic(self):
        root = tk.Tk()
        root.title("OpenGL Rectangle Drawing")
        root.geometry(f"{root.winfo_screenwidth()}x{root.winfo_screenheight()}-0-0")

        app = RectDrawingApp(root)
        app.pack(side="top", fill="both", expand=True)
        app.animate = 1
        root.mainloop()

if __name__ == '__main__':
    unittest.main()