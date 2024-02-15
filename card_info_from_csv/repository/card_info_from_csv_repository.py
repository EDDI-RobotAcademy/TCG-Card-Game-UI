import abc


class CardInfoFromCsvRepository(abc.ABC):

    @abc.abstractmethod
    def readCardData(self, filePath):
        pass

    @abc.abstractmethod
    def build_dictionaries(self, csv_content):
        pass

    @abc.abstractmethod
    def getCardNameForCardNumber(self, cardNumber):
        pass

    @abc.abstractmethod
    def getCardRaceForCardNumber(self, cardNumber):
        pass

    @abc.abstractmethod
    def getCardGradeForCardNumber(self, cardNumber):
        pass

    @abc.abstractmethod
    def getCardTypeForCardNumber(self, cardNumber):
        pass

    @abc.abstractmethod
    def getCardEnergyForCardNumber(self, cardNumber):
        pass

    @abc.abstractmethod
    def getCardAttackForCardNumber(self, cardNumber):
        pass

    @abc.abstractmethod
    def getCardPassiveForCardNumber(self, cardNumber):
        pass

    @abc.abstractmethod
    def getCardSkillForCardNumber(self, cardNumber):
        pass

    @abc.abstractmethod
    def getCardHpForCardNumber(self, cardNumber):
        pass