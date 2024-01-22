import abc


class CardRightUpRenderingRepository(abc.ABC):
    @abc.abstractmethod
    def createCardRightUpRenderingFrame(self, rootWindow):
        pass