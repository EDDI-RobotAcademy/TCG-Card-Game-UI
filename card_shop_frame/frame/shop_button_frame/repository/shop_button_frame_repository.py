import abc


class ShopButtonFrameRepository(abc.ABC):
    @abc.abstractmethod
    def createShopButtonFrame(self, rootWindow):
        pass

    @abc.abstractmethod
    def setRandomCardList(self, randomCardList):
        pass

    @abc.abstractmethod
    def getRandomCardList(self):
        pass
