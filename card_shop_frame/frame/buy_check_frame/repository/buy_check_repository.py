import abc


class BuyCheckRepository(abc.ABC):
    @abc.abstractmethod
    def createBuyCheckFrame(self, rootWindow):
        pass

    @abc.abstractmethod
    def requestUseGameMoney(self, UseGameMoneyRequest):
        pass

    @abc.abstractmethod
    def requestBuyRandomCard(self, buyRandomCardRequest):
        pass

    @abc.abstractmethod
    def saveTransmitIpcChannel(self, transmitIpcChannel):
        pass

    @abc.abstractmethod
    def saveReceiveIpcChannel(self, receiveIpcChannel):
        pass

    @abc.abstractmethod
    def setRandomCardList(self, randomCardList):
        pass

    @abc.abstractmethod
    def getRandomCardList(self):
        pass
