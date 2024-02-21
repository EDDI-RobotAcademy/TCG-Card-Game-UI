import abc


class BuyRandomCardFrameService(abc.ABC):
    @abc.abstractmethod
    def createBuyRandomCardUiFrame(self, rootWindow, switchFrameWithMenuName):
        pass


    @abc.abstractmethod
    def findRandomCardNumbers(self, card_numbers):
        pass