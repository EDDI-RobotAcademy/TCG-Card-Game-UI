import abc


class ReceiverRepository(abc.ABC):
    @abc.abstractmethod
    def saveClientSocket(self, clientSocket):
        pass

    @abc.abstractmethod
    def receiveCommand(self):
        pass

