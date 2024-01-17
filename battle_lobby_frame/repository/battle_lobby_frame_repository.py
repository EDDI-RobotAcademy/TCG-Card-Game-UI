import abc


class BattleLobbyFrameRepository(abc.ABC):
    @abc.abstractmethod
    def createBattleLobbyFrame(self, rootWindow):
        pass
