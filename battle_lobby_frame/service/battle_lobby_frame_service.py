import abc


class BattleLobbyFrameService(abc.ABC):
    @abc.abstractmethod
    def createBattleLobbyUiFrame(self, rootWindow, switchFrameWithMenuName):
        pass

    @abc.abstractmethod
    def createBattleLobbyMyDeckButton(self, request):
        pass

    @abc.abstractmethod
    def injectTransmitIpcChannel(self, transmitIpcChannel):
        pass

    @abc.abstractmethod
    def injectReceiveIpcChannel(self, receiveIpcChannel):
        pass
