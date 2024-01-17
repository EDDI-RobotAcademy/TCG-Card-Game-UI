import abc


class CardFrameRepository(abc.ABC):
    @abc.abstractmethod
    def createCardFrame(self, rootWindow):
        pass