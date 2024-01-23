import abc

class BattleLobbyFrameController(abc.ABC):
    @abc.abstractmethod
    def createDeckButtons(self, response):
        pass