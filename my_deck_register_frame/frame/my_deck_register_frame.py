from OpenGL import GL
from OpenGL.GLU.tess import GLU
from pyopengltk import OpenGLFrame

from my_deck_register_frame.entity.my_deck_register_scene import MyDeckRegisterScene
from my_deck_register_frame.renderer.my_deck_register_frame_renderer import MyDeckRegisterFrameRenderer
from opengl_shape.rectangle import Rectangle


class MyDeckRegisterFrame(OpenGLFrame):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self.domain_scene = MyDeckRegisterScene()

        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        self.width = screen_width
        self.height = screen_height

        self.bind("<Configure>", self.on_resize)

        self.init_shapes()

        self.renderer = MyDeckRegisterFrameRenderer(self.domain_scene, self)


    def init_shapes(self):
        my_deck_register_frame = Rectangle(
            color=(0.6, 0.4, 0.6, 1.0),
            vertices=[(0, 0), (600, 0), (600, 260), (0, 260)],
            local_translation=(20, 20))
        self.domain_scene.add_shape(my_deck_register_frame)
        my_deck_register_frame.set_visible(False)

    # def apply_translation(self, translation):
    #     for shape in self.domain_scene.shapes:
    #         print("shape translate")
    #         shape.translate(translation)

    def apply_translation(self, translation):
        for shape, shape_translation in zip(self.domain_scene.shapes, self.domain_scene.translations):
            print("shape translate")
            shape.local_translate(translation)

    def initgl(self):
        GL.glClearColor(0.8706, 0.7216, 0.5294, 0)
        GL.glOrtho(0, self.width, self.height, 0, -1, 1)

    # def toggle_visibility(self):
    #     my_deck_register_frame = self.domain_scene.shapes[0]
    #     my_deck_register_frame.set_visible(not my_deck_register_frame.get_visible())
    #
    #     self.redraw()

    def toggle_visibility(self):
        my_deck_register_frame = self.domain_scene.shapes[0]
        current_visibility = my_deck_register_frame.get_visible()

        if not current_visibility:
            self.domain_scene.add_shape(my_deck_register_frame)

        my_deck_register_frame.set_visible(not current_visibility)

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
        self.apply_translation((600, 300))
        self.renderer.render()

