from common.card_type import CardType
from opengl_battle_field_pickable_card.pickable_card import LegacyPickableCard


class ReleaseHandler:
    def __init__(self, selected_object, your_hand_repository, your_field_unit_repository, card_info):
        self.selected_object = selected_object
        self.your_hand_repository = your_hand_repository
        self.your_field_unit_repository = your_field_unit_repository
        self.card_info = card_info

    def handle_release(self, x, y):
        if isinstance(self.selected_object, LegacyPickableCard):
            current_field_unit_list = self.your_field_unit_repository.get_current_field_unit_list()
            current_field_unit_list_length = len(current_field_unit_list)

            if current_field_unit_list_length > 0:
                self.handle_current_field_units(x, y, current_field_unit_list)

    def handle_current_field_units(self, x, y, current_field_unit_list):
        for unit_index, current_field_unit in enumerate(current_field_unit_list):
            fixed_card_base = current_field_unit.get_fixed_card_base()
            if fixed_card_base.is_point_inside((x, y)):
                self.handle_tool_card(unit_index)
                self.handle_energy_card(unit_index)
                return

    def handle_tool_card(self, unit_index):
        placed_card_id = self.selected_object.get_card_number()
        card_type = self.card_info.getCardTypeForCardNumber(placed_card_id)

        if card_type == CardType.TOOL.value:
            self.selected_object = None
            print("도구를 붙입니다!")
            self.your_hand_repository.remove_card_by_id(placed_card_id)
            self.your_hand_repository.replace_hand_card_position()

    def handle_energy_card(self, unit_index):
        placed_card_id = self.selected_object.get_card_number()
        card_type = self.card_info.getCardTypeForCardNumber(placed_card_id)

        if card_type == CardType.ENERGY.value:
            self.selected_object = None
            print("에너지를 붙입니다!")
            self.your_hand_repository.remove_card_by_id(placed_card_id)
            self.your_field_unit_repository.get_attached_energy_info().add_energy_at_index(unit_index, 1)
            self.your_hand_repository.replace_hand_card_position()
