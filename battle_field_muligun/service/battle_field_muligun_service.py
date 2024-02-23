import abc

class BattleFieldMuligunFrameService(abc.ABC):

    @abc.abstractmethod
    def createBattleFieldMuligunFrame(self, rootWindow, switchFrameWithMenuName):
        pass

    @abc.abstractmethod
    def injectTransmitIpcChannel(self, transmitIpcChannel):
        pass

    @abc.abstractmethod
    def injectReceiveIpcChannel(self, receiveIpcChannel):
        pass