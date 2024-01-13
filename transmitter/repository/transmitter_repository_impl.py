import time

from transmitter.repository.transmitter_repository import TransmitterRepository


class TransmitterRepositoryImpl(TransmitterRepository):
    __instance = None
    __clientSocket = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
        return cls.__instance

    @classmethod
    def getInstance(cls):
        if cls.__instance is None:
            cls.__instance = cls()
        return cls.__instance

    def saveClientSocket(self, clientSocket):
        self.__clientSocket = clientSocket

    # def __blockToAcquireSocket(self):
    #     if self.__clientSocket is None:
    #         return True
    #
    #     return False
    #
    # def transmitCommand(self):
    #     while self.__blockToAcquireSocket():
    #         time.sleep(0.5)







