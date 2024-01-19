import abc

class BattleRoomButtonService(abc.ABC):
    @abc.abstractmethod
    def generateBattleRoomButton(self, rootFrame):
        pass