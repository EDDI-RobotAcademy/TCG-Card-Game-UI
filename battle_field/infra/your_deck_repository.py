from battle_field.state.current_deck import CurrentDeckState


class YourDeckRepository:
    __instance = None

    current_deck_state = CurrentDeckState()
    # 검색 기능을 위한 Deck Card Object
    # current_deck_card_object_list = []

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
        return cls.__instance

    @classmethod
    def getInstance(cls):
        if cls.__instance is None:
            cls.__instance = cls()
        return cls.__instance

    def save_deck_state(self, deck_list):
        self.current_deck_state.add_to_deck(deck_list)
        print(f"Saved current deck state: {deck_list}")

    def get_current_deck_state(self):
        return self.current_deck_state

    def find_card_from_deck(self, card_id, count):
        print(f"find_card_from_deck(): {card_id}")
        return self.current_deck_state.find_card_by_id_with_count(card_id, count)

    def draw_deck(self):
        self.current_deck_state.draw_card()

    def draw_deck_with_count(self, count):
        drawn_list = []

        for _ in range(count):
            drawn_list.append(self.current_deck_state.draw_card())

        return drawn_list

    def saveReceiveIpcChannel(self, receiveIpcChannel):
        self.__receiveIpcChannel = receiveIpcChannel

    def saveTransmitIpcChannel(self, transmitIpcChannel):
        self.__transmitIpcChannel = transmitIpcChannel