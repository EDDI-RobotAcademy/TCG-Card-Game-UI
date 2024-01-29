import abc


class UnitCard(abc.ABC):
    def __init__(self):
        self.shapes = []

    def add_shape(self, shape):
        self.shapes.append(shape)

    def set_shapes(self, shapes):
        self.shapes = shapes

