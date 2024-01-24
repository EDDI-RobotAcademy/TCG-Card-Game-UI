class BattleField:
    def __init__(self):
        self.unit_card = []
        self.tomb = []
        self.card_deck = []
        self.battle_field_panel = []

    def get_unit_card(self):
        return self.unit_card

    def add_unit_card(self, unit_card):
        self.unit_card.append(unit_card)

    def get_tomb(self):
        return self.tomb

    def add_tomb(self, tomb):
        self.tomb.append(tomb)

    def get_card_deck(self):
        return self.card_deck

    def add_card_deck(self, card_deck):
        self.card_deck.append(card_deck)
    def get_battle_field_panel(self):
        return self.battle_field_panel
    def add_battle_field_panel(self, battle_field_panel):
        self.battle_field_panel.append(battle_field_panel)