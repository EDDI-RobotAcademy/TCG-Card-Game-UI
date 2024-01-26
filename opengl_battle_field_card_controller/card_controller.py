import abc


class CardController(abc.ABC):

    @abc.abstractmethod
    def getCardTypeTable(self, cardType):
        pass

    @abc.abstractmethod
    def itemCardInitShapes(self, local_translation):
        pass

    @abc.abstractmethod
    def trapCardInitShapes(self, local_translation):
        pass

    @abc.abstractmethod
    def supportCardInitShapes(self, local_translation):
        pass

    @abc.abstractmethod
    def toolCardInitShapes(self, local_translation):
        pass

    @abc.abstractmethod
    def energyCardInitShapes(self, local_translation):
        pass

    @abc.abstractmethod
    def environmentCardInitShapes(self, local_translation):
        pass