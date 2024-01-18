from session.repository.session_repository_impl import SessionRepositoryImpl
from session.service.request.session_login_request import SessionLoginRequest
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

    def getSessionInfo(self):
        print("SessionRepositoryImpl: getSessionInfo()")

        return self.__sessionRepository.readRedisTokenSessionInfoToFile()

    def requestLoginWithSession(self):
        print("SessionRepositoryImpl: requestLoginWithSession()")
        sessionInfo = self.__sessionRepository.get_session_info()
        sessionLoginRequest = SessionLoginRequest(sessionInfo)

        return self.__sessionRepository.requestLoginWithSession(sessionLoginRequest)

    def injectTransmitIpcChannel(self, transmitIpcChannel):
        print("SessionRepositoryImpl: injectTransmitIpcChannel()")

        return self.__sessionRepository.injectTransmitIpcChannel(transmitIpcChannel)









