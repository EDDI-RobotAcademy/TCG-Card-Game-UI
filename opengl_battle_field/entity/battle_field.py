class BattleField:
    def __init__(self):
        self.unit_card = []
        self.tomb = []

    def get_unit_card(self):
        return self.unit_card

    def add_unit_card(self, unit_card):
        self.unit_card.append(unit_card)

    def get_tomb(self):
        return self.tomb

    def add_tomb(self, tomb):
        self.tomb.append(tomb)