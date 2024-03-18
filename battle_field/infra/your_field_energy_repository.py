from battle_field.state.field_energy_state import FieldEnergyState
from common.card_race import CardRace


class YourFieldEnergyRepository:
    __instance = None

    field_energy_state = FieldEnergyState()
    __current_field_energy_race = CardRace.DUMMY

    __min_race_value = 1
    __max_race_value = 3

    __to_use_field_energy_count = 1

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
        self.__to_use_field_energy_count = 1
        self.__current_field_energy_race = CardRace.UNDEAD

    def increase_your_field_energy(self, count = 1):
        return self.field_energy_state.increase_your_field_energy(count)

    def decrease_your_field_energy(self, count = 1):
        return self.field_energy_state.decrease_your_field_energy(count)

    def set_your_field_energy(self, field_energy_count):
        self.field_energy_state.set_your_field_energy(field_energy_count)

    def get_your_field_energy(self):
        return self.field_energy_state.get_your_field_energy_count()

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

        if self.__current_field_energy_race == CardRace.TRENT:
            return 97

    def increase_to_use_field_energy_count(self):
        self.__to_use_field_energy_count += 1
        if self.__to_use_field_energy_count > self.field_energy_state.get_your_field_energy_count():
            self.__to_use_field_energy_count = self.field_energy_state.get_your_field_energy_count()

    def decrease_to_use_field_energy_count(self):
        if self.__to_use_field_energy_count <= 1:
            self.__to_use_field_energy_count = 1
        else:
            self.__to_use_field_energy_count -= 1

    def get_to_use_field_energy_count(self):
        return self.__to_use_field_energy_count

    def reset_to_use_field_energy_count(self):
        self.__to_use_field_energy_count = 1

    def saveReceiveIpcChannel(self, receiveIpcChannel):
        self.__receiveIpcChannel = receiveIpcChannel

    def saveTransmitIpcChannel(self, transmitIpcChannel):
        self.__transmitIpcChannel = transmitIpcChannel


    def request_to_attach_energy_to_unit(self, requestToAttachEnergyUnit):
        self.__transmitIpcChannel.put(requestToAttachEnergyUnit)
        return self.__receiveIpcChannel.get()

    def clear_every_resource(self):
        self.field_energy_state = FieldEnergyState()
        self.__current_field_energy_race = CardRace.HUMAN

        self.__to_use_field_energy_count = 1

