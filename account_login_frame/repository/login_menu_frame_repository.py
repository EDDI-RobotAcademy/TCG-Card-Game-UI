import abc


class LoginMenuFrameRepository(abc.ABC):
    @abc.abstractmethod
    def createLoginMenuFrame(self, rootWindow):
        pass

    @abc.abstractmethod
    def saveTransmitIpcChannel(self, transmitIpcChannel):
        pass

    @abc.abstractmethod
    def saveReceiveIpcChannel(self, receiveIpcChannel):
        pass

    @abc.abstractmethod
    def requestLogin(self, accountLoginRequest):
        pass

    