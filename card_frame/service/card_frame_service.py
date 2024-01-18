import abc


class CardFrameService(abc.ABC):
    @abc.abstractmethod
    def createCardUiFrame(self, rootWindow, switchFrameWithMenuName):
        pass