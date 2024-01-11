import abc


class ClientSocketRepository(abc.ABC):
    @abc.abstractmethod
    def createClientSocket(self, host, port):
        pass


