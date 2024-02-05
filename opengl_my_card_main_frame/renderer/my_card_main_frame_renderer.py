from OpenGL import GL

class MyCardMainFrameRenderer:
    def __init__(self, scene, window):
        self.scene = scene
        self.window = window

    def render(self):
        self.window.tkMakeCurrent()
        GL.glClear(GL.GL_COLOR_BUFFER_BIT | GL.GL_DEPTH_BUFFER_BIT)

        # 배경 및 사이드에 있는 나의 덱 화면
        for image_element in self.scene.my_card_background:
            self._render_shape(image_element)

        # 나의 카드 텍스트
        for text in self.scene.text_list:
            self._render_shape(text)

        for button in self.scene.buttons_list:
            self._render_shape(button)

        self.window.tkSwapBuffers()

    def _render_shape(self, shape):
        shape.draw()