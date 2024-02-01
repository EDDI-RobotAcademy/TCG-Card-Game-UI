import abc

class Shape(abc.ABC):
    def __init__(self, master, canvas):
        self.master = master
        self.canvas = canvas
        self.images = []

    @abc.abstractmethod
    def draw(self):
        pass