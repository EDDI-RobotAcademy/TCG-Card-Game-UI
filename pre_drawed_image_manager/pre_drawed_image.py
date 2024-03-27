import os

from card_info_from_csv.repository.card_info_from_csv_repository_impl import CardInfoFromCsvRepositoryImpl
from common.utility import get_project_root
from utility.image_data_loader import ImageDataLoader


class PreDrawedImage:
    __instance = None
    __card_info_from_csv_repository = CardInfoFromCsvRepositoryImpl().getInstance()

    __project_root = get_project_root()

    __pre_drawed_card_frame = {}
    __pre_drawed_battle_field_card_frame = {}
    __pre_drawed_random_buy_card_frame = {}

    __pre_drawed_card_illustration = {}

    __pre_drawed_card_race = {}
    __pre_drawed_card_type = {}
    __pre_drawed_card_attack = {}
    __pre_drawed_card_hp = {}
    __pre_drawed_numbers = {}
    __pre_drawed_character_hp = {}
    __pre_drawed_rectangle_number = {}
    __pre_drawed_energy_race = {}
    __pre_drawed_dark_flame = None
    __pre_drawed_freezing = None

    __pre_drawed_card_type_mark = {}

    __pre_drawed_gif = None

    __pre_drawed_opponent_tomb = None
    __pre_drawed_opponent_lost_zone = None
    __pre_drawed_opponent_trap = None
    __pre_drawed_opponent_card_deck = None
    __pre_drawed_opponent_main_character = None
    __pre_drawed_opponent_hand_panel = None
    __pre_drawed_opponent_unit_field = None

    __pre_drawed_your_tomb = None
    __pre_drawed_your_lost_zone = None
    __pre_drawed_your_trap = None
    __pre_drawed_your_card_deck = None
    __pre_drawed_your_main_character = None
    __pre_drawed_your_hand_panel = None
    __pre_drawed_your_unit_field = None

    __pre_drawed_popup_panel = None

    __pre_drawed_field_energy = {}
    __pre_drawed_battle_field_environment = None
    __pre_drawed_turn_end_button = None
    __pre_drawed_turn_number = {}

    __pre_drawed_win_text = None
    __pre_drawed_lose_text = None
    __pre_drawed_battle_result_background = None

    __pre_drawed_confirm_button = None

    __pre_drawed_prev_button = None
    __pre_drawed_reset_button = None
    __pre_drawed_battle_field_muligun_background = None
    __pre_drawed_battle_field_background = None

    __pre_drawed_buy_random_background = None

    __pre_drawed_card_back_frame = None

    __pre_drawed_next_gold_button = None
    __pre_drawed_prev_gold_button = None
    __pre_drawed_ok_button = None

    __pre_drawed_general_attack_button = None
    __pre_drawed_detail_button = None

    __pre_drawed_multi_draw_button = None

    # TODO: 실제로는 숫자로 처리해야함 (유닛 번호 -> 액티브 스킬 1)
    # 유닛 번호 -> 액티브 스킬 2 형태가 되어야함
    __pre_drawed_shadow_ball_button = None #스킬1 버튼(쉐도우 볼)
    __pre_drawed_sea_of_spector_button = None #스킬2 버튼(망령의 바다)

    __pre_drawed_animation = {}
    __pre_drawed_effect_animation = {}

    __pre_drawed_number_of_energy = {}

    __pre_drawed_surrender_button = None
    __pre_drawed_surrender_confirm_panel = None

    __pre_drawed_unit_energy = {}
    __pre_drawed_unit_hp = {}
    __pre_drawed_unit_attack = {}
    __pre_drawed_unit_race = {}
    __pre_drawed_wizard_card_attack_power = {}

    __pre_drawed_paper = None
    __pre_drawed_scissor = None
    __pre_drawed_rock = None

    __pre_drawed_my_card_background = None
    __pre_drawed_number_of_cards = {}
    __pre_drawed_number_of_details_energy = {}

    __pre_drawed_waiting_message = None
    __pre_drawed_message_on_the_battle_screen = {}
    __pre_draw_use_energy_opponent_unit = {}

    __pre_drawed_battle_field_timer = {}
    __pre_drawed_mulligan_timer = {}

    __pre_drawed_create_deck_button = None
    __pre_drawed_go_back_button = None

    __pre_drawed_page_slash = None
    __pre_drawed_page_number = {}

    __pre_drawed_dark_flame_effect = {}

    __pre_drawed_try_again_screen = None
    __pre_drawed_yes_button = None
    __pre_drawed_no_button = None

    __pre_drawed_preparing_message = None
    __pre_drawed_preparing_ok_button = None

    __pre_drawed_loading_screen = {}
    __pre_drawed_card_drawing_scene = {}

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
        return cls.__instance

    @classmethod
    def getInstance(cls):
        if cls.__instance is None:
            cls.__instance = cls()
        return cls.__instance

    def pre_draw_dark_flame_effect_animation(self):
        pre_drawed_dark_flame_effect = {}
        image_dir = os.path.join(self.__project_root, "local_storage", "animation",
                                 'burn_effect')
        file_list = os.listdir(image_dir)

        for number in range(0, len(file_list)):
            animation_image_data = os.path.join(self.__project_root, "local_storage", "animation", 'burn_effect',
                                                f"{number}.png")
            # print(f"effect_animation_image_data = {animation_image_data}")
            pre_drawed_dark_flame_effect[number] = ImageDataLoader.load_rectangle_image_data(animation_image_data)
        self.__pre_drawed_effect_animation['burn_effect'] = pre_drawed_dark_flame_effect

    def pre_draw_freeze_effect_animation(self):
        pre_drawed_frozen_effect = {}
        image_dir = os.path.join(self.__project_root, "local_storage", "animation",
                                 'frozen_effect')
        file_list = os.listdir(image_dir)

        for number in range(0, len(file_list)):
            animation_image_data = os.path.join(self.__project_root, "local_storage", "animation", 'frozen_effect',
                                                f"{number}.png")
            # print(f"effect_animation_image_data = {animation_image_data}")
            pre_drawed_frozen_effect[number] = ImageDataLoader.load_rectangle_image_data(animation_image_data)
        self.__pre_drawed_effect_animation['frozen_effect'] = pre_drawed_frozen_effect

    def pre_draw_call_of_Leonic_effect_animation(self):
        pre_draw_effect_animation = {}
        image_dir = os.path.join(self.__project_root, "local_storage", "animation",
                                 'call_of_leonic')
        file_list = os.listdir(image_dir)

        for number in range(0, len(file_list)):
            animation_image_data = os.path.join(self.__project_root, "local_storage", "animation", 'call_of_leonic',
                                                f"{number}.png")
            # print(f"effect_animation_image_data = {animation_image_data}")
            pre_draw_effect_animation[number] = ImageDataLoader.load_rectangle_image_data(animation_image_data)
        self.__pre_drawed_effect_animation['call_of_leonic'] = pre_draw_effect_animation

    def pre_draw_full_screen_call_of_Leonic_effect_animation(self, width, height):
        # print(f"pre_draw_full_screen_call_of_leonic -> width: {width}, height: {height}")
        call_of_leonic_animation = {}
        image_dir = os.path.join(self.__project_root, "local_storage", "animation",
                                 'call_of_leonic')
        file_list = os.listdir(image_dir)

        for number in range(0, len(file_list)):
            animation_image_data = os.path.join(self.__project_root, "local_storage", "animation", 'call_of_leonic',
                                                f"{number}.png")
            # print(f"effect_animation_image_data = {animation_image_data}")
            call_of_leonic_animation[number] = ImageDataLoader.load_force_fit_full_screen_image_data(
                animation_image_data, width + 300, height + 300)

        self.__pre_drawed_effect_animation['call_of_leonic'] = call_of_leonic_animation


    def pre_draw_field_of_death_effect_animation(self):
        pre_draw_effect_animation = {}
        image_dir = os.path.join(self.__project_root, "local_storage", "animation",
                                 'field_of_death')
        file_list = os.listdir(image_dir)

        for number in range(0, len(file_list)):
            animation_image_data = os.path.join(self.__project_root, "local_storage", "animation", 'field_of_death',
                                                f"{number}.png")
            # print(f"effect_animation_image_data = {animation_image_data}")
            pre_draw_effect_animation[number] = ImageDataLoader.load_rectangle_image_data(animation_image_data)
        self.__pre_drawed_effect_animation['field_of_death'] = pre_draw_effect_animation

    def pre_draw_overflow_of_energy_effect_animation(self):
        pre_draw_effect_animation = {}
        image_dir = os.path.join(self.__project_root, "local_storage", "animation",
                                 'overflow_of_energy')
        file_list = os.listdir(image_dir)

        for number in range(0, len(file_list)):
            animation_image_data = os.path.join(self.__project_root, "local_storage", "animation", 'overflow_of_energy',
                                                f"{number}.png")
            # print(f"effect_animation_image_data = {animation_image_data}")
            pre_draw_effect_animation[number] = ImageDataLoader.load_rectangle_image_data(animation_image_data)
        self.__pre_drawed_effect_animation['overflow_of_energy'] = pre_draw_effect_animation

    def pre_drawed_swamp_of_ghost_effect_animation(self):
        pre_draw_effect_animation = {}
        image_dir = os.path.join(self.__project_root, "local_storage", "animation",
                                 'swamp_of_ghost')
        file_list = os.listdir(image_dir)

        for number in range(0, len(file_list)):
            animation_image_data = os.path.join(self.__project_root, "local_storage", "animation", 'swamp_of_ghost',
                                                f"{number}.png")
            # print(f"effect_animation_image_data = {animation_image_data}")
            pre_draw_effect_animation[number] = ImageDataLoader.load_rectangle_image_data(animation_image_data)
        self.__pre_drawed_effect_animation['swamp_of_ghost'] = pre_draw_effect_animation


    def pre_draw_card_frame(self):
        for card_number in self.__card_info_from_csv_repository.getCardNumber():
            card_frame_image_data = os.path.join(self.__project_root, "local_storage", "card_frame",
                                                 f"{card_number}.png")
            # self.__pre_drawed_card_frame[card_number] = ImageDataLoader.load_rectangle_image_data(card_frame_image_data)
            # load_rectangle_origin_image_data
            # self.__pre_drawed_card_frame[card_number] = ImageDataLoader.load_card_frame_image_data(card_frame_image_data)
            self.__pre_drawed_card_frame[card_number] = ImageDataLoader.load_rectangle_origin_image_data(card_frame_image_data)

    def pre_draw_opponent_tomb(self):
        tomb_image_path = os.path.join(self.__project_root, "local_storage", "image", "battle_field", "tomb.jpeg")
        self.__pre_drawed_opponent_tomb = ImageDataLoader.load_rectangle_image_data(tomb_image_path)

    def pre_draw_page_slash(self):
        page_slash_image_path = os.path.join(self.__project_root, "local_storage", "my_card_frame", "number_of_page", "0.png")
        self.__pre_drawed_page_slash = ImageDataLoader.load_rectangle_origin_image_data(page_slash_image_path)

    def pre_draw_opponent_lost_zone(self):
        lost_zone_image_path = os.path.join(self.__project_root, "local_storage", "image", "battle_field",
                                            "lost_zone.png")
        self.__pre_drawed_opponent_lost_zone = ImageDataLoader.load_rectangle_image_data(lost_zone_image_path)

    def pre_draw_opponent_trap(self):
        trap_image_path = os.path.join(self.__project_root, "local_storage", "image", "battle_field", "trap.jpeg")
        self.__pre_drawed_opponent_trap = ImageDataLoader.load_rectangle_image_data(trap_image_path)

    def pre_draw_opponent_card_deck(self):
        opponent_card_deck_image_path = os.path.join(self.__project_root, "local_storage", "image", "battle_field",
                                                     "opponent_card_deck.png")
        self.__pre_drawed_opponent_card_deck = ImageDataLoader.load_rectangle_image_data(opponent_card_deck_image_path)

    def pre_draw_opponent_main_character(self):
        opponent_main_character_image_path = os.path.join(self.__project_root, "local_storage", "image", "battle_field",
                                                          "main_character.png")
        self.__pre_drawed_opponent_main_character = ImageDataLoader.load_oval_image_data(
            opponent_main_character_image_path)

    def pre_draw_opponent_hand_panel(self):
        opponent_hand_panel_image_path = os.path.join(self.__project_root, "local_storage", "image", "battle_field",
                                                      "background.png")
        self.__pre_drawed_opponent_hand_panel = ImageDataLoader.load_rectangle_image_data(
            opponent_hand_panel_image_path)

    def pre_draw_opponent_unit_field(self):
        opponent_unit_field_image_path = os.path.join(self.__project_root, "local_storage", "image", "battle_field",
                                                      "background.png")
        self.__pre_drawed_opponent_unit_field = ImageDataLoader.load_rectangle_image_data(
            opponent_unit_field_image_path)

    def pre_draw_popup_panel(self):
        popup_panel_image_path =  os.path.join(self.__project_root, "local_storage", "image", "battle_field",
                                                      "popup_background.png")
        self.__pre_drawed_popup_panel = ImageDataLoader.load_rectangle_image_data(
            popup_panel_image_path)

    def pre_draw_your_tomb(self):
        tomb_image_path = os.path.join(self.__project_root, "local_storage", "image", "battle_field", "tomb.jpeg")
        self.__pre_drawed_your_tomb = ImageDataLoader.load_rectangle_image_data(tomb_image_path)

    def pre_draw_your_lost_zone(self):
        lost_zone_image_path = os.path.join(self.__project_root, "local_storage", "image", "battle_field",
                                            "lost_zone.png")
        self.__pre_drawed_your_lost_zone = ImageDataLoader.load_rectangle_image_data(lost_zone_image_path)

    def pre_draw_your_trap(self):
        trap_image_path = os.path.join(self.__project_root, "local_storage", "image", "battle_field", "trap.jpeg")
        self.__pre_drawed_your_trap = ImageDataLoader.load_rectangle_image_data(trap_image_path)

    def pre_draw_your_card_deck(self):
        your_card_deck_image_path = os.path.join(self.__project_root, "local_storage", "image", "battle_field",
                                                 "your_card_deck.png")
        self.__pre_drawed_your_card_deck = ImageDataLoader.load_rectangle_image_data(your_card_deck_image_path)

    def pre_draw_your_main_character(self):
        your_main_character_image_path = os.path.join(self.__project_root, "local_storage", "image", "battle_field",
                                                      "main_character.png")
        self.__pre_drawed_your_main_character = ImageDataLoader.load_oval_image_data(your_main_character_image_path)

    def pre_draw_your_hand_panel(self):
        your_hand_panel_image_path = os.path.join(self.__project_root, "local_storage", "image", "battle_field",
                                                  "background.png")
        self.__pre_drawed_your_hand_panel = ImageDataLoader.load_rectangle_image_data(your_hand_panel_image_path)

    def pre_draw_create_deck_button(self):
        create_deck_button_image_path = os.path.join(self.__project_root, "local_storage", "my_card_frame", "creat_deck_button.png")
        self.__pre_drawed_create_deck_button = ImageDataLoader.load_rectangle_origin_image_data(create_deck_button_image_path)

    def pre_draw_go_back_button(self):
        go_back_button_image_path = os.path.join(self.__project_root, "local_storage", "my_card_frame", "go_to_back_button.png")
        self.__pre_drawed_go_back_button = ImageDataLoader.load_rectangle_origin_image_data(go_back_button_image_path)

    def pre_draw_your_unit_field(self):
        your_unit_field_image_path = os.path.join(self.__project_root, "local_storage", "image", "battle_field",
                                                  "background.png")
        self.__pre_drawed_your_unit_field = ImageDataLoader.load_rectangle_image_data(your_unit_field_image_path)

    def pre_draw_battle_field_environment(self):
        battle_field_environment_image_path = os.path.join(self.__project_root, "local_storage", "image",
                                                           "battle_field", "environment.jpeg")
        self.__pre_drawed_battle_field_environment = ImageDataLoader.load_rectangle_image_data(
            battle_field_environment_image_path)

    def pre_draw_battle_result_background(self):
        battle_result_background_image_path = os.path.join(self.__project_root, "local_storage", "image", "battle_field",
                                           "battle_result_background.png")
        self.__pre_drawed_battle_result_background = ImageDataLoader.load_rectangle_image_data(battle_result_background_image_path)

    def pre_draw_win_text(self):
        win_text_image_path = os.path.join(self.__project_root, "local_storage", "image", "battle_field",
                                           "win.png")
        self.__pre_drawed_win_text = ImageDataLoader.load_rectangle_image_data(win_text_image_path)

    def pre_draw_lose_text(self):
        lose_text_image_path = os.path.join(self.__project_root, "local_storage", "image", "battle_field",
                                            # "win.png")
                                            "lose.png")
        self.__pre_drawed_lose_text = ImageDataLoader.load_rectangle_image_data(lose_text_image_path)

    def pre_draw_turn_end_button(self):
        turn_end_button_image_path = os.path.join(self.__project_root, "local_storage", "image", "battle_field",
                                                  "turn_end_button.png")
        self.__pre_drawed_turn_end_button = ImageDataLoader.load_rectangle_image_data(turn_end_button_image_path)

    def pre_draw_card_illustration(self):
        for card_number in self.__card_info_from_csv_repository.getCardNumber():
            card_illustration_image_data = os.path.join(self.__project_root, "local_storage", "card_images",
                                                        f"{card_number}.png")
            self.__pre_drawed_card_illustration[card_number] = ImageDataLoader.load_rectangle_image_data(
                card_illustration_image_data)

    def pre_draw_card_drawing_scene(self, width = None, height = None):
        image_dir = os.path.join(self.__project_root, "local_storage", "animation", "card_drawing_scene")
        file_list = os.listdir(image_dir)

        for number in range(0, len(file_list)):
            number_image_data = os.path.join(self.__project_root, "local_storage", "animation", "card_drawing_scene", f"{number}.png")
            # print(f"image data = {number_image_data}")
            self.__pre_drawed_card_drawing_scene[number] = ImageDataLoader.load_rectangle_image_data(number_image_data)

        #todo : 풀스크린으로 변경해야할수있음

        # image_dir = os.path.join(self.__project_root, "local_storage", "animation", "card_drawing_scene")
        # file_list = os.listdir(image_dir)
        #
        # for number in range(0, len(file_list)):
        #     number_image_data = os.path.join(self.__project_root, "local_storage", "animation", "card_drawing_scene", f"{number}.png")
        #     print(f"effect_animation_image_data = {number_image_data}")
        #     self.__pre_drawed_card_drawing_scene[number] = ImageDataLoader.load_force_fit_full_screen_image_data(
        #         number_image_data, width + 300, height + 300)

    def pre_draw_character_hp(self):
        image_dir = os.path.join(self.__project_root, "local_storage", "unit_card_hp")
        file_list = os.listdir(image_dir)

        for number in range(0, len(file_list)):
            number_image_data = os.path.join(self.__project_root, "local_storage", "unit_card_hp", f"{number}.png")
            # print(f"image data = {number_image_data}")
            self.__pre_drawed_character_hp[number] = ImageDataLoader.load_rectangle_image_data(number_image_data)

    def pre_draw_rectangle_number_image(self):
        image_dir = os.path.join(self.__project_root, "local_storage", "card_number_image")
        file_list = os.listdir(image_dir)

        for number in range(0, len(file_list)):
            number_image_data = os.path.join(self.__project_root, "local_storage", "card_number_image", f"{number}.png")
            # print(f"image data = {number_image_data}")
            self.__pre_drawed_rectangle_number[number] = ImageDataLoader.load_rectangle_image_data(number_image_data)

    def pre_draw_confirm_button(self):
        confirm_button_image_path = os.path.join(self.__project_root, "local_storage", "image", "battle_field",
                                                 "confirm_button.png")
        self.__pre_drawed_turn_end_button = ImageDataLoader.load_rectangle_image_data(confirm_button_image_path)

    def pre_draw_card_race(self):
        image_dir = os.path.join(self.__project_root, "local_storage", "card_race_image")
        file_list = os.listdir(image_dir)
        png_files = [file for file in file_list if file.lower().endswith('.png')]

        card_race_image_data_list = {}

        for png_file in png_files:
            race_number = int(png_file[:-4])
            # print(f"race_number: {race_number}")
            card_race_image_data = os.path.join(self.__project_root, "local_storage", "card_race_image", f"{png_file}")
            card_race_image_data_list[race_number] = ImageDataLoader.load_circle_image_data(card_race_image_data)

        for card_number in self.__card_info_from_csv_repository.getCardNumber():
            race_number = self.__card_info_from_csv_repository.getCardRaceForCardNumber(card_number)
            # print(f"race_number: {race_number}, card_number: {card_number}")
            self.__pre_drawed_card_race[card_number] = card_race_image_data_list[race_number]

    def pre_draw_energy_race(self):
        image_dir = os.path.join(self.__project_root, "local_storage", "card_race_image")
        file_list = os.listdir(image_dir)
        png_files = [file for file in file_list if file.lower().endswith('.png')]

        for png_file in png_files:
            race_number = int(png_file[:-4])
            # print(f"race_number: {race_number}")
            card_race_image_data = os.path.join(self.__project_root, "local_storage", "card_race_image", f"{png_file}")
            self.__pre_drawed_energy_race[race_number] = ImageDataLoader.load_circle_image_data(card_race_image_data)

    def pre_draw_card_type(self):
        image_dir = os.path.join(self.__project_root, "local_storage", "card_type_image")
        file_list = os.listdir(image_dir)
        png_files = [file for file in file_list if file.lower().endswith('.png')]

        card_type_image_data_list = {}

        for png_file in png_files:
            type_number = int(png_file[:-4])
            # print(f"type_number: {type_number}")
            card_type_image_data = os.path.join(self.__project_root, "local_storage", "card_type_image", f"{png_file}")
            card_type_image_data_list[type_number] = ImageDataLoader.load_circle_image_data(card_type_image_data)

        for card_number in self.__card_info_from_csv_repository.getCardNumber():
            type_number = self.__card_info_from_csv_repository.getCardTypeForCardNumber(card_number)
            # print(f"type_number: {type_number}, card_number: {card_number}")
            self.__pre_drawed_card_type[card_number] = card_type_image_data_list[type_number]

    def pre_draw_page_number(self):
        image_dir = os.path.join(self.__project_root, "local_storage", "my_card_frame", "number_of_page")
        file_list = os.listdir(image_dir)

        for page_number in range(1, len(file_list) + 1):
            page_number_image_data = os.path.join(self.__project_root, "local_storage", "my_card_frame", "number_of_page", f"{page_number}.png")
            self.__pre_drawed_page_number[page_number] = ImageDataLoader.load_rectangle_origin_image_data(page_number_image_data)

    def pre_draw_mulligan_timer(self):
        image_dir = os.path.join(self.__project_root, "local_storage", "mulligan_timer")
        file_list = os.listdir(image_dir)

        for number in range(0, len(file_list) + 1):
            timer_image_data = os.path.join(self.__project_root, "local_storage", "mulligan_timer", f"{number}.png")
            # print(f"animation image data = {timer_image_data}")
            self.__pre_drawed_mulligan_timer[number] = ImageDataLoader.load_rectangle_image_data(timer_image_data)

    def pre_draw_card_attack(self):
        image_dir = os.path.join(self.__project_root, "local_storage", "card_number_image")
        file_list = os.listdir(image_dir)
        png_files = [file for file in file_list if file.lower().endswith('.png')]

        card_attack_image_data_list = {}

        for png_file in png_files:
            attack_number = int(png_file[:-4])
            # print(f"number images: {attack_number}")
            card_attack_image_data = os.path.join(self.__project_root, "local_storage", "card_number_image",
                                                  f"{png_file}")
            card_attack_image_data_list[attack_number] = ImageDataLoader.load_circle_image_data(card_attack_image_data)

        for card_number in self.__card_info_from_csv_repository.getCardNumber():
            attack_number = self.__card_info_from_csv_repository.getCardAttackForCardNumber(card_number)
            # print(f"attack_number: {attack_number}, card_number: {card_number}")
            self.__pre_drawed_card_attack[card_number] = card_attack_image_data_list[attack_number]

    def pre_draw_card_hp(self):
        image_dir = os.path.join(self.__project_root, "local_storage", "card_number_image")
        file_list = os.listdir(image_dir)
        png_files = [file for file in file_list if file.lower().endswith('.png')]

        card_hp_image_data_list = {}

        for png_file in png_files:
            hp_number = int(png_file[:-4])
            # print(f"number images: {hp_number}")
            card_hp_image_data = os.path.join(self.__project_root, "local_storage", "card_number_image", f"{png_file}")
            card_hp_image_data_list[hp_number] = ImageDataLoader.load_circle_image_data(card_hp_image_data)

        for card_number in self.__card_info_from_csv_repository.getCardNumber():
            hp_number = self.__card_info_from_csv_repository.getCardHpForCardNumber(card_number)
            # print(f"hp_number: {hp_number}, card_number: {card_number}")
            self.__pre_drawed_card_hp[card_number] = card_hp_image_data_list[hp_number]

    def pre_draw_numbers(self):
        image_dir = os.path.join(self.__project_root, "local_storage", "card_number_image")
        file_list = os.listdir(image_dir)

        for number in range(0, len(file_list)):
            number_image_data = os.path.join(self.__project_root, "local_storage", "card_number_image", f"{number}.png")
            # print(f"image data = {number_image_data}")
            self.__pre_drawed_numbers[number] = ImageDataLoader.load_circle_image_data(number_image_data)

    def pre_draw_prev_button(self):
        prev_button_image_data = os.path.join(self.__project_root, "local_storage", "button_image", "prev_button.png")
        self.__pre_drawed_prev_button = ImageDataLoader.load_rectangle_image_data(prev_button_image_data)

    def pre_draw_battle_field_muligun_background(self, width, height):
        # print(f"pre_draw_battle_field_muligun_background -> width = {width}, height = {height}")

        muligun_battle_field_background = os.path.join(self.__project_root, "local_storage", "image", "battle_field",
                                                       "muligun_battle_field_background.png")
        self.__pre_drawed_battle_field_muligun_background = ImageDataLoader.load_background_image_data(
            muligun_battle_field_background, width, height)

    def pre_draw_dark_flame_energy(self):
        dark_flame_energy_image_path = os.path.join(self.__project_root, "local_storage", "card_special_energy_image",
                                                    "dark_flame.png")
        self.__pre_drawed_dark_flame = ImageDataLoader.load_rectangle_image_data(dark_flame_energy_image_path)

    def pre_draw_freezing_energy(self):
        freezing_energy_image_path = os.path.join(self.__project_root, "local_storage", "card_special_energy_image",
                                                  "freezing.png")
        self.__pre_drawed_freezing = ImageDataLoader.load_rectangle_image_data(freezing_energy_image_path)

    def pre_draw_reset_button(self):
        reset_button_image_path = os.path.join(self.__project_root, "local_storage", "image", "battle_field",
                                               "reset_button.png")
        self.__pre_drawed_reset_button = ImageDataLoader.load_rectangle_image_data(reset_button_image_path)

    def pre_draw_card_back_frame(self):
        card_back_frame_image_path = os.path.join(self.__project_root, "local_storage", "image", "battle_field",
                                                  "card_back_frame.png")
        self.__pre_drawed_card_back_frame = ImageDataLoader.load_rectangle_image_data(card_back_frame_image_path)

    def pre_draw_next_gold_button(self):
        next_gold_button_image_path = os.path.join(self.__project_root, "local_storage", "button_image",
                                                   "next_gold_button.png")
        self.__pre_drawed_next_gold_button = ImageDataLoader.load_rectangle_origin_image_data(next_gold_button_image_path)

    def pre_draw_prev_gold_button(self):
        prev_gold_button_image_path = os.path.join(self.__project_root, "local_storage", "button_image",
                                                   "prev_gold_button.png")
        self.__pre_drawed_prev_gold_button = ImageDataLoader.load_rectangle_origin_image_data(prev_gold_button_image_path)

    def pre_draw_ok_button(self):
        prev_gold_button_image_path = os.path.join(self.__project_root, "local_storage", "button_image",
                                                   "ok_button.png")
        self.__pre_drawed_ok_button = ImageDataLoader.load_rectangle_image_data(prev_gold_button_image_path)

    def pre_draw_general_attack_button(self):
        general_ataack_button_path = os.path.join(self.__project_root, "local_storage", "active_panel_button",
                                                  "general_attack_button.png")
        self.__pre_drawed_general_attack_button = ImageDataLoader.load_rectangle_image_data(general_ataack_button_path)

    def pre_draw_view_detail_button(self):
        view_detail_button_path = os.path.join(self.__project_root, "local_storage", "active_panel_button",
                                               "view_details_button.png")
        self.__pre_drawed_detail_button = ImageDataLoader.load_rectangle_image_data(view_detail_button_path)

    def pre_draw_shadow_ball_button(self):
        shadow_ball_button_path = os.path.join(self.__project_root, "local_storage", "active_panel_button",
                                               "shadow_ball_button.png")
        self.__pre_drawed_shadow_ball_button = ImageDataLoader.load_rectangle_image_data(shadow_ball_button_path)

    def pre_draw_sea_of_spector_button(self):
        sea_of_spector_button_path = os.path.join(self.__project_root, "local_storage", "active_panel_button",
                                                  "sea_of_specter_button.png")
        self.__pre_drawed_sea_of_spector_button = ImageDataLoader.load_rectangle_image_data(sea_of_spector_button_path)

    def pre_draw_battle_field_energy(self):
        image_dir = os.path.join(self.__project_root, "local_storage", "field_energy_image")
        file_list = os.listdir(image_dir)

        for number in range(0, len(file_list)):
            field_energy_image_data = os.path.join(self.__project_root, "local_storage", "field_energy_image",
                                                   f"{number}.png")
            # print(f"image data = {field_energy_image_data}")
            self.__pre_drawed_field_energy[number] = ImageDataLoader.load_rectangle_image_data(field_energy_image_data)

    def pre_draw_try_again_screen(self):
        try_again_screen_image_path = os.path.join(self.__project_root, "local_storage", "shop_image", "try_again_screen.png")
        self.__pre_drawed_try_again_screen = ImageDataLoader.load_rectangle_origin_image_data(try_again_screen_image_path)

    def pre_draw_yes_button(self):
        yes_button_path = os.path.join(self.__project_root, "local_storage", "shop_image", "yes_button.png")
        self.__pre_drawed_yes_button =ImageDataLoader.load_rectangle_origin_image_data(yes_button_path)

    def pre_draw_no_button(self):
        no_button_path = os.path.join(self.__project_root, "local_storage", "shop_image", "no_button.png")
        self.__pre_drawed_no_button = ImageDataLoader.load_rectangle_origin_image_data(no_button_path)

    def pre_draw_preparing_message(self):
        preparing_message_image_path = os.path.join(self.__project_root, "local_storage", "preparing_message", "preparing_message.png")
        self.__pre_drawed_preparing_message = ImageDataLoader.load_rectangle_origin_image_data(preparing_message_image_path)

    def pre_draw_preparing_ok_button(self):
        preparing_ok_button_path = os.path.join(self.__project_root, "local_storage", "preparing_message", "ok_button.png")
        self.__pre_drawed_preparing_ok_button =ImageDataLoader.load_rectangle_origin_image_data(preparing_ok_button_path)



    def pre_draw_effect_animation(self):

        self.pre_draw_burst_shadow_ball()
        self.pre_draw_moving_shadow_ball()
        self.pre_draw_dark_blast()
        self.pre_draw_energy_burn()
        self.pre_draw_death_scythe()
        self.pre_draw_magic_attack()
        self.pre_draw_sword_attack()
        self.pre_draw_contract_of_doom()
        # self.pre_draw_sea_of_wraith()
        # self.pre_draw_legacy_sea_of_wraith()
        self.pre_draw_corpse_explosion()
        # self.pre_draw_nether_blade_area_skill()
        # self.pre_draw_nether_blade_targeting_skill()
        self.pre_draw_nether_blade_targeting_skill_remain()
        self.pre_draw_death()

        self.pre_drawed_swamp_of_ghost_effect_animation()
        # self.pre_draw_call_of_Leonic_effect_animation()
        self.pre_draw_field_of_death_effect_animation()
        self.pre_draw_overflow_of_energy_effect_animation()
        self.pre_draw_morale_conversion_effect_animation()

        self.pre_draw_dark_flame_effect_animation()
        self.pre_draw_freeze_effect_animation()

        # self.pre_draw_loading_screen_animation()
        # self.pre_draw_full_screen_loading_screen_animation()

    def pre_draw_loading_screen_animation(self):
        effect_animation = {}
        image_dir = os.path.join(self.__project_root, "local_storage", "animation",
                                 'loading_screen')
        file_list = os.listdir(image_dir)

        for number in range(0, len(file_list)):
            animation_image_data = os.path.join(self.__project_root, "local_storage", "animation",
                                                'loading_screen',
                                                f"{number}.png")
            # print(f"effect_animation_image_data = {animation_image_data}")

            effect_animation[number] = ImageDataLoader.load_rectangle_image_data(animation_image_data)

        self.__pre_drawed_effect_animation['loading_screen'] = effect_animation

    def pre_draw_full_screen_loading_screen_animation(self):
        from screeninfo import get_monitors
        monitors = get_monitors()
        target_monitor = monitors[2] if len(monitors) > 2 else monitors[0]

        width = target_monitor.width
        height = target_monitor.height

        effect_animation = {}
        image_dir = os.path.join(self.__project_root, "local_storage", "animation",
                                 'loading_screen')
        file_list = os.listdir(image_dir)

        for number in range(0, len(file_list)):
            animation_image_data = os.path.join(self.__project_root, "local_storage", "animation",
                                                'loading_screen',
                                                f"{number}.png")
            # print(f"effect_animation_image_data = {animation_image_data}")

            effect_animation[number] = ImageDataLoader.load_force_fit_full_screen_image_data(
                animation_image_data, width + 300, height + 300)

        self.__pre_drawed_effect_animation['loading_screen'] = effect_animation


    def pre_draw_morale_conversion_effect_animation(self):
        effect_animation = {}
        image_dir = os.path.join(self.__project_root, "local_storage", "animation",
                                 'morale_conversion')
        file_list = os.listdir(image_dir)

        for number in range(0, len(file_list)):
            animation_image_data = os.path.join(self.__project_root, "local_storage", "animation",
                                                'morale_conversion',
                                                f"{number}.png")
            # print(f"effect_animation_image_data = {animation_image_data}")
            effect_animation[number] = ImageDataLoader.load_rectangle_image_data(animation_image_data)

        self.__pre_drawed_effect_animation['morale_conversion'] = effect_animation

    def pre_draw_full_screen_nether_blade_deploy(self, width, height):
        # print(f"pre_draw_full_screen_nether_blade_deploy -> width: {width}, height: {height}")
        nether_blade_scene_animation = {}
        image_dir = os.path.join(self.__project_root, "local_storage", "animation",
                                 'nether_blade_scene')
        file_list = os.listdir(image_dir)

        for number in range(0, len(file_list)):
            animation_image_data = os.path.join(self.__project_root, "local_storage", "animation", 'nether_blade_scene',
                                                f"{number}.png")
            # print(f"effect_animation_image_data = {animation_image_data}")
            nether_blade_scene_animation[number] = ImageDataLoader.load_force_fit_full_screen_image_data(animation_image_data, width + 300, height + 300)

        self.__pre_drawed_effect_animation['nether_blade_scene'] = nether_blade_scene_animation


    def pre_draw_full_screen_nether_blade_skill(self, width, height):
        # print(f"pre_draw_full_screen_nether_blade_skill -> width: {width}, height: {height}")
        nether_blade_area_skill_animation = {}
        image_dir = os.path.join(self.__project_root, "local_storage", "animation",
                                 'nether_blade_area_skill')
        file_list = os.listdir(image_dir)

        for number in range(0, len(file_list)):
            animation_image_data = os.path.join(self.__project_root, "local_storage", "animation", 'nether_blade_area_skill',
                                                f"{number}.png")
            # print(f"effect_animation_image_data = {animation_image_data}")
            nether_blade_area_skill_animation[number] = ImageDataLoader.load_force_fit_full_screen_image_data(animation_image_data, width + 300, height + 300)

        self.__pre_drawed_effect_animation['nether_blade_area_skill'] = nether_blade_area_skill_animation

    def pre_draw_full_screen_sea_of_wraith(self, width, height):
        # print(f"pre_draw_full_screen_sea_of_wraith -> width: {width}, height: {height}")
        sea_of_wraith_skill_animation = {}
        image_dir = os.path.join(self.__project_root, "local_storage", "animation", 'sea_of_wraith')
        file_list = os.listdir(image_dir)

        for number in range(0, len(file_list)):
            animation_image_data = os.path.join(self.__project_root, "local_storage", "animation", 'sea_of_wraith',
                                                f"{number}.png")
            # print(f"effect_animation_image_data = {animation_image_data}")
            sea_of_wraith_skill_animation[number] = ImageDataLoader.load_force_fit_full_screen_image_data(animation_image_data, width + 300, height + 300)

        self.__pre_drawed_effect_animation['sea_of_wraith'] = sea_of_wraith_skill_animation

    def pre_draw_full_screen_nether_blade_targeting_skill(self, width, height):
        nether_blade_targeting_skill_animation = {}
        image_dir = os.path.join(self.__project_root, "local_storage", "animation",
                                 'nether_blade_targeting_skill')
        file_list = os.listdir(image_dir)

        for number in range(0, len(file_list)):
            animation_image_data = os.path.join(self.__project_root, "local_storage", "animation", 'nether_blade_targeting_skill',
                                                f"{number}.png")
            # print(f"effect_animation_image_data = {animation_image_data}")
            nether_blade_targeting_skill_animation[number] = ImageDataLoader.load_force_fit_full_screen_image_data(animation_image_data, width + 300, height + 300)

        self.__pre_drawed_effect_animation['nether_blade_targeting_skill'] = nether_blade_targeting_skill_animation

    def pre_draw_nether_blade_targeting_skill_remain(self):
        effect_animation = {}
        image_dir = os.path.join(self.__project_root, "local_storage", "animation",
                                 'nether_blade_targeting_skill_remain')
        file_list = os.listdir(image_dir)

        for number in range(0, len(file_list)):
            animation_image_data = os.path.join(self.__project_root, "local_storage", "animation", 'nether_blade_targeting_skill_remain',
                                                f"{number}.png")
            # print(f"effect_animation_image_data = {animation_image_data}")
            effect_animation[number] = ImageDataLoader.load_rectangle_image_data(animation_image_data)

        self.__pre_drawed_effect_animation['nether_blade_targeting_skill_remain'] = effect_animation

    def pre_draw_death(self):
        death_animation = {}
        image_dir = os.path.join(self.__project_root, "local_storage", "animation",
                                 'death')
        file_list = os.listdir(image_dir)

        for number in range(0, len(file_list)):
            animation_image_data = os.path.join(self.__project_root, "local_storage", "animation", 'death',
                                                f"{number}.png")
            # print(f"effect_animation_image_data = {animation_image_data}")
            death_animation[number] = ImageDataLoader.load_rectangle_image_data(animation_image_data)

        self.__pre_drawed_effect_animation['death'] = death_animation

    def pre_draw_corpse_explosion(self):
        corpse_explosion_animation = {}
        image_dir = os.path.join(self.__project_root, "local_storage", "animation",
                                 'corpse_explosion')
        file_list = os.listdir(image_dir)

        for number in range(0, len(file_list)):
            animation_image_data = os.path.join(self.__project_root, "local_storage", "animation", 'corpse_explosion',
                                                f"{number}.png")
            # print(f"effect_animation_image_data = {animation_image_data}")
            corpse_explosion_animation[number] = ImageDataLoader.load_rectangle_image_data(animation_image_data)

        self.__pre_drawed_effect_animation['corpse_explosion'] = corpse_explosion_animation

    # def pre_draw_sea_of_wraith(self):
    #     sea_of_wraith_animation = {}
    #     image_dir = os.path.join(self.__project_root, "local_storage", "animation",
    #                              'sea_of_wraith')
    #     file_list = os.listdir(image_dir)
    #
    #     for number in range(0, len(file_list)):
    #         animation_image_data = os.path.join(self.__project_root, "local_storage", "animation", 'sea_of_wraith',
    #                                             f"{number}.png")
    #         print(f"effect_animation_image_data = {animation_image_data}")
    #         sea_of_wraith_animation[number] = ImageDataLoader.load_rectangle_image_data(animation_image_data)
    #
    #     self.__pre_drawed_effect_animation['sea_of_wraith'] = sea_of_wraith_animation

    def pre_draw_legacy_sea_of_wraith(self):
        sea_of_wraith_animation = {}
        image_dir = os.path.join(self.__project_root, "local_storage", "animation", 'legacy_sea_of_wraith')
        file_list = os.listdir(image_dir)

        for number in range(0, len(file_list)):
            animation_image_data = os.path.join(self.__project_root, "local_storage", "animation", 'legacy_sea_of_wraith',
                                                f"{number}.png")
            # print(f"effect_animation_image_data = {animation_image_data}")
            sea_of_wraith_animation[number] = ImageDataLoader.load_rectangle_image_data(animation_image_data)

        self.__pre_drawed_effect_animation['legacy_sea_of_wraith'] = sea_of_wraith_animation

    def pre_draw_contract_of_doom(self):
        contract_of_doom_animation = {}
        image_dir = os.path.join(self.__project_root, "local_storage", "animation",
                                 'contract_of_doom')
        file_list = os.listdir(image_dir)

        for number in range(0, len(file_list)):
            animation_image_data = os.path.join(self.__project_root, "local_storage", "animation", 'contract_of_doom',
                                                f"{number}.png")
            # print(f"effect_animation_image_data = {animation_image_data}")
            contract_of_doom_animation[number] = ImageDataLoader.load_rectangle_image_data(animation_image_data)

        self.__pre_drawed_effect_animation['contract_of_doom'] = contract_of_doom_animation

    def pre_draw_burst_shadow_ball(self):
        burst_shadow_ball_animation = {}
        image_dir = os.path.join(self.__project_root, "local_storage", "animation",
                                                   'burst_shadow_ball')
        file_list = os.listdir(image_dir)

        for number in range(0, len(file_list)):
            animation_image_data = os.path.join(self.__project_root, "local_storage", "animation", 'burst_shadow_ball',f"{number}.png")
            # print(f"effect_animation_image_data = {animation_image_data}")
            burst_shadow_ball_animation[number] = ImageDataLoader.load_rectangle_image_data(animation_image_data)

        self.__pre_drawed_effect_animation['burst_shadow_ball'] = burst_shadow_ball_animation

    def pre_draw_moving_shadow_ball(self):
        moving_shadow_ball_animation = {}
        image_dir = os.path.join(self.__project_root, "local_storage", "animation", 'moving_shadow_ball')
        file_list = os.listdir(image_dir)

        for number in range(0, len(file_list)):
            animation_image_data = os.path.join(self.__project_root, "local_storage", "animation", 'moving_shadow_ball',f"{number}.png")
            # print(f"effect_animation_image_data = {animation_image_data}")
            moving_shadow_ball_animation[number] = ImageDataLoader.load_rectangle_image_data(animation_image_data)

        self.__pre_drawed_effect_animation['moving_shadow_ball'] = moving_shadow_ball_animation
    def pre_draw_dark_blast(self):
        dark_blast_animation = {}
        image_dir = os.path.join(self.__project_root, "local_storage", "animation", 'dark_blast')
        file_list = os.listdir(image_dir)

        for number in range(0, len(file_list)):
            animation_image_data = os.path.join(self.__project_root, "local_storage", "animation", 'dark_blast', f"{number}.png")
            # print(f"effect_animation_image_data = {animation_image_data}")
            dark_blast_animation[number] = ImageDataLoader.load_rectangle_image_data(animation_image_data)

        self.__pre_drawed_effect_animation['dark_blast'] = dark_blast_animation

    def pre_draw_energy_burn(self):
        energy_burn_animation = {}
        image_dir = os.path.join(self.__project_root, "local_storage", "animation", 'energy_burn')
        file_list = os.listdir(image_dir)

        for number in range(0, len(file_list)):
            animation_image_data = os.path.join(self.__project_root, "local_storage", "animation", 'energy_burn', f"{number}.png")
            # print(f"effect_animation_image_data = {animation_image_data}")
            energy_burn_animation[number] = ImageDataLoader.load_rectangle_image_data(animation_image_data)

        self.__pre_drawed_effect_animation['energy_burn'] = energy_burn_animation

    def pre_draw_magic_attack(self):
        magic_attack_animation = {}
        image_dir = os.path.join(self.__project_root, "local_storage", "animation", 'magic_attack')
        file_list = os.listdir(image_dir)

        for number in range(0, len(file_list)):
            animation_image_data = os.path.join(self.__project_root, "local_storage", "animation", 'magic_attack', f"{number}.png")
            # print(f"effect_animation_image_data = {animation_image_data}")
            magic_attack_animation[number] = ImageDataLoader.load_rectangle_image_data(animation_image_data)

        self.__pre_drawed_effect_animation['magic_attack'] = magic_attack_animation
    def pre_draw_sword_attack(self):
        sword_attack_animation = {}
        image_dir = os.path.join(self.__project_root, "local_storage", "animation", 'sword_attack')
        file_list = os.listdir(image_dir)

        for number in range(0, len(file_list)):
            animation_image_data = os.path.join(self.__project_root, "local_storage", "animation", 'sword_attack', f"{number}.png")
            # print(f"effect_animation_image_data = {animation_image_data}")
            sword_attack_animation[number] = ImageDataLoader.load_rectangle_image_data(animation_image_data)

        self.__pre_drawed_effect_animation['sword_attack'] = sword_attack_animation

    def pre_draw_death_scythe(self):
        death_scythe_animation = {}
        image_dir = os.path.join(self.__project_root, "local_storage", "animation", 'death_scythe')
        file_list = os.listdir(image_dir)

        for number in range(0, len(file_list)):
            animation_image_data = os.path.join(self.__project_root, "local_storage", "animation", 'death_scythe', f"{number}.png")
            # print(f"effect_animation_image_data = {animation_image_data}")
            death_scythe_animation[number] = ImageDataLoader.load_rectangle_image_data(animation_image_data)

        self.__pre_drawed_effect_animation['death_scythe'] = death_scythe_animation

    def pre_draw_animation(self):
        image_dir = os.path.join(self.__project_root, "local_storage", "animation")
        # image_dir = os.path.join(self.__project_root, "local_storage", "animation_for_test")
        file_list = os.listdir(image_dir)

        for number in range(0, len(file_list)):
            animation_image_data = os.path.join(self.__project_root, "local_storage", "animation", f"{number}.png")
            # animation_image_data = os.path.join(self.__project_root, "local_storage", "animation_for_test", f"{number}.png")
            # print(f"animation image data = {animation_image_data}")
            self.__pre_drawed_animation[number] = ImageDataLoader.load_rectangle_image_data(animation_image_data)

    def pre_draw_number_of_energy(self):
        image_dir = os.path.join(self.__project_root, "local_storage", "number_of_energy")
        # image_dir = os.path.join(self.__project_root, "local_storage", "animation_for_test")
        file_list = os.listdir(image_dir)

        for number in range(0, len(file_list)):
            animation_image_data = os.path.join(self.__project_root, "local_storage", "number_of_energy",
                                                f"{number}.png")
            # animation_image_data = os.path.join(self.__project_root, "local_storage", "animation_for_test", f"{number}.png")
            # print(f"animation image data = {animation_image_data}")
            self.__pre_drawed_number_of_energy[number] = ImageDataLoader.load_rectangle_image_data(animation_image_data)

    def pre_draw_battle_field_background(self, width, height):
        # print(f"pre_draw_battle_field_background -> width = {width}, height = {height}")

        battle_field_background = os.path.join(self.__project_root, "local_storage", "image", "battle_field",
                                               "battle_field_background.png")
        self.__pre_drawed_battle_field_background = ImageDataLoader.load_background_image_data(battle_field_background,
                                                                                               width, height)

    def pre_draw_surrender_button(self):
        surrender_button_image_path = os.path.join(self.__project_root, "local_storage", "option",
                                                   "surrender_button.png")
        self.__pre_drawed_surrender_button = ImageDataLoader.load_rectangle_image_data(
            surrender_button_image_path)

    def pre_draw_surrender_confirm_panel(self):
        surrender_confirm_panel_image_path = os.path.join(self.__project_root, "local_storage", "option",
                                                          "surrender_screen.png")
        self.__pre_drawed_surrender_confirm_panel = ImageDataLoader.load_surrender_screen_image_data(
            surrender_confirm_panel_image_path)

    def pre_draw_unit_energy(self):
        unit_energy_image_path = os.path.join(self.__project_root, "local_storage", "unit_card_energy")
        unit_energy_image_file_list = os.listdir(unit_energy_image_path)

        for number in range(0, len(unit_energy_image_file_list)):
            unit_energy_image_path = os.path.join(self.__project_root, "local_storage", "unit_card_energy", f"{number}.png")
            # print(f"unit_energy_image_data = {unit_energy_image_path}")
            self.__pre_drawed_unit_energy[number] = ImageDataLoader.load_rectangle_origin_image_data(unit_energy_image_path)

    def pre_draw_unit_hp(self):
        unit_hp_image_path = os.path.join(self.__project_root, "local_storage", "unit_card_hp")
        unit_hp_image_file_list = os.listdir(unit_hp_image_path)

        for number in range(0, len(unit_hp_image_file_list)):
            unit_hp_image_path = os.path.join(self.__project_root, "local_storage", "unit_card_hp", f"{number}.png")
            # print(f"unit_hp_image_path = {unit_hp_image_path}")
            self.__pre_drawed_unit_hp[number] = ImageDataLoader.load_rectangle_origin_image_data(unit_hp_image_path)

        # unit_hp_image_path = os.path.join(self.__project_root, "local_storage", "unit_card_hp")
        # unit_hp_image_file_list = os.listdir(unit_hp_image_path)
        # png_files = [file for file in unit_hp_image_file_list if file.lower().endswith('.png')]
        #
        # unit_hp_image_data_list = {}
        #
        # for png_file in png_files:
        #     hp_number = int(png_file[:-4])
        #     print(f"number images: {hp_number}")
        #     unit_hp_image_data = os.path.join(self.__project_root, "local_storage", "unit_card_hp", f"{png_file}")
        #     unit_hp_image_data_list[hp_number] = ImageDataLoader.load_rectangle_origin_image_data(unit_hp_image_data)
        #
        # for card_number in self.__card_info_from_csv_repository.getCardNumber():
        #     hp_number = self.__card_info_from_csv_repository.getCardHpForCardNumber(card_number)
        #     print(f"hp_number: {hp_number}, card_number: {card_number}")
        #     self.__pre_drawed_unit_hp[card_number] = unit_hp_image_data_list[hp_number]

    def pre_draw_unit_attack(self):
        # unit_attack_image_path = os.path.join(self.__project_root, "local_storage", "unit_card_attack_power")
        # unit_attack_image_file_list = os.listdir(unit_attack_image_path)
        #
        # for number in range(0, len(unit_attack_image_file_list)):
        #     unit_attack_image_path = os.path.join(self.__project_root, "local_storage", "unit_card_attack_power", f"{number}.png")
        #     print(f"unit_attack_image_path = {unit_attack_image_path}")
        #     self.__pre_drawed_unit_attack[number] = ImageDataLoader.load_rectangle_origin_image_data(unit_attack_image_path)

        unit_attack_image_path = os.path.join(self.__project_root, "local_storage", "unit_card_attack_power")
        unit_attack_image_file_list = os.listdir(unit_attack_image_path)
        png_files = [file for file in unit_attack_image_file_list if file.lower().endswith('.png')]

        unit_attack_image_data_list = {}

        for png_file in png_files:
            attack_number = int(png_file[:-4])
            # print(f"number images: {attack_number}")
            unit_attack_image_data = os.path.join(self.__project_root, "local_storage", "unit_card_attack_power", f"{png_file}")
            unit_attack_image_data_list[attack_number] = ImageDataLoader.load_rectangle_origin_image_data(unit_attack_image_data)

        for card_number in self.__card_info_from_csv_repository.getCardNumber():
            attack_number = self.__card_info_from_csv_repository.getCardAttackForCardNumber(card_number)
            # print(f"attack_number: {attack_number}, card_number: {card_number}")
            self.__pre_drawed_unit_attack[card_number] = unit_attack_image_data_list[attack_number]

    def pre_draw_unit_race(self):
        # unit_race_image_path = os.path.join(self.__project_root, "local_storage", "unit_card_race")
        # unit_race_image_file_list = os.listdir(unit_race_image_path)
        #
        # for number in range(0, len(unit_race_image_file_list)):
        #     unit_race_image_path = os.path.join(self.__project_root, "local_storage", "unit_card_race", f"{number}.png")
        #     print(f"unit_race_image_path = {unit_race_image_path}")
        #     self.__pre_drawed_unit_race[number] = ImageDataLoader.load_rectangle_origin_image_data(unit_race_image_path)

        unit_race_image_path = os.path.join(self.__project_root, "local_storage", "unit_card_race")
        unit_race_image_file_list = os.listdir(unit_race_image_path)
        png_files = [file for file in unit_race_image_file_list if file.lower().endswith('.png')]

        for png_file in png_files:
            race_number = int(png_file[:-4])
            # print(f"pre_draw_unit_race() -> race_number: {race_number}")
            unit_race_image_path = os.path.join(self.__project_root, "local_storage", "unit_card_race", f"{png_file}")
            self.__pre_drawed_unit_race[race_number] = ImageDataLoader.load_rectangle_origin_image_data(unit_race_image_path)

    def pre_draw_my_card_background(self, width, height):
        # print(f"pre_draw_my_card_background -> width = {width}, height = {height}")

        my_card_background = os.path.join(self.__project_root, "local_storage", "my_card_frame", "my_card_background.png")
        self.__pre_drawed_my_card_background = ImageDataLoader.load_background_image_data(my_card_background, width, height)

    def pre_draw_buy_random_background(self, width, height):
        buy_random_background = os.path.join(self.__project_root, "local_storage", "shop_image", "new_card_background.png")
        self.__pre_drawed_buy_random_background = ImageDataLoader.load_background_image_data(buy_random_background, width, height)

    def pre_draw_rock(self):
        rock = os.path.join(self.__project_root, "local_storage", "rock_paper_scissors_image", "rock.png")
        self.__pre_drawed_rock = ImageDataLoader.load_lanczos_resized_image_data(rock)

    def pre_draw_scissor(self):
        scissor = os.path.join(self.__project_root, "local_storage", "rock_paper_scissors_image", "scissors.png")
        self.__pre_drawed_scissor = ImageDataLoader.load_lanczos_resized_image_data(scissor)

    def pre_draw_paper(self):
        scissor = os.path.join(self.__project_root, "local_storage", "rock_paper_scissors_image", "paper.png")
        self.__pre_drawed_paper = ImageDataLoader.load_lanczos_resized_image_data(scissor)

    def pre_draw_number_of_cards(self):
        image_dir = os.path.join(self.__project_root, "local_storage", "my_card_frame", "number_of_cards_owned")
        file_list = os.listdir(image_dir)

        for number in range(2, 21):
            text_image_data = os.path.join(self.__project_root, "local_storage", "my_card_frame", "number_of_cards_owned",
                                           f"{number}.png")
            # print(f"animation image data = {text_image_data}")
            self.__pre_drawed_number_of_cards[number] = ImageDataLoader.load_rectangle_origin_image_data(text_image_data)

        text_image_data = os.path.join(self.__project_root, "local_storage", "my_card_frame", "number_of_cards_owned", "n.png")
        self.__pre_drawed_number_of_cards['n'] = ImageDataLoader.load_rectangle_origin_image_data(text_image_data)

    def pre_draw_multi_draw_button(self):
        multi_draw_button_image_data = os.path.join(self.__project_root, "local_storage", "button_image", "multi_draw_button.jpg")
        self.__pre_drawed_multi_draw_button = ImageDataLoader.load_rectangle_origin_image_data(multi_draw_button_image_data)

    def pre_draw_number_of_details_energy(self):
        # image_dir = os.path.join(self.__project_root, "local_storage", "energy_details_image")
        # file_list = os.listdir(image_dir)

        for number in range(2, 10):
            text_image_data = os.path.join(self.__project_root, "local_storage", "energy_details_number",
                                           f"{number}.png")
            # print(f"animation image data = {text_image_data}")
            self.__pre_drawed_number_of_details_energy[number] = ImageDataLoader.load_rectangle_image_data(text_image_data)

    def pre_draw_battle_field_card_frame(self):
        for card_number in self.__card_info_from_csv_repository.getCardNumber():
            battle_field_card_frame_image_data = os.path.join(self.__project_root, "local_storage",
                                                              "battle_field_card_frame",
                                                              f"{card_number}.png")
            self.__pre_drawed_battle_field_card_frame[card_number] = (
                ImageDataLoader.load_battle_field_card_frame_image_data(battle_field_card_frame_image_data)
            )

    def pre_draw_random_buy_card_frame(self):
        for card_number in self.__card_info_from_csv_repository.getCardNumber():
            random_buy_card_frame_image_data = os.path.join(self.__project_root, "local_storage",
                                                              "battle_field_card_frame",
                                                              f"{card_number}.png")
            self.__pre_drawed_random_buy_card_frame[card_number] = (
                ImageDataLoader.load_rectangle_origin_image_data(random_buy_card_frame_image_data)
            )



    def pre_draw_waiting_message(self):
        waiting_message_image_path = os.path.join(self.__project_root, "local_storage", "image", "battle_field",
                                                  "waiting_message_opponent_meligun_select.png")
        self.__pre_drawed_waiting_message = ImageDataLoader.load_rectangle_origin_image_data(waiting_message_image_path)

    def pre_draw_turn_number(self):
        turn_number_image_path = os.path.join(self.__project_root, "local_storage", "turn_number")
        turn_number_image_file_list = os.listdir(turn_number_image_path)
        png_files = [file for file in turn_number_image_file_list if file.lower().endswith('.png')]

        for png_file in png_files:
            turn_number = int(png_file[:-4])
            turn_number_image_path = os.path.join(self.__project_root, "local_storage", "turn_number", f"{png_file}")
            self.__pre_drawed_turn_number[turn_number] = ImageDataLoader.load_rectangle_image_data(
                turn_number_image_path)

    def pre_draw_card_type_mark(self):
        card_type_mark_image_path = os.path.join(self.__project_root, "local_storage", "card_type_mark")
        card_type_mark_image_file_list = os.listdir(card_type_mark_image_path)
        png_files = [file for file in card_type_mark_image_file_list if file.lower().endswith('.png')]

        for png_file in png_files:
            card_type_mark = int(png_file[:-4])
            # print(f"pre_draw_unit_race() -> race_number: {card_type_mark}")
            card_type_mark_image_path = os.path.join(self.__project_root, "local_storage", "card_type_mark", f"{png_file}")
            self.__pre_drawed_card_type_mark[card_type_mark] = ImageDataLoader.load_rectangle_image_data(card_type_mark_image_path)

    def pre_draw_wizard_card_attack_power(self):
        wizard_card_attack_image_path = os.path.join(self.__project_root, "local_storage", "wizard_card_attack_power")
        wizard_card_attack_image_file_list = os.listdir(wizard_card_attack_image_path)
        png_files = [file for file in wizard_card_attack_image_file_list if file.lower().endswith('.png')]

        wizard_card_attack_image_data_list = {}

        for png_file in png_files:
            attack_number = int(png_file[:-4])
            # print(f"number images: {attack_number}")
            wizard_card_attack_image_data = os.path.join(self.__project_root, "local_storage", "wizard_card_attack_power",
                                                  f"{png_file}")
            wizard_card_attack_image_data_list[attack_number] = ImageDataLoader.load_rectangle_origin_image_data(
                wizard_card_attack_image_data)

        for card_number in self.__card_info_from_csv_repository.getCardNumber():
            attack_number = self.__card_info_from_csv_repository.getCardAttackForCardNumber(card_number)
            # print(f"attack_number: {attack_number}, card_number: {card_number}")
            self.__pre_drawed_wizard_card_attack_power[card_number] = wizard_card_attack_image_data_list[attack_number]

    def pre_draw_message_on_the_battle_screen(self):
        image_dir = os.path.join(self.__project_root, "local_storage", "message_on_the_battle_screen")
        file_list = os.listdir(image_dir)

        for number in range(0, len(file_list) - 1):
            number_image_data = os.path.join(self.__project_root, "local_storage", "message_on_the_battle_screen",
                                             f"{number}.png")
            # print(f"image data = {number_image_data}")
            self.__pre_drawed_message_on_the_battle_screen[number] = ImageDataLoader.load_message_on_the_battle_screen_image_data(number_image_data)


    def pre_draw_battle_field_timer(self):
        image_dir = os.path.join(self.__project_root, "local_storage", "battle_field_timer")
        file_list = os.listdir(image_dir)

        for number in range(0, len(file_list)):
            number_image_data = os.path.join(self.__project_root, "local_storage", "battle_field_timer",
                                             f"{number}.png")
            # print(f"image data = {number_image_data}")
            self.__pre_drawed_battle_field_timer[number] = ImageDataLoader.load_rectangle_image_data(number_image_data)

    def pre_draw_use_energy_opponent_unit(self):
        image_dir = os.path.join(self.__project_root, "local_storage", "message_on_the_battle_screen", "use_energy_opponent_unit")
        file_list = os.listdir(image_dir)

        for number in range(1, len(file_list) + 1):
            number_image_data = os.path.join(self.__project_root, "local_storage", "message_on_the_battle_screen", "use_energy_opponent_unit",
                                             f"{number}.png")
            # print(f"image data = {number_image_data}")
            self.__pre_draw_use_energy_opponent_unit[number] = ImageDataLoader.load_message_on_the_battle_screen_image_data(number_image_data)

    def pre_draw_mulligan_timer(self):
        image_dir = os.path.join(self.__project_root, "local_storage", "mulligan_timer")
        file_list = os.listdir(image_dir)

        for number in range(0, len(file_list) + 1):
            timer_image_data = os.path.join(self.__project_root, "local_storage", "mulligan_timer", f"{number}.png")
            # print(f"animation image data = {timer_image_data}")
            self.__pre_drawed_mulligan_timer[number] = ImageDataLoader.load_rectangle_image_data(timer_image_data)

    def pre_draw_every_image(self):
        self.pre_draw_popup_panel()

        self.pre_draw_opponent_tomb()
        self.pre_draw_opponent_lost_zone()
        self.pre_draw_opponent_trap()
        self.pre_draw_opponent_card_deck()
        self.pre_draw_opponent_main_character()
        self.pre_draw_opponent_hand_panel()
        self.pre_draw_opponent_unit_field()

        self.pre_draw_your_tomb()
        self.pre_draw_your_lost_zone()
        self.pre_draw_your_trap()
        self.pre_draw_your_card_deck()
        self.pre_draw_your_main_character()
        self.pre_draw_your_hand_panel()
        self.pre_draw_your_unit_field()

        self.pre_draw_battle_field_environment()
        self.pre_draw_turn_end_button()
        self.pre_draw_turn_number()
        self.pre_draw_win_text()
        self.pre_draw_lose_text()
        self.pre_draw_battle_result_background()

        self.pre_draw_card_drawing_scene()

        self.pre_draw_card_illustration()
        self.pre_draw_card_race()
        self.pre_draw_card_type()
        self.pre_draw_card_hp()
        self.pre_draw_card_attack()

        self.pre_draw_numbers()
        self.pre_draw_character_hp()
        self.pre_draw_rectangle_number_image()

        self.pre_draw_prev_button()
        self.pre_draw_confirm_button()

        self.pre_draw_card_frame()
        self.pre_draw_battle_field_card_frame()
        self.pre_draw_random_buy_card_frame()
        self.pre_draw_dark_flame_energy()
        self.pre_draw_freezing_energy()

        self.pre_draw_reset_button()
        self.pre_draw_card_back_frame()

        self.pre_draw_energy_race()
        self.pre_draw_battle_field_energy()

        self.pre_draw_next_gold_button()
        self.pre_draw_prev_gold_button()

        self.pre_draw_ok_button()

        self.pre_draw_general_attack_button()
        self.pre_draw_view_detail_button()
        self.pre_draw_shadow_ball_button()
        self.pre_draw_sea_of_spector_button()

        # self.pre_draw_animation()
        self.pre_draw_effect_animation()

        self.pre_draw_number_of_energy()

        self.pre_draw_surrender_button()
        self.pre_draw_surrender_confirm_panel()

        self.pre_draw_unit_energy()
        self.pre_draw_unit_hp()
        self.pre_draw_unit_attack()
        self.pre_draw_unit_race()

        self.pre_draw_rock()
        self.pre_draw_scissor()
        self.pre_draw_paper()

        self.pre_draw_number_of_cards()
        self.pre_draw_multi_draw_button()
        self.pre_draw_number_of_details_energy()

        self.pre_draw_waiting_message()
        self.pre_draw_card_type_mark()

        self.pre_draw_wizard_card_attack_power()
        self.pre_draw_message_on_the_battle_screen()
        self.pre_draw_use_energy_opponent_unit()

        self.pre_draw_battle_field_timer()
        self.pre_draw_create_deck_button()
        self.pre_draw_go_back_button()

        self.pre_draw_mulligan_timer()

        self.pre_draw_page_slash()
        self.pre_draw_page_number()

        self.pre_draw_try_again_screen()
        self.pre_draw_preparing_message()
        self.pre_draw_preparing_ok_button()


        # self.pre_draw_loading_screen()

        self.pre_draw_yes_button()
        self.pre_draw_no_button()


        # Multi Window Size Issue로 백그라운드만은 미리 그리지 않음
        # self.pre_draw_battle_field_muligun_background()

    def get_pre_draw_go_back_button(self):
        return self.__pre_drawed_go_back_button

    def get_pre_draw_page_slash(self):
        return self.__pre_drawed_page_slash

    def get_pre_draw_opponent_tomb(self):
        return self.__pre_drawed_opponent_tomb

    def get_pre_draw_opponent_lost_zone(self):
        return self.__pre_drawed_opponent_lost_zone

    def get_pre_draw_opponent_trap(self):
        return self.__pre_drawed_opponent_trap

    def get_pre_draw_opponent_card_deck(self):
        return self.__pre_drawed_opponent_card_deck

    def get_pre_draw_opponent_main_character(self):
        return self.__pre_drawed_opponent_main_character

    def get_pre_draw_opponent_hand_panel(self):
        return self.__pre_drawed_opponent_hand_panel

    def get_pre_draw_opponent_unit_field(self):
        return self.__pre_drawed_opponent_unit_field

    def get_pre_draw_your_tomb(self):
        return self.__pre_drawed_your_tomb

    def get_pre_draw_your_lost_zone(self):
        return self.__pre_drawed_your_lost_zone

    def get_pre_draw_your_trap(self):
        return self.__pre_drawed_your_trap

    def get_pre_draw_your_card_deck(self):
        return self.__pre_drawed_your_card_deck

    def get_pre_draw_your_main_character(self):
        return self.__pre_drawed_your_main_character

    def get_pre_draw_your_hand_panel(self):
        return self.__pre_drawed_your_hand_panel

    def get_pre_draw_your_unit_field(self):
        return self.__pre_drawed_your_unit_field

    def get_pre_draw_battle_field_environment(self):
        return self.__pre_drawed_battle_field_environment

    def get_pre_draw_turn_end_button(self):
        return self.__pre_drawed_turn_end_button

    def get_pre_draw_card_illustration_for_card_number(self, card_number):
        return self.__pre_drawed_card_illustration[card_number]

    def get_pre_draw_card_race_with_card_number(self, card_number):
        return self.__pre_drawed_card_race[card_number]

    def get_pre_draw_card_type_with_card_number(self, card_number):
        return self.__pre_drawed_card_type[card_number]

    def get_pre_draw_card_attack_with_card_number(self, card_number):
        return self.__pre_drawed_card_attack[card_number]

    def get_pre_draw_card_hp_with_card_number(self, card_number):
        return self.__pre_drawed_card_hp[card_number]

    def get_pre_draw_number_image(self, number=0):
        # print(f"pre_drawed_number_images: {self.__pre_drawed_numbers[number]}")
        return self.__pre_drawed_numbers[number]

    def get_pre_draw_character_hp_image(self, number=0):
        return self.__pre_drawed_character_hp[number]

    def get_pre_draw_rectangle_number_image(self, number=0):
        return self.__pre_drawed_rectangle_number[number]

    def get_pre_draw_prev_button(self):
        return self.__pre_drawed_prev_button

    def get_pre_draw_battle_field_muligun_background(self):
        return self.__pre_drawed_battle_field_muligun_background

    def get_pre_draw_battle_field_background(self):
        return self.__pre_drawed_battle_field_background

    def get_pre_draw_win_text(self):
        return self.__pre_drawed_win_text

    def get_pre_draw_lose_text(self):
        return self.__pre_drawed_lose_text

    def get_pre_drawed_confirm_button(self):
        return self.__pre_drawed_confirm_button

    def get_pre_draw_card_frame_for_card_number(self, card_number):
        return self.__pre_drawed_card_frame[card_number]

    def get_pre_draw_dark_flame_energy(self):
        return self.__pre_drawed_dark_flame

    def get_pre_draw_freezing_energy(self):
        return self.__pre_drawed_freezing

    def get_pre_draw_reset_button(self):
        return self.__pre_drawed_reset_button

    def get_pre_draw_card_back_frame(self):
        return self.__pre_drawed_card_back_frame

    def get_pre_draw_energy_race_with_race_number(self, race_number):
        return self.__pre_drawed_energy_race[race_number]

    def get_pre_draw_next_gold_button(self):
        return self.__pre_drawed_next_gold_button

    def get_pre_draw_prev_gold_button(self):
        return self.__pre_drawed_prev_gold_button

    def get_pre_draw_ok_button(self):
        return self.__pre_drawed_ok_button

    def get_pre_draw_general_attack_button(self):
        return self.__pre_drawed_general_attack_button

    def get_pre_draw_view_detail_button(self):
        return self.__pre_drawed_detail_button

    def get_pre_draw_shadow_ball_button(self):
        return self.__pre_drawed_shadow_ball_button

    def get_pre_draw_sea_of_spector_button(self):
        return self.__pre_drawed_sea_of_spector_button

    def get_pre_draw_field_energy(self, number=0):
        return self.__pre_drawed_field_energy[number]

    def get_pre_draw_animation(self, number=0):
        return self.__pre_drawed_animation[number]

    def get_pre_draw_number_of_energy(self, number=0):
        return self.__pre_drawed_number_of_energy[number]

    def get_pre_draw_surrender_button(self):
        return self.__pre_drawed_surrender_button

    def get_pre_draw_surrender_confirm_panel(self):
        return self.__pre_drawed_surrender_confirm_panel

    def get_pre_draw_unit_energy(self, number):
        return self.__pre_drawed_unit_energy[number]

    def get_pre_draw_unit_hp(self, card_number):
        return self.__pre_drawed_unit_hp[card_number]

    def get_pre_draw_unit_attack(self, card_number):
        return self.__pre_drawed_unit_attack[card_number]

    def get_pre_draw_unit_race(self, race_number):
        # return self.__pre_drawed_unit_race[number]
        return self.__pre_drawed_unit_race[race_number]

    def get_pre_draw_my_card_background(self):
        return self.__pre_drawed_my_card_background

    def get_pre_draw_rock(self):
        return self.__pre_drawed_rock

    def get_pre_draw_scissor(self):
        return self.__pre_drawed_scissor

    def get_pre_draw_paper(self):
        return self.__pre_drawed_paper

    def get_pre_draw_number_of_cards(self, number):
        return self.__pre_drawed_number_of_cards[number]

    def get_pre_draw_exceed_number_of_cards(self):
        return self.__pre_drawed_number_of_cards['n']

    def get_pre_draw_multi_draw_button(self):
        return self.__pre_drawed_multi_draw_button

    def get_pre_draw_number_of_details_energy(self, number):
        return self.__pre_drawed_number_of_details_energy[number]

    def get_pre_draw_battle_field_card_frame_for_card_number(self, card_number):
        return self.__pre_drawed_battle_field_card_frame[card_number]

    def get_pre_draw_random_buy_card_frame_for_card_number(self, card_number):
        return self.__pre_drawed_random_buy_card_frame[card_number]

    def get_pre_draw_waiting_message(self):
        return self.__pre_drawed_waiting_message

    def get_pre_draw_turn_number(self, number):
        return self.__pre_drawed_turn_number[number]

    def get_pre_draw_card_type_mark(self, type_number):
        return self.__pre_drawed_card_type_mark[type_number]

    def get_pre_draw_effect_animation(self, effect_name, index=0):
        return self.__pre_drawed_effect_animation[effect_name][index]

    def get_pre_draw_wizard_card_attack_power(self, card_number):
        return self.__pre_drawed_wizard_card_attack_power[card_number]

    def get_pre_draw_message_on_the_battle_screen(self, message_number):
        return self.__pre_drawed_message_on_the_battle_screen[message_number]

    def get_pre_draw_battle_field_timer(self, number):
        return self.__pre_drawed_battle_field_timer[number]

    def get_pre_draw_use_energy_opponent_unit(self, opponent_index):
        return self.__pre_draw_use_energy_opponent_unit[opponent_index]

    def get_pre_draw_create_deck_button(self):
        return self.__pre_drawed_create_deck_button

    def get_pre_drawed_buy_random_background(self):
        return self.__pre_drawed_buy_random_background

    def get_pre_draw_battle_result_background(self):
        return self.__pre_drawed_battle_result_background

    def get_pre_draw_popup_panel(self):
        return self.__pre_drawed_popup_panel

    def get_pre_draw_mulligan_timer(self, number=0):
        return self.__pre_drawed_mulligan_timer[number]

    def get_pre_drawed_page_number(self, page_number):
        return self.__pre_drawed_page_number[page_number]

    def get_pre_draw_dark_flame_effect_animation(self, number = 0):
        return self.__pre_drawed_dark_flame_effect[number]

    def get_pre_draw_try_again_screen(self):
        return self.__pre_drawed_try_again_screen

    def get_pre_draw_yes_button(self):
        return self.__pre_drawed_yes_button

    def get_pre_draw_no_button(self):
        return self.__pre_drawed_no_button

    def get_pre_draw_preparing_message(self):
        return self.__pre_drawed_preparing_message

    def get_pre_draw_preparing_ok_button(self):
        return self.__pre_drawed_preparing_ok_button

    def get_pre_draw_loading_screen(self):
        return self.__pre_drawed_loading_screen

    def get_pre_draw_card_drawing_scene(self):
        return self.__pre_drawed_card_drawing_scene