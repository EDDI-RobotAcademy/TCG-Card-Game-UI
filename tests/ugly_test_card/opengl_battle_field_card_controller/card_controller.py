import abc


class CardController(abc.ABC):

    @abc.abstractmethod
    def getCardTypeTable(self, cardType):
        pass

    @abc.abstractmethod
    def itemCardInitShapes(self, local_translation):
        pass