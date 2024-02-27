from math import ceil

from battle_field.state.current_deck import CurrentDeckState
from battle_field.state.deck_page import DeckPage
from battle_field_fixed_card.fixed_field_card import FixedFieldCard


class YourDeckRepository:
    __instance = None

    total_width = None
    total_height = None

    current_deck_state = CurrentDeckState()
    deck_page_list = []
    # 검색 기능을 위한 Deck Card Object
    current_deck_card_object_list = []

    # 405 / 1920, 252 / 1043
    # 6개 구성 (x_right_base_ratio - x_left_base_ratio) / 6
    x_left_base_ratio = 0.211
    x_right_base_ratio = 0.784
    y_top_base_ratio = 0.2416
    y_bottom_base_ratio = 0.593

    current_page = 0

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
        return cls.__instance

    @classmethod
    def getInstance(cls):
        if cls.__instance is None:
            cls.__instance = cls()
        return cls.__instance

    def set_total_window_size(self, width, height):
        self.total_width = width
        self.total_height = height

    def build_deck_page(self):
        deck_list = self.get_current_deck_state()

        num_cards_per_page = 12
        num_pages = ceil(len(deck_list) / num_cards_per_page)

        for page_index in range(num_pages):
            start_index = page_index * num_cards_per_page
            end_index = (page_index + 1) * num_cards_per_page
            current_deck_page = deck_list[start_index:end_index]

            current_page = DeckPage()
            current_page.set_total_window_size(self.total_width, self.total_height)
            current_page.add_deck_to_page(current_deck_page)
            current_page.set_page_number(page_index + 1)
            current_page.create_deck_card_list()

            self.deck_page_list.append(current_page)

    def save_deck_state(self, deck_list):
        self.current_deck_state.add_to_deck(deck_list)
        print(f"Saved current deck state: {deck_list}")

    def get_current_deck_state(self):
        return self.current_deck_state.get_current_deck()

    def next_deck_page(self):
        if self.current_page == len(self.deck_page_list) - 1:
            return

        self.current_page += 1

    def prev_deck_page(self):
        if self.current_page == 0:
            return

        self.current_page -= 1

    def get_current_deck_page(self):
        return self.current_page

    def get_current_page_deck_list(self):
        return self.deck_page_list[self.get_current_deck_page()].get_deck_page_card_object_list()

    def find_card_from_deck(self, card_id, count):
        print(f"find_card_from_deck(): {card_id}")
        return self.current_deck_state.find_card_by_id_with_count(card_id, count)

    # 405 / 1920, 252 / 1043

    def get_next_card_position(self, index):
        # TODO: 배치 간격 고려
        card_width_ratio = 105 / self.total_width
        place_index = index % 6

        if index > 5:
            current_y = self.total_height * self.y_bottom_base_ratio
        else:
            current_y = self.total_height * self.y_top_base_ratio

        base_x = self.total_width * self.x_left_base_ratio
        x_increment = (self.x_right_base_ratio - self.x_left_base_ratio + card_width_ratio) / 6.0
        next_x = base_x + self.total_width * (x_increment * place_index)
        return (next_x, current_y)

    def create_deck_card_list(self):
        current_deck_state = self.get_current_deck_state()
        print(f"current_deck_state: {current_deck_state}")

        for index, card_number in enumerate(current_deck_state):
            print(f"index: {index}, card_number: {card_number}")
            new_card = FixedFieldCard(local_translation=self.get_next_card_position(index))
            new_card.init_card(card_number)
            new_card.set_index(index)
            self.current_deck_card_object_list.append(new_card)

    def get_current_deck_card_object_list(self):
        print(f"your_deck_repository: get_current_deck_card_object_list() -> {self.current_deck_card_object_list}")
        return self.current_deck_card_object_list

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