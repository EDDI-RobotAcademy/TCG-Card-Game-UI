class CurrentDeckState:
    def __init__(self):
        self.current_deck_list = []

    def add_to_deck(self, *cards):
        self.current_deck_list.extend(cards)

    def draw_card(self):
        if self.current_deck_list:
            return self.current_deck_list.pop(0)
        else:
            print("Deck is empty. Cannot draw a card.")

    def get_deck_size(self):
        return len(self.current_deck_list)

    def get_current_deck(self):
        return self.current_deck_list
