import abc


class CardPackFrameRepository(abc.ABC):
    @abc.abstractmethod
    def createCardPackFrame(self, rootWindow):
        pass
