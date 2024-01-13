import abc


class UiFrameService(abc.ABC):
    @abc.abstractmethod
    def switchFrameWithMenuName(self, menuName: str):
        pass

    @abc.abstractmethod
    def registerMainMenuUiFrame(self, mainMenuFrame):
        pass

    @abc.abstractmethod
    def registerLoginMenuUiFrame(self, rootWindow):
        pass

    @abc.abstractmethod
    def injectTransmitIpcChannel(self, transmitIpcChannel):
        pass
