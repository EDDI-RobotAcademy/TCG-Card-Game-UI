import abc


class AccountRegisterFrameService(abc.ABC):
    @abc.abstractmethod
    def createAccountRegisterUiFrame(self, rootWindow):
        pass

    @abc.abstractmethod
    def injectTransmitIpcChannel(self, transmitIpcChannel):
        pass

    @abc.abstractmethod
    def injectReceiveIpcChannel(self, receiveIpcChannel):
        pass
