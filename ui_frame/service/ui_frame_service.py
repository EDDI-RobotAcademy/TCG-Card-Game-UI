import abc


class UiFrameService(abc.ABC):
    @abc.abstractmethod
    def switchFrameWithMenuName(self, menuName: str):
        pass

    @abc.abstractmethod
    def registerMainMenuUiFrame(self, mainMenuFrame):
        pass

    @abc.abstractmethod
    def registerLoginMenuUiFrame(self, loginMenuFrame):
        pass

    @abc.abstractmethod
    def registerAccountRegisterUiFrame(self, accountRegisterFrame):
        pass

    @abc.abstractmethod
    def registerLobbyMenuUiFrame(self, lobbyMenuFrame):
        pass

    @abc.abstractmethod
    def injectTransmitIpcChannel(self, transmitIpcChannel):
        pass
