from OpenGL import GL

class MyDeckRegisterFrameRenderer():
    def __init__(self, scene, window):
        self.scene = scene
        self.window = window
        self.transparent_rect_visible = False

    def render(self):
        self.window.tkMakeCurrent()
        GL.glClear(GL.GL_COLOR_BUFFER_BIT | GL.GL_DEPTH_BUFFER_BIT)

        if self.transparent_rect_visible:
            for rectangle in self.scene.my_deck_background:
                self._render_shape(rectangle)

            for text in self.scene.text_list:
                self._render_shape(text)

            for text_box in self.scene.text_box:
                self._render_shape(text_box)

            for button in self.scene.button_list:
                self._render_shape(button)

        self.window.tkSwapBuffers()

    def _render_shape(self, shape):
        shape.draw()