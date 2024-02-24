class CurrentLostZoneState:
    def __init__(self):
        self.current_lost_zone_card_list = []

    def place_card_to_lost_zone(self, card_id):
        self.current_lost_zone_card_list.append(card_id)

    def get_current_lost_zone_card_list(self):
        return self.current_lost_zone_card_list
