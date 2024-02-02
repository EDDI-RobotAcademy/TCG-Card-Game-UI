from OpenGL import GL

class MyCardMainrameRenderer:
    def __init__(self, scene, window):
        self.scene = scene
        self.window = window

    def render(self):
        self.window.tkMakeCurrent()
        GL.glClear(GL.GL_COLOR_BUFFER_BIT | GL.GL_DEPTH_BUFFER_BIT)

        for image_element in self.scene.image_rectangle_element:
            self._render_shape(image_element)

        # 여기에 카드 덱 프레임, 나의 덱 프레임 사각형 들어 가야 함.

        # 나의 카드 텍스트
        for text in self.scene.text_render:
            self._render_shape(text[0])

        self.window.tkSwapBuffers()

    def _render_shape(self, shape):
        shape.draw()