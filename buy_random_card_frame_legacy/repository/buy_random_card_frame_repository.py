import abc


class BuyRandomCardFrameRepository(abc.ABC):
    @abc.abstractmethod
    def createBuyRandomCardFrame(self, rootWindow):
        pass

    @abc.abstractmethod
    def saveTransmitIpcChannel(self, transmitIpcChannel):
        pass

    @abc.abstractmethod
    def saveReceiveIpcChannel(self, receiveIpcChannel):
        pass

    @abc.abstractmethod
    def requestBuyRandomCard(self, buyRandomCardRequest):
        pass
