from OpenGL import GL

from opengl_tomb import tomb


class BattleFieldFrameRenderer:
    def __init__(self, battle_field_scene, window):
        self.battle_field_scene = battle_field_scene
        self.window = window

    def render(self):
        self.window.tkMakeCurrent()
        GL.glClear(GL.GL_COLOR_BUFFER_BIT | GL.GL_DEPTH_BUFFER_BIT)

        unit_card_list = self.battle_field_scene.get_unit_card()
        for unit_card in unit_card_list:
            unit_shapes = unit_card.get_unit_shapes()
            for shape in unit_shapes:
                self._render_shape(shape)

        tomb_list = self.battle_field_scene.get_tomb()
        for tomb in tomb_list:
            tomb_shapes = tomb.get_tomb_shapes()
            for shape in tomb_shapes:
                self._render_shape(shape)

        self.window.tkSwapBuffers()

    def _render_shape(self, shape):
        shape.draw()