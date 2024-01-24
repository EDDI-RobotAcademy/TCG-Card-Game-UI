import abc


class LobbyMenuFrameRepository(abc.ABC):
    @abc.abstractmethod
    def createLobbyMenuFrame(self, rootWindow):
        pass

    @abc.abstractmethod
    def saveReceiveIpcChannel(self, receiveIpcChannel):
        pass

    @abc.abstractmethod
    def saveTransmitIpcChannel(self, transmitIpcChannel):
        pass

    @abc.abstractmethod
    def requestDeckNameList(self, deckNameRequest):
        pass

    @abc.abstractmethod
    def startMatch(self, startMatchingRequest):
        pass

    @abc.abstractmethod
    def checkMatching(self, checkMatchingRequest):
        pass