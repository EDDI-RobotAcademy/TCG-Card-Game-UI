import abc


class ReceiverService(abc.ABC):
    @abc.abstractmethod
    def injectSocketClient(self, socketClient):
        pass

    @abc.abstractmethod
    def startToReceiveCommand(self):
        pass
