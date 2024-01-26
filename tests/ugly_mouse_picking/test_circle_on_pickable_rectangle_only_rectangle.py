import abc
import math
import random

from OpenGL.GL import *
from OpenGL.GLU import *
import tkinter as tk
from pyopengltk import OpenGLFrame
import unittest

class CustomOpenGLFrame(OpenGLFrame):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self.objects = []
        self.selected_object = None
        self.drag_start = None

        self.bind("<B1-Motion>", self.on_canvas_drag)
        self.bind("<ButtonRelease-1>", self.on_canvas_release)
        self.bind("<Configure>", self.redraw)
        self.bind("<Button-1>", self.on_canvas_click)

    def initgl(self):
        glEnable(GL_DEPTH_TEST)
        self.set_projection_matrix()

    def tkExpose(self, event):
        self.initgl()
        self.redraw()

    def redraw(self, event=None):
        self.tkMakeCurrent()
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()

        for obj in self.objects:
            obj.draw()

        self.tkSwapBuffers()

    def set_projection_matrix(self):
        glViewport(0, 0, self.winfo_reqwidth(), self.winfo_reqheight())
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluOrtho2D(0, self.winfo_reqwidth(), 0, self.winfo_reqheight())
        glMatrixMode(GL_MODELVIEW)

    def on_canvas_drag(self, event):
        x, y = event.x, event.y
        y = self.winfo_reqheight() - y  # Flip y coordinate to match OpenGL coordinate system

        if self.selected_object and self.drag_start:
            dx = x - self.drag_start[0]
            dy = y - self.drag_start[1]

            new_vertices = [
                (vx + dx, vy + dy) for vx, vy in self.selected_object.vertices
            ]

            self.selected_object.update_vertices(new_vertices)
            self.drag_start = (x, y)
            self.redraw()

    def on_canvas_release(self, event):
        self.drag_start = None

    def on_canvas_click(self, event):
        print(f"on_canvas_click: {event}")
        try:
            x, y = event.x, event.y
            y = self.winfo_reqheight() - y  # Flip y coordinate to match OpenGL coordinate system
            print(f"Adjusted coordinates: x={x}, y={y}")

            for obj in self.objects:
                if isinstance(obj, PickableRectangle):
                    obj.selected = False  # 모든 PickableRectangle 객체의 선택 상태를 해제

            self.selected_object = None

            for obj in reversed(self.objects):
                if isinstance(obj, PickableRectangle) and obj.is_point_inside((x, y)):
                    obj.selected = not obj.selected  # 토글 형식으로 선택 상태를 변경
                    self.selected_object = obj
                    self.drag_start = (x, y)
                    print(f"Selected PickableRectangle at ({x}, {y})")  # 디버깅 메시지 추가
                    break

            self.redraw()
        except Exception as e:
            print(f"Exception in on_canvas_click: {e}")

class Shape(abc.ABC):
    def __init__(self, vertices, color=(1.0, 1.0, 1.0, 1.0), global_translation=(0, 0), local_translation=(0, 0), is_pickable=False):
        self.vertices = vertices
        self.global_translation = global_translation
        self.local_translation = local_translation
        self.translation = self.local_translation + self.global_translation
        self.is_pickable = is_pickable
        self.color = color

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
        print("is_point_inside() - self.vertices:", self.vertices)
        print("is_point_inside() - self.vertices[0][0]:", self.vertices[0][0])
        print("is_point_inside() - self.vertices[0][1]:", self.vertices[0][1])
        print("is_point_inside() - self.vertices[2][0]:", self.vertices[2][0])
        print("is_point_inside() - self.vertices[2][1]:", self.vertices[2][1])
        x, y = point

        print("x, y")
        if not (self.vertices[0][0] + self.global_translation[0] + self.local_translation[0] <= x <=
                self.vertices[-2][0] + self.global_translation[0] + self.local_translation[0] and
                self.vertices[0][1] + self.global_translation[1] + self.local_translation[1] <= y <=
                self.vertices[-2][1] + self.global_translation[1] + self.local_translation[1]):
            return False

        winding_number = 0
        j = len(self.vertices) - 1
        print(f"is it ok ? len(self.vertices): {j}")
        for i in range(len(self.vertices)):
            print("is_point_inside() range is ok ?")
            if i < len(self.vertices):
                x1, y1 = self.vertices[j]
                x2, y2 = self.vertices[i]
                print(f"Checking edge {i}: ({x1}, {y1}) - ({x2}, {y2})")

                if y1 + self.global_translation[1] + self.local_translation[1] <= y < y2 + self.global_translation[1] + \
                        self.local_translation[1] or \
                        y2 + self.global_translation[1] + self.local_translation[1] <= y < y1 + self.global_translation[
                    1] + self.local_translation[1]:
                    print("Checking intersection")
                    if x1 + self.global_translation[0] + self.local_translation[0] + (
                            y - y1 - self.global_translation[1] - self.local_translation[1]) / (
                            y2 - y1) * (x2 - x1) > x:
                        winding_number = 1 - winding_number

                j = i

        print("finish is_point_inside()")
        return winding_number == 1

    def update_position(self, x, y):
        new_global_translation = (self.global_translation[0] + x, self.global_translation[1] + y)
        self.global_translate(new_global_translation)
        new_vertices = [(vx + x, vy + y) for vx, vy in self.vertices]
        self.update_vertices(new_vertices)

    def update_vertices(self, new_vertices):
        self.vertices = new_vertices

    @abc.abstractmethod
    def draw(self):
        pass

    def update_position(self, x, y):
        new_global_translation = (self.global_translation[0] + x, self.global_translation[1] + y)
        self.global_translate(new_global_translation)


class Rectangle(Shape):
    def __init__(self, color, vertices, global_translation=(0, 0), local_translation=(0, 0), is_pickable=False):
        super().__init__(vertices, color, global_translation, local_translation, is_pickable)
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

    def move(self, dx, dy):
        self.vertices[0] = (self.vertices[0][0] + dx, self.vertices[0][1] + dy)

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


class PickableRectangle(Rectangle):
    def __init__(self, color, vertices, global_translation=(0, 0), local_translation=(0, 0), is_pickable=True):
        super().__init__(color, vertices, global_translation, local_translation, is_pickable)

    def move(self, dx, dy):
        for i in range(len(self.vertices)):
            self.vertices[i] = (self.vertices[i][0] + dx, self.vertices[i][1] + dy)


class ObjectComposition:
    def __init__(self, local_translation=(0, 0), unit_id=None):
        self.shapes = []
        self.local_translation = local_translation
        self.id = unit_id

    def move_all_objects(self, dx, dy):
        for obj in self.shapes:
            obj.move(dx, dy)

    def change_local_translation(self, _translation):
        self.local_translation = _translation

    def get_object_shapes(self):
        return self.shapes

    def add_shape(self, shape):
        shape.local_translate(self.local_translation)
        self.shapes.append(shape)

    def create_base_pickable_rectangle(self, color, vertices):
        pickable_base = PickableRectangle(color=color,
                                           vertices=vertices,
                                           is_pickable=True)
        pickable_base.set_draw_gradient(True)
        self.add_shape(pickable_base)

    def create_attached_circle(self, color, center, radius):
        attached_circle = Circle(color=color,
                                 center=center,
                                 radius=radius)
        self.add_shape(attached_circle)

    def create_composition_object(self):
        self.create_base_pickable_rectangle(color=(0.0, 0.78, 0.34, 1.0),
                                            vertices=[(0, 0), (50, 0), (50, 150), (0, 150)])

        circle_radius = 15
        self.create_attached_circle(color=(1.0, 0.33, 0.34, 1.0),
                                    center=(0, 0),
                                    radius=circle_radius)


class TestUglyAnimationFrame(unittest.TestCase):
    def test_animation_frame(self):
        root = tk.Tk()
        app = CustomOpenGLFrame(root, width=800, height=800, bg="white")

        composition1 = ObjectComposition(local_translation=(100, 100), unit_id=1)
        composition1.create_composition_object()

        composition2 = ObjectComposition(local_translation=(400, 400), unit_id=2)
        composition2.create_composition_object()

        app.objects = composition1.get_object_shapes() + composition2.get_object_shapes()

        app.pack(fill=tk.BOTH, expand=tk.YES)
        app.mainloop()

if __name__ == '__main__':
    unittest.main()
