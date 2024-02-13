from opengl_pickable_shape.pickable_rectangle import PickableRectangle

class Field:
    __imagePath = None

    def __init__(self, local_translation=(0, 0), scale=1):
        self.shapes = []
        self.local_translation = local_translation
        self.scale = scale

    def get_field_shapes(self):
        return self.shapes
    def change_local_translation(self, _translation):
        self.local_translation = _translation

    def add_shape(self, shape):
        shape.local_translate(self.local_translation)
        self.shapes.append(shape)
    def create_pickable_field_rectangle(self, color, vertices, local_translation):
        pickable_field_base = PickableRectangle(color=color,
                                      local_translation=local_translation,
                                      vertices=vertices)
        self.add_shape(pickable_field_base)
        pickable_field_base.set_draw_gradient(True)
        return pickable_field_base

    def init_shapes(self):

        self.pickable_hand_deck_base = (
            self.create_pickable_field_rectangle(color=(0, 0, 0, 1.0),
                                            local_translation=self.local_translation,
                                            vertices=[(500, 290), (1000, 290), (1000, 490), (500, 490)]))