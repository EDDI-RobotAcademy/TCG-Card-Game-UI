from typing import Tuple, List, Dict
import pandas as pd


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

    def read_card_data(self, file_path):
        dataFile = pd.read_csv(file_path, skiprows=0, index_col=4)
        dataFile.fillna(0, inplace=True)

        return dataFile.itertuples()


    def build_dictionaries(self, csv_content):
        print("Building dictionaries")
        for record in csv_content:
            try:
                card_number = record[0]
                card_name = record[1]
                card_race = record[2]
                card_grade = record[3]
                card_type = record[4]
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
            except Exception as e:
                print("Error : {0}".format(e))



    def get_card_name(self, card_number):
        return self.__name_dictionary[card_number]

    def get_card_race(self, card_number):
        return self.__race_dictionary[card_number]

    def get_card_grade(self, card_number):
        return self.__grade_dictionary[card_number]

    def get_card_type(self, card_number):
        return self.__type_dictionary[card_number]

    def get_card_energy(self, card_number):
        return self.__energy_dictionary[card_number]

    def get_card_attack(self, card_number):
        return self.__attack_dictionary[card_number]

    def get_card_passive(self, card_number):
        return self.__passive_dictionary[card_number]

    def get_card_skill(self, card_number):
        return self.__skill_dictionary[card_number]

    def get_card_hp(self, card_number):
        return self.__hp_dictionary[card_number]