from pyopengltk import OpenGLFrame
from OpenGL import GL, GLU, GLUT

class AlphaBackground(OpenGLFrame):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self.master = master
        self.darkened = False
        self.darken_alpha = 0.5

    def alphaBackground(self):
        GL.glClear(GL.GL_COLOR_BUFFER_BIT | GL.GL_DEPTH_BUFFER_BIT)

        GL.glColor4f(0.0, 0., 0., self.darken_alpha)
        GL.glBegin(GL.GL_QUADS)
        GL.glVertex2f(0, 0)
        GL.glVertex2f(self.width, 0)
        GL.glVertex2f(self.width, self.height)
        GL.glVertex2f(0, self.height)
        GL.glEnd()

        self.tkSwapBuffers()