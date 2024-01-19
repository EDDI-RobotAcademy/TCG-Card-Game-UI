import abc


class CardRightBottomRenderingService(abc.ABC):
    @abc.abstractmethod
    def createCardRightBottomRenderingUiFrame(self, rootWindow):
        pass