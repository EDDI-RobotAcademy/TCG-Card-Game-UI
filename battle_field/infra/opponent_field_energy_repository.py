from battle_field.state.field_energy_state import FieldEnergyState
from common.card_race import CardRace


class OpponentFieldEnergyRepository:
    __instance = None

    # TODO: 네이밍 이슈 (YourField가 아니라 FieldEnergyState로 변경하는 것이 더 좋음
    field_energy_state = FieldEnergyState()

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
        return cls.__instance

    @classmethod
    def getInstance(cls):
        if cls.__instance is None:
            cls.__instance = cls()
        return cls.__instance


    def increase_opponent_field_energy(self, count = 1):
        return self.field_energy_state.increase_opponent_field_energy(count)


    def decrease_opponent_field_energy(self, count = 1):
        return self.field_energy_state.decrease_opponent_field_energy(count)

    def get_opponent_field_energy(self):
        return self.field_energy_state.get_opponent_field_energy_count()

