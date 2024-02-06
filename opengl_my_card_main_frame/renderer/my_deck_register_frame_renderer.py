from OpenGL import GL

class MyDeckRegisterFrameRenderer():
    def __init__(self, scene, window):
        self.scene = scene
        self.window = window
        self.transparent_rect_visible = False

    def render(self):
        self.window.tkMakeCurrent()
        GL.glClear(GL.GL_COLOR_BUFFER_BIT | GL.GL_DEPTH_BUFFER_BIT)
        print(1)
        if self.transparent_rect_visible:
            print(2)
            for rectangle in self.scene.my_deck_background:
                print(rectangle)
                self._render_shape(rectangle)
            print(3)
            for text in self.scene.text_list:
                print(text)
                self._render_shape(text)
            print(4)
            for text_box in self.scene.text_box:
                print(text_box)
                self._render_shape(text_box)
            print(5)
            for button in self.scene.button_list:
                print(button)
                self._render_shape(button)
            print(6)
        self.window.tkSwapBuffers()

    def _render_shape(self, shape):
        shape.draw()