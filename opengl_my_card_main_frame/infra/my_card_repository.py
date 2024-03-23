from math import ceil

from colorama import Fore, Style

from battle_field.state.current_deck import CurrentDeckState

from card_info_from_csv.repository.card_info_from_csv_repository_impl import CardInfoFromCsvRepositoryImpl
from opengl_my_card_main_frame.state.my_card_page import MyCardPage
from opengl_my_card_main_frame.state.my_card_state import MyCardState
from pre_drawed_image_manager.pre_drawed_image import PreDrawedImage


class MyCardRepository:
    __instance = None

    __card_info_repository = CardInfoFromCsvRepositoryImpl.getInstance()
    preDrawedImageInstance = PreDrawedImage.getInstance()

    total_width = None
    total_height = None

    my_card_state = MyCardState()
    my_card_page_list = []
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
        print(f"my_card_repository set_total_window_size -> width: {width}, height: {height}")
        self.total_width = width
        self.total_height = height

    def save_my_card_to_dictionary_state(self, my_card_dictionary_list):
        self.my_card_state.add_to_my_card_dictionary(my_card_dictionary_list)

    def save_my_card_number_to_state(self, acquire_my_card_list):
        self.my_card_state.add_to_my_card(acquire_my_card_list)
        print(f"Saved acquire_my_card_list state: {acquire_my_card_list}")

    def get_my_card_dictionary_from_state(self):
        return self.my_card_state.get_my_card_dictionary()

    def build_my_card_page(self):
        my_card_dictionary = self.get_my_card_dictionary_from_state()
        my_card_list = list(my_card_dictionary.keys())
        my_card_number_list = [int(card_id) for card_id in my_card_list]

        my_card_count_list = list(my_card_dictionary.values())

        # num_cards_per_page = 8
        num_cards_per_page = 4
        num_pages = ceil(len(my_card_number_list) / num_cards_per_page)
        print(f"{Fore.RED}num_pages: {Fore.GREEN}{num_pages}{Style.RESET_ALL}")

        for page_index in range(num_pages):
            start_index = page_index * num_cards_per_page
            end_index = (page_index + 1) * num_cards_per_page
            current_my_card_page = my_card_number_list[start_index:end_index]
            current_my_card_count_page = my_card_count_list[start_index:end_index]

            my_card_page = MyCardPage()
            my_card_page.set_total_window_size(self.total_width, self.total_height)
            my_card_page.add_my_card_to_page(current_my_card_page)
            my_card_page.add_my_card_count_to_page(current_my_card_count_page)

            my_card_page.set_page_number(page_index + 1)
            my_card_page.create_my_card_list()
            my_card_page.create_current_page_representation(page_index + 1)

            self.my_card_page_list.append(my_card_page)

        # x: 934, y: 929
        # x: 970, y: 902
        # self.create_max_page_representation(num_pages)

    def next_my_card_page(self):
        if self.current_page == len(self.my_card_page_list) - 1:
            return

        self.current_page += 1

    def prev_my_card_page(self):
        if self.current_page == 0:
            return

        self.current_page -= 1

    def get_current_my_card_page(self):
        return self.current_page

    def get_current_page_object(self):
        return self.my_card_page_list[self.get_current_my_card_page()]

    def get_my_card_object_list_from_current_page(self):
        # print(self.my_card_page_list)
        # print(self.get_current_my_card_page())
        return self.my_card_page_list[self.get_current_my_card_page()].get_my_card_page_card_object_list()

    def get_my_card_count_object_list_from_current_page(self):
        return self.my_card_page_list[self.get_current_my_card_page()].get_my_card_page_card_count_object_list()
