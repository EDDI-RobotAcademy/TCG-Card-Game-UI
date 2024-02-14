from opengl_battle_field_card.card import Card
from opengl_pickable_shape.pickable_rectangle import PickableRectangle

from OpenGL.GL import *
from OpenGL.GLU import *
class HandDeckCardLegacy:
    __imagePath = None

    def __init__(self, window, battle_field, local_translation=(0, 0), scale=1):
        self.shapes = []
        self.local_translation = local_translation
        self.scale = scale
        self.window = window
        self.battle_field = battle_field

        self.card_number = None
        self.hand_deck_card = None

        self.selected_object = None
        self.drag_start = None
        self.window.bind("<B1-Motion>", self.on_canvas_drag)
        self.window.bind("<ButtonRelease-1>", self.on_canvas_release)
        self.window.bind("<Button-1>", self.on_canvas_click)
        self.window.bind("<Configure>", self.on_resize)
    def get_card_number(self):
        return self.card_number
    def change_local_translation(self, _translation):
        self.local_translation = _translation

    def get_hand_deck_card_shapes(self):
        return self.shapes

    def get_hand_deck_card(self):
        return self.hand_deck_card

    def set_hand_deck_card(self, hand_deck_card):
        self.hand_deck_card = hand_deck_card
    def add_shape(self, shape):
        shape.local_translate(self.local_translation)
        self.shapes.append(shape)

    def create_hand_deck_card(self, card_number):
        hand_deck_card = Card()
        hand_deck_card.init_card(card_number)
        self.add_shape(hand_deck_card.get_pickable_card_base())
        for shape in hand_deck_card.get_pickable_card_base().get_attached_shapes():
            self.add_shape(shape)
            self.set_hand_deck_card(hand_deck_card.get_pickable_card_base())

        # hand_deck_card.set_draw_gradient(True)
        # return hand_deck_card

    # def init_shapes(self):
    #     self.hand_deck_card = (
    #         self.create_hand_deck_card(color=(0, 0, 0, 1.0),
    #                                         local_translation=self.local_translation,
    #                                         vertices=[(600, 860), (1600, 860), (1600, 1055), (600, 1055)]))
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

    def on_resize(self, event):
        print("Handling resize event")
        self.reshape(event.width, event.height)

    def on_canvas_click(self, event):
        print(f"on_canvas_click: {event}")
        try:
            x, y = event.x, event.y
            y = self.window.winfo_reqheight() - y

            for hand_deck_card in self.battle_field.hand_deck_card:
                 if isinstance(hand_deck_card, HandDeckCard):
                    hand_deck_card.selected = False

            # for field in self.battle_field.pickable_field_base:
            #      if isinstance(field, Field):
            #         field.selected = False

            self.selected_object = None
            print(f"{reversed(self.battle_field.hand_deck_card)}")

            for hand_deck_card in reversed(self.battle_field.hand_deck_card):
                pickable_hand_deck_card_base = hand_deck_card.hand_deck_card
                print(f"pickable_hand_deck_card_base type: {(type(hand_deck_card))}")
                print(f"hand_deck_card: {hand_deck_card}")
                print(f"pickable_hand_deck_card_base: {pickable_hand_deck_card_base}")

                if pickable_hand_deck_card_base.is_point_inside((x, y)):
                    print("pickable_unit_card_base.is_point_inside(x, y) pass")
                    hand_deck_card.selected = not hand_deck_card.selected
                    self.selected_object = hand_deck_card
                    self.drag_start = (x, y)
                    print(f"Selected PickableRectangle at ({x}, {y})")
                    break

            self.redraw()
        except Exception as e:
            print(f"Exception in on_canvas_click: {e}")

    def on_canvas_drag(self, event):
        x, y = event.x, event.y
        print(f"x = {x}, y = {y}")
        y = self.window.winfo_reqheight() - y
        print(f"self.window.winfo_reqheight() - y = {y}")

        if self.selected_object and self.drag_start:
            # self.start_drag(event)

            pickable_hand_deck_card = self.selected_object.get_hand_deck_card()
            print(type(pickable_hand_deck_card))
            dx = x - self.drag_start[0]
            dy = y - self.drag_start[1]
            print(f"dx = {dx}, dy = {dy}")
            print(f"drag_start: {self.drag_start}")
            dy *= -1

            for vx, vy in pickable_hand_deck_card.vertices:
                print(f"vx = {vx}, vy = {vy}")

            new_vertices = [
                (vx + dx, vy + dy) for vx, vy in pickable_hand_deck_card.vertices
            ]
            pickable_hand_deck_card.update_vertices(new_vertices)

            tool_card = self.selected_object.get_tool_card()
            new_tool_card_vertices = [
                (vx + dx, vy + dy) for vx, vy in tool_card.vertices
            ]
            tool_card.update_vertices(new_tool_card_vertices)

            for attached_shape in pickable_hand_deck_card.get_attached_shapes():
                new_attached_shape_vertices = [
                    (vx + dx, vy + dy) for vx, vy in attached_shape.vertices
                ]
                attached_shape.update_vertices(new_attached_shape_vertices)

            self.drag_start = (x, y)
            self.redraw()

    def on_canvas_release(self, event):
        # self.cancel_drag()
        self.drag_start = None

    # def on_canvas_click(self, event):
    #     print(f"on_canvas_click: {event}")
    #     try:
    #         x, y = event.x, event.y
    #         y = self.window.winfo_reqheight() - y
    #
    #         for hand_deck in self.battle_field.pickable_hand_deck_base:
    #              if isinstance(hand_deck, HandDeck):
    #                 hand_deck.selected = False
    #
    #         for field in self.battle_field.pickable_field_base:
    #              if isinstance(field, Field):
    #                 field.selected = False
    #
    #         self.selected_object = None
    #         print(f"{reversed(self.battle_field.pickable_hand_deck_base)}")
    #
    #         for hand_deck in reversed(self.battle_field.pickable_hand_deck_base):
    #             pickable_hand_deck_base = hand_deck.pickable_hand_deck_base
    #
    #             if pickable_hand_deck_base.is_point_inside((x, y)):
    #                 print("pickable_unit_card_base.is_point_inside(x, y) pass")
    #                 hand_deck.selected = not hand_deck.selected
    #                 self.selected_object = hand_deck
    #                 self.drag_start = (x, y)
    #                 print(f"Selected PickableRectangle at ({x}, {y})")
    #                 break
    #
    #         self.redraw()
    #     except Exception as e:
    #         print(f"Exception in on_canvas_click: {e}")
    #
    # def on_canvas_drag(self, event):
    #     x, y = event.x, event.y
    #     print(f"x = {x}, y = {y}")
    #     y = self.window.winfo_reqheight() - y
    #     print(f"self.window.winfo_reqheight() - y = {y}")
    #
    #     if self.selected_object and self.drag_start:
    #         # self.start_drag(event)
    #
    #         pickable_hand_deck = self.selected_object.get_pickable_hand_deck_base()
    #         print(type(pickable_hand_deck))
    #         dx = x - self.drag_start[0]
    #         dy = y - self.drag_start[1]
    #         print(f"dx = {dx}, dy = {dy}")
    #         print(f"drag_start: {self.drag_start}")
    #         dy *= -1
    #
    #         for vx, vy in pickable_hand_deck.vertices:
    #             print(f"vx = {vx}, vy = {vy}")
    #
    #         new_vertices = [
    #             (vx + dx, vy + dy) for vx, vy in pickable_hand_deck.vertices
    #         ]
    #         pickable_hand_deck.update_vertices(new_vertices)
    #
    #         tool_card = self.selected_object.get_tool_card()
    #         new_tool_card_vertices = [
    #             (vx + dx, vy + dy) for vx, vy in tool_card.vertices
    #         ]
    #         tool_card.update_vertices(new_tool_card_vertices)
    #
    #         for attached_shape in pickable_hand_deck.get_attached_shapes():
    #             new_attached_shape_vertices = [
    #                 (vx + dx, vy + dy) for vx, vy in attached_shape.vertices
    #             ]
    #             attached_shape.update_vertices(new_attached_shape_vertices)
    #
    #         self.drag_start = (x, y)
    #         self.redraw()