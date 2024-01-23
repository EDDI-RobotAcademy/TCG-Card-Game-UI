import tkinter

from OpenGL import GL, GLU, GLUT
from pyopengltk import OpenGLFrame


class MakeMyDeckFrame(OpenGLFrame):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self.master = master
        self.darkened = False


    def makeMyDeckFrame(self):
        GL.glColor3f(0.5882, 0.4353, 0.2, 0)  # 원래 색상: #966F33
        GL.glBegin(GL.GL_QUADS)
        GL.glVertex2f(300, 260)
        GL.glVertex2f(900, 260)
        GL.glVertex2f(900, 520)
        GL.glVertex2f(300, 520)
        GL.glEnd()

        self.tkSwapBuffers()