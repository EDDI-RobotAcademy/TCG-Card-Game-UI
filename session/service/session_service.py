import abc


class SessionService(abc.ABC):
    @abc.abstractmethod
    def save_session(self, redisTokenSessionInfo):
        pass


    