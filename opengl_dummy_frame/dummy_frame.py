import os
import tkinter

from OpenGL.GL import *
from OpenGL.GLU import *
from pyopengltk import OpenGLFrame

from PIL import Image, ImageTk

from common.utility import get_project_root

from battle_field.entity.effect_animation import EffectAnimation
from battle_field.infra.window_size_repository import WindowSizeRepository
from pre_drawed_image_manager.pre_drawed_image import PreDrawedImage


class DummyFrame(OpenGLFrame):
    is_reshape_not_complete = True

    width = 0
    height = 0
    count = 0.01
    window_size_repository = WindowSizeRepository.getInstance()
    pre_drawed_image_instance = PreDrawedImage.getInstance()

    def __init__(self, master=None, switchFrameWithMenuName=None, **kwargs):
        super().__init__(master, **kwargs)




        self.switch_frame_with_menu_name = switchFrameWithMenuName

        self.bind("<Configure>", self.on_resize)

    def get_real_width(self):
        return self.width

    def get_real_height(self):
        return self.height

    def initgl(self):
        glClearColor(1.0, 1.0, 1.0, 0.0)
        glOrtho(0, self.width, self.height, 0, -1, 1)

        self.tkMakeCurrent()

    def reshape(self, width, height):
        print(f"Reshaping window to width={width}, height={height}")

        if self.is_reshape_not_complete:
            self.init_first_window(width, height)

        # self.current_width = width
        # self.current_height = height
        #
        # self.width_ratio = self.current_width / self.prev_width
        # self.height_ratio = self.current_height / self.prev_height
        #
        # self.width_ratio = min(self.width_ratio, 1.0)
        # self.height_ratio = min(self.height_ratio, 1.0)
        #
        # self.prev_width = self.current_width
        # self.prev_height = self.current_height

        glViewport(0, 0, width, height)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluOrtho2D(0, width, height, 0)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

    def on_resize(self, event):
        self.reshape(event.width, event.height)

    def init_first_window(self, width, height):
        print(f"Operate Only Once -> width: {width}, height: {height}")
        self.width = width
        self.height = height

        self.window_size_repository.set_total_window_size(self.width, self.height)

        self.label = tkinter.Label(self)
        self.label.place(anchor="nw")
        self.load_image()
        self.display_image()

        self.master.after(1000, self.pre_draw_full_screen, width, height)

    def load_image(self):
        # 이미지 로드 및 Tkinter PhotoImage로 변환
        self.original_image = Image.open("local_storage/image/battle_lobby/loading_screen.png")

    def display_image(self):
        # 이미지를 현재 창 크기에 맞게 리사이즈하고 Label에 표시
        resized_img = self.original_image.resize((self.master.winfo_width(), self.master.winfo_height()),
                                                 Image.ANTIALIAS)
        self.image = ImageTk.PhotoImage(resized_img)
        self.label.config(image=self.image)

    def redraw(self):
        if self.is_reshape_not_complete:

            return



        self.switch_frame_with_menu_name("main-menu")


    def pre_draw_full_screen(self, width, height):
        self.pre_drawed_image_instance.pre_draw_full_screen_nether_blade_skill(width, height)
        self.pre_drawed_image_instance.pre_draw_full_screen_sea_of_wraith(width, height)
        self.pre_drawed_image_instance.pre_draw_full_screen_nether_blade_targeting_skill(width, height)
        self.pre_drawed_image_instance.pre_draw_full_screen_nether_blade_deploy(width, height)
        self.pre_drawed_image_instance.pre_draw_full_screen_call_of_Leonic_effect_animation(width, height)

        # self.current_width = self.width
        # self.current_height = self.height
        #
        # self.prev_width = self.width
        # self.prev_height = self.height
        self.is_reshape_not_complete = False


    def resize_image(self, image, width, height):
        """
        이미지를 지정된 크기로 리사이즈합니다.
        """
        return image.resize((width, height))