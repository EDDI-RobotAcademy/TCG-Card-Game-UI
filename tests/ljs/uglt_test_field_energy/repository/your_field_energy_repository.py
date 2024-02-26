from common.card_race import CardRace
from tests.ljs.uglt_test_field_energy.state.current_your_field_energy import CurrentYourFieldEnergyState


class YourFieldEnergyRepositoryForTest:
    __instance = None

    current_energy_state = CurrentYourFieldEnergyState()
    __current_field_energy_race = CardRace.DUMMY

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
        self.current_energy_state.reset_current_your_field_energy()
        self.current_field_energy_race = CardRace.UNDEAD

    def get_current_your_field_energy_state(self):
        return self.current_energy_state

    def reduce_energy(self, count = 1):
        print("Energy Used!!!")
        self.current_energy_state.reduce_current_your_field_energy(count)

    def increase_energy(self, count = 1):
        self.current_energy_state.increase_current_your_field_energy(count)

    def get_current_field_energy_race(self):
        return self.__current_field_energy_race.value

    def to_next_field_energy_race(self):
        next_race_value = (self.__current_field_energy_race.value) + 1

        for race in CardRace:
            if next_race_value == race.value():
                self.current_field_energy_race = race
                print(f"current energy race is: {self.current_field_energy_race}")


    def set_current_field_energy_race(self, card_race):
        self.__current_field_energy_race = card_race
