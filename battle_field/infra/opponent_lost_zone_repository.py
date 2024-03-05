from battle_field.state.current_lost_zone import CurrentLostZoneState
from battle_field_fixed_card.legacy.circle_image_legacy_fixed_field_card import LegacyFixedFieldCard


class OpponentLostZoneRepository:
    __instance = None

    opponent_lost_zone_state = CurrentLostZoneState()

    opponent_lost_zone_card_list = []
    opponent_lost_zone_card_x_position = []

    x_base = 400

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
        return cls.__instance

    @classmethod
    def getInstance(cls):
        if cls.__instance is None:
            cls.__instance = cls()
        return cls.__instance

    def save_opponent_lost_zone_state(self, hand_card_id):
        self.opponent_lost_zone_state.place_card_to_lost_zone(hand_card_id)
        print(f"Saved current lost zone card state: {hand_card_id}")

    def get_opponent_lost_zone_state(self):
        return self.opponent_lost_zone_state.get_current_lost_zone_card_list()

    def create_opponent_lost_zone_card(self, card_id):
        index = len(self.opponent_lost_zone_card_list)
        print(f"create_opponent_lost_zone_card() -> index: {index}, card_id: {card_id}")

        new_card = LegacyFixedFieldCard(local_translation=self.get_next_card_position(index))
        new_card.init_card(card_id)

        self.opponent_lost_zone_card_list.append(new_card)

        self.save_opponent_lost_zone_state(card_id)

    def create_opponent_lost_zone_card_list(self):
        current_opponent_lost_zone_card_list = self.get_opponent_lost_zone_state()
        print(f"current_opponent_lost_zone_card_list: {current_opponent_lost_zone_card_list}")

        for index, card_number in enumerate(current_opponent_lost_zone_card_list):
            print(f"index: {index}, card_number: {card_number}")
            new_card = LegacyFixedFieldCard(local_translation=self.get_next_card_position(index))
            new_card.init_card(card_number)
            new_card.set_index(index)
            self.opponent_lost_zone_card_list.append(new_card)

    def get_opponent_lost_zone_card_list(self):
        return self.opponent_lost_zone_card_list

    def get_next_card_position(self, index):
        # TODO: 배치 간격 고려
        current_y = 300
        x_increment = 170
        next_x = self.x_base + x_increment * index
        return (next_x, current_y)

    def place_card_in_lost_zone(self, unit_card_id):
        self.opponent_lost_zone_card_list.append(unit_card_id)

    def saveReceiveIpcChannel(self, receiveIpcChannel):
        self.__receiveIpcChannel = receiveIpcChannel

    def saveTransmitIpcChannel(self, transmitIpcChannel):
        self.__transmitIpcChannel = transmitIpcChannel
