import abc


class ShopButtonFrameService(abc.ABC):
    @abc.abstractmethod
    def createShopButtonUiFrame(self, rootWindow, switchFrameWithMenuName):
        pass

    @abc.abstractmethod
    def findRace(self):
        pass

