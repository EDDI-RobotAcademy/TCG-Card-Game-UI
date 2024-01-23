from pyopengltk import OpenGLFrame
from OpenGL import GL, GLU, GLUT


class MyCardMainFrame(OpenGLFrame):
    def __init__(self, master=None, **kwargs):
        super().__init__(master)
        self.master = master
        self.darkened = False
        self.darken_alpha = 0.5

    def initgl(self):
        GL.glClearColor(0.8706, 0.7216, 0.5294, 0)
        GL.glEnable(GL.GL_BLEND)
        GL.glBlendFunc(GL.GL_SRC_ALPHA, GL.GL_ONE_MINUS_SRC_ALPHA)
        GL.glLoadIdentity()
        GLU.gluOrtho2D(0, self.width, self.height, 0)
        GLUT.glutInit()

    def redraw(self, event=None):
        GL.glClear(GL.GL_COLOR_BUFFER_BIT | GL.GL_DEPTH_BUFFER_BIT)

        GL.glColor4f(0.8706, 0.7216, 0.5294, 0)
        GL.glBegin(GL.GL_QUADS)
        GL.glVertex2f(0, 0)
        GL.glVertex2f(self.width, 0)
        GL.glVertex2f(self.width, self.height)
        GL.glVertex2f(0, self.height)
        GL.glEnd()

        self.tkSwapBuffers()

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