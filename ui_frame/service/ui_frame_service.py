import abc


class UiFrameService(abc.ABC):
    @abc.abstractmethod
    def createUiFrame(self, rootWindow):
        pass

