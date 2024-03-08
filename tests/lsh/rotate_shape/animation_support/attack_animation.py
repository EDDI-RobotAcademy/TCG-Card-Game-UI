from colorama import Fore, Style


class AttackAnimation:
    __instance = None

    is_finished = False
    your_field_hp_shape = None
    your_field_card_index = None
    your_weapon_shape = None

    opponent_fixed_card_attached_shape = None
    opponent_field_card_index = None
    opponent_field_unit = None

    need_post_process = False


    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
        return cls.__instance

    @classmethod
    def getInstance(cls):
        if cls.__instance is None:
            cls.__instance = cls()
        return cls.__instance

    def __init__(self):
        self.total_width = None
        self.total_height = None

        self.local_translation = (0, 0)

        self.width_ratio = 1
        self.height_ratio = 1

        self.selected_object = None

    def set_total_window_size(self, width, height):
        self.total_width = width
        self.total_height = height

    def get_total_width(self):
        return self.total_width

    def get_total_height(self):
        return self.total_height

    def set_animation_actor(self, selected_object):
        print(f"{Fore.RED}selected_object{Fore.GREEN} {selected_object}{Style.RESET_ALL}")
        self.selected_object = selected_object

    def get_animation_actor(self):
        return self.selected_object

    def set_is_finished(self, is_finished):
        self.is_finished = is_finished

    def get_is_finished(self):
        return self.is_finished

    def set_your_field_hp_shape(self, your_field_hp_shape):
        self.your_field_hp_shape = your_field_hp_shape

    def set_your_field_death_unit_index(self, your_field_card_index):
        self.your_field_card_index = your_field_card_index

    def set_opponent_field_hp_shape(self, opponent_fixed_card_attached_shape):
        self.opponent_fixed_card_attached_shape = opponent_fixed_card_attached_shape

    def set_opponent_field_death_unit_index(self, opponent_field_card_index):
        self.opponent_field_card_index = opponent_field_card_index

    def set_need_post_process(self, need_post_process):
        self.need_post_process = need_post_process

    def get_need_post_process(self):
        return self.need_post_process

    def set_your_weapon_shape(self, your_weapon_shape):
        self.your_weapon_shape = your_weapon_shape

    def get_your_weapon_shape(self):
        return self.your_weapon_shape

    def set_opponent_field_unit(self, opponent_field_unit):
        self.opponent_field_unit = opponent_field_unit

    def get_opponent_field_unit(self):
        return self.opponent_field_unit


