from screeninfo import get_monitors

import tkinter
import unittest

from OpenGL.GL import *
from OpenGL.GLU import *
from pyopengltk import OpenGLFrame

from battle_field.infra.your_hand_repository import YourHandRepository
from battle_field_muligun.entity.scene.battle_field_muligun_scene import BattleFieldMuligunScene
from image_shape.circle_image import CircleImage
from image_shape.circle_number_image import CircleNumberImage
from initializer.init_domain import DomainInitializer
from opengl_battle_field_pickable_card.pickable_card import PickableCard
from opengl_rectangle_lightning_border.lightning_border import LightningBorder
from opengl_shape.circle import Circle
from opengl_shape.rectangle import Rectangle


class PreDrawedBattleFieldFrameRefactor(OpenGLFrame):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)

        monitors = get_monitors()
        target_monitor = monitors[2] if len(monitors) > 2 else monitors[0]

        self.width = target_monitor.width
        self.height = target_monitor.height

        self.is_reshape_not_complete = True

        self.current_width = self.width
        self.current_height = self.height

        self.prev_width = self.width
        self.prev_height = self.height

        self.width_ratio = 1.0
        self.height_ratio = 1.0

        self.battle_field_muligun_background_shape_list = None

        self.active_panel_rectangle = None
        self.selected_object = None
        self.prev_selected_object = None
        self.drag_start = None

        self.lightning_border = LightningBorder()

        self.your_hand_repository = YourHandRepository.getInstance()
        self.hand_card_list = None

        self.bind("<Configure>", self.on_resize)
        self.bind("<B1-Motion>", self.on_canvas_drag)
        self.bind("<ButtonRelease-1>", self.on_canvas_release)
        self.bind("<Button-1>", self.on_canvas_left_click)
        self.bind("<Button-3>", self.on_canvas_right_click)

    def initgl(self):
        glClearColor(1.0, 1.0, 1.0, 0.0)
        glOrtho(0, self.width, self.height, 0, -1, 1)

        self.tkMakeCurrent()

    def init_first_window(self, width, height):
        print(f"Operate Only Once -> width: {width}, height: {height}")
        self.width = width
        self.height = height

        self.current_width = self.width
        self.current_height = self.height

        self.prev_width = self.width
        self.prev_height = self.height
        self.is_reshape_not_complete = False

        battle_field_muligun_scene = BattleFieldMuligunScene()
        battle_field_muligun_scene.create_battle_field_muligun_scene(self.width, self.height)
        self.battle_field_muligun_background_shape_list = battle_field_muligun_scene.get_battle_field_muligun_background()

        # 1848 기준 -> 1848 - (105 * 5 + 170 * 4) = 643
        # 643 / 2 = 321.5
        # 321.5 / 1848 = 17.4% => 0.174
        # 위 수식은 적합하지 않음 (0.286 포함)
        self.your_hand_repository.set_x_base(530)
        self.your_hand_repository.save_current_hand_state([6, 8, 19, 151, 93])
        # self.your_hand_repository.save_current_hand_state([151])
        self.your_hand_repository.create_hand_card_list()

        self.hand_card_list = self.your_hand_repository.get_current_hand_card_list()

    def reshape(self, width, height):
        print(f"Reshaping window to width={width}, height={height}")

        if self.is_reshape_not_complete:
            self.init_first_window(width, height)

        self.current_width = width
        self.current_height = height

        self.width_ratio = self.current_width / self.prev_width
        self.height_ratio = self.current_height / self.prev_height

        self.width_ratio = min(self.width_ratio, 1.0)
        self.height_ratio = min(self.height_ratio, 1.0)

        self.prev_width = self.current_width
        self.prev_height = self.current_height

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
            battle_field_muligun_background_shape.set_width_ratio(self.width_ratio)
            battle_field_muligun_background_shape.set_height_ratio(self.height_ratio)
            battle_field_muligun_background_shape.draw()

    def redraw(self):
        if self.is_reshape_not_complete:
            return

        self.tkMakeCurrent()
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        self.draw_base()

        for hand_card in self.hand_card_list:
            attached_tool_card = hand_card.get_tool_card()
            if attached_tool_card is not None:
                attached_tool_card.set_width_ratio(self.width_ratio)
                attached_tool_card.set_height_ratio(self.height_ratio)
                attached_tool_card.draw()

            pickable_card_base = hand_card.get_pickable_card_base()
            pickable_card_base.set_width_ratio(self.width_ratio)
            pickable_card_base.set_height_ratio(self.height_ratio)
            pickable_card_base.draw()

            attached_shape_list = pickable_card_base.get_attached_shapes()

            for attached_shape in attached_shape_list:
                attached_shape.set_width_ratio(self.width_ratio)
                attached_shape.set_height_ratio(self.height_ratio)
                attached_shape.draw()

        if self.selected_object:
            pickable_card_base = self.selected_object.get_pickable_card_base()

            self.lightning_border.set_width_ratio(self.width_ratio)
            self.lightning_border.set_height_ratio(self.height_ratio)

            self.lightning_border.set_padding(50)
            self.lightning_border.update_shape(pickable_card_base)
            self.lightning_border.draw_lightning_border()

        if self.active_panel_rectangle:
            # self.active_panel_rectangle.set_width_ratio(self.width_ratio)
            # self.active_panel_rectangle.set_height_ratio(self.height_ratio)
            self.active_panel_rectangle.draw()

        self.tkSwapBuffers()

    def on_canvas_drag(self, event):
        x, y = event.x, event.y
        y = self.winfo_reqheight() - y
        print(f"on_canvas_drag -> x: {x}, y: {y}")

        if self.selected_object and self.drag_start:
            pickable_card = self.selected_object.get_pickable_card_base()

            dx = x - self.drag_start[0]
            dy = y - self.drag_start[1]
            dx /= self.width_ratio
            dy /= self.height_ratio
            dy *= -1

            new_vertices = [
                (vx + dx, vy + dy) for vx, vy in pickable_card.vertices
            ]
            pickable_card.update_vertices(new_vertices)

            tool_card = self.selected_object.get_tool_card()
            if tool_card is not None:
                new_tool_card_vertices = [
                    (vx + dx, vy + dy) for vx, vy in tool_card.vertices
                ]
                tool_card.update_vertices(new_tool_card_vertices)
                print(f"Rectangle -> update_vertices dx: {dx}, dy: {dy}")

            for attached_shape in pickable_card.get_attached_shapes():
                if isinstance(attached_shape, CircleImage):
                    # print(f"CircleImage -> before update_center() attached_shape.center: {attached_shape.center}, dx: {dx}, dy: {dy}")
                    new_attached_shape_center = (attached_shape.vertices[0][0] + dx, attached_shape.vertices[0][1] + dy)
                    # print("CircleImage -> update_center()")
                    attached_shape.update_circle_vertices(new_attached_shape_center)
                    continue

                if isinstance(attached_shape, CircleNumberImage):
                    new_attached_shape_center = (attached_shape.vertices[0][0] + dx, attached_shape.vertices[0][1] + dy)
                    # print("CircleNumberImage -> update_center()")
                    attached_shape.update_circle_vertices(new_attached_shape_center)
                    continue

                if isinstance(attached_shape, Circle):
                    new_attached_shape_center = (attached_shape.vertices[0][0] + dx, attached_shape.vertices[0][1] + dy)
                    # print("Circle -> update_center()")
                    attached_shape.update_center(new_attached_shape_center)
                    continue

                new_attached_shape_vertices = [
                    (vx + dx, vy + dy) for vx, vy in attached_shape.vertices
                ]
                attached_shape.update_vertices(new_attached_shape_vertices)

            self.drag_start = (x, y)

    def on_canvas_release(self, event):
        self.drag_start = None

    def on_canvas_left_click(self, event):
        try:
            x, y = event.x, event.y
            y = self.winfo_reqheight() - y

            for hand_card in self.hand_card_list:
                if isinstance(hand_card, PickableCard):
                    hand_card.selected = False

            self.selected_object = None

            for hand_card in reversed(self.hand_card_list):
                pickable_card_base = hand_card.get_pickable_card_base()
                pickable_card_base.set_width_ratio(self.width_ratio)
                pickable_card_base.set_height_ratio(self.height_ratio)

                if pickable_card_base.is_point_inside((x, y)):
                    hand_card.selected = not hand_card.selected
                    self.selected_object = hand_card
                    self.drag_start = (x, y)

                    if self.selected_object != self.prev_selected_object:
                        self.active_panel_rectangle = None
                        self.prev_selected_object = self.selected_object

                    break

        except Exception as e:
            print(f"Exception in on_canvas_click: {e}")

    def on_canvas_right_click(self, event):
        x, y = event.x, event.y

        if self.selected_object:
            convert_y = self.winfo_reqheight() - y
            pickable_card_base = self.selected_object.get_pickable_card_base()
            if pickable_card_base.is_point_inside((x, convert_y)):
                new_rectangle = self.create_opengl_rectangle((x, y))
                self.active_panel_rectangle = new_rectangle

    def create_opengl_rectangle(self, start_point):
        rectangle_size = 50 * self.width_ratio
        rectangle_color = (1.0, 0.0, 0.0, 1.0)

        end_point = (start_point[0] + rectangle_size, start_point[1] + rectangle_size)

        new_rectangle = Rectangle(rectangle_color, [
            (start_point[0], start_point[1]),
            (end_point[0], start_point[1]),
            (end_point[0], end_point[1]),
            (start_point[0], end_point[1])
        ])
        new_rectangle.created_by_right_click = True
        return new_rectangle


class TestDrawPickableHandWithResize(unittest.TestCase):

    def test_draw_pickable_hand_with_resize(self):
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
