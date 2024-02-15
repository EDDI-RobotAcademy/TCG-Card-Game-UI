import math
import os
import random

from OpenGL.GL import *
from OpenGL.GLU import *
from pyopengltk import OpenGLFrame

from common.utility import get_project_root
from opengl_battle_field_card.card import Card


class LightningSegment:
    def __init__(self, start, end, brightness=1.0):
        self.start = start
        self.end = end
        self.brightness = brightness

def average(point1, point2):
    return ((point1[0] + point2[0]) / 2, (point1[1] + point2[1]) / 2)

def normalize(vector):
    length = (vector[0]**2 + vector[1]**2)**0.5
    return (vector[0] / length, vector[1] / length)

def perpendicular(vector):
    return (-vector[1], vector[0])

def rotate(vector, angle):
    x = vector[0] * math.cos(angle) - vector[1] * math.sin(angle)
    y = vector[0] * math.sin(angle) + vector[1] * math.cos(angle)
    return (x, y)

def random_float(min_val, max_val):
    return random.uniform(min_val, max_val)

def generate_lightning(start_point, end_point, maximum_offset, num_generations, branch_probability, length_scale):
    segment_list = [LightningSegment(start_point, end_point)]
    offset_amount = maximum_offset

    for generation in range(num_generations):
        for segment in segment_list[:]:
            segment_list.remove(segment)

            mid_point = average(segment.start, segment.end)
            direction = normalize((segment.end[0] - segment.start[0], segment.end[1] - segment.start[1]))
            normal = perpendicular(direction)

            mid_point = (mid_point[0] + normal[0] * random_float(-offset_amount, offset_amount),
                         mid_point[1] + normal[1] * random_float(-offset_amount, offset_amount))

            segment_list.append(LightningSegment(segment.start, mid_point, segment.brightness))
            segment_list.append(LightningSegment(mid_point, segment.end, segment.brightness))

            if generation % 2 == 0 and random.random() < branch_probability:
                branch_direction = rotate(direction, random_float(-math.pi / 2, math.pi / 2))
                split_end = (mid_point[0] + branch_direction[0] * length_scale,
                             mid_point[1] + branch_direction[1] * length_scale)

                segment_list.append(LightningSegment(mid_point, split_end, segment.brightness * 0.5))

        offset_amount /= 2.0

    return segment_list


class PickingCardLightningBorderFrame2(OpenGLFrame):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self.unit_card_list = []
        self.selected_object = None
        self.drag_start = None

        print("Picking Action LightningBorder2")

        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        self.width = screen_width
        self.height = screen_height

        first_unit = Card(local_translation=(100, 100))
        first_unit.init_card(6)

        self.unit_card_list.append(first_unit)

        second_unit = Card(local_translation=(400, 400))
        second_unit.init_card(8)

        self.unit_card_list.append(second_unit)

        self.bind("<B1-Motion>", self.on_canvas_drag)
        self.bind("<ButtonRelease-1>", self.on_canvas_release)
        self.bind("<Button-1>", self.on_canvas_click)
        self.bind("<Configure>", self.on_resize)

    def initgl(self):
        print("Initializing OpenGL")

        glClearColor(1.0, 1.0, 1.0, 0.0)
        glOrtho(0, self.width, self.height, 0, -1, 1)

    def toggle_visibility(self):
        for unit_card in self.unit_card_list:
            tool_card = unit_card.get_tool_card()
            tool_card.set_visible(not tool_card.get_visible())

            pickable_unit_card = unit_card.get()
            attached_shape_list = pickable_unit_card.get_attached_shapes()
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

        for unit_card in self.unit_card_list:
            attached_tool_card = unit_card.get_tool_card()
            attached_tool_card.draw()

            pickable_unit_card_base = unit_card.get_pickable_card_base()
            pickable_unit_card_base.draw()

            attached_shape_list = pickable_unit_card_base.get_attached_shapes()

            for attached_shape in attached_shape_list:
                attached_shape.draw()

        if self.selected_object:
            pickable_unit_card_base = self.selected_object.get_pickable_card_base()
            local_translation = pickable_unit_card_base.get_local_translation()

            # print(f"local_translation: {local_translation}")
            # print(f"pickable_unit_card_base.vertices[0][0] + local_translation[0]: {pickable_unit_card_base.vertices[0][0] + local_translation[0]}")
            # print(f"pickable_unit_card_base.vertices[0][1] + local_translation[1]: {pickable_unit_card_base.vertices[0][1] + local_translation[1]}")
            # print(f"pickable_unit_card_base.vertices[2][0] + local_translation[0]: {pickable_unit_card_base.vertices[2][0] + local_translation[0]}")
            # print(f"pickable_unit_card_base.vertices[2][1] + local_translation[1]: {pickable_unit_card_base.vertices[2][1] + local_translation[1]}")
            #
            # print(f"pickable_unit_card_base.vertices[0][0]: {pickable_unit_card_base.vertices[0][0]}")
            # print(f"pickable_unit_card_base.vertices[0][1]: {pickable_unit_card_base.vertices[0][1]}")
            # print(f"pickable_unit_card_base.vertices[2][0]: {pickable_unit_card_base.vertices[2][0]}")
            # print(f"pickable_unit_card_base.vertices[2][1]: {pickable_unit_card_base.vertices[2][1]}")

            lightning_start = (
                pickable_unit_card_base.vertices[0][0] + local_translation[0] - 50,
                pickable_unit_card_base.vertices[0][1] + local_translation[1] - 50
            )
            lightning_end = (
                pickable_unit_card_base.vertices[2][0] + local_translation[0] + 50,
                pickable_unit_card_base.vertices[0][1] + local_translation[1] - 50
            )

            lightning_segments = generate_lightning(
                (
                    pickable_unit_card_base.vertices[0][0] + local_translation[0] - 50,
                    pickable_unit_card_base.vertices[0][1] + local_translation[1] - 50
                ),
                (
                    pickable_unit_card_base.vertices[2][0] + local_translation[0] + 50,
                    pickable_unit_card_base.vertices[0][1] + local_translation[1] - 50
                ),
                10, 5, 0.2, 0.7)

            lightning_segments.extend(generate_lightning(
                (
                    pickable_unit_card_base.vertices[2][0] + local_translation[0] + 50,
                    pickable_unit_card_base.vertices[0][1] + local_translation[1] - 50
                ),
                (
                    pickable_unit_card_base.vertices[2][0] + local_translation[0] + 50,
                    pickable_unit_card_base.vertices[2][1] + local_translation[1] + 50
                ),
                10, 5, 0.2, 0.7))

            lightning_segments.extend(generate_lightning(
                (
                    pickable_unit_card_base.vertices[0][0] + local_translation[0] - 50,
                    pickable_unit_card_base.vertices[2][1] + local_translation[1] + 50
                ),
                (
                    pickable_unit_card_base.vertices[2][0] + local_translation[0] + 50,
                    pickable_unit_card_base.vertices[2][1] + local_translation[1] + 50
                ),
                10, 5, 0.2, 0.7))

            lightning_segments.extend(generate_lightning(
                (
                    pickable_unit_card_base.vertices[0][0] + local_translation[0] - 50,
                    pickable_unit_card_base.vertices[0][1] + local_translation[1] - 50
                ),
                (
                    pickable_unit_card_base.vertices[0][0] + local_translation[0] - 50,
                    pickable_unit_card_base.vertices[2][1] + local_translation[1] + 50
                ),
                10, 5, 0.2, 0.7))

            for segment in lightning_segments:
                self.draw_lightning_segment(segment)

        self.tkSwapBuffers()

    def draw_lightning_segment(self, segment):
        glLineWidth(3.0)
        neon_color = (0.0, 0.78, 0.34, segment.brightness)

        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

        glColor4fv(neon_color)

        glBegin(GL_LINE_STRIP)
        glVertex2f(segment.start[0], segment.start[1])
        glVertex2f(segment.end[0], segment.end[1])
        glEnd()

        glDisable(GL_BLEND)


    def on_canvas_drag(self, event):
        x, y = event.x, event.y
        print(f"x = {x}, y = {y}")
        y = self.winfo_reqheight() - y
        print(f"self.winfo_reqheight() - y = {y}")

        if self.selected_object and self.drag_start:
            print(f"selected_object: {self.selected_object}")
            pickable_unit = self.selected_object.get_pickable_card_base()
            print(f"pickable_unit: {pickable_unit}")

            dx = x - self.drag_start[0]
            dy = y - self.drag_start[1]
            print(f"dx = {dx}, dy = {dy}")
            print(f"drag_start: {self.drag_start}")
            dy *= -1

            print(f"pickable local translation: {pickable_unit.get_local_translation()}")

            for vx, vy in pickable_unit.vertices:
                print(f"vx = {vx}, vy = {vy}")

            new_vertices = [
                (vx + dx, vy + dy) for vx, vy in pickable_unit.vertices
            ]
            pickable_unit.update_vertices(new_vertices)

            tool_card = self.selected_object.get_tool_card()
            new_tool_card_vertices = [
                (vx + dx, vy + dy) for vx, vy in tool_card.vertices
            ]
            tool_card.update_vertices(new_tool_card_vertices)

            for attached_shape in pickable_unit.get_attached_shapes():
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

            for unit_card in self.unit_card_list:
                if isinstance(unit_card, Card):
                    unit_card.selected = False

            self.selected_object = None

            for unit_card in reversed(self.unit_card_list):
                print("find selected Pickable Rectangle")
                pickable_unit_card_base = unit_card.get_pickable_card_base()

                if pickable_unit_card_base.is_point_inside((x, y)):
                    print(f"pickable_unit_card_base.is_point_inside(x, y) pass")
                    unit_card.selected = not unit_card.selected
                    self.selected_object = unit_card
                    self.drag_start = (x, y)
                    print(f"Selected PickableRectangle at ({x}, {y})")
                    print(f"vertices: {pickable_unit_card_base.vertices[0][0]}, "
                          f"{pickable_unit_card_base.vertices[0][1]}, "
                          f"{pickable_unit_card_base.vertices[2][0]}, "
                          f"{pickable_unit_card_base.vertices[2][1]}")

                    break

            self.redraw()

        except Exception as e:
            print(f"Exception in on_canvas_click: {e}")
