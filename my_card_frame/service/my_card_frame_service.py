import abc


class MyCardFrameService(abc.ABC):
    @abc.abstractmethod
    def createMyCardUiFrame(self, rootWindow):
        pass
