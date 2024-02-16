class CurrentHandState:
    def __init__(self):
        self.current_hand_list = []

    def add_to_hand(self, card_list):
        # print(f"add_to_hand: {card_list}")
        for card in card_list:
            # print(f"add_to_hand: {card}")
            self.current_hand_list.append(card)

    def remove_from_hand(self, *cards):
        for card in cards:
            if card in self.current_hand_list:
                self.current_hand_list.remove(card)
            else:
                print(f"Card '{card}' not found in the current hand.")

    def clear_current_hand(self):
        self.current_hand_list = []

    def get_current_hand(self):
        return self.current_hand_list

