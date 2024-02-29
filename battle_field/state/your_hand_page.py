from battle_field_fixed_card.fixed_field_card import FixedFieldCard
from opengl_battle_field_pickable_card.pickable_card import PickableCard


class YourHandPage:

    page_number = 0

    total_width = 0
    total_height = 0


    def __init__(self):
        self.your_hand_page_card_list = []
        self.your_hand_page_card_object_list = []

    def set_total_window_size(self, width, height):
        self.total_width = width
        self.total_height = height

    def set_hand_page_number(self, page_number):
        self.page_number = page_number

    def add_hand_to_page(self, hand_list):
        if isinstance(hand_list, list):
            self.your_hand_page_card_list.extend(hand_list)

    def update_hand_to_page(self, hand_list):
        if isinstance(hand_list, list):
            self.your_hand_page_card_list = []
            self.your_hand_page_card_list.extend(hand_list)

    def get_your_hand_page_card_list(self):
        return self.your_hand_page_card_list

    def get_your_hand_page_card_object_list(self):
        return self.your_hand_page_card_object_list


    def remove_your_hand_card_by_multiple_index(self, card_index_list):
        for index in sorted(card_index_list, reverse=True):
            if 0 <= index < len(self.your_hand_page_card_object_list):
                del self.your_hand_page_card_object_list[index]
                del self.your_hand_page_card_object_list[index]
            else:
                print(f"Invalid index: {index}. No card removed for this index.")

        print(
            f"Removed cards at indices {card_index_list} -> current_opponent_field_list: "
            f"{self.current_field_unit_card_object_list}, "
            f"current_opponent_field_state: {self.get_current_field_unit_state()}")
