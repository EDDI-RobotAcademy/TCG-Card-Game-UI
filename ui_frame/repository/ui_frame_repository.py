import abc


class UiFrameRepository(abc.ABC):
    @abc.abstractmethod
    def registerUiFrame(self, name, newFrame):
        pass

