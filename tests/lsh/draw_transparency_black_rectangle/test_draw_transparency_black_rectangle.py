from battle_field.entity.battle_field_scene import BattleFieldScene

import tkinter
import unittest

from OpenGL.GL import *
from OpenGL.GLU import *
from pyopengltk import OpenGLFrame

from battle_field.infra.your_field_unit_repository import YourFieldUnitRepository
from battle_field.infra.your_hand_repository import YourHandRepository
from battle_field.infra.your_tomb_repository import YourTombRepository
from battle_field_fixed_card.fixed_field_card import FixedFieldCard
from card_info_from_csv.repository.card_info_from_csv_repository_impl import CardInfoFromCsvRepositoryImpl
from common.card_type import CardType
from image_shape.circle_image import CircleImage
from initializer.init_domain import DomainInitializer
from opengl_battle_field_pickable_card.pickable_card import PickableCard
from opengl_rectangle_lightning_border.lightning_border import LightningBorder
from opengl_shape.rectangle import Rectangle


class PreDrawedBattleFieldFrameRefactor(OpenGLFrame):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)

        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        self.width = screen_width
        self.height = screen_height

        self.active_panel_rectangle = None
        self.selected_object = None
        self.prev_selected_object = None
        self.drag_start = None

        self.active_panel_rectangle = []

        self.lightning_border = LightningBorder()

        self.battle_field_scene = BattleFieldScene()
        self.battle_field_scene.create_battle_field_scene()

        self.opponent_tomb_shapes = self.battle_field_scene.get_opponent_tomb()
        self.opponent_lost_zone_shapes = self.battle_field_scene.get_opponent_lost_zone()
        self.opponent_trap_shapes = self.battle_field_scene.get_opponent_trap()
        self.opponent_deck_shapes = self.battle_field_scene.get_opponent_deck()
        self.opponent_main_character_shapes = self.battle_field_scene.get_opponent_main_character()
        self.opponent_hand_panel_shapes = self.battle_field_scene.get_opponent_hand_panel()
        self.opponent_unit_field_shapes = self.battle_field_scene.get_opponent_unit_field()

        self.your_tomb_shapes = self.battle_field_scene.get_your_tomb()
        self.your_lost_zone_shapes = self.battle_field_scene.get_your_lost_zone()
        self.your_trap_shapes = self.battle_field_scene.get_your_trap()
        self.your_deck_shapes = self.battle_field_scene.get_your_deck()
        self.your_main_character_shapes = self.battle_field_scene.get_your_main_character()
        self.your_hand_panel_shapes = self.battle_field_scene.get_your_hand_panel()
        self.your_unit_field_shapes = self.battle_field_scene.get_your_unit_field()

        self.battle_field_environment_shapes = self.battle_field_scene.get_battle_field_environment()

        self.your_hand_repository = YourHandRepository.getInstance()
        self.your_hand_repository.save_current_hand_state([8, 19, 151, 2, 9, 20, 30, 36])
        self.your_hand_repository.create_hand_card_list()

        self.hand_card_list = self.your_hand_repository.get_current_hand_card_list()

        self.your_field_unit_repository = YourFieldUnitRepository.getInstance()

        self.your_tomb_repository = YourTombRepository.getInstance()
        # TODO: Naming Issue
        self.card_info = CardInfoFromCsvRepositoryImpl.getInstance()

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


    def redraw(self):
        self.tkMakeCurrent()
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

        glColor4f(0.0, 0.0, 0.0, 0.5)  # Black color with 50% transparency
        glBegin(GL_QUADS)
        glVertex2f(100, 400)
        glVertex2f(400, 400)
        glVertex2f(400, 100)
        glVertex2f(100, 100)
        glEnd()

        self.tkSwapBuffers()


class TestDrawTransparencyBlackRectangle(unittest.TestCase):

    def test_draw_transparency_black_rectangle(self):
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

        root.after(0, animate)

        root.mainloop()


if __name__ == '__main__':
    unittest.main()
