import abc


class CardLeftBottomRenderingRepository(abc.ABC):
    @abc.abstractmethod
    def createCardLeftBottomRenderingFrame(self, rootWindow):
        pass