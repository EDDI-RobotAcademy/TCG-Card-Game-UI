from opengl_pickable_shape.pickable_rectangle import PickableRectangle


class TestCard:
    def __init__(self, window, battle_field, local_translation=(0, 0), scale=1):
        self.shapes = []
        self.local_translation = local_translation
        self.scale = scale
        self.window = window
        self.battle_field = battle_field
        self.pickable_card_base = None
    def get_pickable_card_shapes(self):
        return self.shapes
    def get_pickable_card_base(self):
        return self.pickable_card_base
    def add_shape(self, shape):
        shape.local_translate(self.local_translation)
        self.shapes.append(shape)
    def create_pickable_card_rectangle(self, color, vertices, local_translation):
        pickable_card_base = PickableRectangle(color=color,
                                               local_translation=local_translation,
                                               vertices=vertices)
        self.add_shape(pickable_card_base)
        pickable_card_base.set_draw_gradient(True)
        return pickable_card_base
    def init_shapes(self):
        self.pickable_card_base = (self.create_pickable_card_rectangle(color=(0, 0, 0, 1.0),
                                                                       local_translation=self.local_translation,
                                                                       vertices=[(100, 500), (200, 500), (200, 700), (100, 700)]))

        self.pickable_card_base = (self.create_pickable_card_rectangle(color=(0, 0, 0, 1.0),
                                                                       local_translation=self.local_translation,
                                                                       vertices=[(220, 500), (320, 500), (320, 700), (220, 700)]))

        self.pickable_card_base = (self.create_pickable_card_rectangle(color=(0, 0, 0, 1.0),
                                                                       local_translation=self.local_translation,
                                                                       vertices=[(340, 500), (440, 500), (440, 700), (340, 700)]))

        self.pickable_card_base = (self.create_pickable_card_rectangle(color=(0, 0, 0, 1.0),
                                                                       local_translation=self.local_translation,
                                                                       vertices=[(460, 500), (560, 500), (560, 700), (460, 700)]))

        self.pickable_card_base = (self.create_pickable_card_rectangle(color=(0, 0, 0, 1.0),
                                                                       local_translation=self.local_translation,
                                                                       vertices=[(580, 500), (680, 500), (680, 700), (580, 700)]))

