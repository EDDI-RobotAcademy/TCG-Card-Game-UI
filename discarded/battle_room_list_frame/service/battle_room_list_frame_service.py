import abc


class BattleRoomListFrameService(abc.ABC):
    @abc.abstractmethod
    def createBattleRoomListUiFrame(self, rootWindow, switchFrameWithMenuName):
        pass
