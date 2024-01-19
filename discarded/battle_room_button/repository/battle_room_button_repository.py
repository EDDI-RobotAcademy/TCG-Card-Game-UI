import abc

class BattleRoomButtonRepository(abc.ABC):
    @abc.abstractmethod
    def createBattleRoomButton(self, rootFrame):
        pass