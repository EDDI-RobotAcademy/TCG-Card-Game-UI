import abc


class BattleLobbyMenuFrameRepository(abc.ABC):
    @abc.abstractmethod
    def createBattleLobbyMenuFrame(self, rootWindow):
        pass
