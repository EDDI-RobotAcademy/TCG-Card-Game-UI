import abc


class CardLeftUpRenderingRepository(abc.ABC):
    @abc.abstractmethod
    def createCardLeftUpRenderingFrame(self, rootWindow):
        pass