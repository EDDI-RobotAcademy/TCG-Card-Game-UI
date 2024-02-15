import os

from common.utility import get_project_root
from utility.image_data_loader import ImageDataLoader


class PreDrawedImage:
    __instance = None

    __project_root = get_project_root()

    __pre_drawed_opponent_tomb = None
    __pre_drawed_opponent_lost_zone = None
    __pre_drawed_opponent_trap = None
    __pre_drawed_opponent_card_deck = None
    __pre_drawed_opponent_main_character = None
    __pre_drawed_opponent_hand_panel = None

    __pre_drawed_your_tomb = None
    __pre_drawed_your_card_deck = None
    __pre_drawed_your_main_character = None
    __pre_drawed_your_hand_panel = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
        return cls.__instance

    @classmethod
    def getInstance(cls):
        if cls.__instance is None:
            cls.__instance = cls()
        return cls.__instance

    def pre_draw_opponent_tomb(self):
        tomb_image_path = os.path.join(self.__project_root, "local_storage", "image", "battle_field", "tomb.jpeg")
        self.__pre_drawed_opponent_tomb = ImageDataLoader.load_rectangle_image_data(tomb_image_path)

    def pre_draw_opponent_lost_zone(self):
        lost_zone_image_path = os.path.join(self.__project_root, "local_storage", "image", "battle_field", "lost_zone.png")
        self.__pre_drawed_opponent_lost_zone = ImageDataLoader.load_rectangle_image_data(lost_zone_image_path)

    def pre_draw_opponent_trap(self):
        trap_image_path = os.path.join(self.__project_root, "local_storage", "image", "battle_field", "trap.jpeg")
        self.__pre_drawed_opponent_trap = ImageDataLoader.load_rectangle_image_data(trap_image_path)

    def pre_draw_opponent_card_deck(self):
        opponent_card_deck_image_path = os.path.join(self.__project_root, "local_storage", "image", "battle_field", "opponent_card_deck.png")
        self.__pre_drawed_opponent_card_deck = ImageDataLoader.load_rectangle_image_data(opponent_card_deck_image_path)

    def pre_draw_opponent_main_character(self):
        opponent_main_character_image_path = os.path.join(self.__project_root, "local_storage", "image", "battle_field", "main_character.png")
        self.__pre_drawed_opponent_main_character = ImageDataLoader.load_oval_image_data(opponent_main_character_image_path)

    def pre_draw_opponent_hand_panel(self):
        opponent_hand_panel_image_path = os.path.join(self.__project_root, "local_storage", "image", "battle_field", "background.png")
        self.__pre_drawed_opponent_hand_panel = ImageDataLoader.load_rectangle_image_data(opponent_hand_panel_image_path)

    def pre_draw_your_tomb(self):
        tomb_image_path = os.path.join(self.__project_root, "local_storage", "image", "battle_field", "tomb.jpeg")
        self.__pre_drawed_your_tomb = ImageDataLoader.load_rectangle_image_data(tomb_image_path)

    def pre_draw_your_card_deck(self):
        your_card_deck_image_path = os.path.join(self.__project_root, "local_storage", "image", "battle_field", "your_card_deck.png")
        self.__pre_drawed_your_card_deck = ImageDataLoader.load_rectangle_image_data(your_card_deck_image_path)

    def pre_draw_your_main_character(self):
        your_main_character_image_path = os.path.join(self.__project_root, "local_storage", "image", "battle_field", "main_character.png")
        self.__pre_drawed_your_main_character = ImageDataLoader.load_oval_image_data(your_main_character_image_path)

    def pre_draw_your_hand_panel(self):
        your_hand_panel_image_path = os.path.join(self.__project_root, "local_storage", "image", "battle_field", "background.png")
        self.__pre_drawed_your_hand_panel = ImageDataLoader.load_rectangle_image_data(your_hand_panel_image_path)

    def pre_draw_every_image(self):
        self.pre_draw_opponent_tomb()
        self.pre_draw_opponent_lost_zone()
        self.pre_draw_opponent_trap()
        self.pre_draw_opponent_card_deck()
        self.pre_draw_opponent_main_character()
        self.pre_draw_opponent_hand_panel()

        self.pre_draw_your_tomb()
        self.pre_draw_your_card_deck()
        self.pre_draw_your_main_character()
        self.pre_draw_your_hand_panel()

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

    def get_pre_draw_your_tomb(self):
        return self.__pre_drawed_your_tomb

    def get_pre_draw_your_card_deck(self):
        return self.__pre_drawed_your_card_deck

    def get_pre_draw_your_main_character(self):
        return self.__pre_drawed_your_main_character

    def get_pre_draw_your_hand_panel(self):
        return self.__pre_drawed_your_hand_panel
