import abc


class LobbyMenuFrameService(abc.ABC):
    @abc.abstractmethod
    def createLobbyUiFrame(self, rootWindow, switchFrameWithMenuName):
        pass

    @abc.abstractmethod
    def injectTransmitIpcChannel(self, transmitIpcChannel):
        pass
    @abc.abstractmethod
    def injectReceiveIpcChannel(self, receiveIpcChannel):
        pass

    @abc.abstractmethod
    def switchToBattleLobby(self, windowToDestroy):
        pass