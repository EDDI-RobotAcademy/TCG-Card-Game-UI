import abc


class TransmitterRepository(abc.ABC):

    @abc.abstractmethod
    def saveClientSocket(self, clientSocket):
        pass

    @abc.abstractmethod
    def saveIpcChannel(self, ipcChannel):
        pass

    # @abc.abstractmethod
    # def transmitCommand(self):
    #     pass


