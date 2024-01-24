import abc


class BattleLobbyFrameRepository(abc.ABC):
    @abc.abstractmethod
    def createBattleLobbyFrame(self, rootWindow):
        pass


    @abc.abstractmethod
    def addDeckToDeckList(self, deck):
        pass

    @abc.abstractmethod
    def addDeckIdToDeckIdList(self, deckId):
        pass

    @abc.abstractmethod
    def selectDeck(self, deck):
        pass

    @abc.abstractmethod
    def requestCardList(self, RequestDeckCardList):
        pass

    @abc.abstractmethod
    def exitBattleLobby(self):
        pass

    @abc.abstractmethod
    def saveTransmitIpcChannel(self, transmitIpcChannel):
        pass

    @abc.abstractmethod
    def saveReceiveIpcChannel(self, receiveIpcChannel):
        pass

    @abc.abstractmethod
    def getCurrentDeckIndex(self):
        pass