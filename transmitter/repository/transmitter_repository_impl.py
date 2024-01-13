import json
import pickle
import time
import socket

from transmitter.repository.transmitter_repository import TransmitterRepository


class TransmitterRepositoryImpl(TransmitterRepository):
    __instance = None
    __clientSocket = None
    __uiIpcChannel = None

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
        print("TransmitterRepositoryImpl: saveClientSocket()")
        self.__clientSocket = clientSocket

    def saveUiIpcChannel(self, uiIpcChannel):
        print("TransmitterRepositoryImpl: saveIpcChannel()")
        self.__uiIpcChannel = uiIpcChannel

    def __blockToAcquireSocket(self):
        if self.__clientSocket is None:
            return True

        return False

    def transmitCommand(self):
        print("TransmitterRepositoryImpl: transmitCommand()")

        while self.__blockToAcquireSocket():
            time.sleep(0.5)

        socketObject = self.__clientSocket.getSocket()

        while True:
            try:
                transmitData = self.__uiIpcChannel.get()
                print(f"transmitData: {transmitData}")

                serializedData = json.dumps(transmitData.toDictionary())
                socketObject.sendall(serializedData.encode())

                # serializedData = pickle.dumps(transmitData)
                # socketObject.sendall(serializedData)

            except (socket.error, BrokenPipeError) as exception:
                print(f"사용자 연결 종료")
                return None

            except socket.error as exception:
                print(f"전송 중 에러 발생: str{exception}")

            except Exception as exception:
                print(f"transmitter: {str(exception)}")

            finally:
                time.sleep(0.5)






