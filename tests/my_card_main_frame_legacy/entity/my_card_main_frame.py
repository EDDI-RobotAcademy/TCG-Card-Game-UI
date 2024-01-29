from OpenGL import GL, GLU, GLUT
from pyopengltk import OpenGLFrame
from opengl_shape.rectangle import Rectangle


class MyCardMainFrame(OpenGLFrame):
    def __init__(self, master=None, width=1200, height=800, **kwargs):
        super().__init__(master, **kwargs)
        self.master = master
        self.darkened = False
        self.width = width
        self.height = height
        self.background_rectangle = Rectangle(color=(0.0, 0.0, 0.0, 0),
                                              vertices=[(0, 0), (self.width, 0), (self.width, self.height),
                                                        (0, self.height)])

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

    def set_background_alpha(self, alpha):
        self.background_rectangle.set_alpha(alpha)
        self.background_rectangle.draw()

        self.tkSwapBuffers()