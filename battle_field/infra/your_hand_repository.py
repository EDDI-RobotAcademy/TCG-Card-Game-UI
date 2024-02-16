from battle_field.state.current_hand import CurrentHandState
from opengl_battle_field_card.card import Card


class YourHandRepository:
    __instance = None

    current_hand_state = CurrentHandState()
    current_hand_card_list = []

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
        return cls.__instance

    @classmethod
    def getInstance(cls):
        if cls.__instance is None:
            cls.__instance = cls()
        return cls.__instance

    def save_current_hand_state(self, hand_list):
        self.current_hand_state.add_to_hand(hand_list)
        print(f"Saved current hand state: {hand_list}")

    def get_current_hand_state(self):
        return self.current_hand_state.get_current_hand()

    def create_hand_card_list(self):
        current_hand = self.get_current_hand_state()
        print(f"current_hand: {current_hand}")

        for card_number in current_hand:
            print(f"card_number: {card_number}")
            new_card = Card(local_translation=self.get_next_card_position())
            new_card.init_card(card_number)
            self.current_hand_card_list.append(new_card)

    def get_next_card_position(self):
        # TODO: 배치 간격 고려
        return (100, 100)

    def get_current_hand_card_list(self):
        return self.current_hand_card_list

