import abc


class CardShopMenuFrameRepository(abc.ABC):
    @abc.abstractmethod
    def createCardShopMenuFrame(self, rootWindow):
        pass
