import abc


class AccountRegisterFrameRepository(abc.ABC):
    @abc.abstractmethod
    def createAccountRegisterFrame(self, rootWindow):
        pass

    @abc.abstractmethod
    def saveTransmitIpcChannel(self, transmitIpcChannel):
        pass

    @abc.abstractmethod
    def saveReceiveIpcChannel(self, receiveIpcChannel):
        pass

