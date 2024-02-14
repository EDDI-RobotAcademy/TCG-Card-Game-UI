import os
import tkinter

from pyopengltk import OpenGLFrame
from OpenGL import GL, GLU

from common.card_type import CardType
from common.utility import get_project_root
from opengl_battle_field.entity.battle_field import BattleField
from opengl_battle_field.renderer.battle_field_frame_renderer import BattleFieldFrameRenderer
from opengl_battle_field_panel.battle_field_panel import BattleFieldPanel
from opengl_battle_field_unit.unit_card import UnitCard
from opengl_battle_field_card.card import Card
from opengl_card_deck.card_deck import CardDeck
from opengl_energy_field.energy_field import EnergyField
from opengl_environment.environment import Environment
from opengl_field.field import Field
from opengl_hand_deck_card.hand_deck_card import HandDeckCard
from opengl_hand_deck_panel.hand_deck_panel import HandDeckPanel
from opengl_lost_zone.lost_zone import LostZone
from opengl_main_character.main_character import MainCharacter
from opengl_pickable_shape.pickable_rectangle import PickableRectangle
from opengl_tomb.tomb import Tomb
from opengl_trap.trap import Trap


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

        self.drag_start = None
        # self.bind("<B1-Motion>", self.on_canvas_drag)
        self.bind("<ButtonRelease-1>", self.on_canvas_release)
        self.bind("<Button-1>", self.click_event_on_hand_deck_card)
        self.bind("<Configure>", self.on_resize)

        self.selected_count = 0
        self.selected_object = None
        self.selected_target = None
        self.use_table = {CardType.UNIT: self.use_unit_card,
                     CardType.ENERGY: self.use_energy_card,
                     CardType.TOOL: self.use_tool_card,
                     CardType.TRAP: self.use_trap_card,
                     CardType.SUPPORT: self.use_support_card}

    def make_battle_field(self):
        project_root = get_project_root()

        battle_field_panel = BattleFieldPanel()
        battle_field_panel.init_shapes()
        self.battle_field.add_battle_field_panel(battle_field_panel)

        opponent_tomb = Tomb()
        opponent_tomb.init_shapes()
        self.battle_field.add_tomb(opponent_tomb)

        your_tomb = Tomb(local_translation=(1670, 780))
        your_tomb.init_shapes()
        self.battle_field.add_tomb(your_tomb)

        opponent_card_deck = CardDeck()
        opponent_card_deck.init_opponent_shapes()
        self.battle_field.add_card_deck(opponent_card_deck)

        your_card_deck = CardDeck()
        your_card_deck.init_your_shapes()
        self.battle_field.add_card_deck(your_card_deck)

        opponent_trap = Trap()
        opponent_trap.init_shapes()
        self.battle_field.add_trap(opponent_trap)

        your_trap = Trap(local_translation=(-1040, 480))
        your_trap.init_shapes()
        self.battle_field.add_trap(your_trap)

        opponent_lost_zone = LostZone()
        opponent_lost_zone.init_shapes()
        self.battle_field.add_lost_zone(opponent_lost_zone)

        your_lost_zone = LostZone(local_translation=(-1620, 300))
        your_lost_zone.init_shapes()
        self.battle_field.add_lost_zone(your_lost_zone)

        environment = Environment()
        environment.init_shapes()
        self.battle_field.add_environment(environment)

        energy_field = EnergyField()
        energy_field.init_shapes()
        self.battle_field.add_energy_field(energy_field)

        opponent_main_character = MainCharacter()
        opponent_main_character.init_opponent_main_character_shapes()
        self.battle_field.add_main_character(opponent_main_character)

        your_main_character = MainCharacter()
        your_main_character.init_your_main_character_shapes()
        self.battle_field.add_main_character(your_main_character)

        your_hand_deck_panel = HandDeckPanel(window=self, battle_field=self.battle_field)
        your_hand_deck_panel.init_shapes()
        self.battle_field.add_pickable_hand_deck_panel_base(your_hand_deck_panel)

        your_field = Field()
        your_field.init_shapes()
        self.battle_field.add_pickable_field_base(your_field)

        hand_deck_card = HandDeckCard(window=self, battle_field=self.battle_field, local_translation=(500, 500), card_type=CardType.UNIT)
        hand_deck_card.init_hand_deck_card(2)
        self.battle_field.add_pickable_hand_deck_card_base(hand_deck_card)

        # first_unit = UnitCard()
        # first_unit.init_shapes(os.path.join(project_root, "local_storage", "card_images", "card1.png"))
        # self.battle_field.add_unit_card(first_unit)

        # second_unit = Card(local_translation=(500, 500))
        # second_unit.init_card(2)
        # self.battle_field.add_pickable_card_base(second_unit)
        # print(f"second_unit{second_unit}")

    def apply_global_translation(self, translation):
        card_list = self.battle_field.get_pickable_hand_deck_card_base()
        for card in card_list:
            card_shapes = card.get_get_pickable_hand_deck_card_base_shapes()
            for shape in card_shapes:
                print("apply_global_translation")
                shape.global_translate(translation)

    # def summon_units(self):
    #     project_root = get_project_root()
    #     unitList = self.battle_field.get_unit_card()
    #     unitCount = len(unitList)
    #     print(f"unitList : {unitList}")
    #
    #     if unitCount > 2:
    #         placeX = 500 * (unitCount) * 3/(unitCount)
    #         #placeX = 1500.0
    #         self.resize_units()
    #         summon_unit = UnitCard(local_translation=(placeX, 0))
    #         summon_unit.init_shapes(
    #             os.path.join(project_root, "local_storage", "card_images", f"card{unitCount + 1}.png"))
    #         self.battle_field.add_unit_card(summon_unit)
    #         summon_unit.redraw_shapes_with_scale(unitCount)
    #
    #     else:
    #         placeX = 500 * (unitCount)
    #         summon_unit = UnitCard(local_translation=(placeX, 0))
    #         summon_unit.init_shapes(
    #             os.path.join(project_root, "local_storage", "card_images", f"card{unitCount + 1}.png"))
    #         self.battle_field.add_unit_card(summon_unit)

    def draw_cards(self):
        project_root = get_project_root()
        handDeckCardList = self.battle_field.get_pickable_hand_deck_card_base()
        handDeckCardCount = len(handDeckCardList)

        if handDeckCardCount > 10:
            # placeX = 200 * (handDeckCount) * 3/(handDeckCount)
            placeX = 200 * (handDeckCardCount)
            draw_card = handDeckCardList(local_translation=(placeX, 0), window=self, battle_field=self.battle_field)
            draw_card.init_shapes(5)
            self.battle_field.add_pickable_hand_deck_card_base(draw_card)
            print(f"{self.battle_field.add_pickable_hand_deck_card_base(draw_card)}")

        else:
            placeX = 200 * (handDeckCardCount)
            draw_card = HandDeckCard(local_translation=(placeX, 0), window=self, battle_field=self.battle_field)
            draw_card.init_hand_deck_card(5)
            self.battle_field.add_pickable_hand_deck_card_base(draw_card)

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
    def click_event_on_hand_deck_card(self, event):
        print(f"on_canvas_click: {event}")
        try:
            x, y = event.x, event.y
            y = self.winfo_reqheight() - y

            for hand_deck_card in self.battle_field.get_pickable_hand_deck_card_base():
                 if isinstance(hand_deck_card, HandDeckCard):
                    hand_deck_card.selected = False

            for field in self.battle_field.get_pickable_field_base():
                if isinstance(field, Field):
                    field.selected = False

            for card in reversed(self.battle_field.get_pickable_hand_deck_card_base()):
                composition_shape_list = card.get_get_pickable_hand_deck_card_base_shapes()
                for shape in composition_shape_list:
                    if isinstance(shape, PickableRectangle) and shape.is_point_inside((x, y)):
                        card.selected = not card.selected
                        if self.selected_object == card:
                            self.selected_object = None
                            self.master.title(f"unselected object: {card}")
                        elif self.selected_object == None:
                            if card.is_hand or card.card_type == CardType.UNIT:
                                self.selected_object = card
                                self.master.title(f"new selected {card.card_type} object: {card}")
                        elif self.selected_object.card_type == CardType.ENERGY or self.selected_object.card_type == CardType.TOOL:
                            self.selected_target = card
                            self.master.title(f"selected {card.card_type} target: {card}")
                        break

            for field in reversed(self.battle_field.get_pickable_field_base()):
                composition_shape_list = field.get_field_shapes()
                for shape in composition_shape_list:
                    if (self.selected_object is not None and isinstance(shape, PickableRectangle)
                            and shape.is_point_inside((x, y))):
                        if self.selected_object.is_hand:
                            self.use_table[self.selected_object.card_type](self.selected_object)


                        else:
                            if self.selected_object.card_type == CardType.UNIT:
                                # Todo : 필드의 카드를 클릭하면, 유닛의 사망처리에 관련된 UI기능이 호출됨
                                self.selected_object.move_to_tomb()
                                self.selected_count -= 1
                                self.master.title(f"Unit destroyed!!")
                                self.battle_field.unit_in_field.remove(self.selected_object)
                                for i, unit in enumerate(self.battle_field.unit_in_field):
                                    unit.local_translation = (i * 120, 0)
                                    unit.move_to_field(150, 325)

                        self.selected_object = None

                        break

            self.redraw()
        except Exception as e:
            print(f"Exception in on_canvas_click: {e}")
    def on_canvas_release(self, event):
        self.drag_start = None
    def use_unit_card(self, selected_object):
        selected_object.local_translation = (self.selected_count * 120, 0)
        selected_object.move_to_field(150, 325)
        self.battle_field.unit_in_field.append(selected_object)
        self.master.title(f"use Unit Card!! : {self.battle_field.unit_in_field}")
        self.selected_count += 1
    def use_tool_card(self, selected_object):
        if self.selected_target.card_type == CardType.UNIT:
            self.selected_target.equip_tool()
            selected_object.move_to_tomb()
            self.selected_target = None
            self.master.title(f"use Tool Card!! : {selected_object}")
        else:
            self.master.title(f"Wrong Target! {selected_object.card_type}")
            self.selected_object = None
            self.selected_target = None
    def use_support_card(self, selected_object):
        selected_object.move_to_tomb()
        self.master.title(f"use Support Card!! : {selected_object}")
        #Todo : 서포트 카드 사용에 따른 효과를 쓰면됩니다.
    def use_trap_card(self, selected_object):
        selected_object.local_translation = (0, 0)
        selected_object.move_to_field(1000, 325)
        self.master.title(f"use Trap Card!! : {selected_object}")
    def use_energy_card(self, selected_object):
        if self.selected_target.card_type == CardType.UNIT:
            selected_object.move_to_tomb()
            self.master.title(f"use Energy Card!! : {selected_object}")
            self.selected_target.set_energy()
            self.selected_target = None
        else:
            self.master.title(f"Wrong Target! {selected_object.card_type}")
            self.selected_object = None
            self.selected_target = None
