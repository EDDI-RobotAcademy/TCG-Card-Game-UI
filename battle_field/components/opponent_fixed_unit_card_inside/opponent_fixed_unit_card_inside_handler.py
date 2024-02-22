from battle_field.components.opponent_fixed_unit_card_inside.opponent_field_area_action import OpponentFieldAreaAction
from battle_field.infra.opponent_field_unit_repository import OpponentFieldUnitRepository
from battle_field.infra.your_hand_repository import YourHandRepository
from card_info_from_csv.repository.card_info_from_csv_repository_impl import CardInfoFromCsvRepositoryImpl
from common.card_race import CardRace
from common.card_type import CardType


class OpponentFixedUnitCardInsideHandler:
    __instance = None

    __required_energy = -1
    __required_energy_race = CardRace.DUMMY
    __opponent_field_area_action = None
    __opponent_unit_index = -1
    __action_set_card_index = -1

    __your_hand_repository = YourHandRepository.getInstance()
    __opponent_field_unit_repository = OpponentFieldUnitRepository.getInstance()
    __card_info_repository = CardInfoFromCsvRepositoryImpl.getInstance()

    __lightning_border_list = []

    __opponent_fixed_unit_card_inside_handler_table = {}

    def __new__(cls):

        if cls.__instance is None:
            cls.__instance = super().__new__(cls)

            # cls.__instance.your_hand_repository = your_hand_repository
            # cls.__instance.opponent_field_unit_repository = opponent_field_unit_repository
            # cls.__instance.card_info = card_info

            cls.__instance.__opponent_fixed_unit_card_inside_handler_table[8] = cls.__instance.death_sice_need_two_undead_energy

        return cls.__instance

    @classmethod
    def getInstance(cls):

        if cls.__instance is None:
            cls.__instance = cls()
        return cls.__instance

    def get_required_energy(self):
        return self.__required_energy

    def decrease_required_energy(self):
        self.__required_energy -= 1

    def clear_required_energy(self):
        self.__required_energy = -1

    def get_required_energy_race(self):
        return self.__required_energy_race

    def clear_required_energy_race(self):
        self.__required_energy_race = CardRace.DUMMY

    def get_opponent_field_area_action(self):
        return self.__opponent_field_area_action

    def clear_opponent_field_area_action(self):
        self.__opponent_field_area_action = None

    def get_opponent_unit_index(self):
        return self.__opponent_unit_index

    def clear_opponent_unit_index(self):
        self.__opponent_unit_index = -1

    def get_action_set_card_index(self):
        return self.__action_set_card_index

    def clear_action_set_card_index(self):
        self.__action_set_card_index = -1

    def get_lightning_border_list(self):
        return self.__lightning_border_list

    def clear_lightning_border_list(self):
        self.__lightning_border_list = []

    def handle_pickable_card_inside_unit(self, selected_object, x, y):
        print(f"handle_pickable_card_inside_unit: {selected_object}, {x}, {y}")
        card_type = self.__card_info_repository.getCardTypeForCardNumber(selected_object.get_card_number())
        print(f"card_type: {card_type}")

        if card_type not in [CardType.ITEM.value]:
            return

        opponent_field_unit_list = self.__opponent_field_unit_repository.get_current_field_unit_card_object_list()

        for opponent_unit_index, opponent_field_unit in enumerate(opponent_field_unit_list):
            if opponent_field_unit.get_fixed_card_base().is_point_inside((x, y)):
                self.handle_inside_field_unit(selected_object, opponent_unit_index)
                return True

        return False

    def handle_inside_field_unit(self, selected_object, opponent_unit_index):
        placed_card_id = selected_object.get_card_number()
        card_type = self.__card_info_repository.getCardTypeForCardNumber(placed_card_id)

        placed_card_index = self.__your_hand_repository.find_index_by_selected_object(selected_object)

        if card_type == CardType.ITEM.value:
            self.handle_item_card(placed_card_id, opponent_unit_index, placed_card_index)

    def handle_item_card(self, placed_card_id, unit_index, placed_card_index):
        print("아이템 카드를 사용합니다!")

        proper_handler = self.__opponent_fixed_unit_card_inside_handler_table[placed_card_id]
        proper_handler(placed_card_index, unit_index)

        # self.your_hand_repository.remove_card_by_id(placed_card_id)
        # self.opponent_field_unit_repository.remove_current_field_unit_card(unit_index)
        # self.your_hand_repository.replace_hand_card_position()

    def death_sice_need_two_undead_energy(self, placed_card_index, unit_index):
        self.__required_energy = 2
        self.__required_energy_race = CardRace.UNDEAD
        self.__opponent_field_area_action = OpponentFieldAreaAction.REQUIRE_ENERGY_TO_USAGE
        self.__opponent_unit_index = unit_index
        self.__action_set_card_index = placed_card_index

        your_current_hand_card_list = self.__your_hand_repository.get_current_hand_card_list()

        for your_current_hand_card in your_current_hand_card_list:
            your_hand_card_id = your_current_hand_card.get_card_number()
            if your_hand_card_id == 93:
                card_base = your_current_hand_card.get_pickable_card_base()
                self.__lightning_border_list.append(card_base)


