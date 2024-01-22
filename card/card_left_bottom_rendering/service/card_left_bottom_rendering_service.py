import abc


class CardLeftBottomRenderingService(abc.ABC):
    @abc.abstractmethod
    def createCardLeftBottomRenderingUiFrame(self, rootWindow):
        pass