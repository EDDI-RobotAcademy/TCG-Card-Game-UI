from client_socket.entity.client_socket import ClientSocket
from client_socket.repository.client_socket_repository import ClientSocketRepository

from decouple import config

import socket


class ClientSocketRepositoryImpl(ClientSocketRepository):
    __instance = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
        return cls.__instance

    @classmethod
    def getInstance(cls):
        if cls.__instance is None:
            cls.__instance = cls()
        return cls.__instance

    def createClientSocket(self):
        socketObject = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__clientSocket = ClientSocket(config('TARGET_HOST'), int(config('TARGET_PORT')), socketObject)
        return self.__clientSocket

    def connectionToTargetHost(self):
        if not self.__clientSocket:
            self.createClientSocket(config('TARGET_HOST'), int(config('TARGET_PORT')))

        clientSocketObject = self.__clientSocket.getSocket()

        try:
            clientSocketObject.connect(
                (
                    self.__clientSocket.getHost(),
                    self.__clientSocket.getPort()
                )
            )

        except ConnectionRefusedError:
            print(f"{self.__clientSocket.getHost()}:{self.__clientSocket.getPort()} 에 연결 중 거절되었습니다")

        except Exception as exception:
            print(f"연결 중 에러 발생: {str(exception)}")

    