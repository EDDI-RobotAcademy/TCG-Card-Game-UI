from battle_field.state.current_tomb import CurrentTombState
from battle_field_fixed_card.fixed_field_card import FixedFieldCard


class RoundRepository:
    __instance = None

    current_round_number = 1

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
        return cls.__instance

    @classmethod
    def getInstance(cls):
        if cls.__instance is None:
            cls.__instance = cls()
        return cls.__instance

    def increase_current_round_number(self):
        self.current_round_number += 1

    def get_current_round_number(self):
        return self.current_round_number
