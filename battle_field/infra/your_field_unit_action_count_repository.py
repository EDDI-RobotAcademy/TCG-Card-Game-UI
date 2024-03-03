from battle_field.state.current_tomb import CurrentTombState
from battle_field_fixed_card.fixed_field_card import FixedFieldCard


class CurrentFieldUnitActionCountRepository:
    __instance = None

    current_field_unit_action_count = CurrentFieldUnitActionCountState()

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
        return cls.__instance

    @classmethod
    def getInstance(cls):
        if cls.__instance is None:
            cls.__instance = cls()
        return cls.__instance

    def save_current_tomb_state(self, hand_card_id):
        self.current_field_unit_action_count.place_unit_to_tomb(hand_card_id)
        print(f"Saved current tomb_card state: {hand_card_id}")

    def get_current_tomb_state(self):
        return self.current_tomb_state.get_current_tomb_unit_list()



