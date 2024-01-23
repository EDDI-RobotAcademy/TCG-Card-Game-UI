import abc


class BattleFieldFrameRepository(abc.ABC):
    @abc.abstractmethod
    def drawBattleFieldFrame(self, rootWindow):
        pass


