import unittest
from OpenGL.GL import *
from OpenGL.GLU import *
import tkinter as tk
from pyopengltk import OpenGLFrame

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

class PickableOpenGLFrame(OpenGLFrame):
    def __init__(self, master=None, **kwargs):
        OpenGLFrame.__init__(self, master, **kwargs)
        self.objects = [PickableObject(100, 100, 50, 50), PickableObject(200, 200, 50, 50)]
        self.selected_object = None
        self.drag_start = None

        self.glcanvas = self.create_gl_canvas()
        self.initgl()

        self.glcanvas.pack(fill=tk.BOTH, expand=tk.YES)
        self.bind_events()

    def create_gl_canvas(self):
        glcanvas = OpenGLFrame(self, width=400, height=400, bg="white")
        glcanvas.bind("<B1-Motion>", self.on_canvas_drag)
        glcanvas.bind("<ButtonRelease-1>", self.on_canvas_release)
        return glcanvas

    # def initgl(self):
    #     GL.glClearColor(0.8706, 0.7216, 0.5294, 0)
    #     GL.glEnable(GL.GL_BLEND)
    #     GL.glBlendFunc(GL.GL_SRC_ALPHA, GL.GL_ONE_MINUS_SRC_ALPHA)
    #     GL.glLoadIdentity()
    #     GLU.gluOrtho2D(0, self.alpha_background_entity.width, self.alpha_background_entity.height, 0)

    def initgl(self):
        glEnable(GL_DEPTH_TEST)
        self.set_projection_matrix()
        glLoadIdentity()
        self.redraw()

    def bind_events(self):
        self.glcanvas.bind("<Configure>", self.redraw)

    def redraw(self, event=None):
        self.draw_objects()

    def draw_objects(self):
        self.glcanvas.tkMakeCurrent()
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()

        for obj in self.objects:
            obj.draw()

        self.glcanvas.tkSwapBuffers()

    def set_projection_matrix(self):
        glViewport(0, 0, self.glcanvas.winfo_reqwidth(), self.glcanvas.winfo_reqheight())
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluOrtho2D(0, self.glcanvas.winfo_reqwidth(), 0, self.glcanvas.winfo_reqheight())
        glMatrixMode(GL_MODELVIEW)

    def on_canvas_drag(self, event):
        x, y = event.x, event.y
        y = self.glcanvas.winfo_reqheight() - y

        if self.selected_object and self.drag_start:
            dx = x - self.drag_start[0]
            dy = y - self.drag_start[1]

            self.selected_object.update_position(self.selected_object.x + dx, self.selected_object.y + dy)
            self.drag_start = (x, y)
            self.redraw()

    def on_canvas_release(self, event):
        x, y = event.x, event.y
        y = self.glcanvas.winfo_reqheight() - y

        self.drag_start = None

    def on_canvas_click(self, event):
        x, y = event.x, event.y
        y = self.glcanvas.winfo_reqheight() - y  # Flip y coordinate to match OpenGL coordinate system

        self.selected_object = None

        for obj in reversed(self.objects):
            if obj.is_point_inside((x, y)):
                self.selected_object = obj
                self.drag_start = (x, y)
                break

        self.redraw()

class TestUglyAnimationFrame(unittest.TestCase):

    def test_animation_frame(self):
        root = tk.Tk()
        app = PickableOpenGLFrame(root)
        app.pack(fill=tk.BOTH, expand=tk.YES)
        app.mainloop()

if __name__ == '__main__':
    unittest.main()
