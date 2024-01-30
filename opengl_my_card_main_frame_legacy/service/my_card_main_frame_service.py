import abc


class MyCardMainFrameService(abc.ABC):
    @abc.abstractmethod
    def createMyCardMainUiFrame(self, rootWindow, switchFrameWithMenuName):
        pass