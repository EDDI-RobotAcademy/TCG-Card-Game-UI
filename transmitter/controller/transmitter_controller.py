import abc


class TransmitterController(abc.ABC):
    @abc.abstractmethod
    def requestToInjectSocketClient(self, socketClient):
        pass

    @abc.abstractmethod
    def requestToInjectIpcChannel(self, ipcChannel):
        pass


