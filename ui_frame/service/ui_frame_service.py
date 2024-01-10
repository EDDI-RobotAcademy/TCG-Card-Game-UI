import abc


class UiFrameService(abc.ABC):
    @abc.abstractmethod
    def registerMainMenuUiFrame(self, mainMenuFrame):
        pass

    @abc.abstractmethod
    def registerLoginMenuUiFrame(self, rootWindow):
        pass
