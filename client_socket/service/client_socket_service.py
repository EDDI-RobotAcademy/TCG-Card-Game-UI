import abc


class ClientSocketService(abc.ABC):
    @abc.abstractmethod
    def createClientSocket(self):
        pass

    @abc.abstractmethod
    def connectToTargetHost(self):
        pass


