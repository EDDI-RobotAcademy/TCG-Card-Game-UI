from OpenGL import GL
from OpenGL.GLU.tess import GLU
from pyopengltk import OpenGLFrame
from my_deck_construction_frame.entity.rectangel_frame import RectangleFrame


class MyDeckConstructionFrame(OpenGLFrame):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self.master = master
        self.rectangle_entity = RectangleFrame()

        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        self.width = screen_width
        self.height = screen_height

    def initgl(self):
        GL.glClearColor(0.8706, 0.7216, 0.5294, 0)
        GL.glEnable(GL.GL_BLEND)
        GL.glBlendFunc(GL.GL_SRC_ALPHA, GL.GL_ONE_MINUS_SRC_ALPHA)
        GL.glLoadIdentity()
        GLU.gluOrtho2D(0, self.width, self.height, 0)


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

    def draw_frame(self):
        self.rectangle_entity.rectangle_draw()
        self.tkSwapBuffers()

    def toggle_visibility(self):
        current_visibility = self.rectangle_entity.get_visible()
        self.rectangle_entity.set_visible(not current_visibility)

        self.draw_frame()