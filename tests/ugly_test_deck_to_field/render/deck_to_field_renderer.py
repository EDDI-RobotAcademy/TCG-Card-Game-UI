from OpenGL import GL


class DeckToFieldRenderer:
    def __init__(self, deck_to_field_scene, window):
        self.deck_to_field_scene = deck_to_field_scene
        self.window = window
    def render(self):
        self.window.tkMakeCurrent()
        GL.glClear(GL.GL_COLOR_BUFFER_BIT | GL.GL_DEPTH_BUFFER_BIT)

        field_list = self.deck_to_field_scene.get_field()
        for field in field_list:
            field_shapes = field.get_field_shapes()
            for shape in field_shapes:
                self._render_shape(shape)

        card_list = self.deck_to_field_scene.get_card()
        for card in card_list:
            card_shapes = card.get_pickable_card_shapes()
            for shape in card_shapes:
                self._render_shape(shape)

        self.window.tkSwapBuffers()
    def _render_shape(self, shape):
        shape.draw()