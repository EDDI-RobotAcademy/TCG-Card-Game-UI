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
