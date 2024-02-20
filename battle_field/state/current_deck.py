class CurrentDeckState:
    def __init__(self):
        self.current_deck_list = []

    def add_to_deck(self, card_list):
        for card in card_list:
            self.current_deck_list.append(card)

    # def add_to_deck(self, *cards):
    #     self.current_deck_list.extend(cards)

    def draw_card(self):
        if self.current_deck_list:
            return self.current_deck_list.pop(0)
        else:
            print("Deck is empty. Cannot draw a card.")

    def get_deck_size(self):
        return len(self.current_deck_list)

    def get_current_deck(self):
        return self.current_deck_list

    def find_card_by_id(self, card_id):
        for card in self.current_deck_list:
            if card == card_id:
                self.current_deck_list.remove(card)
                return card
        return None

    def find_card_by_id_with_count(self, card_id, count):
        found_card_list = []
        remaining_count = count

        while remaining_count > 0 and card_id in self.current_deck_list:
            found_card = self.find_card_by_id(card_id)
            if found_card is not None:
                found_card_list.append(found_card)
                remaining_count -= 1

        return found_card_list

