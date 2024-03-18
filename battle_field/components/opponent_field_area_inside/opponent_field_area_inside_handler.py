class OpponentFieldAreaInsideHandler:
    __instance = None

    __field_area_action = None
    __lightning_border_list = []
    __action_set_card_id = 0
    __recently_added_card_index = None

    __required_to_process_passive_skill_multiple_unit_list = []
    __required_to_process_passive_skill_multiple_unit_map = {}

    __unit_action = None
    __turn_start_action = None
    __active_field_area_action = None

    # __your_hand_repository = YourHandRepository.getInstance()
    # __your_field_unit_repository = YourFieldUnitRepository.getInstance()
    # __your_deck_repository = YourDeckRepository.getInstance()
    # __card_info_repository = CardInfoFromCsvRepositoryImpl.getInstance()
    # __your_tomb_repository = YourTombRepository.getInstance()
    # __session_info_repository = SessionRepositoryImpl.getInstance()
    #
    # __your_field_unit_action_repository = YourFieldUnitActionRepository.getInstance()
    # __detector_about_test = DetectorAboutTest.getInstance()

    __field_area_inside_handler_table = {}

    __width_ratio = 1
    __height_ratio = 1

    def __new__(cls):

        if cls.__instance is None:
            cls.__instance = super().__new__(cls)

            # cls.__field_area_inside_handler_table[2] = cls.__instance.handle_support_card_energy_boost
            # cls.__field_area_inside_handler_table[20] = cls.__instance.handle_support_card_draw_deck
            # cls.__field_area_inside_handler_table[30] = cls.__instance.handle_support_card_search_unit_from_deck
            # cls.__field_area_inside_handler_table[36] = cls.__instance.handle_nothing

        return cls.__instance

    @classmethod
    def getInstance(cls):

        if cls.__instance is None:
            cls.__instance = cls()
        return cls.__instance

    def get_field_area_action(self):
        # print(f"get_field_area_action: {self.__field_area_action}")
        return self.__field_area_action

    def set_field_area_action(self, field_area_action):
        self.__field_area_action = field_area_action

    def clear_field_area_action(self):
        self.__field_area_action = None

    def get_active_field_area_action(self):
        return self.__active_field_area_action

    def set_active_field_area_action(self, active_field_area_action):
        self.__active_field_area_action = active_field_area_action

    def clear_active_field_area_action(self):
        self.__active_field_area_action = None

    def set_field_turn_start_action(self, turn_start_action):
        self.__turn_start_action = turn_start_action

    def get_field_turn_start_action(self):
        return self.__turn_start_action

    def clear_field_turn_start_action(self):
        self.__turn_start_action = None

    def set_unit_action(self, unit_action):
        self.__unit_action = unit_action

    def get_unit_action(self):
        return self.__unit_action

    # def set_required_to_process_opponent_passive_skill_multiple_unit_list(self, required_to_process_passive_skill_multiple_unit_list):
    #     self.__required_to_process_passive_skill_multiple_unit_list = required_to_process_passive_skill_multiple_unit_list
    #
    # def get_required_to_process_opponent_passive_skill_multiple_unit_list(self):
    #     return self.__required_to_process_passive_skill_multiple_unit_list

    def set_required_to_process_opponent_passive_skill_multiple_unit_map(self, required_to_process_passive_skill_multiple_unit_map):
        self.__required_to_process_passive_skill_multiple_unit_map = required_to_process_passive_skill_multiple_unit_map

    def get_required_to_process_opponent_passive_skill_multiple_unit_map(self):
        return self.__required_to_process_passive_skill_multiple_unit_map

