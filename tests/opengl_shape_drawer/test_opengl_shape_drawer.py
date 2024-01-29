import tkinter
import unittest

from pyopengltk import OpenGLFrame
from OpenGL import GL, GLU

from tests.opengl_shape_legacy.service.opengl_shape_service_impl import OpenglShapeDrawerServiceImpl


class TestFrame(OpenGLFrame):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)

        self.width = self.winfo_reqwidth()
        self.height = self.winfo_reqheight()

        self.bind("<Configure>", self.on_resize)

    def initgl(self):
        GL.glClearColor(1.0, 1.0, 1.0, 0.0)
        GL.glOrtho(0, self.width, self.height, 0, -1, 1)

    def redraw(self):
        self.tkMakeCurrent()
        print("Redraw method called")
        GL.glClear(GL.GL_COLOR_BUFFER_BIT | GL.GL_DEPTH_BUFFER_BIT)

        GL.glBegin(GL.GL_QUADS)
        GL.glColor4f(1.0, 0.0, 0.0, 1.0)
        GL.glVertex2f(100, 100)
        GL.glVertex2f(300, 100)
        GL.glVertex2f(300, 300)
        GL.glVertex2f(100, 300)
        GL.glEnd()

        self.tkSwapBuffers()

    def reshape(self, width, height):
        GL.glViewport(0, 0, width, height)
        GL.glMatrixMode(GL.GL_PROJECTION)
        GL.glLoadIdentity()
        GLU.gluOrtho2D(0, width, height, 0)
        GL.glMatrixMode(GL.GL_MODELVIEW)
        GL.glLoadIdentity()

    def on_resize(self, event):
        self.reshape(event.width, event.height)


class TestOpenGLShapeDrawer(unittest.TestCase):

    def test_opengl_shaper_create_rectangle(self):
        opengl_shape_drawer_service = OpenglShapeDrawerServiceImpl.getInstance()
        rectangle_id = opengl_shape_drawer_service.create_rectangle(
            color=(0.6, 0.4, 0.6, 1.0),
            vertices=[(0, 0), (350, 0), (350, 500), (0, 500)]
        )

        shape = opengl_shape_drawer_service.get_shape_drawer_scene()
        print(f"shape: {shape}")

        self.assertTrue(rectangle_id is not None)
        self.assertTrue(opengl_shape_drawer_service.get_shape_drawer_scene() is not None)

    def test_opengl_shaper_render_rectangle(self):
        root = tkinter.Tk()
        window = TestFrame(root, width=800, height=800)
        window.pack(fill=tkinter.BOTH, expand=1)

        window.initgl()

        root.mainloop()

    # Multi Frame 의 경우 고려할 사항이 많으므로 우선은 단일 프레임 전환을 고려함
    def test_opengl_shaper_render_multi_frames(self):
        root = tkinter.Tk()

        frame1 = TestFrame(root, width=400, height=400)
        frame1.pack(fill=tkinter.BOTH, expand=1)

        frame2 = TestFrame(root, width=400, height=400)
        frame2.pack(fill=tkinter.BOTH, expand=1)

        root.mainloop()


if __name__ == '__main__':
    unittest.main()