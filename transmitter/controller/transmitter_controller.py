import abc


class TransmitterController(abc.ABC):
    @abc.abstractmethod
    def requestToInjectSocketClient(self, socketClient):
        pass

    @abc.abstractmethod
    def requestToInjectUiIpcChannel(self, uiIpcChannel):
        pass

    @abc.abstractmethod
    def requestToTransmitCommand(self):
        pass




