import abc


class BattleLobbyFrameService(abc.ABC):
    @abc.abstractmethod
    def createBattleLobbyUiFrame(self, rootWindow, switchFrameWithMenuName):
        pass

    @abc.abstractmethod
    def createBattleLobbyMyDeckButton(self, request):
        pass