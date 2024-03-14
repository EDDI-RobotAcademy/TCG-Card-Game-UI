import abc


class ShopButtonFrameService(abc.ABC):
    @abc.abstractmethod
    def createShopButtonUiFrame(self, rootWindow, switchFrameWithMenuName):
        pass


