from OpenGL import GL

class MyCardMainrameRendererAfterClickButton:
    def __init__(self, scene, window):
        self.scene = scene
        self.window = window
        self.transparent_rect_visible = False

    def render(self):
        self.window.tkMakeCurrent()
        GL.glClear(GL.GL_COLOR_BUFFER_BIT | GL.GL_DEPTH_BUFFER_BIT)

        if self.transparent_rect_visible:
            for rectangle in self.scene.alpha_rectangle:
                self._render_shape(rectangle)

            for text in self.scene.text_render:
                self._render_shape(text[1:])

            for text_box in self.scene.text_box:
                self._render_shape(text_box)


        self.window.tkSwapBuffers()

    def _render_shape(self, shape):
        shape.draw()