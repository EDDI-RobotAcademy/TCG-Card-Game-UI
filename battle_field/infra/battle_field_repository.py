from battle_field.state.current_deck import CurrentDeckState
from battle_field.state.current_hand import CurrentHandState
from battle_field.state.game_end import GameEndState
from battle_field_fixed_card.fixed_details_card import FixedDetailsCard


class BattleFieldRepository:
    __instance = None

    battle_field_button_list = []
    __game_end_state = GameEndState()
    __current_use_card_id = None


    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
        return cls.__instance

    @classmethod
    def getInstance(cls):
        if cls.__instance is None:
            cls.__instance = cls()
        return cls.__instance

    def save_master(self, master):
        self.frame_master = master

    def get_master(self):
        return self.frame_master

    def get_battle_field_button_list(self):
        return self.battle_field_button_list

    def add_battle_field_button(self, button):
        self.battle_field_button_list.append(button)

    def saveReceiveIpcChannel(self, receiveIpcChannel):
        self.__receiveIpcChannel = receiveIpcChannel

    def saveTransmitIpcChannel(self, transmitIpcChannel):
        self.__transmitIpcChannel = transmitIpcChannel

    def injectNoWaitIpcChannel(self, noWaitIpcChannel):
        self.__noWaitIpcChannel = noWaitIpcChannel


    def lose(self):
        self.__game_end_state.game_lose()

    def win(self):
        self.__game_end_state.game_win()

    def get_is_game_end(self):
        return self.__game_end_state.get_is_game_end_state()

    def get_is_win(self):
        return self.__game_end_state.get_is_win_state()

    def reset_game_state(self):
        self.__game_end_state.reset_state()

    def set_current_use_card_id(self, card_id):
        self.__current_use_card_id = card_id

    def get_current_use_card_id(self):
        return self.__current_use_card_id

    def reset_current_use_card_id(self):
        self.__current_use_card_id = None

    def clear_every_resource(self):
        self.battle_field_button_list = []
        self.__game_end_state = GameEndState()
        self.__current_use_card_id = None

