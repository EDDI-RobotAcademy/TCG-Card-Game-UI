import abc


class BattleLobbyFrameService(abc.ABC):
    @abc.abstractmethod
    def createBattleLobbyUiFrame(self, rootWindow, switchFrameWithMenuName):
        pass
