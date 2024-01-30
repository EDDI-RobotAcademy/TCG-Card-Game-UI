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
    def getCardTypeDictionary(self, cardNumber):
        pass
    @abc.abstractmethod
    def getCardEnergyDictionary(self, cardNumber):
        pass
    @abc.abstractmethod
    def getCardAttackDictionary(self, cardNumber):
        pass
    @abc.abstractmethod
    def getCardPassiveDictionary(self, cardNumber):
        pass
    @abc.abstractmethod
    def getCardSkillDictionary(self, cardNumber):
        pass
    @abc.abstractmethod
    def getCardHp(self, cardNumber):
        pass