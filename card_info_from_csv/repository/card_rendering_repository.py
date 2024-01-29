import abc


class CardRenderingRepository(abc.ABC):

    @abc.abstractmethod
    def readCsvFile(self, filePath):
        pass

    @abc.abstractmethod
    def findCardByNumber(self, cards, cardNumber):
        pass