class MyCardState:
    def __init__(self):
        self.my_card_dictionary = {}

    def add_to_my_card_dictionary(self, card_dictionary_list):
        for item in card_dictionary_list:
            card_id, quantity = item.popitem()
            self.my_card_dictionary[card_id] = quantity

    def add_to_my_card(self, card_list):
        for card_id in card_list:
            self.my_card_dictionary[card_id] = self.my_card_dictionary.get(card_id, 0) + 1

    def get_my_card_size(self):
        return len(self.my_card_dictionary)

    def get_my_card_dictionary(self):
        return self.my_card_dictionary
