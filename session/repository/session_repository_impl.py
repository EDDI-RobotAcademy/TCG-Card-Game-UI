from session.entity.session import Session
from session.repository.session_repository import SessionRepository


class SessionRepositoryImpl(SessionRepository):
    __instance = None
    __session = None

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

    def writeRedisTokenSessionInfoToFile(self, redisTokenSessionInfo):
        print("SessionRepositoryImpl: writeRedisTokenSessionInfoToFile()")

        self.__session = Session(redisTokenSessionInfo)

        try:
            with open(self.SESSION_INFO_FILE_PATH, 'w') as file:
                file.write(str(redisTokenSessionInfo))
        except Exception as e:
            print(f"파일에 세션 작성 중 에러 발생: {e}")




