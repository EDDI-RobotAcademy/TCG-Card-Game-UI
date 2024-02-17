from battle_field.state.current_hand import CurrentHandState
from opengl_battle_field_pickable_card.pickable_card import PickableCard


class YourHandRepository:
    __instance = None

    current_hand_state = CurrentHandState()
    current_hand_card_list = []
    current_hand_card_x_position = []

    x_base = 300

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

        # self.make_hand_card_list_location(len(hand_list))

    # def make_hand_card_list_location(self, card_length):
    #     current_x = self.x_base
    #     increment_x_position = 135
    #
    #     for i in range(card_length):
    #         self.current_hand_card_x_position.append((current_x + increment_x_position * i, 830))

    def get_current_hand_state(self):
        return self.current_hand_state.get_current_hand()

    def create_hand_card_list(self):
        current_hand = self.get_current_hand_state()
        print(f"current_hand: {current_hand}")

        for index, card_number in enumerate(current_hand):
            print(f"index: {index}, card_number: {card_number}")
            new_card = PickableCard(local_translation=self.get_next_card_position(index))
            new_card.init_card(card_number)
            self.current_hand_card_list.append(new_card)

    def remove_card_by_id(self, card_id):
        card_list = self.get_current_hand_card_list()

        for card in card_list:
            if card.get_card_number() == card_id:
                card_list.remove(card)

        self.current_hand_state.remove_from_hand(card_id)

        print(f"after clear -> current_hand_list: {self.current_hand_card_list}, current_hand_state: {self.get_current_hand_state()}")

    def get_next_card_position(self, index):
        # TODO: 배치 간격 고려
        current_y = 830
        x_increment = 170
        next_x = self.x_base + x_increment * index
        return (next_x, current_y)

    def get_current_hand_card_list(self):
        return self.current_hand_card_list

