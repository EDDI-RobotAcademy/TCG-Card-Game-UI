import abc


class BattleRoomListFrameRepository(abc.ABC):
    @abc.abstractmethod
    def createBattleRoomListFrame(self, rootWindow, request):
        pass
