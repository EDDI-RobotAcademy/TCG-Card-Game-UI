import os

from pyopengltk import OpenGLFrame
from OpenGL import GL, GLU

from common.utility import get_project_root
from opengl_battle_field.entity.battle_field import BattleField
from opengl_battle_field.renderer.battle_field_frame_renderer import BattleFieldFrameRenderer
from opengl_battle_field_panel.battle_field_panel import BattleFieldPanel
from opengl_battle_field_unit.unit_card import UnitCard
from opengl_card_deck.card_deck import CardDeck
from opengl_tomb.tomb import Tomb
from tests.ugly_test_card.opengl_battle_field_card.card import Card


class BattleFieldFrame(OpenGLFrame):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self.battle_field = BattleField()

        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        self.width = screen_width
        self.height = screen_height

        self.bind("<Configure>", self.on_resize)

        self.make_battle_field()

        project_root = get_project_root()
        print("프로젝트 최상위:", project_root)

        self.renderer = BattleFieldFrameRenderer(self.battle_field, self)

    def make_battle_field(self):
        project_root = get_project_root()

        # opponent_tomb = Tomb()
        # opponent_tomb.init_shapes(os.path.join(project_root, "local_storage", "image", "battle_field", "tomb.jpeg"))
        # self.battle_field.add_tomb(opponent_tomb)
        #
        # your_tomb = Tomb(local_translation=(1670, 780))
        # your_tomb.init_shapes(os.path.join(project_root, "local_storage", "image", "battle_field", "tomb.jpeg"))
        # self.battle_field.add_tomb(your_tomb)
        #
        # opponent_card_deck = CardDeck()
        # opponent_card_deck.init_shapes(os.path.join(project_root, "local_storage", "image", "battle_field", "opponent_card_deck.png"),
        #                                os.path.join(project_root, "local_storage", "image", "battle_field", "opponent_card_deck.png"),
        #                                os.path.join(project_root, "local_storage", "image", "battle_field", "opponent_card_deck.png"),
        #                                os.path.join(project_root, "local_storage", "image", "battle_field", "opponent_card_deck.png"),
        #                                os.path.join(project_root, "local_storage", "image", "battle_field", "opponent_card_deck.png"))
        # self.battle_field.add_card_deck(opponent_card_deck)
        #
        # your_card_deck = CardDeck(local_translation=(1650, 320))
        # your_card_deck.init_shapes(
        #     os.path.join(project_root, "local_storage", "image", "battle_field", "your_card_deck.png"),
        #     os.path.join(project_root, "local_storage", "image", "battle_field", "your_card_deck.png"),
        #     os.path.join(project_root, "local_storage", "image", "battle_field", "your_card_deck.png"),
        #     os.path.join(project_root, "local_storage", "image", "battle_field", "your_card_deck.png"),
        #     os.path.join(project_root, "local_storage", "image", "battle_field", "your_card_deck.png"))
        # self.battle_field.add_card_deck(your_card_deck)
        #
        # battle_field_panel = BattleFieldPanel()
        # battle_field_panel.init_shapes(os.path.join(project_root, "local_storage", "image", "battle_field", "battle_field_panel.jpeg"))
        # self.battle_field.add_battle_field_panel(battle_field_panel)


        first_unit = UnitCard()
        first_unit.init_shapes(os.path.join(project_root, "local_storage", "card_images", "card1.png"))

        second_unit = Card(local_translation=(500, 0))
        second_unit.init_shapes(os.path.join(project_root, "local_storage", "card_images", "card2.png"))

        self.battle_field.add_unit_card(first_unit)
        self.battle_field.add_unit_card(second_unit)


    def apply_global_translation(self, translation):
        unit_card_list = self.battle_field.get_unit_card()
        for unit_card in unit_card_list:
            unit_shapes = unit_card.get_unit_shapes()
            for shape in unit_shapes:
                print("apply_global_translation")
                shape.global_translate(translation)


    def summon_units(self):
        project_root = get_project_root()
        unitList = self.battle_field.get_unit_card()
        unitCount = len(unitList)
        print(f"unitList : {unitList}")

        if unitCount > 2:
            placeX = 500 * (unitCount) * 3/(unitCount)
            #placeX = 1500.0
            self.resize_units()
            summon_unit = UnitCard(local_translation=(placeX, 0))
            summon_unit.init_shapes(
                os.path.join(project_root, "local_storage", "card_images", f"card{unitCount + 1}.png"))
            self.battle_field.add_unit_card(summon_unit)
            summon_unit.redraw_shapes_with_scale(unitCount)

        else:
            placeX = 500 * (unitCount)
            summon_unit = UnitCard(local_translation=(placeX, 0))
            summon_unit.init_shapes(
                os.path.join(project_root, "local_storage", "card_images", f"card{unitCount + 1}.png"))
            self.battle_field.add_unit_card(summon_unit)



    def resize_units(self):
        unitList = self.battle_field.get_unit_card()

        unitCount = len(unitList).__float__()
        print(f"unitCount : {unitCount}")

        for unit in unitList:
            unit.redraw_shapes_with_scale(unitCount)



    def initgl(self):
        GL.glClearColor(1.0, 1.0, 1.0, 0.0)
        GL.glOrtho(0, self.width, self.height, 0, -1, 1)

    def toggle_visibility(self):
        unit_card_list = self.battle_field.get_unit_card()
        for unit_card in unit_card_list:
            unit_shapes = unit_card.get_unit_shapes()

            attached_tool_card = unit_shapes[0]
            attached_tool_card.set_visible(not attached_tool_card.get_visible())

            equipped_mark = unit_shapes[3]
            equipped_mark.set_visible(not equipped_mark.get_visible())

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
        self.apply_global_translation((50, 50))
        self.tkSwapBuffers()
        self.after(100, self.renderer.render)