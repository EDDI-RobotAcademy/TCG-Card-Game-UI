import abc


class SessionRepository(abc.ABC):
    @abc.abstractmethod
    def writeRedisTokenSessionInfoToFile(self, redisTokenSessionInfo):
        pass



    