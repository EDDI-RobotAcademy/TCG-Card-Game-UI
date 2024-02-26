from common.card_race import CardRace
from tests.ljs.uglt_test_field_energy.state.current_your_field_energy import CurrentYourFieldEnergyState


class YourFieldEnergyRepositoryForTest:
    __instance = None

    __current_energy_state = CurrentYourFieldEnergyState()
    __current_field_energy_race = CardRace.DUMMY

    __min_race_value = 1
    __max_race_value = 3

    __to_use_field_energy_count = 0



    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
        return cls.__instance

    @classmethod
    def getInstance(cls):
        if cls.__instance is None:
            cls.__instance = cls()
        return cls.__instance

    def reset_field_energy(self):
        self.__current_energy_state.reset_current_your_field_energy()
        self.__to_use_field_energy_count = 0
        self.__current_field_energy_race = CardRace.UNDEAD

    def get_current_your_field_energy_state(self):
        return self.__current_energy_state

    def reduce_energy(self, count = 1):
        print("Energy Used!!!")
        return self.__current_energy_state.reduce_current_your_field_energy(count)

    def increase_energy(self, count = 1):
        self.__current_energy_state.increase_current_your_field_energy(count)

    def get_current_field_energy_race(self):
        return self.__current_field_energy_race

    def to_next_field_energy_race(self):
        next_race_value = (self.__current_field_energy_race.value) + 1
        if next_race_value > self.__max_race_value:
            next_race_value = self.__min_race_value

        for race in CardRace:
            if next_race_value == race.value:
                self.__current_field_energy_race = race
                print(f"current energy race is: {self.__current_field_energy_race}")

    def to_prev_field_energy_race(self):
        prev_race_value = (self.__current_field_energy_race.value) - 1
        if prev_race_value < self.__min_race_value:
            prev_race_value = self.__max_race_value

        for race in CardRace:
            if prev_race_value == race.value:
                self.__current_field_energy_race = race
                print(f"current energy race is: {self.__current_field_energy_race}")


    def set_current_field_energy_race(self, card_race):
        self.__current_field_energy_race = card_race

    def get_current_field_energy_card_id(self):
        if self.__current_field_energy_race == CardRace.HUMAN:
            return 99

        if self.__current_field_energy_race == CardRace.UNDEAD:
            return 93

        if self.__current_field_energy_race == CardRace.TRANT:
            return 97

    def increase_to_use_field_energy_count(self):
        self.__to_use_field_energy_count += 1
        if self.__to_use_field_energy_count > self.get_current_your_field_energy_state().get_current_your_field_energy():
            self.__to_use_field_energy_count = self.get_current_your_field_energy_state().get_current_your_field_energy()

    def decrease_to_use_field_energy_count(self):
        self.__to_use_field_energy_count -= 1
        if self.__to_use_field_energy_count < 1:
            self.__to_use_field_energy_count = 1

    def get_to_use_field_energy_count(self):
        return self.__to_use_field_energy_count
