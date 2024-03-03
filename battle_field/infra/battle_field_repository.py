from battle_field.state.current_deck import CurrentDeckState
from battle_field.state.current_hand import CurrentHandState
from battle_field.state.game_end import GameEndState


class BattleFieldRepository:
    __instance = None

    battle_field_button_list = []
    __game_end_state = GameEndState()
    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
        return cls.__instance

    @classmethod
    def getInstance(cls):
        if cls.__instance is None:
            cls.__instance = cls()
        return cls.__instance

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
