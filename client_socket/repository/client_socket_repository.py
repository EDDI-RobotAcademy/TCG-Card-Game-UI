import abc


class ClientSocketRepository(abc.ABC):
    @abc.abstractmethod
    def createClientSocket(self):
        pass

    @abc.abstractmethod
    def connectionToTargetHost(self):
        pass


