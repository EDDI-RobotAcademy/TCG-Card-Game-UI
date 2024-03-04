from battle_field_fixed_card.fixed_field_card import LegacyFixedFieldCard


class DeckPage:

    page_number = 0

    total_width = 0
    total_height = 0

    # 430 / 1920, 252 / 1043
    # 1490 / 1920, 252 / 1043
    # 6개 구성 (x_right_base_ratio - x_left_base_ratio) / 6
    x_left_base_ratio = 0.224
    x_right_base_ratio = 0.768
    y_top_base_ratio = 0.2416
    y_bottom_base_ratio = 0.593

    def __init__(self):
        self.deck_page_card_list = []
        self.deck_page_card_object_list = []

    def set_total_window_size(self, width, height):
        self.total_width = width
        self.total_height = height

    def set_page_number(self, page_number):
        self.page_number = page_number

    def add_deck_to_page(self, deck_list):
        if isinstance(deck_list, list):
            self.deck_page_card_list.extend(deck_list)

    def update_deck_to_page(self, deck_list):
        if isinstance(deck_list, list):
            self.deck_page_card_list = []
            self.deck_page_card_list.extend(deck_list)

    def get_deck_page_card_list(self):
        return self.deck_page_card_list

    def get_deck_page_card_object_list(self):
        return self.deck_page_card_object_list

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
        deck_page_card_list = self.get_deck_page_card_list()
        print(f"current_deck_state: {deck_page_card_list}")

        for index, card_number in enumerate(deck_page_card_list):
            print(f"index: {index}, card_number: {card_number}")
            new_card = LegacyFixedFieldCard(local_translation=self.get_next_card_position(index))
            new_card.init_card(card_number)
            new_card.set_index(index)
            self.deck_page_card_object_list.append(new_card)

    def remove_card_by_multiple_index(self, card_index_list):
        for index in sorted(card_index_list, reverse=True):
            if 0 <= index < len(self.deck_page_card_object_list):
                del self.deck_page_card_object_list[index]
                del self.deck_page_card_object_list[index]
            else:
                print(f"Invalid index: {index}. No card removed for this index.")

        print(
            f"Removed cards at indices {card_index_list} -> current_opponent_field_list: "
            f"{self.current_field_unit_card_object_list}, "
            f"current_opponent_field_state: {self.get_current_field_unit_state()}")
