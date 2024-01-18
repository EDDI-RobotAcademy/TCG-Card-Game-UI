import abc


class CardMergeFrameRepository(abc.ABC):
    @abc.abstractmethod
    def createCardMergeFrame(self, rootWindow):
        pass