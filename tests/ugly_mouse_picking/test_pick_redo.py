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

            self.selected_object.update_position(self.selected_object.x + dx, self.selected_object.y + dy)
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

class PickableObject:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.selected = False

    def draw(self):
        if self.selected:
            glColor3f(1.0, 0.0, 0.0)
        else:
            glColor3f(0.0, 1.0, 0.0)

        glBegin(GL_QUADS)
        glVertex2f(self.x, self.y)
        glVertex2f(self.x + self.width, self.y)
        glVertex2f(self.x + self.width, self.y + self.height)
        glVertex2f(self.x, self.y + self.height)
        glEnd()

    def is_point_inside(self, point):
        return self.x <= point[0] <= self.x + self.width and self.y <= point[1] <= self.y + self.height

    def update_position(self, x, y):
        self.x = x
        self.y = y

class TestUglyAnimationFrame(unittest.TestCase):
    def test_animation_frame(self):
        root = tk.Tk()
        app = CustomOpenGLFrame(root, width=400, height=400, bg="white")
        app.objects = [PickableObject(100, 100, 50, 50), PickableObject(200, 200, 50, 50)]
        app.pack(fill=tk.BOTH, expand=tk.YES)
        app.mainloop()

if __name__ == '__main__':
    unittest.main()
