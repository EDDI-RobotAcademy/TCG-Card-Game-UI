import abc


class CardHousingRenderingService(abc.ABC):
    @abc.abstractmethod
    def createCardHousingUiRendering(self, rootWindow, switchFrameWithMenuName):
        pass