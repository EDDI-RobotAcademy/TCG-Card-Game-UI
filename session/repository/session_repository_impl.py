import os

from session.entity.session import Session
from session.repository.session_repository import SessionRepository


class SessionRepositoryImpl(SessionRepository):
    __instance = None
    __session = None
    __transmitIpcChannel = None

    SESSION_INFO_FILE_PATH = 'local_storage/session_info.txt'

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
        return cls.__instance

    @classmethod
    def getInstance(cls):
        if cls.__instance is None:
            cls.__instance = cls()
        return cls.__instance

    def get_session_info(self):
        print("SessionRepositoryImpl: get_session_info()")

        return self.__session.get_session_id()

    def writeRedisTokenSessionInfoToFile(self, redisTokenSessionInfo):
        print("SessionRepositoryImpl: writeRedisTokenSessionInfoToFile()")

        self.__session = Session(redisTokenSessionInfo)

        try:
            with open(self.SESSION_INFO_FILE_PATH, 'w') as file:
                file.write(str(redisTokenSessionInfo))
        except Exception as e:
            print(f"파일에 세션 작성 중 에러 발생: {e}")

    def readRedisTokenSessionInfoToFile(self):
        print("SessionRepositoryImpl: readRedisTokenSessionInfoToFile()")

        sessionInfoFilePath = os.path.join(os.getcwd(), self.SESSION_INFO_FILE_PATH)
        print(f"ConsoleUiRepository - infoFilePath: {sessionInfoFilePath}")

        if os.path.exists(sessionInfoFilePath):
            with open(sessionInfoFilePath, 'r') as file:
                content = file.read().strip()

                if content:
                    self.__session = Session(content)
                    return content
                else:
                    print(f"Missing session token")
                    return None
        else:
            with open(sessionInfoFilePath, 'w') as file:
                file.write("")
                return None

    def requestLoginWithSession(self, sessionLoginRequest):
        print("SessionRepositoryImpl: requestLoginWithSession()")

        self.__transmitIpcChannel.put(sessionLoginRequest)

    def injectTransmitIpcChannel(self, transmitIpcChannel):
        print("SessionRepositoryImpl: injectTransmitIpcChannel()")

        self.__transmitIpcChannel = transmitIpcChannel











