import abc


class CardHousingRenderingRepository(abc.ABC):
    @abc.abstractmethod
    def createCardHousingRendering(self, rootWindow):
        pass