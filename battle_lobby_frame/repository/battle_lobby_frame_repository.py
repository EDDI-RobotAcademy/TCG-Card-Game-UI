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
    def setDeckToDeckList(self, i, deck):
        pass

    @abc.abstractmethod
    def removeDeckFromDeckList(self, deck):
        pass

    @abc.abstractmethod
    def selectDeck(self, deck):
        pass

    @abc.abstractmethod
    def enterToRandomMatchingBattle(self):
        pass
