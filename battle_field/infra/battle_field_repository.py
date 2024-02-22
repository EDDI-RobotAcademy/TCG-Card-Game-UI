from battle_field.state.current_deck import CurrentDeckState
from battle_field.state.current_hand import CurrentHandState


class BattleFieldRepository:
    __instance = None

    __is_in_game = False

    battle_field_button_list = []
    is_game_over = False
    is_win = False

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


    def start_get_no_wait_data(self):
        while self.__is_in_game:
            self.__noWaitIpcChannel.get_nowait()


    def start_game(self):
        self.__is_in_game = True
        self.start_get_no_wait_data()

    def game_end(self):
        self.__is_in_game = False
