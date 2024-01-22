class ShapeDrawerScene:
    def __init__(self):
        self.shapes = []

    def add_shape(self, shape):
        self.shapes.append(shape)

    def get_shapes(self):
        return self.shapes

