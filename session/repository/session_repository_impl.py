import os

from session.entity.session import Session
from session.repository.session_repository import SessionRepository


class SessionRepositoryImpl(SessionRepository):
    __instance = None

    __session = None
    __first_fake_session = None
    __second_fake_session = None

    __transmitIpcChannel = None
    __receiveIpcChannel = None

    SESSION_INFO_FILE_PATH = 'local_storage/session_info.txt'
    FIRST_FAKE_SESSION_INFO_FILE_PATH = 'local_storage/first_fake_session_info.txt'
    SECOND_FAKE_SESSION_INFO_FILE_PATH = 'local_storage/second_fake_session_info.txt'

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
        print("SessionRepositoryImpl: get_session_info() :", self.__session.get_session_id())

        return self.__session.get_session_id()

    def get_first_fake_session_info(self):
        return self.__first_fake_session.get_session_id()

    def get_second_fake_session_info(self):
        return self.__second_fake_session.get_session_id()

    def writeRedisTokenSessionInfoToFile(self, redisTokenSessionInfo):
        print("SessionRepositoryImpl: writeRedisTokenSessionInfoToFile()")

        self.__session = Session(redisTokenSessionInfo)

        try:
            with open(self.SESSION_INFO_FILE_PATH, 'w') as file:
                file.write(str(redisTokenSessionInfo))
        except Exception as e:
            print(f"파일에 세션 작성 중 에러 발생: {e}")

    def writeFirstFakeRedisTokenSessionInfoToFile(self, firstFakeRedisTokenSessionInfo):
        print("SessionRepositoryImpl: writeFirstFakeRedisTokenSessionInfoToFile()")

        self.__first_fake_session = Session(firstFakeRedisTokenSessionInfo)

        try:
            with open(self.FIRST_FAKE_SESSION_INFO_FILE_PATH, 'w') as file:
                file.write(str(firstFakeRedisTokenSessionInfo))
        except Exception as e:
            print(f"파일에 세션 작성 중 에러 발생: {e}")

    def writeSecondFakeRedisTokenSessionInfoToFile(self, secondFakeRedisTokenSessionInfo):
        print("SessionRepositoryImpl: writeSecondFakeRedisTokenSessionInfoToFile()")

        self.__second_fake_session = Session(secondFakeRedisTokenSessionInfo)

        try:
            with open(self.SECOND_FAKE_SESSION_INFO_FILE_PATH, 'w') as file:
                file.write(str(secondFakeRedisTokenSessionInfo))
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
        return self.__receiveIpcChannel.get()

    def injectTransmitIpcChannel(self, transmitIpcChannel):
        print("SessionRepositoryImpl: injectTransmitIpcChannel()")

        self.__transmitIpcChannel = transmitIpcChannel

    def injectReceiveIpcChannel(self, receiveIpcChannel):
        print("SessionRepositoryImpl: injectReceiveIpcChannel()")

        self.__receiveIpcChannel = receiveIpcChannel









