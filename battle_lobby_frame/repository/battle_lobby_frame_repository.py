import abc


class BattleLobbyFrameRepository(abc.ABC):
    @abc.abstractmethod
    def createBattleLobbyFrame(self, rootWindow):
        pass

    @abc.abstractmethod
    def getDeckList(self):
        pass

    @abc.abstractmethod
    def addDeckToDeckList(self, deck):
        pass

    @abc.abstractmethod
    def selectDeck(self, deck):
        pass

    @abc.abstractmethod
    def enterToRandomMatchingBattle(self,request):
        pass

    @abc.abstractmethod
    def exitBattleLobby(self, switchFrameWithMenuName):
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