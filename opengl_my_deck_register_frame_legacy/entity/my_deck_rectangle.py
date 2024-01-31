from opengl_shape.rectangle import Rectangle


class MyDeckRegisterRectangle:
    def __init__(self, local_translation=(0, 0)):
        self.local_translation = local_translation

    def create_my_deck_register_rectangle(self):
        my_deck_register_rectangle = Rectangle(
            color=(0.6, 0.4, 0.6, 1.0),
            vertices=[(0, 0), (600, 0), (600, 260), (0, 260)],
            local_translation=(20, 20))

        my_deck_register_rectangle.set_visible(True)

        return my_deck_register_rectangle