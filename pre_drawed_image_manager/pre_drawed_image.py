import os

from card_info_from_csv.repository.card_info_from_csv_repository_impl import CardInfoFromCsvRepositoryImpl
from common.utility import get_project_root
from utility.image_data_loader import ImageDataLoader


class PreDrawedImage:
    __instance = None
    __card_info_from_csv_repository = CardInfoFromCsvRepositoryImpl().getInstance()

    __project_root = get_project_root()

    __pre_drawed_card_frame = {}

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

    __pre_drawed_field_energy = {}
    __pre_drawed_battle_field_environment = None
    __pre_drawed_turn_end_button = None

    __pre_drawed_win_text = None
    __pre_drawed_lose_text = None

    __pre_drawed_confirm_button = None

    __pre_drawed_prev_button = None
    __pre_drawed_reset_button = None
    __pre_drawed_battle_field_muligun_background = None
    __pre_drawed_battle_field_background = None

    __pre_drawed_card_back_frame = None

    __pre_drawed_next_gold_button = None
    __pre_drawed_prev_gold_button = None
    __pre_drawed_ok_button = None

    __pre_drawed_general_attack_button = None
    __pre_drawed_detail_button = None

    # TODO: 실제로는 숫자로 처리해야함 (유닛 번호 -> 액티브 스킬 1)
    # 유닛 번호 -> 액티브 스킬 2 형태가 되어야함
    __pre_drawed_shadow_ball_button = None #스킬1 버튼(쉐도우 볼)
    __pre_drawed_sea_of_spector_button = None #스킬2 버튼(망령의 바다)

    __pre_drawed_animation = {}

    __pre_drawed_number_of_energy = {}

    __pre_drawed_surrender_button = None
    __pre_drawed_surrender_confirm_panel = None

    __pre_drawed_unit_energy = {}
    __pre_drawed_unit_hp = {}
    __pre_drawed_unit_attack = {}
    __pre_drawed_unit_race = {}

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
        return cls.__instance

    @classmethod
    def getInstance(cls):
        if cls.__instance is None:
            cls.__instance = cls()
        return cls.__instance

    def pre_draw_card_frame(self):
        for card_number in self.__card_info_from_csv_repository.getCardNumber():
            card_frame_image_data = os.path.join(self.__project_root, "local_storage", "card_frame",
                                                 f"{card_number}.png")
            # self.__pre_drawed_card_frame[card_number] = ImageDataLoader.load_rectangle_image_data(card_frame_image_data)
            self.__pre_drawed_card_frame[card_number] = ImageDataLoader.load_card_frame_image_data(card_frame_image_data)

    def pre_draw_opponent_tomb(self):
        tomb_image_path = os.path.join(self.__project_root, "local_storage", "image", "battle_field", "tomb.jpeg")
        self.__pre_drawed_opponent_tomb = ImageDataLoader.load_rectangle_image_data(tomb_image_path)

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

    def pre_draw_your_unit_field(self):
        your_unit_field_image_path = os.path.join(self.__project_root, "local_storage", "image", "battle_field",
                                                  "background.png")
        self.__pre_drawed_your_unit_field = ImageDataLoader.load_rectangle_image_data(your_unit_field_image_path)

    def pre_draw_battle_field_environment(self):
        battle_field_environment_image_path = os.path.join(self.__project_root, "local_storage", "image",
                                                           "battle_field", "environment.jpeg")
        self.__pre_drawed_battle_field_environment = ImageDataLoader.load_rectangle_image_data(
            battle_field_environment_image_path)

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

    def pre_draw_character_hp(self):
        image_dir = os.path.join(self.__project_root, "local_storage", "card_number_image")
        file_list = os.listdir(image_dir)

        for number in range(0, len(file_list)):
            number_image_data = os.path.join(self.__project_root, "local_storage", "card_number_image", f"{number}.png")
            print(f"image data = {number_image_data}")
            self.__pre_drawed_character_hp[number] = ImageDataLoader.load_rectangle_image_data(number_image_data)

    def pre_draw_rectangle_number_image(self):
        image_dir = os.path.join(self.__project_root, "local_storage", "card_number_image")
        file_list = os.listdir(image_dir)

        for number in range(0, len(file_list)):
            number_image_data = os.path.join(self.__project_root, "local_storage", "card_number_image", f"{number}.png")
            print(f"image data = {number_image_data}")
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
            print(f"race_number: {race_number}")
            card_race_image_data = os.path.join(self.__project_root, "local_storage", "card_race_image", f"{png_file}")
            card_race_image_data_list[race_number] = ImageDataLoader.load_circle_image_data(card_race_image_data)

        for card_number in self.__card_info_from_csv_repository.getCardNumber():
            race_number = self.__card_info_from_csv_repository.getCardRaceForCardNumber(card_number)
            print(f"race_number: {race_number}, card_number: {card_number}")
            self.__pre_drawed_card_race[card_number] = card_race_image_data_list[race_number]

    def pre_draw_energy_race(self):
        image_dir = os.path.join(self.__project_root, "local_storage", "card_race_image")
        file_list = os.listdir(image_dir)
        png_files = [file for file in file_list if file.lower().endswith('.png')]

        for png_file in png_files:
            race_number = int(png_file[:-4])
            print(f"race_number: {race_number}")
            card_race_image_data = os.path.join(self.__project_root, "local_storage", "card_race_image", f"{png_file}")
            self.__pre_drawed_energy_race[race_number] = ImageDataLoader.load_circle_image_data(card_race_image_data)

    def pre_draw_card_type(self):
        image_dir = os.path.join(self.__project_root, "local_storage", "card_type_image")
        file_list = os.listdir(image_dir)
        png_files = [file for file in file_list if file.lower().endswith('.png')]

        card_type_image_data_list = {}

        for png_file in png_files:
            type_number = int(png_file[:-4])
            print(f"type_number: {type_number}")
            card_type_image_data = os.path.join(self.__project_root, "local_storage", "card_type_image", f"{png_file}")
            card_type_image_data_list[type_number] = ImageDataLoader.load_circle_image_data(card_type_image_data)

        for card_number in self.__card_info_from_csv_repository.getCardNumber():
            type_number = self.__card_info_from_csv_repository.getCardTypeForCardNumber(card_number)
            print(f"type_number: {type_number}, card_number: {card_number}")
            self.__pre_drawed_card_type[card_number] = card_type_image_data_list[type_number]

    def pre_draw_card_attack(self):
        image_dir = os.path.join(self.__project_root, "local_storage", "card_number_image")
        file_list = os.listdir(image_dir)
        png_files = [file for file in file_list if file.lower().endswith('.png')]

        card_attack_image_data_list = {}

        for png_file in png_files:
            attack_number = int(png_file[:-4])
            print(f"number images: {attack_number}")
            card_attack_image_data = os.path.join(self.__project_root, "local_storage", "card_number_image",
                                                  f"{png_file}")
            card_attack_image_data_list[attack_number] = ImageDataLoader.load_circle_image_data(card_attack_image_data)

        for card_number in self.__card_info_from_csv_repository.getCardNumber():
            attack_number = self.__card_info_from_csv_repository.getCardAttackForCardNumber(card_number)
            print(f"attack_number: {attack_number}, card_number: {card_number}")
            self.__pre_drawed_card_attack[card_number] = card_attack_image_data_list[attack_number]

    def pre_draw_card_hp(self):
        image_dir = os.path.join(self.__project_root, "local_storage", "card_number_image")
        file_list = os.listdir(image_dir)
        png_files = [file for file in file_list if file.lower().endswith('.png')]

        card_hp_image_data_list = {}

        for png_file in png_files:
            hp_number = int(png_file[:-4])
            print(f"number images: {hp_number}")
            card_hp_image_data = os.path.join(self.__project_root, "local_storage", "card_number_image", f"{png_file}")
            card_hp_image_data_list[hp_number] = ImageDataLoader.load_circle_image_data(card_hp_image_data)

        for card_number in self.__card_info_from_csv_repository.getCardNumber():
            hp_number = self.__card_info_from_csv_repository.getCardHpForCardNumber(card_number)
            print(f"hp_number: {hp_number}, card_number: {card_number}")
            self.__pre_drawed_card_hp[card_number] = card_hp_image_data_list[hp_number]

    def pre_draw_numbers(self):
        image_dir = os.path.join(self.__project_root, "local_storage", "card_number_image")
        file_list = os.listdir(image_dir)

        for number in range(0, len(file_list)):
            number_image_data = os.path.join(self.__project_root, "local_storage", "card_number_image", f"{number}.png")
            print(f"image data = {number_image_data}")
            self.__pre_drawed_numbers[number] = ImageDataLoader.load_circle_image_data(number_image_data)

    def pre_draw_prev_button(self):
        prev_button_image_data = os.path.join(self.__project_root, "local_storage", "button_image", "prev_button.png")
        self.__pre_drawed_prev_button = ImageDataLoader.load_rectangle_image_data(prev_button_image_data)

    def pre_draw_battle_field_muligun_background(self, width, height):
        print(f"pre_draw_battle_field_muligun_background -> width = {width}, height = {height}")

        muligun_battle_field_background = os.path.join(self.__project_root, "local_storage", "image", "battle_field",
                                                       "muligun_battle_field_background.png")
        self.__pre_drawed_battle_field_muligun_background = ImageDataLoader.load_background_image_data(
            muligun_battle_field_background, width, height)

    def pre_draw_dark_flame_energy(self):
        dark_flame_energy_image_path = os.path.join(self.__project_root, "local_storage", "card_special_energy_image",
                                                    "dark_flame.png")
        self.__pre_drawed_dark_flame = ImageDataLoader.load_circle_image_data(dark_flame_energy_image_path)

    def pre_draw_freezing_energy(self):
        freezing_energy_image_path = os.path.join(self.__project_root, "local_storage", "card_special_energy_image",
                                                  "freezing.png")
        self.__pre_drawed_freezing = ImageDataLoader.load_circle_image_data(freezing_energy_image_path)

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
        self.__pre_drawed_next_gold_button = ImageDataLoader.load_rectangle_image_data(next_gold_button_image_path)

    def pre_draw_prev_gold_button(self):
        prev_gold_button_image_path = os.path.join(self.__project_root, "local_storage", "button_image",
                                                   "prev_gold_button.png")
        self.__pre_drawed_prev_gold_button = ImageDataLoader.load_rectangle_image_data(prev_gold_button_image_path)

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
            print(f"image data = {field_energy_image_data}")
            self.__pre_drawed_field_energy[number] = ImageDataLoader.load_rectangle_image_data(field_energy_image_data)

    def pre_draw_animation(self):
        image_dir = os.path.join(self.__project_root, "local_storage", "animation")
        # image_dir = os.path.join(self.__project_root, "local_storage", "animation_for_test")
        file_list = os.listdir(image_dir)

        for number in range(0, len(file_list)):
            animation_image_data = os.path.join(self.__project_root, "local_storage", "animation", f"{number}.png")
            # animation_image_data = os.path.join(self.__project_root, "local_storage", "animation_for_test", f"{number}.png")
            print(f"animation image data = {animation_image_data}")
            self.__pre_drawed_animation[number] = ImageDataLoader.load_rectangle_image_data(animation_image_data)

    def pre_draw_number_of_energy(self):
        image_dir = os.path.join(self.__project_root, "local_storage", "number_of_energy")
        # image_dir = os.path.join(self.__project_root, "local_storage", "animation_for_test")
        file_list = os.listdir(image_dir)

        for number in range(0, len(file_list)):
            animation_image_data = os.path.join(self.__project_root, "local_storage", "number_of_energy",
                                                f"{number}.png")
            # animation_image_data = os.path.join(self.__project_root, "local_storage", "animation_for_test", f"{number}.png")
            print(f"animation image data = {animation_image_data}")
            self.__pre_drawed_number_of_energy[number] = ImageDataLoader.load_rectangle_image_data(animation_image_data)

    def pre_draw_battle_field_background(self, width, height):
        print(f"pre_draw_battle_field_background -> width = {width}, height = {height}")

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
        self.__pre_drawed_surrender_confirm_panel = ImageDataLoader.load_rectangle_image_data(
            surrender_confirm_panel_image_path)

    def pre_draw_unit_energy(self):
        unit_energy_image_path = os.path.join(self.__project_root, "local_storage", "unit_card_energy")
        unit_energy_image_file_list = os.listdir(unit_energy_image_path)

        for number in range(0, len(unit_energy_image_file_list)):
            unit_energy_image_path = os.path.join(self.__project_root, "local_storage", "unit_card_energy", f"{number}.png")
            print(f"unit_energy_image_data = {unit_energy_image_path}")
            self.__pre_drawed_unit_energy[number] = ImageDataLoader.load_rectangle_origin_image_data(unit_energy_image_path)

    def pre_draw_unit_hp(self):
        unit_hp_image_path = os.path.join(self.__project_root, "local_storage", "unit_card_hp")
        unit_hp_image_file_list = os.listdir(unit_hp_image_path)

        for number in range(0, len(unit_hp_image_file_list)):
            unit_hp_image_path = os.path.join(self.__project_root, "local_storage", "unit_card_hp", f"{number}.png")
            print(f"unit_hp_image_path = {unit_hp_image_path}")
            self.__pre_drawed_unit_hp[number] = ImageDataLoader.load_rectangle_origin_image_data(unit_hp_image_path)

    def pre_draw_unit_attack(self):
        unit_attack_image_path = os.path.join(self.__project_root, "local_storage", "unit_card_attack_power")
        unit_attack_image_file_list = os.listdir(unit_attack_image_path)

        for number in range(0, len(unit_attack_image_file_list)):
            unit_attack_image_path = os.path.join(self.__project_root, "local_storage", "unit_card_attack_power", f"{number}.png")
            print(f"unit_attack_image_path = {unit_attack_image_path}")
            self.__pre_drawed_unit_attack[number] = ImageDataLoader.load_rectangle_origin_image_data(unit_attack_image_path)

    def pre_draw_unit_race(self):
        unit_race_image_path = os.path.join(self.__project_root, "local_storage", "unit_card_race")
        unit_race_image_file_list = os.listdir(unit_race_image_path)

        for number in range(0, len(unit_race_image_file_list)):
            unit_race_image_path = os.path.join(self.__project_root, "local_storage", "unit_card_race", f"{number}.png")
            print(f"unit_race_image_path = {unit_race_image_path}")
            self.__pre_drawed_unit_race[number] = ImageDataLoader.load_rectangle_origin_image_data(unit_race_image_path)

    def pre_draw_every_image(self):
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
        self.pre_draw_win_text()
        self.pre_draw_lose_text()

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

        self.pre_draw_animation()

        self.pre_draw_number_of_energy()

        self.pre_draw_surrender_button()
        self.pre_draw_surrender_confirm_panel()

        self.pre_draw_unit_energy()
        self.pre_draw_unit_hp()
        self.pre_draw_unit_attack()
        self.pre_draw_unit_race()

        # Multi Window Size Issue로 백그라운드만은 미리 그리지 않음
        # self.pre_draw_battle_field_muligun_background()

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

    def get_pre_draw_unit_hp(self, number):
        return self.__pre_drawed_unit_hp[number]

    def get_pre_draw_unit_attack(self, number):
        return self.__pre_drawed_unit_attack[number]

    def get_pre_draw_unit_race(self, number):
        return self.__pre_drawed_unit_race[number]
