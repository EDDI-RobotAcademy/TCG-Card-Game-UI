import abc


class Shape(abc.ABC):
    def __init__(self, color, vertices):
        self.color = color
        self.vertices = vertices

    @abc.abstractmethod
    def draw(self):
        pass
