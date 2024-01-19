import abc


class CardRightBottomRenderingRepository(abc.ABC):
    @abc.abstractmethod
    def createCardRightBottomRenderingFrame(self, rootWindow):
        pass