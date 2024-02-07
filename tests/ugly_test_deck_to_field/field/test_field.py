from opengl_shape.rectangle import Rectangle


class TestField:
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
    def create_field_rectangle(self, color, vertices):
        field_base = Rectangle(color=color,
                                       vertices=vertices)
        field_base.set_visible(True)
        self.add_shape(field_base)

    def init_shapes(self):

        self.create_field_rectangle(color=(0.5, 0.5, 0.54, 0),
                                   vertices=[(50, 200), (730, 200), (730, 450), (50, 450)])