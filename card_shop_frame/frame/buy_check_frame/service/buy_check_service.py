import abc


class BuyCheckService(abc.ABC):
    @abc.abstractmethod
    def createBuyCheckUiFrame(self, rootWindow, switchFrameWithMenuName):
        pass
