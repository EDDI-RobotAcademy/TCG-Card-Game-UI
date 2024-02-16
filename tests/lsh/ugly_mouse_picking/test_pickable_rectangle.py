import abc
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

            for obj in self.objects:
                obj.selected = False  # 모든 객체의 선택 상태를 해제

            self.selected_object = None

            for obj in reversed(self.objects):
                if obj.is_point_inside((x, y)):
                    obj.selected = not obj.selected  # 토글 형식으로 선택 상태를 변경
                    self.selected_object = obj
                    self.drag_start = (x, y)
                    print(f"Selected object at ({x}, {y})")  # 디버깅 메시지 추가
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

class PickableRectangle(Rectangle):
    def __init__(self, color, vertices, global_translation=(0, 0), local_translation=(0, 0), is_pickable=True):
        super().__init__(color, vertices, global_translation, local_translation, is_pickable)




class TestUglyAnimationFrame(unittest.TestCase):
    def test_animation_frame(self):
        root = tk.Tk()
        app = CustomOpenGLFrame(root, width=800, height=800, bg="white")

        app.objects = [
            PickableRectangle(color=(1.0, 0.0, 0.0, 1.0), vertices=[(100, 100), (150, 100), (150, 150), (100, 150)]),
            PickableRectangle(color=(0.0, 0.0, 1.0, 1.0), vertices=[(200, 200), (250, 200), (250, 250), (200, 250)])]

        app.pack(fill=tk.BOTH, expand=tk.YES)
        app.mainloop()

if __name__ == '__main__':
    unittest.main()
