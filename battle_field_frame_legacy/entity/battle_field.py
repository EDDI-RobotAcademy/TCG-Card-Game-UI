import tkinter as tk
from pyopengltk import OpenGLFrame
from OpenGL import GL, GLU, GLUT

class BattleFieldFrame(OpenGLFrame):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self.darkened = False
        self.darken_alpha = 0.0
        self.card_texture = None

        self.width = self.winfo_reqwidth()
        self.height = self.winfo_reqheight()

        self.bind("<Configure>", self.on_resize)

    def initgl(self):
        GL.glClearColor(1.0, 1.0, 1.0, 0.0)
        GLU.gluOrtho2D(0, self.width, self.height, 0)
        GLUT.glutInit()

    def reshape(self, width, height):
        print("reshape")
        GL.glViewport(0, 0, width, height)
        GL.glMatrixMode(GL.GL_PROJECTION)
        GL.glLoadIdentity()
        GLU.gluOrtho2D(0, width, height, 0)
        GL.glMatrixMode(GL.GL_MODELVIEW)
        GL.glLoadIdentity()

    def on_resize(self, event):
        print("on_resize")
        self.reshape(event.width, event.height)