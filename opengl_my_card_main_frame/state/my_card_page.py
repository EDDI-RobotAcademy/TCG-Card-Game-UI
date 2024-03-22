from colorama import Fore, Style

from battle_field_fixed_card.fixed_field_card import FixedFieldCard
from card_info_from_csv.repository.card_info_from_csv_repository_impl import CardInfoFromCsvRepositoryImpl
from common.card_grade import CardGrade
from common.card_type import CardType
from image_shape.non_background_image import NonBackgroundImage
from opengl_battle_field_pickable_card.pickable_card import PickableCard
from pre_drawed_image_manager.pre_drawed_image import PreDrawedImage


class MyCardPage:

    __card_info_repository = CardInfoFromCsvRepositoryImpl.getInstance()
    __pre_drawed_image_instance = PreDrawedImage.getInstance()

    page_number = 0

    total_width = 0
    total_height = 0

    # 430 / 1920, 252 / 1043
    # 1490 / 1920, 252 / 1043
    # 6개 구성 (x_right_base_ratio - x_left_base_ratio) / 6
    # x_left_base_ratio = 0.024
    # 32 / 1848 -> 0.01731
    x_left_base_ratio = 0.01731
    x_right_base_ratio = 0.568

    # 282.625 -> 565.25
    # 282.625 / 1018 -> 0.27762

    # x: 364, y: 78
    # x: 390, y: 974
    # 974 - 78 = 896
    # 896 / 1018 -> 0.88015
    # 78 / 1018 -> 0.07662

    # 0.88015 / 2 -> 0.440075
    # 0.07662 + 0.440075 -> 0.516695
    # 0.07662 + 0.440075 - 0.27762 -> 0.516695 - 0.27762 -> 0.239075

    # x: 1028, y: 862
    # x: 1031, y: 974
    # 974 - 862 - > 112
    # 112 / 1018 -> 0.110019
    # 0.239075 + 0.110019 -> 0.349094
    # 0.239075 - 0.110019 -> 0.129056
    # 0.239075 / 2 -> 0.1195375
    # 0.1195375 + 0.129056 -> 0.2485935

    # y_bottom_base_ratio = 0.27762
    # y_bottom_base_ratio = 0.349094

    # 0.239075 - 0.03143 -> 0.207645
    # 32 / 1018 -> 0.03143
    y_bottom_base_ratio = 0.207645
    y_top_base_ratio = 0.593

    def __init__(self):
        self.my_card_page_card_list = []
        self.my_card_page_card_object_list = []

        self.my_card_page_card_count_list = []
        self.my_card_page_card_count_object_list = []

        self.start_x_point = 0
        self.end_x_point = self.total_width * 0.36
        self.start_y_point = 0
        self.end_y_point = self.total_height * 56

    def set_total_window_size(self, width, height):
        self.total_width = width
        self.total_height = height

    def set_page_number(self, page_number):
        self.page_number = page_number

    def add_my_card_to_page(self, my_card_list):
        if isinstance(my_card_list, list):
            self.my_card_page_card_list.extend(my_card_list)

    def add_my_card_count_to_page(self, my_card_count_list):
        if isinstance(my_card_count_list, list):
            self.my_card_page_card_count_list.extend(my_card_count_list)

    def update_my_card_to_page(self, my_card_list):
        if isinstance(my_card_list, list):
            self.my_card_page_card_list = []
            self.my_card_page_card_list.extend(my_card_list)

    def get_my_card_page_card_list(self):
        return self.my_card_page_card_list

    def get_my_card_page_card_object_list(self):
        return self.my_card_page_card_object_list

    def get_my_card_page_card_count_list(self):
        return self.my_card_page_card_count_list

    def get_my_card_page_card_count_object_list(self):
        return self.my_card_page_card_count_object_list

    # x: 50, y: 232
    # x: 1574, y: 242
    # 50 / 1848 -> 0.02705
    # 1574 / 1848 -> 0.85173
    # 242 / 1016 -> 0.23818
    # 732 / 1016 -> 0.72047

    # target_width = 1524 = 5x + 4y
    # 340 * 4 = 1360
    # 1524 - 1360 = 32.8 (33)
    # 373 / 1848 -> 0.20183
    # 340 / 1848 -> 0.18398
    # 1524 / 1848 -> 0.82467

    def get_next_card_position(self, index):
        print(f"my_card_page -> get_next_card_position() - self.total_width: {self.total_width}")
        # TODO: 배치 간격 고려
        current_card_size = 350
        card_width_ratio = current_card_size / self.total_width
        card_height_ratio = current_card_size * 1.615 / self.total_height

        # book_height_margin = 80
        # book_height_margin_ratio = book_height_margin / self.total_height
        book_height_margin_ratio = 0.07874
        print(f"book_height_margin_ratio: {book_height_margin_ratio}")

        # bottom_criteria_height = 860
        # bottom_criteria_height_ratio = bottom_criteria_height / self.total_height
        # print(f"bottom_criteria_height_ratio: {bottom_criteria_height_ratio}")

        # real_usage_height = bottom_criteria_height - book_height_margin
        # real_usage_height_ratio = real_usage_height / self.total_height
        # print(f"real_usage_height_ratio: {real_usage_height_ratio}")

        # card_height_margin_in_book = 128.6
        # card_height_margin_in_book_ratio = card_height_margin_in_book / self.total_height
        card_height_margin_in_book_ratio = 0.126574
        print(f"card_height_margin_in_book_ratio: {card_height_margin_in_book_ratio}")

        # 800 - 210 - 581.4 = 8.6
        # 80 + 581.4 + 105 + 8.6 = 775
        # 775 / 1016 -> 0.76279

        # 80 + 105 + 8.6 = 193.6
        # 193.6 / 1016 -> 0.19055

        # 80 + 120 + 8.6 = 208.6
        # 208.6 / 1016 -> 0.20531
        # 0.20669

        # card_position_height = (book_height_margin + card_height_margin_in_book) / self.total_height

        # card_extra_margin_height_ratio = real_usage_height_ratio - (card_height_margin_in_book_ratio * 2 + card_height_ratio)
        # print(f"card_extra_margin_height_ratio: {card_extra_margin_height_ratio}")
        #
        # top_height = (book_height_margin_ratio +
        #               card_height_margin_in_book_ratio +
        #               card_extra_margin_height_ratio)

        # bottom_height = (top_height + card_height_ratio) * self.total_height
        bottom_height = (book_height_margin_ratio + card_height_margin_in_book_ratio) * self.total_height
        test_height = 0.76279 * self.total_height
        # other_test_height = 0.20669 * self.total_height

        place_index = index % 4

        # card_width_ratio
        card_between_width_margin = 55
        card_between_width_margin_ratio = card_between_width_margin / self.total_width

        # 1631 / 1850 = 0.88162
        limit_boundary_width_ratio = 0.88162
        # 1630 / 1850 = 0.88108
        # limit_boundary_width_ratio = 0.88108

        # extra_margin_ratio = (limit_boundary_width_ratio - (card_width_ratio * 4.0 + card_between_width_margin_ratio * 3.0)) / 2.0
        extra_margin_ratio = (limit_boundary_width_ratio - (card_width_ratio * 4.0 + card_between_width_margin_ratio * 3.0)) / 2.0
        print(f"extra_margin_ratio: {extra_margin_ratio}")

        # current_y = self.total_height * self.y_bottom_base_ratio
        # base_x = self.total_width * self.x_left_base_ratio
        # 1631 - 1590 (360 * 4 + 50 * 3) = 41
        # 41 / 2 = 20.5
        # 20.5 / 1850 = 0.011081
        base_x = extra_margin_ratio * self.total_width

        # 0.20183 - 0.18398
        # 0.82467
        # x_increment = 0.87467 / 4.0
        # x_increment = (limit_boundary_width_ratio - extra_margin_ratio * 2) / 4.0
        next_x = base_x + self.total_width * (card_between_width_margin_ratio * place_index) + self.total_width * card_width_ratio * place_index
        print(f"{Fore.RED}next_x: {next_x}, bottom: {bottom_height}{Style.RESET_ALL}")
        # print(f"{Fore.RED}other_test_height: {other_test_height}{Style.RESET_ALL}")
        return (next_x, bottom_height)

    def create_my_card_list(self):
        my_card_page_card_list = self.get_my_card_page_card_list()
        # print(f"my_card_page_card_list: {my_card_page_card_list}")

        my_card_page_card_count_list = self.get_my_card_page_card_count_list()

        for index, card_id in enumerate(my_card_page_card_list):
            # print(f"index: {index}, card_number: {card_id}")
            my_card = PickableCard(local_translation=self.get_next_card_position(index))
            # new_card = FixedFieldCard(local_translation=self.get_next_card_position(index))
            # print("Success to make PickableCard")
            my_card.init_card_in_my_card_frame(card_id, self.total_width, self.total_height)
            # my_card.init_card(card_id)
            # print("Success to create card frame")
            my_card.set_index(index)
            self.my_card_page_card_object_list.append(my_card)

        # for index, card_count in enumerate(my_card_page_card_count_list):
        #     my_card_count = 0
        #     if card_count == 1:
        #         continue
        #
        #     else:
        #         number_of_cards_image_data = self.__pre_drawed_image_instance.get_pre_draw_number_of_cards(card_count)
        #         number_of_cards_text = NonBackgroundImage(image_data=number_of_cards_image_data,
        #                                                   vertices=[
        #                                                       (self.start_x_point, self.start_y_point),
        #                                                       (self.end_x_point, self.start_y_point),
        #                                                       (self.end_x_point, self.end_y_point),
        #                                                       (self.start_x_point, self.end_y_point)
        #                                                   ],
        #                                                   local_translation=self.get_next_card_count_position(index))
        #
        #         self.my_card_page_card_count_object_list.append(number_of_cards_text)



        # number_left_x_point = self.width * 0.130  # 첫 번째 카드는 이 위치로 고정
        # number_right_x_point = self.width * 0.166
        # number_top_y_point = self.height * 0.450  # 첫 번째줄은 이 높이로 고정하면 될 듯
        # number_bottom_y_point = self.height * 0.506
        # for index, card_count in enumerate(card_count_list):
        #     try:
        #         if card_count == 1:
        #             # number_of_cards_data = self.__pre_drawed_image_instance.get_pre_draw_number_of_cards(9)
        #             self.my_card_main_scene.add_text_list(None)
        #         else:
        #             number_of_cards_data = self.__pre_drawed_image_instance.get_pre_draw_number_of_cards(card_count)
        #
        #             number_of_cards_text = NonBackgroundImage(image_data=number_of_cards_data,
        #                                                        vertices=[
        #                                                            (number_left_x_point, number_top_y_point),
        #                                                            (number_right_x_point, number_top_y_point),
        #                                                            (number_right_x_point, number_bottom_y_point),
        #                                                            (number_left_x_point, number_bottom_y_point)
        #                                                        ])
        #             self.my_card_main_scene.add_text_list(number_of_cards_text)
        #
        #         number_left_x_point += self.width * 0.164
        #         number_right_x_point += self.width * 0.164
        #
        #         if (index + 1) % 4 == 0:
        #             number_top_y_point = self.height * 0.940  # 두 번째 줄 부턴 위치 바뀜
        #             number_bottom_y_point = self.height * 0.996
        #             number_left_x_point = self.width * 0.130
        #             number_right_x_point = self.width * 0.166
        #
        #             if (index + 1) % 8 == 0:
        #                 number_left_x_point = self.width * 0.130
        #                 number_right_x_point = self.width * 0.166
        #                 number_top_y_point = self.height * 0.450
        #                 number_bottom_y_point = self.height * 0.506
        #
        #         if (index + 1) % 8 == 0:
        #             continue
        #
        #     except Exception as e:
        #         print(f"Error number text: {e}")
        #         pass

        # x: 385, y: 434
        # x: 435, y: 433
        # 카드 간격 <-> 50
        # 50 / 1850 -> 0.02702

        # 0.036 <= x_ratio
        # 0.056 <= y_ratio

        def get_next_card_count_position(self, index):
            print(f"my_card_page -> get_next_card_count_position() - self.total_width: {self.total_width}")
            # TODO: 배치 간격 고려
            card_width_ratio = 350 / self.total_width
            place_index = index % 4

            current_y = self.total_height * (self.y_bottom_base_ratio - 0.1)

            card_between_width_margin = 55
            card_between_width_margin_ratio = card_between_width_margin / self.total_width

            # 1631 / 1850 = 0.88162
            limit_boundary_width_ratio = 0.88162
            # 1630 / 1850 = 0.88108
            # limit_boundary_width_ratio = 0.88108

            # extra_margin_ratio = (limit_boundary_width_ratio - (card_width_ratio * 4.0 + card_between_width_margin_ratio * 3.0)) / 2.0
            extra_margin_ratio = (limit_boundary_width_ratio - (card_width_ratio * 4.0 + card_between_width_margin_ratio * 3.0)) / 2.0
            print(f"extra_margin_ratio: {extra_margin_ratio}")

            base_x = extra_margin_ratio * self.total_width

            # 0.20183 - 0.18398
            # 0.82467
            # x_increment = 0.87467 / 4.0
            # x_increment = (limit_boundary_width_ratio - extra_margin_ratio * 2) / 4.0
            next_x = base_x + self.total_width * (card_between_width_margin_ratio * place_index) + self.total_width * card_width_ratio * place_index
            print(f"{Fore.RED}next_x: {next_x}{Style.RESET_ALL}")

            # next_x = base_x + self.total_width * (x_increment * place_index)
            return (next_x, current_y)
