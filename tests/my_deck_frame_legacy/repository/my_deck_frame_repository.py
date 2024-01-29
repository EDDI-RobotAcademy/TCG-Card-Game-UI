import abc


class MyDeckFrameRepository(abc.ABC):
    @abc.abstractmethod
    def createMyDeckFrame(self, rootWindow):
        pass