import abc


class TransmitterService(abc.ABC):
    @abc.abstractmethod
    def injectSocketClient(self, socketClient):
        pass

    @abc.abstractmethod
    def injectUiIpcChannel(self, uiIpcChannel):
        pass




