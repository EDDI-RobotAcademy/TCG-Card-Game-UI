import abc


class Shape(abc.ABC):
    def __init__(self, color, vertices, translation=(0, 0)):
        self.color = color
        self.vertices = vertices
        self.translation = translation

    def translate(self, translation):
        self.translation = (self.translation[0] + translation[0], self.translation[1] + translation[1])

    @abc.abstractmethod
    def draw(self):
        pass
