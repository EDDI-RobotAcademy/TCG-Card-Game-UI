import abc

class FakeBattleFieldFrameService(abc.ABC):

    @abc.abstractmethod
    def createFakeBattleFieldFrame(self, rootWindow, switchFrameWithMenuName):
        pass

    @abc.abstractmethod
    def injectTransmitIpcChannel(self, transmitIpcChannel):
        pass

    @abc.abstractmethod
    def injectReceiveIpcChannel(self, receiveIpcChannel):
        pass