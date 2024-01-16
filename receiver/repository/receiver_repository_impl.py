import time
import socket

from receiver.repository.receiver_repository import ReceiverRepository


class ReceiverRepositoryImpl(ReceiverRepository):
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

    def __blockToAcquireSocket(self):
        if self.__clientSocket is None:
            return True

        return False

    def saveClientSocket(self, clientSocket):
        print("ReceiverRepositoryImpl: saveClientSocket()")
        self.__clientSocket = clientSocket

    def receiveCommand(self):
        print("ReceiverRepositoryImpl: receiveCommand()")

        while self.__blockToAcquireSocket():
            time.sleep(0.5)

        socketObject = self.__clientSocket.getSocket()

        while True:
            try:
                data = socketObject.recv(1024)

                if not data:
                    socketObject.close()
                    break

                decodedData = data.decode()
                print("\033[91m수신된 정보:\033[0m\033[92m", decodedData)

            except (socket.error, BrokenPipeError) as exception:
                print(f"사용자 연결 종료")
                return None

            except socket.error as exception:
                print(f"전송 중 에러 발생: str{exception}")

            except Exception as exception:
                print(f"transmitter: {str(exception)}")

            finally:
                time.sleep(0.5)





