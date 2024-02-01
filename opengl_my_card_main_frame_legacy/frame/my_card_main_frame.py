# import tkinter as tk
from OpenGL import GL, GLU, GLUT
from pyopengltk import OpenGLFrame
from OpenGL.GL import *
from OpenGL.GLU import *

from opengl_my_card_main_frame_legacy.entity.alpha_rectangle import AlphaRectangle
from opengl_my_card_main_frame_legacy.entity.my_card_main_frame_scene import MyCardMainFrameScene
from opengl_my_card_main_frame_legacy.renderer.my_card_main_frame_renderer import MyCardMainFrameRenderer
from opengl_my_deck_register_frame_legacy.entity.my_deck_rectangle import MyDeckRegisterRectangle


class MyCardMainFrame(OpenGLFrame):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self.master = master
        self.domain_scene = MyCardMainFrameScene()

        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        self.width = screen_width
        self.height = screen_height

        self.transparent_rect_visible = False

        #self.canvas = tk.Canvas(self, width=self.width, height=self.height)
        #self.canvas.pack()

        self.bind("<Configure>", self.on_resize)

        self.renderer = MyCardMainFrameRenderer(self.domain_scene, self)


    def initgl(self):
        print("initgl")
        glClearColor(0.8706, 0.7216, 0.5294, 0)

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

        GL.glColor4f(0.8706, 0.7216, 0.5294, 0)
        GL.glBegin(GL.GL_QUADS)
        GL.glVertex2f(0, 0)
        GL.glVertex2f(self.width, 0)
        GL.glVertex2f(self.width, self.height)
        GL.glVertex2f(0, self.height)
        GL.glEnd()

        #self.canvas.delete("all")

        if self.transparent_rect_visible:
            self.init_shapes(0.5)
            self.deck_shape()
            #self.canvas.create_rectangle(20, 20, 620, 280, fill='green')

        self.tkSwapBuffers()
        self.renderer.render()

    def init_shapes(self, alpha):
        alpha_background_frame = AlphaRectangle(width=self.width, height=self.height)
        alpha_background_frame.set_background_alpha(alpha)
        self.domain_scene.add_shape(alpha_background_frame)

    def deck_shape(self):
        my_deck_frame = MyDeckRegisterRectangle.create_my_deck_register_rectangle()
        self.domain_scene.add_shape(my_deck_frame)


    def apply_translation(self, translation):
        for shape, shape_translation in zip(self.domain_scene.shapes, self.domain_scene.translations):
            print("shape translate")
            shape.local_translate(translation)


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


    def on_resize(self, event):
        self.reshape(event.width, event.height)


