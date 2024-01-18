import abc


class CardMergeFrameService(abc.ABC):
    @abc.abstractmethod
    def createCardMergeUiFrame(self, rootWindow):
        pass