import abc


class SelectRaceUiFrameRepository(abc.ABC):
    @abc.abstractmethod
    def createSelectRaceUiFrame(self, rootWindow):
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
