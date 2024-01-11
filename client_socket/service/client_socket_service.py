import abc


class ClientSocketService(abc.ABC):
    @abc.abstractmethod
    def createClientSocket(self, host, port):
        pass


