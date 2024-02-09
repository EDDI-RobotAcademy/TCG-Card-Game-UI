from opengl_pickable_shape.pickable_rectangle import PickableRectangle
from opengl_shape.rectangle import Rectangle


class TestField:
    __imagePath = None

    def __init__(self, local_translation=(0, 0), scale=1):
        self.shapes = []
        self.local_translation = local_translation
        self.scale = scale
        self.pickable_card_base = None

    def get_field_shapes(self):
        return self.shapes
    def change_local_translation(self, _translation):
        self.local_translation = _translation

    def get_pickable_card_base(self):
        return self.pickable_card_base

    def add_shape(self, shape):
        shape.local_translate(self.local_translation)
        self.shapes.append(shape)
    def create_field_rectangle(self, color, vertices, local_translation=(0,0)):
        # field_base = PickableRectangle(color=color,
        #                                vertices=vertices)
        # field_base.set_visible(True)
        # self.add_shape(field_base)

        pickable_field_base = PickableRectangle(color=color,
                                               local_translation=local_translation,
                                               vertices=vertices)
        self.add_shape(pickable_field_base)
        pickable_field_base.set_draw_gradient(True)
        return pickable_field_base

    def init_shapes(self):
        self.pickable_card_base = self.create_field_rectangle(color=(0.5, 0.5, 0.54, 0),
                                   vertices=[(50, 200), (730, 200), (730, 450), (50, 450)])

