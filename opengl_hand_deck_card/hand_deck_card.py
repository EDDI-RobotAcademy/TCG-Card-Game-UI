import os
from OpenGL.GL import *
from OpenGL.GLU import *

from card_info_from_csv.repository.card_info_from_csv_repository_impl import CardInfoFromCsvRepositoryImpl
from opengl_pickable_shape.pickable_rectangle import PickableRectangle
from common.utility import get_project_root
from opengl_shape.image_rectangle_element import ImageRectangleElement
from opengl_shape.rectangle import Rectangle
from opengl_battle_field_card_controller.card_controller_impl import CardControllerImpl


class HandDeckCard:
    __imagePath = None

    def __init__(self, window, battle_field, local_translation=(0, 0), scale=1, card_type=None):
        self.card_type = card_type
        self.tool_card = None
        self.pickable_hand_deck_card_base = None
        self.card_number = None
        self.is_hand = True

        self.window = window
        self.battle_field = battle_field
        self.local_translation = local_translation
        self.scale = scale
        self.shapes = []

        # self.selected_object = None
        # self.drag_start = None
        # self.window.bind("<B1-Motion>", self.on_canvas_drag)
        # self.window.bind("<ButtonRelease-1>", self.on_canvas_release)
        # self.window.bind("<Button-1>", self.on_canvas_click)
        # self.window.bind("<Configure>", self.on_resize)
    def get_card_number(self):
        return self.card_number

    def set_card_number(self, card_number):
        self.card_number = card_number

    def change_local_translation(self, _translation):
        self.local_translation = _translation

    def get_pickable_hand_deck_card_base(self):
        return self.pickable_hand_deck_card_base

    def get_tool_card(self):
        return self.tool_card

    def add_shape(self, shape):
        shape.local_translate(self.local_translation)
        self.shapes.append(shape)

    def get_get_pickable_hand_deck_card_base_shapes(self):
        return self.shapes

    def create_attached_tool_card_rectangle(self, color, vertices, local_translation):
        attached_tool_card = Rectangle(color=color,
                                       local_translation=local_translation,
                                       vertices=vertices)
        attached_tool_card.set_draw_gradient(True)
        attached_tool_card.set_visible(False)
        self.add_shape(attached_tool_card)
        return attached_tool_card

    def create_card_background_rectangle(self, image_path, vertices, local_translation):
        card_background_illustration = ImageRectangleElement(image_path=image_path,
                                                             local_translation=local_translation,
                                                             vertices=vertices)
        card_background_illustration.set_visible(False)
        self.add_shape(card_background_illustration)
        return card_background_illustration

    def create_card_base_pickable_rectangle(self, color, vertices, local_translation):
        pickable_hand_deck_card_base = PickableRectangle(color=color,
                                               local_translation=local_translation,
                                               vertices=vertices)
        pickable_hand_deck_card_base.set_draw_gradient(True)
        self.add_shape(pickable_hand_deck_card_base)
        return pickable_hand_deck_card_base

    def create_illustration(self, image_path, vertices, local_translation):
        card_illustration = ImageRectangleElement(image_path=image_path,
                                                  local_translation=local_translation,
                                                  vertices=vertices)
        self.add_shape(card_illustration)
        return card_illustration

    def create_equipped_mark(self, image_path, vertices, local_translation):
        card_equipped_mark = ImageRectangleElement(image_path=image_path,
                                                   local_translation=local_translation,
                                                   vertices=vertices)
        card_equipped_mark.set_visible(False)
        self.add_shape(card_equipped_mark)
        return card_equipped_mark

    def init_hand_deck_card(self, card_number):
        self.set_card_number(card_number)
        project_root = get_project_root()

        cardInfo = CardInfoFromCsvRepositoryImpl.getInstance()
        csvInfo = cardInfo.readCardData(os.path.join(project_root, 'local_storage', 'card', 'data.csv'))
        cardInfo.build_dictionaries(csvInfo)

        CardControllerImpl()
        card_controller = CardControllerImpl.getInstance()

        self.tool_card = self.create_attached_tool_card_rectangle(
            color=(0.6, 0.4, 0.6, 1.0),
            local_translation=self.local_translation,
            vertices=[(15, 15), (139, 15), (139, 215), (15, 215)])

        self.pickable_hand_deck_card_base = (
            self.create_card_base_pickable_rectangle(
                color=(0.0, 0.78, 0.34, 1.0),
                local_translation=self.local_translation,
                vertices=[(0, 0), (124, 0), (124, 200), (0, 200)]
            )
        )

        self.pickable_hand_deck_card_base.set_attached_shapes(
            self.create_illustration(
                image_path=os.path.join(project_root, "local_storage", "card_images", f"{card_number}.png"),
                local_translation=self.local_translation,
                vertices=[(15, 15), (109, 15), (109, 109), (15, 109)]
            )
        )

        self.pickable_hand_deck_card_base.set_attached_shapes(
            self.create_equipped_mark(
                image_path=os.path.join(project_root, "local_storage", "card_images", "equip_white.jpg"),
                local_translation=self.local_translation,
                vertices=[(164, 30), (204, 30), (204, 70), (164, 70)]
            )
        )

        card_controller_shapes = card_controller.getCardTypeTable(cardInfo.getCardTypeDictionary(card_number))
        card_shapes = card_controller_shapes(self.local_translation, card_number)
        for shape in card_shapes:
            self.pickable_hand_deck_card_base.set_attached_shapes(shape)

        self.pickable_hand_deck_card_base.set_attached_shapes(
            self.create_card_background_rectangle(
                image_path=os.path.join(project_root, "local_storage", "card_images", "background.png"),
                local_translation=self.local_translation,
                vertices=[(0, 0), (124, 0), (124, 200), (0, 200)]
            )
        )
    def reshape(self, width, height):
        print(f"Reshaping window to width={width}, height={height}")
        glViewport(0, 0, width, height)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluOrtho2D(0, width, height, 0)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

    def redraw(self):
        # self.window.apply_global_translation((50, 50))
        self.window.tkSwapBuffers()
        self.window.after(0, self.window.renderer.render)

    def move_to_field(self, field_x, field_y):
        self.is_hand = False
        self.shapes.clear()
        self.x1, self.x2, self.y1, self.y2 = field_x - 50, field_x + 50, field_y - 100, field_y + 100
        # self.pickable_card_base.set_visible=False
        self.pickable_hand_deck_card_base = (self.create_card_base_pickable_rectangle(color=(0.0, 0.78, 0.34, 1.0),
                                                                       local_translation=self.local_translation,
                                                                       vertices=[(self.x1, self.y1), (self.x2, self.y1),
                                                                                 (self.x2, self.y2),
                                                                                 (self.x1, self.y2)]),)
    def set_energy(self):
        self.is_hand = False
        self.shapes.clear()
        if self.tool_card is not None:
            self.add_shape(self.tool_card)

        # self.pickable_card_base.set_visible=False
        self.pickable_hand_deck_card_base = (self.create_card_base_pickable_rectangle(color=(1, 1, 1, 1.0),
                                                                       local_translation=self.local_translation,
                vertices=[(self.x1, self.y1), (self.x2, self.y1), (self.x2, self.y2),(self.x1, self.y2)]),)

    def equip_tool(self):
        self.is_hand = False
        self.shapes.clear()
        self.tool_card = self.create_attached_tool_card_rectangle(color=(0.7,0.1,0.3,1), local_translation=self.local_translation,
                         vertices=[(self.x1+20, self.y1), (self.x2+20, self.y1), (self.x2+20, self.y2), (self.x1+20, self.y2)])
        self.add_shape(self.tool_card)

        self.pickable_card_base = (self.create_card_base_pickable_rectangle(color=(1, 1, 1, 1.0),
                                                                       local_translation=self.local_translation,
                                                                       vertices=[(self.x1, self.y1), (self.x2, self.y1),
                                                                                 (self.x2, self.y2),
                                                                                 (self.x1, self.y2)]),)
    def move_to_tomb(self):
        self.shapes.clear()