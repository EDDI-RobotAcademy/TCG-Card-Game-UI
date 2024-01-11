from client_socket.entity.client_socket import ClientSocket
from client_socket.repository.client_socket_repository import ClientSocketRepository

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

    def createClientSocket(self, host, port):
        socketObject = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__clientSocket = ClientSocket(host, port, socketObject)
        return self.__clientSocket

    