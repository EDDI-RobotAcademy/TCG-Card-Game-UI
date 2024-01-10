import abc


class MainMenuFrameService(abc.ABC):
    @abc.abstractmethod
    def createMainUiFrame(self, rootWindow):
        pass

    