from OpenGL.GL import *
from OpenGL.GLU import *
from pyopengltk import OpenGLFrame

from common.utility import get_project_root
from opengl_battle_field_pickable_card.legacy.pickable_card import LegacyPickableCard
from tests.jsh.ugly_test_card.renderer.card_frame_renderer import CardFrameRenderer


class CardFrame(OpenGLFrame):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self.card_list = []
        self.selected_object = None
        self.drag_start = None

        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        self.width = screen_width
        self.height = screen_height

        project_root = get_project_root()

        first_card = LegacyPickableCard(local_translation=(100, 100), scale=300)
        first_card.init_card_scale(5)

        self.card_list.append(first_card)

        second_card = LegacyPickableCard(local_translation=(400, 400))
        second_card.init_card(8)

        self.card_list.append(second_card)

        self.renderer = CardFrameRenderer(self.card_list, self)

        # self.bind("<B1-Motion>", self.renderer.on_canvas_drag)
        # self.bind("<ButtonRelease-1>", self.renderer.on_canvas_release)
        # self.bind("<Button-1>", self.renderer.on_canvas_click)
        self.bind("<B1-Motion>", self.on_canvas_drag)
        self.bind("<ButtonRelease-1>", self.on_canvas_release)
        self.bind("<Button-1>", self.on_canvas_click)
        self.bind("<Configure>", self.on_resize)

    def initgl(self):
        print("Initializing OpenGL")
        # glEnable(GL_DEPTH_TEST)
        # glClearColor(0.0, 0.0, 0.0, 1.0)
        # self.set_projection_matrix()
        glClearColor(1.0, 1.0, 1.0, 0.0)
        glOrtho(0, self.width, self.height, 0, -1, 1)

    def toggle_visibility(self):
        for card in self.card_list:
            tool_card = card.get_tool_card()
            tool_card.set_visible(not tool_card.get_visible())

            pickable_card = card.get_pickable_card_base()
            attached_shape_list = pickable_card.get_attached_shapes()
            print(f"attached shape: {attached_shape_list}")

            for attached_shape in attached_shape_list:
                print(f"attached shape: {attached_shape.vertices}")

            equipped_mark = attached_shape_list[1]
            current_status = equipped_mark.get_visible()
            print(f"current visible status: {current_status}")
            equipped_mark.set_visible(not equipped_mark.get_visible())

        self.redraw()

    def set_projection_matrix(self):
        glViewport(0, 0, self.winfo_reqwidth(), self.winfo_reqheight())
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluOrtho2D(0, self.winfo_reqwidth(), 0, self.winfo_reqheight())
        glMatrixMode(GL_MODELVIEW)

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
        print("Redrawing OpenGL scene")
        self.tkMakeCurrent()
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        # glLoadIdentity()

        # glClearColor(0.0, 0.0, 0.0, 1.0)

        # if self.renderer:
        #     self.renderer.render()

        for card in self.card_list:
            attached_tool_card = card.get_tool_card()
            attached_tool_card.draw()

            pickable_card_base = card.get_pickable_card_base()
            pickable_card_base.draw()

            attached_shape_list = pickable_card_base.get_attached_shapes()

            for attached_shape in attached_shape_list:
                attached_shape.draw()

        self.tkSwapBuffers()

    def on_canvas_drag(self, event):
        x, y = event.x, event.y
        print(f"x = {x}, y = {y}")
        y = self.winfo_reqheight() - y
        print(f"self.winfo_reqheight() - y = {y}")

        if self.selected_object and self.drag_start:
            print(f"selected_object: {self.selected_object}")
            pickable_card = self.selected_object.get_pickable_card_base()
            print(f"pickable_unit: {pickable_card}")

            dx = x - self.drag_start[0]
            dy = y - self.drag_start[1]
            print(f"dx = {dx}, dy = {dy}")
            print(f"drag_start: {self.drag_start}")
            dy *= -1

            for vx, vy in pickable_card.vertices:
                print(f"vx = {vx}, vy = {vy}")

            new_vertices = [
                (vx + dx, vy + dy) for vx, vy in pickable_card.vertices
            ]
            pickable_card.update_vertices(new_vertices)

            tool_card = self.selected_object.get_tool_card()
            new_tool_card_vertices = [
                (vx + dx, vy + dy) for vx, vy in tool_card.vertices
            ]
            tool_card.update_vertices(new_tool_card_vertices)

            for attached_shape in pickable_card.get_attached_shapes():
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
            y = self.winfo_reqheight() - y

            for card in self.card_list:
                if isinstance(card, LegacyPickableCard):
                    card.selected = False

            self.selected_object = None

            for card in reversed(self.card_list):
                print("find selected Pickable Rectangle")
                pickable_card_base = card.get_pickable_card_base()

                if pickable_card_base.is_point_inside((x, y)):
                    print(f"pickable_unit_card_base.is_point_inside(x, y) pass")
                    card.selected = not card.selected
                    self.selected_object = card
                    self.drag_start = (x, y)
                    print(f"Selected PickableRectangle at ({x}, {y})")
                    break

            self.redraw()
        except Exception as e:
            print(f"Exception in on_canvas_click: {e}")
