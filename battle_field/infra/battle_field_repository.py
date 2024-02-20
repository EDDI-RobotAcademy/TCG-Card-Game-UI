from battle_field.state.current_deck import CurrentDeckState
from battle_field.state.current_hand import CurrentHandState


class BattleFieldRepository:
    __instance = None

    current_hand_state = CurrentHandState()
    current_deck_state = CurrentDeckState()

    battle_field_button_list = []

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
        return cls.__instance

    @classmethod
    def getInstance(cls):
        if cls.__instance is None:
            cls.__instance = cls()
        return cls.__instance

    def save_current_hand_state(self, hand_list):
        self.current_hand_state.add_to_hand(hand_list)

    def save_current_deck_state(self, deck_list):
        self.current_deck_state.add_to_deck(deck_list)

    def get_current_hand_state(self):
        return self.current_hand_state.get_current_hand()

    def get_current_deck_state(self):
        return self.current_deck_state.get_current_deck()

    def get_battle_field_button_list(self):
        return self.battle_field_button_list

    def add_battle_field_button(self, button):
        self.battle_field_button_list.append(button)


    def saveReceiveIpcChannel(self, receiveIpcChannel):
        self.__receiveIpcChannel = receiveIpcChannel

    def saveTransmitIpcChannel(self, transmitIpcChannel):
        self.__transmitIpcChannel = transmitIpcChannel
