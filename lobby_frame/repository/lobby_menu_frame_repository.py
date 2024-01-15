import abc


class LobbyMenuFrameRepository(abc.ABC):
    @abc.abstractmethod
    def createLobbyMenuFrame(self, rootWindow):
        pass
