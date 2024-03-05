import tkinter
import unittest

from OpenGL.GL import *
from OpenGL.GLU import *
from pyopengltk import OpenGLFrame

from battle_field.infra.legacy.circle_image_legacy_your_hand_repository import CircleImageLegacyYourHandRepository
from battle_field_muligun.entity.scene.battle_field_muligun_scene import BattleFieldMuligunScene
from initializer.init_domain import DomainInitializer
from opengl_rectangle_lightning_border.lightning_border import LightningBorder


class PreDrawedBattleFieldFrameRefactor(OpenGLFrame):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)

        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        self.width = screen_width
        self.height = screen_height

        self.click_card_effect_rectangle = None
        self.selected_object = None
        self.prev_selected_object = None
        self.drag_start = None

        self.click_card_effect_rectangles = []
        self.selected_objects = []
        self.checking_draw_effect = {}

        self.lightning_border = LightningBorder()

        self.battle_field_muligun_scene = BattleFieldMuligunScene()
        self.battle_field_muligun_scene.create_battle_field_muligun_scene(self.width, self.height)
        self.battle_field_muligun_background_shape_list = self.battle_field_muligun_scene.get_battle_field_muligun_background()

        self.your_hand_repository = CircleImageLegacyYourHandRepository.getInstance()
        self.your_hand_repository.save_current_hand_state([6, 8, 19, 20, 151])
        self.your_hand_repository.create_hand_card_list_muligun()

        self.hand_card_list = self.your_hand_repository.get_current_hand_card_list()

        self.bind("<Configure>", self.on_resize)

    def initgl(self):
        glClearColor(1.0, 1.0, 1.0, 0.0)
        glOrtho(0, self.width, self.height, 0, -1, 1)

        self.tkMakeCurrent()

    def reshape(self, width, height):
        print(f"Reshaping window to width={width}, height={height}")
        glViewport(0, 0, width, height)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluOrtho2D(0, width, height, 0)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

    def on_resize(self, event):
        self.reshape(event.width, event.height)

    def draw_base(self):
        for battle_field_muligun_background_shape in self.battle_field_muligun_background_shape_list:
            battle_field_muligun_background_shape.draw()

    def redraw(self):
        self.tkMakeCurrent()
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

        self.draw_base()

        glDisable(GL_BLEND)

        for hand_card in self.hand_card_list:
            attached_tool_card = hand_card.get_tool_card()
            if attached_tool_card is not None:
                attached_tool_card.draw()

            pickable_card_base = hand_card.get_pickable_card_base()
            pickable_card_base.draw()

            attached_shape_list = pickable_card_base.get_attached_shapes()

            for attached_shape in attached_shape_list:
                attached_shape.draw()

        self.tkSwapBuffers()

class TestDrawBattleFieldMuligunWithNewBackground(unittest.TestCase):

    def test_draw_battle_field_muligun_with_new_background(self):
        DomainInitializer.initEachDomain()

        root = tkinter.Tk()
        root.geometry(f"{root.winfo_screenwidth()}x{root.winfo_screenheight()}-0-0")
        root.deiconify()

        pre_drawed_battle_field_frame = PreDrawedBattleFieldFrameRefactor(root)
        pre_drawed_battle_field_frame.pack(fill=tkinter.BOTH, expand=1)
        root.update_idletasks()

        def animate():
            pre_drawed_battle_field_frame.redraw()
            root.after(17, animate)
            # root.after(33, animate)

        root.after(0, animate)

        root.mainloop()


if __name__ == '__main__':
    unittest.main()
