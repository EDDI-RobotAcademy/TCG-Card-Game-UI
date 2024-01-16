import abc


class ReceiverService(abc.ABC):
    @abc.abstractmethod
    def injectSocketClient(self, socketClient):
        pass

    @abc.abstractmethod
    def injectUiIpcChannel(self, uiIpcChannel):
        pass

    @abc.abstractmethod
    def startToReceiveCommand(self):
        pass
