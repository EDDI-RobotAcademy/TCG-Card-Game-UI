import abc


class MatchingWindowService(abc.ABC):

    @abc.abstractmethod
    def createMatchingWindow(self, rootWindow):
        pass

    @abc.abstractmethod
    def startMatching(self, rootWindow):
        pass

    @abc.abstractmethod
    def injectTransmitIpcChannel(self, transmitIpcChannel):
        pass

    @abc.abstractmethod
    def injectReceiveIpcChannel(self, receiveIpcChannel):
        pass