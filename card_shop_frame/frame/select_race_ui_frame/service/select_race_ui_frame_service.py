import abc


class SelectRaceUiFrameService(abc.ABC):
    @abc.abstractmethod
    def createSelectRaceUiFrame(self, rootWindow, switchFrameWithMenuName):
        pass
