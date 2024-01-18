import abc


class CardBackFrameService(abc.ABC):
    @abc.abstractmethod
    def createCardBackUiFrame(self, rootWindow):
        pass