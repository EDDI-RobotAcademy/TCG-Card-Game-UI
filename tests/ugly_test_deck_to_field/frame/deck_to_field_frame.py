from OpenGL import GL
from OpenGL.GLU.tess import GLU
from pyopengltk import OpenGLFrame

from common.card_type import CardType
from common.utility import get_project_root
from opengl_shape.rectangle import Rectangle
from tests.ugly_test_deck_to_field.card.test_card import TestCard
from tests.ugly_test_deck_to_field.entity.deck_to_field import DeckToField
from tests.ugly_test_deck_to_field.field.test_field import TestField
from tests.ugly_test_deck_to_field.render.deck_to_field_renderer import DeckToFieldRenderer
from opengl_pickable_shape.pickable_rectangle import PickableRectangle


class DeckToFieldFrame(OpenGLFrame):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self.deck_to_field = DeckToField()
        self.selected_object = None
        self.selected_count = 0
        self.selected_target = None

        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        self.width = screen_width
        self.height = screen_height

        self.make_battle_field()

        project_root = get_project_root()
        print("프로젝트 최상위:", project_root)

        self.renderer = DeckToFieldRenderer(self.deck_to_field, self)

        self.use_table = {CardType.UNIT: self.use_unit_card,
                     CardType.ENERGY: self.use_energy_card,
                     CardType.TOOL: self.use_tool_card,
                     CardType.TRAP: self.use_trap_card,
                     CardType.SUPPORT: self.use_support_card}

        self.bind("<Button-1>", self.clickEvent)

    def make_battle_field(self):
        project_root = get_project_root()

        card1 = TestCard(project_root, self, local_translation=(0,0), card_type=CardType.UNIT)
        card1.init_shapes()
        self.deck_to_field.add_card(card1)

        card2 = TestCard(project_root, self, local_translation=(120, 0), color=(1, 0, 0, 1), card_type=CardType.ENERGY)
        card2.init_shapes()
        self.deck_to_field.add_card(card2)

        card3 = TestCard(project_root, self, local_translation=(240, 0), color=(0, 1, 0, 1), card_type=CardType.SUPPORT)
        card3.init_shapes()
        self.deck_to_field.add_card(card3)

        card4 = TestCard(project_root, self, local_translation=(360, 0), color=(0, 0, 1, 1), card_type=CardType.TRAP)
        card4.init_shapes()
        self.deck_to_field.add_card(card4)

        card5 = TestCard(project_root, self, local_translation=(480, 0), color=(0.5, 0.5, 0, 1), card_type=CardType.TOOL)
        card5.init_shapes()
        self.deck_to_field.add_card(card5)

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

    def clickEvent(self, event):

        try:
            x, y = event.x, event.y
            y = self.winfo_reqheight() - y

            for card in self.deck_to_field.get_card():
                if isinstance(card, TestCard):
                    card.selected = False

            for field in self.deck_to_field.get_field():
                if isinstance(field, TestField):
                    field.selected = False



            for card in reversed(self.deck_to_field.get_card()):
                composition_shape_list = card.get_pickable_card_shapes()
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


            for field in reversed(self.deck_to_field.get_field()):
                composition_shape_list = field.get_field_shapes()
                for shape in composition_shape_list:
                    if self.selected_object is not None and isinstance(shape, PickableRectangle) and shape.is_point_inside((x, y)):
                        if self.selected_object.is_hand:
                            self.use_table[self.selected_object.card_type](self.selected_object)


                        else:
                            if self.selected_object.card_type == CardType.UNIT:
                            #Todo : 필드의 카드를 클릭하면, 유닛의 사망처리에 관련된 UI기능이 호출됨
                                self.selected_object.move_to_tomb()
                                self.selected_count -= 1
                                self.master.title(f"Unit destroyed!!")
                                self.deck_to_field.unit_in_field.remove(self.selected_object)
                                for i,unit in enumerate(self.deck_to_field.unit_in_field):
                                    unit.local_translation = (i * 120, 0)
                                    unit.move_to_field(150,325)


                        self.selected_object = None

                        break



            self.redraw()
        except Exception as e:
            print(f"Exception in on_canvas_click: {e}")

    def use_unit_card(self, selected_object):
        selected_object.local_translation = (self.selected_count * 120, 0)
        selected_object.move_to_field(150, 325)
        self.deck_to_field.unit_in_field.append(selected_object)
        self.master.title(f"use Unit Card!! : {self.deck_to_field.unit_in_field}")
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
