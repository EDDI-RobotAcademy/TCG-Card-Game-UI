import abc


class LobbyMenuFrameService(abc.ABC):
    @abc.abstractmethod
    def createLobbyUiFrame(self, rootWindow, switchFrameWithMenuName):
        pass
