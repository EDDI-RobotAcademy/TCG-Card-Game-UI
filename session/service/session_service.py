import abc


class SessionService(abc.ABC):
    @abc.abstractmethod
    def save_session(self, redisTokenSessionInfo):
        pass

    @abc.abstractmethod
    def getSessionInfo(self):
        pass

    @abc.abstractmethod
    def requestLoginWithSession(self):
        pass

    @abc.abstractmethod
    def injectTransmitIpcChannel(self, transmitIpcChannel):
        pass

    @abc.abstractmethod
    def injectReceiveIpcChannel(self, receiveIpcChannel):
        pass


