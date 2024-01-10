import abc


class UiFrameController(abc.ABC):
    @abc.abstractmethod
    def requestToCreateUiFrame(self, rootWindow):
        pass

    