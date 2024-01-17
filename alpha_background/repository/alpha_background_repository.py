import abc


class AlphaBackgroundRepository(abc.ABC):
    @abc.abstractmethod
    def createAlphaBackground(self, rootWindow):
        pass