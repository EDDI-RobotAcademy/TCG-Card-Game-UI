import tkinter as tk
from OpenGL import GL, GLU
from pyopengltk import OpenGLFrame
from OpenGL.GL import *
from OpenGL.GLU import *

from tkinter_shape.alpha_rectangle import AlphaRectangle
from tkinter_shape.image_rectangle_element import MyCardMainFramImage
from opengl_my_card_main_frame.entity.my_card_main_scene import MyCardMainScene
from opengl_my_card_main_frame.renderer.my_card_main_frame_renderer import MyCardMainrameRenderer
from opengl_my_card_main_frame.renderer.my_card_main_frame_renderer_after_click_button import MyCardMainrameRendererAfterClickButton
from opengl_my_deck_register_frame.service.my_deck_register_frame_service_impl import MyDeckRegisterFrameServiceImpl
from text_field.text_box import TextBox
from text_field.text_render import TextRender


class MyCardMainFrame(OpenGLFrame):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self.my_card_main_scene = MyCardMainScene()
        self.current_rely = 0.20

        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        self.width = screen_width
        self.height = screen_height


        # 캔버스 생성
        self.canvas = tk.Canvas(self, width=self.width, height=self.height)
        self.canvas.pack()

        self.make_main_frame_before()

        self.renderer = MyCardMainrameRenderer(self.my_card_main_scene, self)

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

    def make_main_frame_before(self):

        # 배경 화면
        image_rectangle_element = MyCardMainFramImage(self.master, self.canvas)
        image_rectangle_element.create_background_image(self.width, self.height, image_path="local_storage/image/battle_lobby/background.png")
        self.my_card_main_scene.add_image_rectangle(image_rectangle_element)

        # 나의 덱 화면
        x1 = self.width - self.width // 4
        my_deck_rectangle = AlphaRectangle(self.master, self.canvas)
        my_deck_rectangle.create_alpha_rectangle(x1, 0, self.width, self.height, fill='#835C3B')
        self.my_card_main_scene.add_alpha_rectangle(my_deck_rectangle)

        # my card text
        text_x = self.width // 3 + 90
        text_y = self.height // 6 - 50
        text_render = TextRender(self.master, self.canvas, None, self.width, self.height)
        text_render.render_text(x=text_x, y=text_y, custom_text="My Card", text_color="black", font_size=50)
        self.my_card_main_scene.add_text_render(text_render)

        # 나의 덱 text
        text_x = self.width // 2 + 450
        text_y = self.height // 6 - 60
        text_my_deck = TextRender(self.master, self.canvas, None, self.width, self.height)
        text_my_deck.render_text(x=text_x, y=text_y, custom_text="나의 덱", text_color="black", font_size=30)
        self.my_card_main_scene.add_text_render(text_my_deck)

    def make_main_frame_after(self):

        # 검정 투명 화면
        alpha_rectangle = AlphaRectangle(self.master, self.canvas)
        alpha_rectangle.create_alpha_rectangle(0, 0, self.width, self.height, fill='black', alpha=0.7)
        self.my_card_main_scene.add_alpha_rectangle(alpha_rectangle)

        # 덱 생성 사각형
        x1 = (self.width - 800) // 2
        y1 = (self.height - 500) // 2
        x2 = x1 + 800
        y2 = y1 + 500
        deck_rectangle = AlphaRectangle(self.master, self.canvas)
        deck_rectangle.create_alpha_rectangle(x1, y1, x2, y2, fill='#966F33')
        self.my_card_main_scene.add_alpha_rectangle(deck_rectangle)

        text_x = self.width // 2
        text_y = self.height // 6 + 135
        text_render = TextRender(self.master, self.canvas, None, self.width, self.height)
        text_render.render_text(x=text_x, y=text_y, custom_text="덱 생성", text_color="black", font_size=30)
        self.my_card_main_scene.add_text_render(text_render)

        text_x = self.width // 2
        text_y = self.height // 6 + 200
        text_render = TextRender(self.master, self.canvas, None, self.width, self.height)
        text_render.render_text(x=text_x, y=text_y, custom_text="생성할 덱의 이름을 입력하시오", text_color="black", font_size=20)
        self.my_card_main_scene.add_text_render(text_render)

        self.deck_text_box = TextBox(self.master, self.canvas, None)
        self.deck_text_box.text_box(font_size=20, lines=3)
        self.my_card_main_scene.add_text_box(self.deck_text_box)

    def toggle_visibility(self):
        self.make_main_frame_after()
        self.renderer_after = MyCardMainrameRendererAfterClickButton(self.my_card_main_scene, self)
        self.button_submit = tk.Button(self.canvas, text="확인", command=self.on_submit_click)
        self.button_submit.place(relx=0.5, rely=0.65, anchor='center')

    def reshape(self, width, height):
        GL.glViewport(0, 0, width, height)
        GL.glMatrixMode(GL.GL_PROJECTION)
        GL.glLoadIdentity()
        GLU.gluOrtho2D(0, width, height, 0)
        GL.glMatrixMode(GL.GL_MODELVIEW)
        GL.glLoadIdentity()

    def on_submit_click(self):
        text_boxes = self.my_card_main_scene.get_text_box()
        for text_box in text_boxes:
            textbox_string = text_box.get_textbox_string()
            text_value = textbox_string.get()
        entry_deck_name = text_value
        self.my_deck_register_frame_service.on_deck_register_click(entry_deck_name)

        self.canvas.delete("all")
        self.button_submit.destroy()
        self.deck_text_box.hideTextBox()
        self.redraw()

        # 버튼 생성해서 캔버스에 올림.
        try:
            if self.my_deck_register_frame_service.on_deck_register_click(entry_deck_name):
                deck_button= self.my_deck_register_frame_service.create_register_deck_button(self.canvas, entry_deck_name)
                deck_button.place(relx=0.88, rely=self.current_rely, anchor="center")
                self.current_rely += 0.1

        except Exception as e:
            print(f"An error occurred: {e}")

    def redraw(self):
        self.make_main_frame_before()


