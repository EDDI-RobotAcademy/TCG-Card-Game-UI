import abc


class LobbyMenuFrameController(abc.ABC):
    @abc.abstractmethod
    def switchFrameToBattleLobby(self, windowToDestroy):
        pass
