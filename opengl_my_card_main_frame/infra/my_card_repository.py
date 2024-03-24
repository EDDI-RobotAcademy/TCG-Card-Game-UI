from math import ceil

from colorama import Fore, Style

from battle_field.state.current_deck import CurrentDeckState

from card_info_from_csv.repository.card_info_from_csv_repository_impl import CardInfoFromCsvRepositoryImpl
from image_shape.non_background_image import NonBackgroundImage
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
    page_slash_object = None
    max_page_object = None

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
        self.create_max_page_representation(num_pages)
        self.create_page_slash()

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


    def create_max_page_representation(self, num_pages):
        # x: 934, y: 929
        # x: 970, y: 902
        # 31 / 1848 = 0.0167748
        start_x_point = 0.4981674 * self.total_width
        end_x_point = 0.5320914 * self.total_width
        start_y_point = 0.866437 * self.total_height
        end_y_point = 0.9354015 * self.total_height

        max_page_number_image = self.preDrawedImageInstance.get_pre_drawed_page_number(num_pages)
        max_page_number = NonBackgroundImage(image_data=max_page_number_image,
                                             vertices=[
                                                 (start_x_point, start_y_point),
                                                 (end_x_point, start_y_point),
                                                 (end_x_point, end_y_point),
                                                 (start_x_point, end_y_point)
                                             ])
        self.max_page_object = max_page_number

    def get_max_page_object(self):
        return self.max_page_object

    def create_page_slash(self):
        # x: 934, y: 929
        # x: 970, y: 902
        # 31 / 1848 = 0.0167748
        start_x_point = 0.4764674 * self.total_width
        end_x_point = 0.5103914 * self.total_width
        start_y_point = 0.866437 * self.total_height
        end_y_point = 0.9354015 * self.total_height

        page_slash_image = self.preDrawedImageInstance.get_pre_draw_page_slash()
        page_slash = NonBackgroundImage(image_data=page_slash_image,
                                        vertices=[
                                            (start_x_point, start_y_point),
                                            (end_x_point, start_y_point),
                                            (end_x_point, end_y_point),
                                            (start_x_point, end_y_point)
                                        ])
        self.page_slash_object = page_slash

    def get_page_slash_object(self):
        return self.page_slash_object
