import abc


class CardPackFrameService(abc.ABC):
    @abc.abstractmethod
    def createCardPackUiFrame(self, rootWindow):
        pass
