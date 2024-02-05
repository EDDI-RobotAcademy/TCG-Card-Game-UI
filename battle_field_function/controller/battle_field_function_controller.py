import abc


class BattleFieldFunctionController(abc.ABC):

    @abc.abstractmethod
    def callSurrender(self, switchFrameWithMenuName):
        pass

    @abc.abstractmethod
    def callShuffleDeck(self):
        pass

    @abc.abstractmethod
    def callFirstTurnDrawCard(self):
        pass

    @abc.abstractmethod
    def callDrawCard(self):
        pass

    @abc.abstractmethod
    def useCard(self, cardId):
        pass
