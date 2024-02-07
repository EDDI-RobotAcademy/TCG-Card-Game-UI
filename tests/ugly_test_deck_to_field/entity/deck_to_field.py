class DeckToField:
    def __init__(self):
        self.card = []
        self.field = []

    def get_card(self):
        return self.card
    def add_card(self, card):
        self.card.append(card)
    def get_field(self):
        return self.field
    def add_field(self, field):
        self.field.append(field)