import abc


class SessionRepository(abc.ABC):
    @abc.abstractmethod
    def writeRedisTokenSessionInfoToFile(self, redisTokenSessionInfo):
        pass

    @abc.abstractmethod
    def readRedisTokenSessionInfoToFile(self):
        pass

    @abc.abstractmethod
    def requestLoginWithSession(self, sessionLoginRequest):
        pass

    @abc.abstractmethod
    def injectTransmitIpcChannel(self, transmitIpcChannel):
        pass


    