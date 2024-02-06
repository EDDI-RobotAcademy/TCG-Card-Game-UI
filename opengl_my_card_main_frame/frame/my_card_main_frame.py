import tkinter as tk
from OpenGL import GL, GLU
from pyopengltk import OpenGLFrame
from OpenGL.GL import *
from OpenGL.GLU import *

from opengl_my_card_main_frame.entity.my_deck_register_scene import MyDeckRegisterScene
from tkinter_shape.alpha_rectangle import AlphaRectangle
from tkinter_shape.button_maker import ButtonMaker
from tkinter_shape.image_rectangle_element import ImageRectangel
from opengl_my_card_main_frame.entity.my_card_main_scene import MyCardMainScene
from opengl_my_card_main_frame.renderer.my_card_main_frame_renderer import MyCardMainFrameRenderer
from opengl_my_card_main_frame.renderer.my_deck_register_frame_renderer import MyDeckRegisterFrameRenderer
from opengl_my_deck_register_frame.service.my_deck_register_frame_service_impl import MyDeckRegisterFrameServiceImpl
from text_field.text_box import TextBox
from text_field.text_render import TextRender


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

        # 캔버스 생성
        self.canvas = tk.Canvas(self, width=self.width, height=self.height)
        self.canvas.pack()

        # 덱 생성 버튼 누르기 전 화면 그리기
        self.make_card_main_frame()
        self.renderer = MyCardMainFrameRenderer(self.my_card_main_scene, self)

        self.my_deck_register_frame_service = MyDeckRegisterFrameServiceImpl.getInstance()


    def initgl(self):
        print("initgl")
        glClearColor(0, 0, 0, 0)

        glViewport(0, 0, self.width, self.height)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluOrtho2D(0, self.width, self.height, 0)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)


    def make_card_main_frame(self):

        # 나의 카드 배경 화면
        image_rectangle_element = ImageRectangel(self.master, self.canvas)
        image_rectangle_element.create_background_image(self.width, self.height, image_path="local_storage/image/battle_lobby/background.png")
        self.my_card_main_scene.add_my_card_background(image_rectangle_element)

        # 나의 덱 화면
        x1 = self.width - self.width // 4
        my_deck_rectangle = AlphaRectangle(self.master, self.canvas)
        my_deck_rectangle.create_alpha_rectangle(x1, 0, self.width, self.height, fill='#835C3B')
        self.my_card_main_scene.add_my_card_background(my_deck_rectangle)

        # my card text
        text_x = self.width // 3 + 90
        text_y = self.height // 6 - 50
        text_render = TextRender(self.master, self.canvas, None, self.width, self.height)
        text_render.render_text(x=text_x, y=text_y, custom_text="My Card", text_color="black", font_size=50)
        self.my_card_main_scene.add_text_list(text_render)

        # 나의 덱 text
        text_x = self.width // 2 + 450
        text_y = self.height // 6 - 60
        text_my_deck = TextRender(self.master, self.canvas, None, self.width, self.height)
        text_my_deck.render_text(x=text_x, y=text_y, custom_text="나의 덱", text_color="black", font_size=30)
        self.my_card_main_scene.add_text_list(text_my_deck)

    def make_my_deck_register_frame(self):

        # 검정 투명 화면
        alpha_rectangle = AlphaRectangle(self.master, self.canvas)
        alpha_rectangle.create_alpha_rectangle(0, 0, self.width, self.height, fill='black', alpha=0.7)
        self.my_deck_register_scene.add_alpha_rectangle(alpha_rectangle)

        # 덱 생성 사각형
        x1 = (self.width - 800) // 2
        y1 = (self.height - 500) // 2
        x2 = x1 + 800
        y2 = y1 + 500
        deck_rectangle = AlphaRectangle(self.master, self.canvas)
        deck_rectangle.create_alpha_rectangle(x1, y1, x2, y2, fill='#966F33')
        self.my_deck_register_scene.add_my_deck_background(deck_rectangle)

        # 텍스트
        text_x = self.width // 2
        text_y = self.height // 6 + 135
        text_render = TextRender(self.master, self.canvas, None, self.width, self.height)
        text_render.render_text(x=text_x, y=text_y, custom_text="덱 생성", text_color="black", font_size=30)
        self.my_deck_register_scene.add_text_list(text_render)

        text_x = self.width // 2
        text_y = self.height // 6 + 200
        text_render = TextRender(self.master, self.canvas, None, self.width, self.height)
        text_render.render_text(x=text_x, y=text_y, custom_text="생성할 덱의 이름을 입력 하시오", text_color="black", font_size=20)
        self.my_deck_register_scene.add_text_list(text_render)

        # 텍스트 박스
        self.deck_text_box = TextBox(self.master, self.canvas, None)
        self.deck_text_box.text_box(font_size=20, lines=3)
        self.my_deck_register_scene.add_text_box(self.deck_text_box)
        self.my_deck_register_scene.add_deck_name_list(self.deck_text_box.get_textbox_string()) # 생성한 덱의 이름을 리스트에 저장

    # 덱 생성 버튼을 누르면 진행
    def toggle_visibility(self):
        self.make_my_deck_register_frame()
        self.renderer_after = MyDeckRegisterFrameRenderer(self.my_deck_register_scene, self)
        self.button_submit = ButtonMaker(self.master, self.canvas)
        self.ok_button = self.button_submit.create_button(button_name="확인", bg="black", work= self.on_submit_click)
        #self.button_submit = tk.Button(self.canvas, text="확인", command=self.on_submit_click)
        #self.button_submit.place(relx=0.5, rely=0.65, anchor='center')

    def on_submit_click(self):
        for textbox_string in self.my_deck_register_scene.get_deck_name_list():
            text = textbox_string.get()
        entry_deck_name = text

        self.my_deck_register_frame_service.on_deck_register_click(entry_deck_name)

        self.canvas.delete("all")
        #self.button_submit.destroy()
        self.ok_button.destroy()
        self.deck_text_box.hideTextBox()
        self.redraw()

        # 덱 버튼 생성해서 캔버스에 올림.
        # 여기서 말하는 덱 버튼은 사용자가 새로 생성한 덱을 말함.
        try:
            deck_button= self.my_deck_register_frame_service.create_register_deck_button(self.canvas, entry_deck_name)
            self.my_deck_register_scene.add_deck_button_list(deck_button)
            print(f"생성한 버튼은?: {self.my_deck_register_scene.get_deck_button_list()}")
            deck_button.place(relx=0.88, rely=self.current_rely, anchor="center")
            deck_button.bind("<Button-1>", self.make_my_deck_rectangle)
            self.current_rely += 0.1

        except Exception as e:
            print(f"An error occurred: {e}")

    def redraw(self):
        self.make_card_main_frame()

    # 생성한 덱 버튼을 누르면 그 버튼에 해당하는 덱 화면 만들기.
    def make_my_deck_rectangle(self, event=None):
        self.transparent_rect_visible = False
        if not self.transparent_rect_visible:
            x2 = self.width - self.width // 4
            my_deck_rectangle = AlphaRectangle(self.master, self.canvas)
            my_deck_rectangle.create_alpha_rectangle(0, 0, x2, self.height, fill='#C19A6B')
            #self.my_card_main_scene.add_my_deck_list(my_deck_rectangle)
            print("확인용 메시지: 덱 나타나라 얍!")