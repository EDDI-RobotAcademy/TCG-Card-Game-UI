import abc


class ShapeRepository(abc.ABC):
    @abc.abstractmethod
    def create_rectangle(self, color, vertices):
        pass
