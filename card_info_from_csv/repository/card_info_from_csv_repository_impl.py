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
    __cardJobDictionary = {}
    __cardEnergyDictionary = {}
    __cardAttackDictionary = {}
    __cardPassiveDictionary = {}
    __cardSkillDictionary = {}
    __cardHpDictionary = {}
    __cardSkillCounterDictionary = {}
    __cardSkillFirstDictionary = {}
    __cardSkillSecondDictionary = {}
    __cardPassiveFirstDictionary = {}
    __cardPassiveSecondDictionary = {}
    __cardSkillFirstDamageDictionary = {}
    __cardSkillSecondDamageDictionary = {}
    __cardPassiveFirstDamageDictionary = {}
    __cardPassiveSecondDamageDictionary = {}
    __cardSkillFirstUndeadEnergyRequiredDictionary = {}
    __cardSkillFirstHumanEnergyRequiredDictionary = {}
    __cardSkillFirstTrentEnergyRequiredDictionary = {}
    __cardSkillSecondUndeadEnergyRequiredDictionary = {}
    __cardSkillSecondHumanEnergyRequiredDictionary = {}
    __cardSkillSecondTrentEnergyRequiredDictionary = {}


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
        with open(filePath, 'r') as file:
            dataFile = pd.read_csv(file, skiprows=0, index_col=4)
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
                self.__cardJobDictionary[cardInfo.getCardNumber()] = cardInfo.getCardJob()
                self.__cardEnergyDictionary[cardInfo.getCardNumber()] = cardInfo.getCardEnergy()
                self.__cardAttackDictionary[cardInfo.getCardNumber()] = cardInfo.getCardAttack()
                self.__cardPassiveDictionary[cardInfo.getCardNumber()] = cardInfo.getCardPassive()
                self.__cardSkillDictionary[cardInfo.getCardNumber()] = cardInfo.getCardSkill()
                self.__cardHpDictionary[cardInfo.getCardNumber()] = cardInfo.getCardHp()
                self.__cardSkillCounterDictionary[cardInfo.getCardNumber()] = cardInfo.getCardSkillCounter()
                self.__cardSkillFirstDictionary[cardInfo.getCardNumber()] = cardInfo.getCardSkillFirst()
                self.__cardSkillSecondDictionary[cardInfo.getCardNumber()] = cardInfo.getCardSkillSecond()
                self.__cardPassiveFirstDictionary[cardInfo.getCardNumber()] = cardInfo.getCardPassiveFirst()
                self.__cardPassiveSecondDictionary[cardInfo.getCardNumber()] = cardInfo.getCardPassiveSecond()
                self.__cardSkillFirstDamageDictionary[cardInfo.getCardNumber()] = cardInfo.getCardSkillFirstDamage()
                self.__cardSkillSecondDamageDictionary[cardInfo.getCardNumber()] = cardInfo.getCardSkillSecondDamage()
                self.__cardPassiveFirstDamageDictionary[cardInfo.getCardNumber()] = cardInfo.getCardPassiveFirstDamage()
                self.__cardPassiveSecondDamageDictionary[cardInfo.getCardNumber()] = cardInfo.getCardPassiveSecondDamage()
                self.__cardSkillFirstUndeadEnergyRequiredDictionary[cardInfo.getCardNumber()] = cardInfo.getCardSkillFirstUndeadEnergyRequired()
                self.__cardSkillFirstHumanEnergyRequiredDictionary[cardInfo.getCardNumber()] = cardInfo.getCardSkillFirstHumanEnergyRequired()
                self.__cardSkillFirstTrentEnergyRequiredDictionary[cardInfo.getCardNumber()] = cardInfo.getCardSkillFirstTrentEnergyRequired()
                self.__cardSkillSecondUndeadEnergyRequiredDictionary[cardInfo.getCardNumber()] = cardInfo.getCardSkillSecondUndeadEnergyRequired()
                self.__cardSkillSecondHumanEnergyRequiredDictionary[cardInfo.getCardNumber()] = cardInfo.getCardSkillSecondHumanEnergyRequired()
                self.__cardSkillSecondTrentEnergyRequiredDictionary[cardInfo.getCardNumber()] = cardInfo.getCardSkillSecondTrentEnergyRequired()

            except Exception as e:
                print("Error : {0}".format(e))

    def getCardNumber(self):
        return self.__cardNumberDictionary

    def getCardNameForCardNumber(self, cardNumber):
        return self.__cardNameDictionary[cardNumber]

    def getCardRaceForCardNumber(self, cardNumber):
        return self.__cardRaceDictionary[cardNumber]

    def getCardGradeForCardNumber(self, cardNumber):
        return self.__cardGradeDictionary[cardNumber]

    def getCardTypeForCardNumber(self, cardNumber):
        return self.__cardTypeDictionary[cardNumber]

    def getCardJobForCardNumber(self, cardNumber):
        return self.__cardJobDictionary[cardNumber]

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

    def getCardSkillCounterForCardNumber(self, cardNumber):
        return self.__cardSkillCounterDictionary[cardNumber]

    def getCardSkillFirstForCardNumber(self, cardNumber):
        return self.__cardSkillFirstDictionary[cardNumber]

    def getCardSkillSecondForCardNumber(self, cardNumber):
        return self.__cardSkillSecondDictionary[cardNumber]

    def getCardPassiveFirstForCardNumber(self, cardNumber):
        return self.__cardPassiveFirstDictionary[cardNumber]

    def getCardPassiveSecondForCardNumber(self, cardNumber):
        return self.__cardPassiveSecondDictionary[cardNumber]

    def getCardSkillFirstDamageForCardNumber(self, cardNumber):
        return self.__cardSkillFirstDamageDictionary[cardNumber]

    def getCardSkillSecondDamageForCardNumber(self, cardNumber):
        return self.__cardSkillSecondDamageDictionary[cardNumber]

    def getCardPassiveFirstDamageForCardNumber(self, cardNumber):
        return self.__cardPassiveFirstDamageDictionary[cardNumber]

    def getCardPassiveSecondDamageForCardNumber(self, cardNumber):
        return self.__cardPassiveSecondDamageDictionary[cardNumber]

    def getCardSkillFirstUndeadEnergyRequiredForCardNumber(self, cardNumber):
        return self.__cardSkillFirstUndeadEnergyRequiredDictionary[cardNumber]

    def getCardSkillFirstHumanEnergyRequiredForCardNumber(self, cardNumber):
        return self.__cardSkillFirstHumanEnergyRequiredDictionary[cardNumber]

    def getCardSkillFirstTrentEnergyRequiredForCardNumber(self, cardNumber):
        return self.__cardSkillFirstTrentEnergyRequiredDictionary[cardNumber]

    def getCardSkillSecondUndeadEnergyRequiredForCardNumber(self, cardNumber):
        return self.__cardSkillSecondUndeadEnergyRequiredDictionary[cardNumber]

    def getCardSkillSecondHumanEnergyRequiredForCardNumber(self, cardNumber):
        return self.__cardSkillSecondHumanEnergyRequiredDictionary[cardNumber]

    def getCardSkillSecondTrentEnergyRequiredForCardNumber(self, cardNumber):
        return self.__cardSkillSecondTrentEnergyRequiredDictionary[cardNumber]


