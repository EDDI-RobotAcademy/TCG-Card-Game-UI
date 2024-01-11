from client_socket.repository.client_socket_repository_impl import ClientSocketRepositoryImpl
from client_socket.service.client_socket_service import ClientSocketService


class ClientSocketServiceImpl(ClientSocketService):
    __instance = None

    def __new__(cls, repository):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
            cls.__instance.__clientSocketRepository = ClientSocketRepositoryImpl.getInstance()
        return cls.__instance

    @classmethod
    def getInstance(cls, repository=None):
        if cls.__instance is None:
            cls.__instance = cls(repository)
        return cls.__instance

    def createClientSocket(self, host, port):
        return self.__clientSocketRepository.create(host, port)





