class CardInfo:

    def __init__(self, card_type, card_name, card_race, card_health, card_attack, card_energy):
        self.__card_type = card_type
        self.__card_name = card_name
        self.__card_race = card_race
        self.__card_health = card_health
        self.__card_attack = card_attack
        self.__card_energy = card_energy


    def getCardType(self):
        return self.__card_type

    def getCardName(self):
        return self.__card_name

    def getCardRace(self):
        return self.__card_race

    def getCardHealth(self):
        return self.__card_health

    def getCardAtaack(self):
        return self.__card_attack

    def getCardEnergy(self):
        return self.__card_energy



