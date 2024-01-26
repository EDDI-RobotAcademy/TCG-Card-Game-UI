class BattleField:
    def __init__(self):
        self.battle_field_panel = []
        self.unit_card = []
        self.tomb = []
        self.card_deck = []
        self.trap = []
        self.lost_zone = []
        self.environment = []

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

    def add_card_deck(self, card_deck: object) -> object:
        self.card_deck.append(card_deck)

    def get_battle_field_panel(self):
        return self.battle_field_panel

    def add_battle_field_panel(self, battle_field_panel):
        self.battle_field_panel.append(battle_field_panel)

    def get_trap(self):
        return self.trap

    def add_trap(self, trap):
        self.trap.append(trap)

    def get_lost_zone(self):
        return self.lost_zone

    def add_lost_zone(self, lost_zone):
        self.lost_zone.append(lost_zone)

    def get_environment(self):
        return self.environment

    def add_environment(self, environment):
        self.environment.append(environment)