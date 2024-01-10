import abc


class UiFrameService(abc.ABC):
    @abc.abstractmethod
    def createMainUiFrame(self, rootWindow):
        pass

    @abc.abstractmethod
    def createLoginUiFrame(self, rootWindow):
        pass
