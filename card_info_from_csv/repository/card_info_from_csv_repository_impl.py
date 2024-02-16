from card_info_from_csv.entity.card_info_from_csv_entity import CardInfoFromCsv
import pandas as pd

from card_info_from_csv.repository.card_info_from_csv_repository import CardInfoFromCsvRepository


class CardInfoFromCsvRepositoryImpl(CardInfoFromCsvRepository):
    __instance = None
    __cardNumberDictionary = []
    __cardNameDictionary = {}
    __cardRaceDictionary = {}
    __cardGradeDictionary = {}
    __cardTypeDictionary = {}
    __cardEnergyDictionary = {}
    __cardAttackDictionary = {}
    __cardPassiveDictionary = {}
    __cardSkillDictionary = {}
    __cardHpDictionary = {}

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
        return cls.__instance

    @classmethod
    def getInstance(cls):
        if cls.__instance is None:
            cls.__instance = cls()
        return cls.__instance

    def readCardData(self, filePath):
        dataFile = pd.read_csv(filePath, skiprows=0, index_col=4)
        dataFile.fillna(0, inplace=True)

        return dataFile.itertuples()

    def build_dictionaries(self, csv_content):
        print("Building dictionaries")
        for record in csv_content:
            try:
                cardInfo = CardInfoFromCsv(record)

                self.__cardNumberDictionary.append(cardInfo.getCardNumber())
                self.__cardNameDictionary[cardInfo.getCardNumber()] = cardInfo.getCardName()
                self.__cardRaceDictionary[cardInfo.getCardNumber()] = cardInfo.getCardRace()
                self.__cardGradeDictionary[cardInfo.getCardNumber()] = cardInfo.getCardGrade()
                self.__cardTypeDictionary[cardInfo.getCardNumber()] = cardInfo.getCardType()
                self.__cardEnergyDictionary[cardInfo.getCardNumber()] = cardInfo.getCardEnergy()
                self.__cardAttackDictionary[cardInfo.getCardNumber()] = cardInfo.getCardAttack()
                self.__cardPassiveDictionary[cardInfo.getCardNumber()] = cardInfo.getCardPassive()
                self.__cardSkillDictionary[cardInfo.getCardNumber()] = cardInfo.getCardSkill()
                self.__cardHpDictionary[cardInfo.getCardNumber()] = cardInfo.getCardHp()

            except Exception as e:
                print("Error : {0}".format(e))

    def getCardNumber(self):
        print(f"self.__cardNumberDictionary : {self.__cardNumberDictionary}")
        return self.__cardNumberDictionary

    def getCardNameForCardNumber(self, cardNumber):
        return self.__cardNameDictionary[cardNumber]

    def getCardRaceForCardNumber(self, cardNumber):
        return self.__cardRaceDictionary[cardNumber]

    def getCardGradeForCardNumber(self, cardNumber):
        return self.__cardGradeDictionary[cardNumber]

    def getCardTypeForCardNumber(self, cardNumber):
        return self.__cardTypeDictionary[cardNumber]

    def getCardEnergyForCardNumber(self, cardNumber):
        return self.__cardEnergyDictionary[cardNumber]

    def getCardAttackForCardNumber(self, cardNumber):
        return self.__cardAttackDictionary[cardNumber]

    def getCardPassiveForCardNumber(self, cardNumber):
        return self.__cardPassiveDictionary[cardNumber]

    def getCardSkillForCardNumber(self, cardNumber):
        return self.__cardSkillDictionary[cardNumber]

    def getCardHpForCardNumber(self, cardNumber):
        return self.__cardHpDictionary[cardNumber]