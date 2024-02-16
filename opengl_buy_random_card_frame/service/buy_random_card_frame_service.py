import abc


class BuyRandomCardFrameService(abc.ABC):
    @abc.abstractmethod
    def createBuyRandomCardUiFrame(self, rootWindow, switchFrameWithMenuName):
        pass
