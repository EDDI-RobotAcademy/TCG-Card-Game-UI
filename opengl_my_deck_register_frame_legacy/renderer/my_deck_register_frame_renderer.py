from OpenGL import GL

class MyDeckRegisterFrameRenderer:
    def __init__(self, scene, window):
        self.scene = scene
        self.window = window

    def render(self):
        self.window.tkMakeCurrent()
        GL.glClear(GL.GL_COLOR_BUFFER_BIT | GL.GL_DEPTH_BUFFER_BIT)

        for shape in self.scene.shapes:
            self._render_shape(shape)

        self.window.tkSwapBuffers()

    def _render_shape(self, shape):
        shape.draw()