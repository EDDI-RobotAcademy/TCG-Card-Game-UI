
from opengl_pickable_shape.pickable_rectangle import PickableRectangle
from opengl_shape.image_rectangle_element import ImageRectangleElement

from OpenGL.GL import *
from OpenGL.GLU import *
class HandDeck:
    __imagePath = None

    def __init__(self, window, battle_field, local_translation=(0, 0), scale=1):
        self.shapes = []
        self.local_translation = local_translation
        self.scale = scale
        self.window = window
        self.battle_field = battle_field

        self.pickable_card_base = None
        self.selected_object = None
        self.drag_start = None

        self.window.bind("<B1-Motion>", self.on_canvas_drag)
        self.window.bind("<ButtonRelease-1>", self.on_canvas_release)
        self.window.bind("<Button-1>", self.on_canvas_click)
        self.window.bind("<Configure>", self.on_resize)

    def change_local_translation(self, _translation):
        self.local_translation = _translation

    def get_pickable_hand_deck_shapes(self):
        return self.shapes

    def get_pickable_hand_deck_base(self):
        return self.pickable_hand_deck_base

    def add_shape(self, shape):
        shape.local_translate(self.local_translation)
        self.shapes.append(shape)

    def create_hand_deck_rectangle(self, color, vertices, local_translation):
        pickable_hand_deck_base = PickableRectangle(color=color,
                                      local_translation=local_translation,
                                      vertices=vertices)
        self.add_shape(pickable_hand_deck_base)
        print(f"pickable_hand_deck_base 요기 ?{pickable_hand_deck_base}")
        pickable_hand_deck_base.set_draw_gradient(True)
        return pickable_hand_deck_base

    def create_illustration(self, image_path, vertices, local_translation):
        hand_deck_illustration = ImageRectangleElement(image_path=image_path,
                                                  local_translation=local_translation,
                                                  vertices=vertices)
        self.add_shape(hand_deck_illustration)
        return hand_deck_illustration

    def init_shapes(self, imagePath):
        self.__imagePath = imagePath

        self.pickable_hand_deck_base = (
            self.create_hand_deck_rectangle(color=(0, 0, 0, 1.0),
                                            local_translation=self.local_translation,
                                            vertices=[(600, 860), (750, 860), (750, 1055), (600, 1055)]))

        self.pickable_hand_deck_base.set_attached_shapes(
            self.create_illustration(image_path=self.__imagePath,
                                     local_translation=self.local_translation,
                                     vertices=[(600, 860), (750, 860), (750, 1055), (600, 1055)]))


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
    # def draw(self):
    #     for shape in self.shapes:
    #         shape.draw()
    def redraw(self):
        self.window.apply_global_translation((50, 50))
        self.window.tkSwapBuffers()
        self.window.after(10, self.window.renderer.render)

    def on_canvas_drag(self, event):
        x, y = event.x, event.y
        print(f"x = {x}, y = {y}")
        y = self.window.winfo_reqheight() - y
        print(f"self.window.winfo_reqheight() - y = {y}")

        if self.selected_object and self.drag_start:
            pickable_hand_deck = self.selected_object.get_pickable_hand_deck_base()
            print(type(pickable_hand_deck))
            dx = x - self.drag_start[0]
            dy = y - self.drag_start[1]
            print(f"dx = {dx}, dy = {dy}")
            print(f"drag_start: {self.drag_start}")
            dy *= -1

            for vx, vy in pickable_hand_deck.vertices:
                print(f"vx = {vx}, vy = {vy}")

            new_vertices = [
                (vx + dx, vy + dy) for vx, vy in pickable_hand_deck.vertices
            ]
            pickable_hand_deck.update_vertices(new_vertices)

            # tool_card = self.selected_object.get_tool_card()
            # new_tool_card_vertices = [
            #     (vx + dx, vy + dy) for vx, vy in tool_card.vertices
            # ]
            # tool_card.update_vertices(new_tool_card_vertices)
            #
            for attached_shape in pickable_hand_deck.get_attached_shapes():
                new_attached_shape_vertices = [
                    (vx + dx, vy + dy) for vx, vy in attached_shape.vertices
                ]
                attached_shape.update_vertices(new_attached_shape_vertices)

            self.drag_start = (x, y)
            self.redraw()

    def on_canvas_release(self, event):
        self.drag_start = None

    def on_canvas_click(self, event):
        print(f"on_canvas_click: {event}")
        try:
            x, y = event.x, event.y
            y = self.window.winfo_reqheight() - y

            for hand_deck in self.battle_field.pickable_hand_deck_base:

                 if isinstance(hand_deck, HandDeck):
                    hand_deck.selected = False

            self.selected_object = None
            print(f"{reversed(self.battle_field.pickable_hand_deck_base)}")

            for hand_deck in reversed(self.battle_field.pickable_hand_deck_base):
                pickable_hand_deck_base = hand_deck.pickable_hand_deck_base

                if pickable_hand_deck_base.is_point_inside((x, y)):
                    print("pickable_unit_card_base.is_point_inside(x, y) pass")
                    hand_deck.selected = not hand_deck.selected
                    self.selected_object = hand_deck
                    self.drag_start = (x, y)
                    print(f"Selected PickableRectangle at ({x}, {y})")
                    break

            self.redraw()
        except Exception as e:
            print(f"Exception in on_canvas_click: {e}")