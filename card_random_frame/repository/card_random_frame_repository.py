import abc


class CardRandomFrameRepository(abc.ABC):
    @abc.abstractmethod
    def createCardRandomFrame(self, rootWindow):
        pass