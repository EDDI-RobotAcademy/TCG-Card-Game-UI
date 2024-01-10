import abc


class MainMenuFrameRepository(abc.ABC):
    @abc.abstractmethod
    def createMainMenuFrame(self, rootWindow):
        pass

    