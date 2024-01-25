import math
import tkinter
import random

from OpenGL import GL, GLU
from OpenGL.GL import *
from OpenGL.GLU import *
import tkinter as tk
from pyopengltk import OpenGLFrame
import unittest

import numpy as np

from PIL import Image
from OpenGL import GL

import os

from common.utility import get_project_root

import abc


class Shape(abc.ABC):
    def __init__(self, vertices, global_translation=(0, 0), local_translation=(0, 0), is_pickable=False):
        self.vertices = vertices
        self.global_translation = global_translation
        self.local_translation = local_translation
        self.translation = self.local_translation + self.global_translation
        self.is_pickable = is_pickable

    def local_translate(self, local_translate):
        self.local_translation = local_translate

    def global_translate(self, global_translate):
        self.global_translation = global_translate

    def set_alpha(self, new_alpha):
        if len(self.color) == 4:
            self.color = self.color[:3] + (new_alpha,)
        else:
            self.color = self.color + (new_alpha,)

    def is_point_inside(self, point):
        x, y = point

        if not (self.vertices[0][0] <= x <= self.vertices[2][0] and
                self.vertices[0][1] <= y <= self.vertices[2][1]):
            return False

        winding_number = 0
        for i in range(len(self.vertices)):
            x1, y1 = self.vertices[i]
            x2, y2 = self.vertices[(i + 1) % len(self.vertices)]

            if y1 <= y < y2 or y2 <= y < y1:
                if x1 + (y - y1) / (y2 - y1) * (x2 - x1) > x:
                    winding_number += 1

        return winding_number % 2 == 1
    def update_vertices(self, new_vertices):
        self.vertices = new_vertices

    @abc.abstractmethod
    def draw(self):
        pass


class Rectangle(Shape):
    def __init__(self, color, vertices, global_translation=(0, 0), local_translation=(0, 0), is_pickable=False):
        super().__init__(vertices, global_translation, local_translation, is_pickable)
        self.color = color
        self.draw_border = True
        self.draw_gradient = False
        self.is_visible = True

    def set_visible(self, visible):
        self.is_visible = visible

    def get_visible(self):
        return self.is_visible

    def set_draw_border(self, value):
        self.draw_border = value

    def set_draw_gradient(self, value):
        self.draw_gradient = value

    def draw(self):
        if not self.is_visible:
            return

        if self.draw_border:
            # Draw border
            glLineWidth(2.0)
            glColor4f(0.0, 0.0, 0.0, 1.0)
            glBegin(GL_LINE_LOOP)
            glVertex2f(self.vertices[0][0] + self.global_translation[0] + self.local_translation[0] - 1,
                       self.vertices[0][1] + self.global_translation[1] + self.local_translation[1] - 1)
            glVertex2f(self.vertices[1][0] + self.global_translation[0] + self.local_translation[0] + 1,
                       self.vertices[1][1] + self.global_translation[1] + self.local_translation[1] - 1)
            glVertex2f(self.vertices[2][0] + self.global_translation[0] + self.local_translation[0] + 1,
                       self.vertices[2][1] + self.global_translation[1] + self.local_translation[1] + 1)
            glVertex2f(self.vertices[3][0] + self.global_translation[0] + self.local_translation[0] - 1,
                       self.vertices[3][1] + self.global_translation[1] + self.local_translation[1] + 1)
            glEnd()

        glBegin(GL_QUADS)

        if self.draw_gradient:
            color_variation = random.uniform(1.7, 2.9)
            colored_border = [c * color_variation for c in self.color]

            for i, vertex in enumerate(self.vertices):
                gradient_factor = i / (len(self.vertices) - 1)  # Normalize to [0, 1]
                interpolated_color = [c * (1.0 - gradient_factor) + rc * gradient_factor for c, rc in
                                      zip(self.color, colored_border)]

                glColor4f(*interpolated_color)
                glVertex2f(vertex[0] + self.global_translation[0] + self.local_translation[0],
                           vertex[1] + self.global_translation[1] + self.local_translation[1])
        else:
            for vertex in self.vertices:
                glColor4f(*self.color)
                glVertex2f(vertex[0] + self.global_translation[0] + self.local_translation[0],
                           vertex[1] + self.global_translation[1] + self.local_translation[1])

        glEnd()


class Circle(Shape):
    def __init__(self, color, center, radius, local_translation=(0, 0), global_translation=(0, 0)):
        super().__init__([center], local_translation, global_translation)
        self.color = color
        self.radius = radius
        self.draw_border = True

    def set_draw_border(self, value):
        self.draw_border = value

    def draw(self):
        glColor4f(*self.color)
        glBegin(GL_POLYGON)
        for i in range(100):
            theta = 2.0 * math.pi * i / 100
            x = self.radius * math.cos(theta) + self.vertices[0][0] + self.global_translation[0] + self.local_translation[0]
            y = self.radius * math.sin(theta) + self.vertices[0][1] + self.global_translation[1] + self.local_translation[1]
            glVertex2f(x, y)
        glEnd()

        if self.draw_border:
            glLineWidth(2.0)
            glColor4f(0.0, 0.0, 0.0, 1.0)
            glBegin(GL_LINE_LOOP)
            for i in range(100):
                theta = 2.0 * math.pi * i / 100
                x = self.radius * math.cos(theta) + self.vertices[0][0] + self.global_translation[0] + self.local_translation[0] - 1
                y = self.radius * math.sin(theta) + self.vertices[0][1] + self.global_translation[1] + self.local_translation[1] - 1
                glVertex2f(x, y)
            glEnd()


class ImageElement(Shape):
    def __init__(self, image_path, vertices, global_translation=(0, 0), local_translation=(0, 0)):
        super().__init__(vertices, global_translation, local_translation)
        self.image_path = image_path
        self.is_visible = True

    def set_visible(self, visible):
        self.is_visible = visible

    def get_visible(self):
        return self.is_visible

    def draw(self):
        if self.get_visible():
            white_rect = Rectangle(color=(1.0, 1.0, 1.0, 1.0),
                                   vertices=self.vertices,
                                   global_translation=self.global_translation,
                                   local_translation=self.local_translation)
            white_rect.draw()

            image_data = self._load_image_data(self.image_path)
            texture_ids = GL.glGenTextures(1)

            GL.glBindTexture(GL.GL_TEXTURE_2D, texture_ids)
            GL.glTexParameteri(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_MAG_FILTER, GL.GL_LINEAR)
            GL.glTexParameteri(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_MIN_FILTER, GL.GL_LINEAR)
            GL.glTexImage2D(GL.GL_TEXTURE_2D, 0, GL.GL_RGBA, image_data.shape[1], image_data.shape[0],
                            0, GL.GL_RGBA, GL.GL_UNSIGNED_BYTE, image_data)

            GL.glEnable(GL.GL_TEXTURE_2D)
            GL.glBindTexture(GL.GL_TEXTURE_2D, texture_ids)

            GL.glBegin(GL.GL_QUADS)
            GL.glTexCoord2f(0, 0)
            print(f"x: {self.vertices[0][0] + self.local_translation[0]}, y: {self.vertices[0][1] + self.local_translation[1]}")
            GL.glVertex2f(self.vertices[0][0] + self.local_translation[0] + self.global_translation[0],
                          self.vertices[0][1] + self.local_translation[1] + self.global_translation[1])

            GL.glTexCoord2f(1, 0)
            GL.glVertex2f(self.vertices[1][0] + self.local_translation[0] + self.global_translation[0],
                          self.vertices[1][1] + self.local_translation[1] + self.global_translation[1])

            GL.glTexCoord2f(1, 1)
            GL.glVertex2f(self.vertices[2][0] + self.local_translation[0] + self.global_translation[0],
                          self.vertices[2][1] + self.local_translation[1] + self.global_translation[1])

            GL.glTexCoord2f(0, 1)
            GL.glVertex2f(self.vertices[3][0] + self.local_translation[0] + self.global_translation[0],
                          self.vertices[3][1] + self.local_translation[1] + self.global_translation[1])
            GL.glEnd()

            GL.glDisable(GL.GL_TEXTURE_2D)

    def _load_image_data(self, path):
        image = Image.open(path)
        resized_image = image.resize((300, 300))

        rgba_image = resized_image.convert("RGBA")
        img_data = np.array(rgba_image)

        return img_data


class UnitCard:
    __imagePath = None

    def __init__(self, local_translation=(0, 0), unit_id=None):
        self.shapes = []
        self.local_translation = local_translation
        self.id = unit_id

    def change_local_translation(self, _translation):
        self.local_translation = _translation

    def get_unit_shapes(self):
        return self.shapes

    def add_shape(self, shape):
        shape.local_translate(self.local_translation)
        self.shapes.append(shape)

    def create_attached_tool_card_rectangle(self, color, vertices):
        attached_tool_card = Rectangle(color=color,
                                       vertices=vertices)
        attached_tool_card.set_draw_gradient(True)
        attached_tool_card.set_visible(False)
        self.add_shape(attached_tool_card)

    def create_card_base_rectangle(self, color, vertices):
        unit_card_base = Rectangle(color=color,
                                   vertices=vertices,
                                   is_pickable=True)
        unit_card_base.set_draw_gradient(True)
        self.add_shape(unit_card_base)

    def create_illustration(self, image_path, vertices):
        unit_illustration = ImageElement(image_path=image_path,
                                         vertices=vertices)
        self.add_shape(unit_illustration)

    def create_equipped_mark(self, image_path, vertices):
        unit_equipped_mark = ImageElement(image_path=image_path,
                                          vertices=vertices)
        unit_equipped_mark.set_visible(False)
        self.add_shape(unit_equipped_mark)

    def create_unit_energy_circle(self, color, center, radius):
        unit_energy_circle = Circle(color=color,
                                    center=center,
                                    radius=radius)
        self.add_shape(unit_energy_circle)

    def create_unit_tribe_circle(self, color, center, radius):
        unit_tribe_circle = Circle(color=color,
                                   center=center,
                                   radius=radius)
        self.add_shape(unit_tribe_circle)

    def create_unit_attack_circle(self, color, center, radius):
        unit_attack_circle = Circle(color=color,
                                    center=center,
                                    radius=radius)
        self.add_shape(unit_attack_circle)

    def create_unit_hp_circle(self, color, center, radius):
        unit_hp_circle = Circle(color=color,
                                center=center,
                                radius=radius)
        self.add_shape(unit_hp_circle)

    def init_shapes(self, image_path):
        self.__imagePath = image_path
        self.create_attached_tool_card_rectangle(color=(0.6, 0.4, 0.6, 1.0),
                                                 vertices=[(20, 20), (370, 20), (370, 520), (20, 520)])

        self.create_card_base_rectangle(color=(0.0, 0.78, 0.34, 1.0),
                                        vertices=[(0, 0), (350, 0), (350, 500), (0, 500)])

        self.create_illustration(image_path=self.__imagePath,
                                 vertices=[(25, 25), (325, 25), (325, 325), (25, 325)])

        project_root = get_project_root()
        self.create_equipped_mark(
            image_path=os.path.join(project_root, "local_storage", "card_images", "equip_white.jpg"),
            vertices=[(390, 30), (430, 30), (430, 70), (390, 70)])

        circle_radius = 30
        self.create_unit_energy_circle(color=(1.0, 0.33, 0.34, 1.0),
                                       center=(0, 0),
                                       radius=circle_radius)

        self.create_unit_tribe_circle(color=(0.678, 0.847, 0.902, 1.0),
                                      center=(350, 0),
                                      radius=circle_radius)

        self.create_unit_attack_circle(color=(0.988, 0.976, 0.800, 1.0),
                                       center=(350, 500),
                                       radius=circle_radius)

        self.create_unit_hp_circle(color=(0.267, 0.839, 0.475, 1.0),
                                   center=(0, 500),
                                   radius=circle_radius)


class BattleField:
    def __init__(self):
        self.unit_card = []
        self.tomb = []
        self.card_deck = []
        self.battle_field_panel = []

    def get_unit_card(self):
        return self.unit_card

    def add_unit_card(self, unit_card):
        self.unit_card.append(unit_card)


class BattleFieldFrame(OpenGLFrame):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self.battle_field = BattleField()
        self.selected_shape = None

        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        self.width = screen_width
        self.height = screen_height

        self.bind("<Configure>", self.on_resize)
        self.bind("<Button-1>", self.on_canvas_click)
        self.bind("<B1-Motion>", self.on_canvas_drag)
        self.bind("<ButtonPress-1>", self.on_canvas_press)
        self.bind("<ButtonRelease-1>", self.on_canvas_release)

        self.make_battle_field()

        project_root = get_project_root()
        print("프로젝트 최상위:", project_root)

        self.renderer = BattleFieldFrameRenderer(self.battle_field, self)

    def make_battle_field(self):
        project_root = get_project_root()

        first_unit = UnitCard(unit_id=1)
        first_unit.init_shapes(os.path.join(project_root, "local_storage", "card_images", "card1.png"))

        self.battle_field.add_unit_card(first_unit)


    def apply_global_translation(self, translation):
        unit_card_list = self.battle_field.get_unit_card()
        for unit_card in unit_card_list:
            unit_shapes = unit_card.get_unit_shapes()
            for shape in unit_shapes:
                print("apply_global_translation")
                shape.global_translate(translation)

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

    def on_canvas_release(self, event):
        print("Mouse button released.")

    def on_canvas_click(self, event):
        print("on_canvas_click() operate ?")
        try:
            x, y = event.x, event.y
            y = self.winfo_reqheight() - y

            unit_card_list = self.battle_field.get_unit_card()

            for unit_card in reversed(unit_card_list):
                unit_shapes = unit_card.get_unit_shapes()

                pickable_shape = next((shape for shape in unit_shapes if shape.is_pickable), None)

                if pickable_shape and pickable_shape.is_point_inside((x, y)):
                    print(f"Clicked on Unit ID: {unit_card.id}")
                    self.move_all_shapes(unit_card, (x, y))
                    return
            print("No unit picked.")

        except Exception as e:
            print(f"Exception in on_canvas_click: {e}")

    def find_shape_at_point(self, point):
        x, y = point

        # Iterate through shapes in reverse order to prioritize shapes on top
        unit_card_list = self.battle_field.get_unit_card()
        for unit_card in reversed(unit_card_list):
            unit_shapes = unit_card.get_unit_shapes()

            for shape in unit_shapes:
                if shape.is_point_inside((x, y)):
                    return shape
        return None

    def on_canvas_drag(self, event):
        if self.selected_shape:
            x, y = event.x, event.y
            y = self.winfo_reqheight() - y

            self.selected_shape.local_translate((x - self.last_x, y - self.last_y))
            self.redraw()

            self.last_x, self.last_y = x, y

    def move_all_shapes(self, unit_card, new_position):
        translation = (
        new_position[0] - unit_card.local_translation[0], new_position[1] - unit_card.local_translation[1])

        for shape in unit_card.get_unit_shapes():
            shape.global_translate(translation)

        self.redraw()

    def on_canvas_press(self, event):
        try:
            if self.selected_shape:
                self.last_x, self.last_y = event.x, self.winfo_reqheight() - event.y
        except Exception as e:
            print(f"Exception in on_canvas_press: {e}")

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


class BattleFieldFrameRenderer:
    def __init__(self, battle_field_scene, window):
        self.battle_field_scene = battle_field_scene
        self.window = window

    def render(self):
        self.window.tkMakeCurrent()
        GL.glClear(GL.GL_COLOR_BUFFER_BIT | GL.GL_DEPTH_BUFFER_BIT)

        unit_card_list = self.battle_field_scene.get_unit_card()
        for unit_card in unit_card_list:
            unit_shapes = unit_card.get_unit_shapes()
            for shape in unit_shapes:
                self._render_shape(shape)

        self.window.tkSwapBuffers()

    def _render_shape(self, shape):
        shape.draw()

class TestUglyAnimationFrame(unittest.TestCase):
    def test_pick_unit_frame(self):
        root = tk.Tk()
        root.geometry(f"{root.winfo_screenwidth()}x{root.winfo_screenheight()}-10-10")
        app = BattleFieldFrame(root, bg="white")
        app.pack(fill=tkinter.BOTH, expand=1)

        toggle_button = tkinter.Button(root, text="Toggle Visibility", command=app.toggle_visibility)
        toggle_button.place(x=100, y=10)

        root.mainloop()

if __name__ == '__main__':
    unittest.main()
