import abc


class MyDeckRegisterFrameService(abc.ABC):
    @abc.abstractmethod
    def createMyDeckRegisterUiFrame(self, rootWindow, switchFrameWithMenuName):
        pass

    @abc.abstractmethod
    def injectTransmitIpcChannel(self, transmitIpcChannel):
        pass

    @abc.abstractmethod
    def injectReceiveIpcChannel(self, receiveIpcChannel):
        pass
