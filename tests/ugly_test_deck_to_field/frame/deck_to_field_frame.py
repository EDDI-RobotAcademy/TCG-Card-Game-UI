from OpenGL import GL
from OpenGL.GLU.tess import GLU
from pyopengltk import OpenGLFrame

from common.utility import get_project_root
from tests.ugly_test_deck_to_field.card.test_card import TestCard
from tests.ugly_test_deck_to_field.entity.deck_to_field import DeckToField
from tests.ugly_test_deck_to_field.field.test_field import TestField
from tests.ugly_test_deck_to_field.render.deck_to_field_renderer import DeckToFieldRenderer


class DeckToFieldFrame(OpenGLFrame):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self.deck_to_field = DeckToField()

        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        self.width = screen_width
        self.height = screen_height

        self.make_battle_field()

        project_root = get_project_root()
        print("프로젝트 최상위:", project_root)

        self.renderer = DeckToFieldRenderer(self.deck_to_field, self)

    def make_battle_field(self):
        project_root = get_project_root()

        card = TestCard(project_root, self)
        card.init_shapes()
        self.deck_to_field.add_card(card)

        field = TestField()
        field.init_shapes()
        self.deck_to_field.add_field(field)

    def initgl(self):
        GL.glClearColor(1.0, 1.0, 1.0, 0.0)
        GL.glOrtho(0, self.width, self.height, 0, -1, 1)

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
        # self.apply_global_translation((50, 50))
        self.tkSwapBuffers()
        self.after(100, self.renderer.render)