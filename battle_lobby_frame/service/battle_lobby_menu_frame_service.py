import abc


class BattleLobbyMenuFrameService(abc.ABC):
    @abc.abstractmethod
    def createBattleLobbyUiFrame(self, rootWindow, switchFrameWithMenuName):
        pass
