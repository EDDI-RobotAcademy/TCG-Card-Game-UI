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

