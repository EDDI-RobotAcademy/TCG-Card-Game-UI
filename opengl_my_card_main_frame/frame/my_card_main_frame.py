import tkinter as tk
from OpenGL import GL, GLU, GLUT
from pyopengltk import OpenGLFrame
from OpenGL.GL import *
from OpenGL.GLU import *

from opengl_my_card_main_frame.entity.alpha_rectangle import AlphaBlackRectangle
from opengl_my_deck_register_frame.entity.my_deck_rectangle import MyDeckRegisterRectangle
from opengl_my_deck_register_frame.entity.my_deck_render_text import MyDeckRegisterTextEntity


class MyCardMainFrame(OpenGLFrame):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)

        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        self.width = screen_width
        self.height = screen_height

        self.transparent_rect_visible = False

        self.canvas = tk.Canvas(self, width=self.width, height=self.height)
        self.canvas.pack()

        self.textbox_string = tk.StringVar()
        self.textbox_string.trace_add('write', self.update_displayed_text)

        self.alpha_rectangle_drawer = AlphaBlackRectangle(master, self.canvas)
        self.my_deck_rectangle_drawer = MyDeckRegisterRectangle(master, self.canvas)
        self.text_drawer = MyDeckRegisterTextEntity(master, self.canvas, self.textbox_string, self.width, self.height)

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
        # 배경 화면 대신하는 도형
        self.alpha_rectangle_drawer.create_alpha_rectangle(0, 0, self.width, self.height, fill='yellow')

        # 투명 검정 화면 그리기
        if self.transparent_rect_visible:
            self.alpha_rectangle_drawer.create_alpha_rectangle(0, 0, self.width, self.height, fill='black', alpha=0.7)
            self.my_deck_rectangle_drawer.create_rectangle()

            self.text_drawer.render_text()
            self.canvas.textbox = self.text_drawer.text_box()
            self.canvas.textbox.place(relx=0.5, rely=0.6, anchor='center')

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

    def update_displayed_text(self, *args):
        self.text_drawer.render_text()
        # self.update_idletasks()
        self.redraw()



