from pyopengltk import OpenGLFrame
from OpenGL import GL, GLU, GLUT


class MyCardFrame(OpenGLFrame):
    def __init__(self, master=None, **kwargs):
        super().__init__(master)
        self.master = master
        self.darken_alpha = 0.5

    def initgl(self):
        GL.glClearColor(0.5, 0.5, 0.5, 1.0)
        GL.glEnable(GL.GL_BLEND)
        GL.glBlendFunc(GL.GL_SRC_ALPHA, GL.GL_ONE_MINUS_SRC_ALPHA)
        GL.glLoadIdentity()
        GLU.gluOrtho2D(0, self.width, self.height, 0)
        GLUT.glutInit()

