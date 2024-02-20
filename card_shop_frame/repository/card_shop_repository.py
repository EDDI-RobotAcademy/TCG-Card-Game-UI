import abc


class CardShopMenuFrameRepository(abc.ABC):
    @abc.abstractmethod
    def createCardShopMenuFrame(self, rootWindow):
        pass

    @abc.abstractmethod
    def saveTransmitIpcChannel(self, transmitIpcChannel):
        pass

    @abc.abstractmethod
    def saveReceiveIpcChannel(self, receiveIpcChannel):
        pass

    @abc.abstractmethod
    def setRace(self, race):
        pass

    @abc.abstractmethod
    def getRace(self):
        pass

    @abc.abstractmethod
    def setMyMoney(self, myMoney):
        pass

    @abc.abstractmethod
    def getMyMoney(self):
        pass
