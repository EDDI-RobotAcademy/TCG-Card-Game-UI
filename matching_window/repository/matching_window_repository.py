import abc


class MatchingWindowRepository(abc.ABC):

    @abc.abstractmethod
    def saveReceiveIpcChannel(self, receiveIpcChannel):
        pass

    @abc.abstractmethod
    def saveTransmitIpcChannel(self, transmitIpcChannel):
        pass

    @abc.abstractmethod
    def createMatchingWindowFrame(self, rootWindow):
        pass

    @abc.abstractmethod
    def requestMatching(self, request):
        pass

    @abc.abstractmethod
    def cancelMatching(self, request):
        pass

    @abc.abstractmethod
    def checkMatching(self, request):
        pass