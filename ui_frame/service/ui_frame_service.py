import abc


class UiFrameService(abc.ABC):
    @abc.abstractmethod
    def registerMainMenuUiFrame(self, mainMenuFrame):
        pass

    @abc.abstractmethod
    def createLoginUiFrame(self, rootWindow):
        pass
