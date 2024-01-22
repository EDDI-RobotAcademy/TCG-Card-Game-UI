import abc


class CardRightUpRenderingService(abc.ABC):
    @abc.abstractmethod
    def createCardRightUpRenderingUiFrame(self, rootWindow):
        pass