import abc


class CardBackFrameRepository(abc.ABC):
    @abc.abstractmethod
    def createCardBackFrame(self, rootWindow):
        pass