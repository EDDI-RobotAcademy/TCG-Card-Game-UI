import abc


class MyDeckFrameService(abc.ABC):
    @abc.abstractmethod
    def createMyDeckUiFrame(self, rootWindow, switchFrameWithMenuName):
        pass
