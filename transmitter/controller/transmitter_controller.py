import abc


class TransmitterController(abc.ABC):
    @abc.abstractmethod
    def requestToInjectSocketClient(self, socketClient):
        pass


    