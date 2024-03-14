from colorama import Fore, Style


class AttackAnimation:
    __instance = None

    is_finished = False
    your_field_hp_shape = None
    your_field_card_index = None
    your_weapon_shape = None
    your_field_unit = None

    your_usage_card_id = None

    your_field_unit_hp_shape_list = []
    your_field_unit_remaining_hp_list = []
    your_dead_field_unit_index_list = []
    your_main_character_health_point = None
    your_lost_card_id_list = []
    your_field_unit_index_list = []
    your_field_unit_health_point_map = {}

    opponent_fixed_card_attached_shape = None
    opponent_field_card_index = None
    opponent_field_unit = None

    opponent_lost_card_id = None
    opponent_main_character = None

    is_opponent_field_unit_death = False
    is_your_field_unit_death = False

    need_post_process = False

    is_it_wide_area_attack = False
    wide_attack_opponent_field_hp_list = []

    your_attacker_unit_moving_x = 0
    animation_actor_damage = 0

    animation_action = None

    opponent_animation_actor = None
    opponent_animation_actor_damage = 0

    notify_data = None

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

    def set_opponent_animation_actor(self, opponent_animation_actor):
        self.opponent_animation_actor = opponent_animation_actor

    def get_opponent_animation_actor(self):
        return self.opponent_animation_actor

    def set_is_finished(self, is_finished):
        self.is_finished = is_finished

    def get_is_finished(self):
        return self.is_finished

    def set_notify_data(self, notify_data):
        self.notify_data = notify_data

    def get_notify_data(self):
        return self.notify_data

    def set_your_field_hp_shape(self, your_field_hp_shape):
        self.your_field_hp_shape = your_field_hp_shape

    def get_your_field_hp_shape(self):
        return self.your_field_hp_shape

    def set_your_field_death_unit_index(self, your_field_card_index):
        self.your_field_card_index = your_field_card_index

    def get_your_field_death_unit_index(self):
        return self.your_field_card_index

    def set_opponent_field_hp_shape(self, opponent_fixed_card_attached_shape):
        self.opponent_fixed_card_attached_shape = opponent_fixed_card_attached_shape

    def get_opponent_field_hp_shape(self):
        return self.opponent_fixed_card_attached_shape

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

    def set_opponent_field_unit_death(self, opponent_field_unit_death):
        self.is_opponent_field_unit_death = opponent_field_unit_death

    def get_opponent_field_unit_death(self):
        return self.is_opponent_field_unit_death

    def set_your_field_unit_death(self, your_field_unit_death):
        self.is_your_field_unit_death = your_field_unit_death

    def get_your_field_unit_death(self):
        return self.is_your_field_unit_death

    def set_your_field_unit(self, your_field_unit):
        self.your_field_unit = your_field_unit

    def get_your_field_unit(self):
        return self.your_field_unit

    def set_is_it_wide_area_attack(self, is_it_wide_area_attack):
        self.is_it_wide_area_attack = is_it_wide_area_attack

    def get_is_it_wide_area_attack(self):
        return self.is_it_wide_area_attack

    def add_wide_attack_opponent_field_hp_list(self, hp_number):
        self.wide_attack_opponent_field_hp_list.append(hp_number)

    def get_wide_attack_opponent_field_hp_list(self):
        return self.wide_attack_opponent_field_hp_list

    def clear_wide_attack_opponent_field_hp_list(self):
        self.wide_attack_opponent_field_hp_list = []

    def set_your_attacker_unit_moving_x(self, your_attacker_unit_moving_x):
        self.your_attacker_unit_moving_x = your_attacker_unit_moving_x

    def get_your_attacker_unit_moving_x(self):
        return self.your_attacker_unit_moving_x

    def set_animation_actor_damage(self, damage):
        self.animation_actor_damage = damage

    def get_animation_actor_damage(self):
        return self.animation_actor_damage

    def set_opponent_animation_actor_damage(self, opponent_damage):
        self.opponent_animation_actor_damage = opponent_damage

    def get_opponent_animation_actor_damage(self):
        return self.opponent_animation_actor_damage

    def add_your_field_unit_hp_shape_list(self, your_field_unit_hp_shape):
        self.your_field_unit_hp_shape_list.append(your_field_unit_hp_shape)

    def get_your_field_unit_hp_shape_list(self):
        return self.your_field_unit_hp_shape_list

    def clear_your_field_unit_hp_shape_list(self):
        self.your_field_unit_hp_shape_list = []

    def add_your_dead_field_unit_index_list(self, your_dead_field_unit_index):
        self.your_dead_field_unit_index_list.append(your_dead_field_unit_index)

    def get_your_dead_field_unit_index_list(self):
        return self.your_dead_field_unit_index_list

    def clear_your_dead_field_unit_index_list(self):
        self.your_dead_field_unit_index_list = []

    def set_your_main_character_health_point(self, your_main_character_health_point):
        self.your_main_character_health_point = your_main_character_health_point

    def get_your_main_character_health_point(self):
        return self.your_main_character_health_point

    def add_your_lost_card_id_list(self, your_lost_card_id_list):
        self.your_lost_card_id_list.append(your_lost_card_id_list)

    def get_your_lost_card_id_list(self):
        return self.your_lost_card_id_list

    def clear_your_lost_card_id_list(self):
        self.your_lost_card_id_list = []

    def set_animation_action(self, animation_action):
        self.animation_action = animation_action

    def get_animation_action(self):
        return self.animation_action

    def add_your_field_unit_index_list(self, your_field_unit_index_list):
        self.your_field_unit_index_list.append(your_field_unit_index_list)

    def get_your_field_unit_index_list(self):
        return self.your_field_unit_index_list

    def clear_your_field_unit_index_list(self):
        self.your_field_unit_index_list = []

    def add_your_field_unit_remaining_hp_list(self, your_field_unit_remaining_hp_list):
        self.your_field_unit_remaining_hp_list.append(your_field_unit_remaining_hp_list)

    def get_your_field_unit_remaining_hp_list(self):
        return self.your_field_unit_remaining_hp_list

    def clear_your_field_unit_remaining_hp_list(self):
        self.your_field_unit_remaining_hp_list = []

    def set_your_field_unit_health_point_map(self, your_field_unit_health_point_map):
        self.your_field_unit_health_point_map = your_field_unit_health_point_map

    def get_your_field_unit_health_point_map(self):
        return self.your_field_unit_health_point_map

    def clear_your_field_unit_health_point_map(self):
        self.your_field_unit_health_point_map = {}

    def set_your_usage_card_id(self, your_usage_card_id):
        self.your_usage_card_id = your_usage_card_id

    def get_your_usage_card_id(self):
        return self.your_usage_card_id

    def set_opponent_lost_card_id(self, opponent_lost_card_id):
        self.opponent_lost_card_id = opponent_lost_card_id

    def get_opponent_lost_card_id(self):
        return self.opponent_lost_card_id
      
    def set_opponent_main_character(self, opponent_main_character):
        self.opponent_main_character = opponent_main_character

    def get_opponent_main_character(self):
        return self.opponent_main_character

    def set_extra_ability(self, extra_ability):
        self.extra_ability = extra_ability

    def get_extra_ability(self):
        return self.extra_ability

