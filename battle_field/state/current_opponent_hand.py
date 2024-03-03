class CurrentOpponentHandState:
    def __init__(self):
        self.current_opponent_hand_list = []

    def add_to_opponent_hand(self, card_list):
        for card in card_list:
            self.current_opponent_hand_list.append(card)

    def get_current_opponent_hand(self):
        return self.current_opponent_hand_list