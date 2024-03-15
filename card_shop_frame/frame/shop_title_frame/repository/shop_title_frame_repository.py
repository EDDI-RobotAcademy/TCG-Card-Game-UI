import abc


class ShopTitleFrameRepository(abc.ABC):
    @abc.abstractmethod
    def createShopTitleFrame(self, rootWindow):
        pass
