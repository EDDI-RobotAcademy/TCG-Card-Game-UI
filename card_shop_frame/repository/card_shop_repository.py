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
