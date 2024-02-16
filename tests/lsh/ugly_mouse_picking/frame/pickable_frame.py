from OpenGL.GL import *
from OpenGL.GLU import *
import tkinter as tk
from pyopengltk import OpenGLFrame

class PickableFrame(OpenGLFrame):
    def __init__(self, master=None, renderer=None, **kwargs):
        super().__init__(master, **kwargs)
        self.renderer = renderer
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

        if self.renderer:
            self.renderer.render()

        self.tkSwapBuffers()

    def set_projection_matrix(self):
        glViewport(0, 0, self.winfo_reqwidth(), self.winfo_reqheight())
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluOrtho2D(0, self.winfo_reqwidth(), 0, self.winfo_reqheight())
        glMatrixMode(GL_MODELVIEW)

    def on_canvas_drag(self, event):
        x, y = event.x, event.y
        y = self.winfo_reqheight() - y

        if self.selected_object and self.drag_start:
            dx = x - self.drag_start[0]
            dy = y - self.drag_start[1]

            self.selected_object.update_position(self.selected_object.x + dx, self.selected_object.y + dy)
            self.drag_start = (x, y)
            self.redraw()

    def on_canvas_release(self, event):
        self.drag_start = None

    def on_canvas_click(self, event):
        x, y = event.x, event.y
        y = self.winfo_reqheight() - y

        for obj in self.renderer.objects:
            obj.selected = False

        self.selected_object = None

        for obj in reversed(self.renderer.objects):
            if obj.is_point_inside((x, y)):
                obj.selected = not obj.selected
                self.selected_object = obj
                self.drag_start = (x, y)
                break

        self.redraw()