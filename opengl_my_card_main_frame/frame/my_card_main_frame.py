from pyopengltk import OpenGLFrame
from OpenGL import GL, GLU, GLUT

from opengl_my_card_main_frame.entity.alpha_rectangle import AlphaRectangle
from opengl_my_card_main_frame.entity.my_card_main_frame_scene import MyCardMainFrameScene
from opengl_my_card_main_frame.renderer.my_card_main_frame_renderer import MyCardMainFrameRenderer


class MyCardMainFrame(OpenGLFrame):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self.master = master
        self.domain_scene = MyCardMainFrameScene()

        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        self.width = screen_width
        self.height = screen_height

        self.bind("<Configure>", self.on_resize)

        self.init_shapes(0.5)
        self.renderer = MyCardMainFrameRenderer(self.domain_scene, self)

    def initgl(self):
        GL.glClearColor(0.8706, 0.7216, 0.5294, 0)
        GL.glEnable(GL.GL_BLEND)
        GL.glBlendFunc(GL.GL_SRC_ALPHA, GL.GL_ONE_MINUS_SRC_ALPHA)
        GL.glLoadIdentity()
        GLU.gluOrtho2D(0, self.width, self.height, 0)
        # GLUT.glutInit()

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

    def init_shapes(self, alpha):
        alpha_background_frame = AlphaRectangle(width=self.width, height=self.height)
        alpha_background_frame.set_background_alpha(alpha)
        #alpha_background_frame.is_visible = False
        self.domain_scene.add_shape(alpha_background_frame)
        print("검정색 배경 적용 되었니?")


    def apply_translation(self, translation):
        for shape, shape_translation in zip(self.domain_scene.shapes, self.domain_scene.translations):
            print("shape translate")
            shape.local_translate(translation)


    # def toggle_visibility(self):
    #     alpha_background_frame = self.domain_scene.shapes[0]
    #
    #     if alpha_background_frame.is_visible:
    #         alpha_background_frame.set_visible(True)
    #
    #     self.redraw()
    def toggle_visibility(self):
        alpha_background_frame = self.domain_scene.shapes[0]
        alpha_background_frame.is_visible = not alpha_background_frame.is_visible
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

    def redraw(self):
        self.apply_translation((0, 0))
        self.renderer.render()

