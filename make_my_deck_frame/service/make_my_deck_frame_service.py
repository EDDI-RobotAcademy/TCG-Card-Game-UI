import abc


class MakeMyDeckFrameService(abc.ABC):
    @abc.abstractmethod
    def createMakeMyDeckUiFrame(self, rootWindow, switchFrameWithMenuName):
        pass
