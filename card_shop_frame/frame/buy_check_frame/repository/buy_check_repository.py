import abc


class BuyCheckRepository(abc.ABC):
    @abc.abstractmethod
    def createBuyCheckFrame(self, rootWindow):
        pass
