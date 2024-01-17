from session.repository.session_repository_impl import SessionRepositoryImpl
from session.service.session_service import SessionService


class SessionServiceImpl(SessionService):
    __instance = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
            cls.__instance.__sessionRepository = SessionRepositoryImpl.getInstance()
        return cls.__instance

    @classmethod
    def getInstance(cls):
        if cls.__instance is None:
            cls.__instance = cls()
        return cls.__instance

    def save_session(self, redisTokenSessionInfo):
        print("SessionRepositoryImpl: save_session()")

        self.__sessionRepository.writeRedisTokenSessionInfoToFile(redisTokenSessionInfo)






