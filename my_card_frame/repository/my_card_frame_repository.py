import abc


class MyCardFrameRepository(abc.ABC):
    @abc.abstractmethod
    def createMyCardFrame(self, rootWindow):
        pass
