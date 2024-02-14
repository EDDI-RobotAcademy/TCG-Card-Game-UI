from OpenGL import GL

class MyDeckRegisterFrameRenderer:
    def __init__(self, scene, window):
        self.scene = scene
        self.window = window

    def render(self):
        self.window.tkMakeCurrent()

        for rectangle in self.scene.alpha_rectangle:
            self._render_shape(rectangle)

        for rectangle in self.scene.my_deck_background:
            self._render_shape(rectangle)

        for text in self.scene.text_list:
            self._render_shape(text)

        for button in self.scene.button_list:
            self._render_shape(button)

        self.window.tkSwapBuffers()

    def _render_shape(self, shape):
        shape.draw()