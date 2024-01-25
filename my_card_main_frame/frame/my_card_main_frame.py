from pyopengltk import OpenGLFrame
from OpenGL import GL, GLU, GLUT

from my_card_main_frame.entity.alpha_rectangle import AlphaRectangle

class MyCardFrame(OpenGLFrame):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self.master = master
        self.alpha_background_entity = AlphaRectangle()

        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        self.width = screen_width
        self.height = screen_height

    def initgl(self):
        GL.glClearColor(0.8706, 0.7216, 0.5294, 0)
        GL.glEnable(GL.GL_BLEND)
        GL.glBlendFunc(GL.GL_SRC_ALPHA, GL.GL_ONE_MINUS_SRC_ALPHA)
        GL.glLoadIdentity()
        GLU.gluOrtho2D(0, self.alpha_background_entity.width, self.alpha_background_entity.height, 0)
        # GLUT.glutInit()


    def redraw(self, event=None):
        GL.glClear(GL.GL_COLOR_BUFFER_BIT | GL.GL_DEPTH_BUFFER_BIT)

        GL.glColor4f(0.8706, 0.7216, 0.5294, 0)
        GL.glBegin(GL.GL_QUADS)
        GL.glVertex2f(0, 0)
        GL.glVertex2f(self.alpha_background_entity.width, 0)
        GL.glVertex2f(self.alpha_background_entity.width, self.alpha_background_entity.height)
        GL.glVertex2f(0, self.alpha_background_entity.height)
        GL.glEnd()

        self.tkSwapBuffers()

    def set_frame_alpha(self, alpha):
        self.alpha_background_entity.set_background_alpha(alpha)
        self.alpha_background_entity.draw()

        self.tkSwapBuffers()

    def toggle_visibility(self):
        if self.alpha_background_entity.is_visible:
            self.set_frame_alpha(0.5)
            self.alpha_background_entity.is_visible = False
        else:
            self.set_frame_alpha(1.0)
            self.alpha_background_entity.is_visible = True