
class CardInfoFromCsv:
    __cardNumber = None
    __cardName = None
    __cardRace = None
    __cardGrade = None
    __cardType = None
    __cardEnergy = None
    __cardAttack = None
    __cardPassive = None
    __cardSkill = None
    __cardHp = None

    def __init__(self, record):
        self.__cardNumber = record[0]
        self.__cardName = record[1]
        self.__cardRace = record[2]
        self.__cardGrade = record[3]
        self.__cardType = record[4]
        self.__cardEnergy = record[6]
        self.__cardAttack = record[7]
        self.__cardPassive = record[9]
        self.__cardSkill = record[10]
        self.__cardHp = record[11]

    def getCardNumber(self):
        return self.__cardNumber
    def getCardName(self):
        return self.__cardName

    def getCardRace(self):
        return self.__cardRace

    def getCardGrade(self):
        return self.__cardGrade

    def getCardType(self):
        return self.__cardType

    def getCardEnergy(self):
        return self.__cardEnergy

    def getCardAttack(self):
        return self.__cardAttack

    def getCardPassive(self):
        return self.__cardPassive

    def getCardSkill(self):
        return self.__cardSkill

    def getCardHp(self):
        return self.__cardHp