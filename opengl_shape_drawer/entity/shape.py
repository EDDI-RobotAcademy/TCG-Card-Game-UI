import abc


class Shape(abc.ABC):
    id_counter = 0

    def __init__(self, color, vertices):
        self.id = Shape.generate_id()
        self.color = color
        self.vertices = vertices

    def get_shape_id(self):
        return self.id

    @staticmethod
    def generate_id():
        Shape.id_counter += 1
        return Shape.id_counter

    @abc.abstractmethod
    def draw(self):
        pass
