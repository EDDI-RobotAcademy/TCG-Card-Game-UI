import abc


class UiFrameController(abc.ABC):
    @abc.abstractmethod
    def requestToCreateUiFrame(self):
        pass

    @abc.abstractmethod
    def requestToStartPrintGameUi(self):
        pass

    @abc.abstractmethod
    def requestToInjectTransmitIpcChannel(self, ipcChannel):
        pass

    @abc.abstractmethod
    def requestToInjectReceiveIpcChannel(self, ipcChannel):
        pass

    @abc.abstractmethod
    def requestToInjectMusicPlayIpcChannel(self, ipcChannel):
        pass
