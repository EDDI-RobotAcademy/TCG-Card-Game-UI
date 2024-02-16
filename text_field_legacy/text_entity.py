import abc

class TextEntity(abc.ABC):
    def __init__(self, master, canvas):
        self.master = master
        self.canvas = canvas

    @abc.abstractmethod
    def draw(self):
        pass
