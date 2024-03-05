from opengl_battle_field_pickable_card.legacy.pickable_card import LegacyPickableCard


class LegacyYourHandPage:

    page_number = 0

    total_width = 0
    total_height = 0

    x_base = 0

    def __init__(self):
        self.your_hand_page_card_list = []
        self.your_hand_page_card_object_list = []

    def set_total_window_size(self, width, height):
        self.total_width = width
        self.total_height = height

    def set_hand_page_number(self, page_number):
        print(f"set_hand_page_number -> page_number: {page_number}")
        self.page_number = page_number

    def add_hand_to_page(self, hand_list):
        print(f"YourHandPage -> add_hand_to_page(): {hand_list}")
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

    def get_next_card_position(self, index):
        current_y = 830

        start = self.total_width * 0.2976
        end = self.total_width * 0.6997
        gap_width = (end - start - 525.0) / 4.0

        x_increment = 105 + gap_width

        # 550 <-> 1290
        # Card -> 105
        # Gap -> gap_width => gap_count = Card Count - 1
        # 740 = 105 * 5 + gap_width * 4
        # 740 = 525 + 215
        # 215 / 4 = 53.75
        place_index = index % 5

        self.x_base = start
        next_x = self.x_base + x_increment * place_index
        return (next_x, current_y)

    def create_your_hand_card_list(self):
        your_hand_page_card_list = self.get_your_hand_page_card_list()
        print(f"your_hand_page_card_list: {your_hand_page_card_list}")

        for index, card_number in enumerate(your_hand_page_card_list):
            print(f"index: {index}, card_number: {card_number}")
            new_card = LegacyPickableCard(local_translation=self.get_next_card_position(index))
            new_card.init_card(card_number)
            new_card.set_index(index)
            self.your_hand_page_card_object_list.append(new_card)

    def remove_your_hand_card_by_multiple_index(self, card_index_list):
        for index in sorted(card_index_list, reverse=True):
            if 0 <= index < len(self.your_hand_page_card_object_list):
                del self.your_hand_page_card_object_list[index]
                del self.your_hand_page_card_object_list[index]
            else:
                print(f"Invalid index: {index}. No card removed for this index.")

        print(
            f"Removed cards at indices {card_index_list} -> your_hand_page_card_list: "
            f"{self.your_hand_page_card_list}, "
            f"your_hand_page_card_object_list: {self.your_hand_page_card_object_list}")

    def find_index_by_selected_object(self, selected_object):
        for index, card in enumerate(self.your_hand_page_card_object_list):
            if card == selected_object:
                return index
        return -1

    def remove_card_by_index(self, card_placed_index):
        print(f"remove_card_by_index -> self.your_hand_page_card_object_list: {self.your_hand_page_card_object_list}, card_placed_index: {card_placed_index}")

        if 0 <= card_placed_index < len(self.your_hand_page_card_object_list):
            del self.your_hand_page_card_object_list[card_placed_index]
            # self.current_hand_state.remove_hand_by_index(card_placed_index)

            print(
                f"Removed card index {card_placed_index} -> your_hand_page_card_object_list: {self.your_hand_page_card_object_list}")
        else:
            print(f"Invalid index: {card_placed_index}. 지울 것이 없다.")
