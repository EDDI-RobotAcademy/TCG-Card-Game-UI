import abc


class CardRandomFrameService(abc.ABC):
    @abc.abstractmethod
    def createCardRandomUiFrame(self, rootWindow, switchFrameWithMenuName):
        pass