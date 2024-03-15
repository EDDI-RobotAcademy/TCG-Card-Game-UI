import abc


class ShopTitleFrameService(abc.ABC):
    @abc.abstractmethod
    def createShopTitleUiFrame(self, rootWindow, switchFrameWithMenuName):
        pass
