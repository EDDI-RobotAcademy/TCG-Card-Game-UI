import abc


class TransmitterRepository(abc.ABC):

    @abc.abstractmethod
    def saveClientSocket(self, clientSocket):
        pass

    @abc.abstractmethod
    def saveUiIpcChannel(self, uiIpcChannel):
        pass

    # @abc.abstractmethod
    # def transmitCommand(self):
    #     pass


