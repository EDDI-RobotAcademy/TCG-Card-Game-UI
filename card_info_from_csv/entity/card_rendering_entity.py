from typing import Tuple, List, Dict


class CardInfoFromCsv:
    __instance = None
    __name_dictionary = {}
    __race_dictionary = {}
    __grade_dictionary = {}
    __type_dictionary = {}
    __energy_dictionary = {}
    __attack_dictionary = {}
    __passive_dictionary = {}
    __skill_dictionary = {}
    __hp_dictionary = {}

    def __init__(self):
        print("Initializing Card Info")
    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
        return cls.__instance

    @classmethod
    def getInstance(cls):
        if cls.__instance is None:
            cls.__instance = cls()
        return cls.__instance

    def build_dictionaries(self, csv_content):
        print("Building dictionaries")
        for record in csv_content:
            card_number = record[4]
            card_name = record[0]
            card_race = record[1]
            card_grade = record[2]
            card_type = record[3]
            card_energy = record[6]
            card_attack = record[7]
            card_passive = record[9]
            card_skill = record[10]
            card_hp = record[11]

            self.__name_dictionary[card_number] = card_name
            self.__race_dictionary[card_number] = card_race
            self.__grade_dictionary[card_number] = card_grade
            self.__type_dictionary[card_number] = card_type
            self.__energy_dictionary[card_number] = card_energy
            self.__attack_dictionary[card_number] = card_attack
            self.__passive_dictionary[card_number] = card_passive
            self.__skill_dictionary[card_number] = card_skill
            self.__hp_dictionary[card_number] = card_hp
            print(f"{self.__name_dictionary[card_number]}")

    def get_card_name(self, card_number):
        return self.__name_dictionary.get(card_number)

    def get_card_race(self, card_number):
        return self.__race_dictionary.get(card_number)

    def get_card_grade(self, card_number):
        return self.__grade_dictionary.get(card_number)

    def get_card_type(self, card_number):
        return self.__type_dictionary.get(card_number)

    def get_card_energy(self, card_number):
        return self.__energy_dictionary.get(card_number)

    def get_card_attack(self, card_number):
        return self.__attack_dictionary.get(card_number)

    def get_card_passive(self, card_number):
        return self.__passive_dictionary.get(card_number)

    def get_card_skill(self, card_number):
        return self.__skill_dictionary.get(card_number)

    def get_card_hp(self, card_number):
        return self.__hp_dictionary.get(card_number)