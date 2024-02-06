import abc


class CardShopMenuFrameService(abc.ABC):
    @abc.abstractmethod
    def createCardShopUiFrame(self, rootWindow, switchFrameWithMenuName):
        pass

