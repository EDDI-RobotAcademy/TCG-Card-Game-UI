import abc


class CardLeftUpRenderingService(abc.ABC):
    @abc.abstractmethod
    def createCardLeftUpRenderingUiFrame(self, rootWindow):
        pass