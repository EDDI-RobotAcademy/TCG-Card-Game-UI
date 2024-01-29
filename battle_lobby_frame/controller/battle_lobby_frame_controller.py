import abc

class BattleLobbyFrameController(abc.ABC):
    @abc.abstractmethod
    def createDeckButtons(self, response, switchFrameWithMenuName):
        pass

    @abc.abstractmethod
    def startCheckTime(self):
        pass