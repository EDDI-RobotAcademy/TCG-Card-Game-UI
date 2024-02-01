import tkinter as tk
from OpenGL import GL, GLU, GLUT
from pyopengltk import OpenGLFrame
from OpenGL.GL import *
from OpenGL.GLU import *

from opengl_my_card_main_frame.entity.alpha_rectangle import AlphaRectangle
from opengl_my_card_main_frame.entity.background_image import MyCardMainFramImage
from opengl_my_deck_register_frame.entity.my_deck_rectangle import MyDeckRegisterRectangle
from opengl_my_deck_register_frame.entity.my_deck_render_text import MyDeckRegisterTextEntity
from opengl_my_deck_register_frame.service.my_deck_register_frame_service_impl import MyDeckRegisterFrameServiceImpl


class MyCardMainFrame(OpenGLFrame):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)

        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        self.width = screen_width
        self.height = screen_height

        self.transparent_rect_visible = False

        # 캔버스 생성
        self.canvas = tk.Canvas(self, width=self.width, height=self.height)
        self.canvas.pack()

        self.textbox_string = tk.StringVar()
        self.text_drawer = MyDeckRegisterTextEntity(master, self.canvas, None, self.width, self.height)
        self.textbox_string.trace_add('write', self.text_drawer.update_displayed_text)

        self.background_drawer = MyCardMainFramImage(master, self.canvas)
        self.alpha_rectangle_drawer = AlphaRectangle(master, self.canvas)
        self.my_deck_rectangle_drawer = MyDeckRegisterRectangle(master, self.canvas)


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

    def redraw(self, event=None):
        GL.glClear(GL.GL_COLOR_BUFFER_BIT | GL.GL_DEPTH_BUFFER_BIT)

        self.canvas.delete("all")
        # opengl frame에 tkinter canvas를 올리면 frame 배경이 보이지 않으므로 이를 대체할 배경 도형 추가
        #self.alpha_rectangle_drawer.create_alpha_rectangle(0, 0, self.width, self.height, fill='yellow')
        self.background_drawer.create_background_image(self.width, self.height, image_path="local_storage/image/battle_lobby/background.png")
        text_x = self.width // 2
        text_y = self.height // 6
        self.text_drawer.render_text(x=text_x, y=text_y, custom_text="My Card", text_color="black", font_size=50)

        if self.transparent_rect_visible:
            # 투명 검정 화면 그리기
            self.alpha_rectangle_drawer.create_alpha_rectangle(0, 0, self.width, self.height, fill='black', alpha=0.7)
            # 덱 생성 화면 그리기
            deck_rectangle = self.my_deck_rectangle_drawer.create_rectangle(self.width, self.height)

            x1, y1, x2, y2 = self.canvas.coords(deck_rectangle)
            x = (x1 + x2)/2
            y = y1 + 70
            self.text_drawer.render_text(x=x, y=y, custom_text="덱 생성", text_color="black", font_size=30)

            # 생성할 덱 이름을 입력하세요
            x1, y1, x2, y2 = self.canvas.coords(deck_rectangle)
            x = (x1 + x2)/2
            y = y1 + 130
            self.text_drawer.render_text(x=x, y=y)

            self.canvas.textbox = self.text_drawer.text_box(font_size=20, lines=3)
            self.canvas.textbox.place(relx=0.5, rely=0.55, anchor='center')

            button_submit = tk.Button(self.canvas, text="확인", command=self.on_submit_click)
            button_submit.place(relx=0.5, rely=0.65, anchor='center')

        self.tkSwapBuffers()

    def toggle_visibility(self):
        self.transparent_rect_visible = not self.transparent_rect_visible
        self.redraw()

    def reshape(self, width, height):
        GL.glViewport(0, 0, width, height)
        GL.glMatrixMode(GL.GL_PROJECTION)
        GL.glLoadIdentity()
        GLU.gluOrtho2D(0, width, height, 0)
        GL.glMatrixMode(GL.GL_MODELVIEW)
        GL.glLoadIdentity()

    def on_submit_click(self):
        entry_deckname = self.canvas.textbox.get()
        self.my_deck_register_frame_service = MyDeckRegisterFrameServiceImpl.getInstance()
        self.my_deck_register_frame_service.on_deck_register_click(entry_deckname)
