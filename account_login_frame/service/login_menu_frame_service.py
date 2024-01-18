import abc


class LoginMenuFrameService(abc.ABC):
    @abc.abstractmethod
    def createLoginUiFrame(self, rootWindow, switchFrameWithMenuName):
        pass
