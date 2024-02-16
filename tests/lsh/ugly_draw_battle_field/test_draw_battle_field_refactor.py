from battle_field.entity.battle_field_environment import BattleFieldEnvironment
from battle_field.entity.opponent_deck import OpponentDeck
from battle_field.entity.opponent_hand_panel import OpponentHandPanel
from battle_field.entity.opponent_lost_zone import OpponentLostZone
from battle_field.entity.opponent_main_character import OpponentMainCharacter
from battle_field.entity.opponent_tomb import OpponentTomb
from battle_field.entity.opponent_trap import OpponentTrap
from battle_field.entity.opponent_unit_field import OpponentUnitField
from battle_field.entity.your_deck import YourDeck
from battle_field.entity.your_hand_panel import YourHandPanel
from battle_field.entity.your_lost_zone import YourLostZone
from battle_field.entity.your_main_character import YourMainCharacter
from battle_field.entity.your_tomb import YourTomb
from battle_field.entity.your_trap import YourTrap
from battle_field.entity.your_unit_field import YourUnitField

import tkinter
import unittest

from OpenGL.GL import *
from OpenGL.GLU import *
from pyopengltk import OpenGLFrame


class PreDrawedBattleFieldFrameRefactor(OpenGLFrame):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)

        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        self.width = screen_width
        self.height = screen_height

        self.opponent_tomb = OpponentTomb()
        self.opponent_tomb.init_shapes()
        self.opponent_tomb_shapes = self.opponent_tomb.get_tomb_shapes()

        self.opponent_lost_zone = OpponentLostZone()
        self.opponent_lost_zone.init_shapes()
        self.opponent_lost_zone_shapes = self.opponent_lost_zone.get_lost_zone_shapes()

        self.opponent_trap = OpponentTrap()
        self.opponent_trap.init_shapes()
        self.opponent_trap_shapes = self.opponent_trap.get_trap_shapes()

        self.opponent_card_deck = OpponentDeck()
        self.opponent_card_deck.init_shapes()
        self.opponent_card_deck_shapes = self.opponent_card_deck.get_opponent_card_deck_shapes()

        self.opponent_main_character = OpponentMainCharacter()
        self.opponent_main_character.init_opponent_main_character_shapes()
        self.opponent_main_character_shapes = self.opponent_main_character.get_main_character_shapes()

        self.opponent_hand_panel = OpponentHandPanel()
        self.opponent_hand_panel.init_shapes()
        self.opponent_hand_panel_shapes = self.opponent_hand_panel.get_opponent_hand_panel_shapes()

        self.opponent_unit_field = OpponentUnitField()
        self.opponent_unit_field.init_shapes()
        self.opponent_unit_field_shapes = self.opponent_unit_field.get_opponent_unit_field_shapes()

        self.your_tomb = YourTomb()
        self.your_tomb.init_shapes()
        self.your_tomb_shapes = self.your_tomb.get_tomb_shapes()

        self.your_lost_zone = YourLostZone()
        self.your_lost_zone.init_shapes()
        self.your_lost_zone_shapes = self.your_lost_zone.get_lost_zone_shapes()

        self.your_trap = YourTrap()
        self.your_trap.init_shapes()
        self.your_trap_shapes = self.your_trap.get_trap_shapes()

        self.your_card_deck = YourDeck()
        self.your_card_deck.init_shapes()
        self.your_card_deck_shapes = self.your_card_deck.get_your_card_deck_shapes()

        self.your_main_character = YourMainCharacter()
        self.your_main_character.init_your_main_character_shapes()
        self.your_main_character_shapes = self.your_main_character.get_main_character_shapes()

        self.your_hand_panel = YourHandPanel()
        self.your_hand_panel.init_shapes()
        self.your_hand_panel_shapes = self.your_hand_panel.get_your_hand_panel_shapes()

        self.your_unit_field = YourUnitField()
        self.your_unit_field.init_shapes()
        self.your_unit_field_shapes = self.your_unit_field.get_your_unit_field_shapes()

        self.battle_field_environment = BattleFieldEnvironment()
        self.battle_field_environment.init_shapes()
        self.battle_field_environment_shapes = self.battle_field_environment.get_environment_shapes()

        self.bind("<Configure>", self.on_resize)

    def initgl(self):
        glClearColor(1.0, 1.0, 1.0, 0.0)
        glOrtho(0, self.width, self.height, 0, -1, 1)

        self.tkMakeCurrent()
        # glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        #
        # for opponent_tomb_shape in self.opponent_tomb_shapes:
        #     opponent_tomb_shape.draw()
        #
        # for opponent_lost_zone_shape in self.opponent_lost_zone_shapes:
        #     opponent_lost_zone_shape.draw()
        #
        # for opponent_trap_shape in self.opponent_trap_shapes:
        #     opponent_trap_shape.draw()
        #
        # for opponent_card_deck_shape in self.opponent_card_deck_shapes:
        #     opponent_card_deck_shape.draw()
        #
        # for opponent_main_character_shape in self.opponent_main_character_shapes:
        #     opponent_main_character_shape.draw()
        #
        # for opponent_hand_panel_shape in self.opponent_hand_panel_shapes:
        #     opponent_hand_panel_shape.draw()
        #
        # for opponent_unit_field_shape in self.opponent_unit_field_shapes:
        #     opponent_unit_field_shape.draw()
        #
        # for your_tomb_shape in self.your_tomb_shapes:
        #     your_tomb_shape.draw()
        #
        # for your_lost_zone_shape in self.your_lost_zone_shapes:
        #     your_lost_zone_shape.draw()
        #
        # for your_trap_shape in self.your_trap_shapes:
        #     your_trap_shape.draw()
        #
        # for your_card_deck_shape in self.your_card_deck_shapes:
        #     your_card_deck_shape.draw()
        #
        # for your_main_character_shape in self.your_main_character_shapes:
        #     your_main_character_shape.draw()
        #
        # for your_hand_panel_shape in self.your_hand_panel_shapes:
        #     your_hand_panel_shape.draw()
        #
        # for your_unit_field_shape in self.your_unit_field_shapes:
        #     your_unit_field_shape.draw()
        #
        # for battle_field_environment_shape in self.battle_field_environment_shapes:
        #     battle_field_environment_shape.draw()
        #
        # self.tkSwapBuffers()

    def reshape(self, width, height):
        print(f"Reshaping window to width={width}, height={height}")
        glViewport(0, 0, width, height)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluOrtho2D(0, width, height, 0)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

    def on_resize(self, event):
        print("Handling resize event")
        self.reshape(event.width, event.height)

    def redraw(self):
        # self.tkMakeCurrent()
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        for opponent_tomb_shape in self.opponent_tomb_shapes:
            opponent_tomb_shape.draw()

        for opponent_lost_zone_shape in self.opponent_lost_zone_shapes:
            opponent_lost_zone_shape.draw()

        for opponent_trap_shape in self.opponent_trap_shapes:
            opponent_trap_shape.draw()

        for opponent_card_deck_shape in self.opponent_card_deck_shapes:
            opponent_card_deck_shape.draw()

        for opponent_main_character_shape in self.opponent_main_character_shapes:
            opponent_main_character_shape.draw()

        for opponent_hand_panel_shape in self.opponent_hand_panel_shapes:
            opponent_hand_panel_shape.draw()

        for opponent_unit_field_shape in self.opponent_unit_field_shapes:
            opponent_unit_field_shape.draw()

        for your_tomb_shape in self.your_tomb_shapes:
            your_tomb_shape.draw()

        for your_lost_zone_shape in self.your_lost_zone_shapes:
            your_lost_zone_shape.draw()

        for your_trap_shape in self.your_trap_shapes:
            your_trap_shape.draw()

        for your_card_deck_shape in self.your_card_deck_shapes:
            your_card_deck_shape.draw()

        for your_main_character_shape in self.your_main_character_shapes:
            your_main_character_shape.draw()

        for your_hand_panel_shape in self.your_hand_panel_shapes:
            your_hand_panel_shape.draw()

        for your_unit_field_shape in self.your_unit_field_shapes:
            your_unit_field_shape.draw()

        for battle_field_environment_shape in self.battle_field_environment_shapes:
            battle_field_environment_shape.draw()

        self.tkSwapBuffers()



class TestDrawBattleFieldRefactor(unittest.TestCase):

    def test_draw_battle_field_refactor(self):
        root = tkinter.Tk()
        root.geometry(f"{root.winfo_screenwidth()}x{root.winfo_screenheight()}-0-0")
        root.deiconify()

        pre_drawed_battle_field_frame = PreDrawedBattleFieldFrameRefactor(root)
        pre_drawed_battle_field_frame.pack(fill=tkinter.BOTH, expand=1)
        root.update_idletasks()

        def animate():
            pre_drawed_battle_field_frame.redraw()
            # root.after(17, animate)
            root.after(33, animate)

        root.after(0, animate)

        root.mainloop()


if __name__ == '__main__':
    unittest.main()
