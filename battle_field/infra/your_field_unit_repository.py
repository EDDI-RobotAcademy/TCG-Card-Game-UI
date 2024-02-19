from battle_field.state.attached_energy_info import AttachedEnergyInfoState
from battle_field.state.current_field_unit import CurrentFieldUnitState
from battle_field_fixed_card.fixed_field_card import FixedFieldCard


class YourFieldUnitRepository:
    __instance = None

    # TODO: 당장 구현이 매우 촉바가므로 에너지의 경우 종족에 관련한 사항은 배제하고 수치값만 고려
    attached_energy_info = AttachedEnergyInfoState()

    current_field_unit_state = CurrentFieldUnitState()
    current_field_unit_list = []
    current_field_unit_x_position = []

    x_base = 300

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
        return cls.__instance

    @classmethod
    def getInstance(cls):
        if cls.__instance is None:
            cls.__instance = cls()
        return cls.__instance

    def save_current_field_unit_state(self, hand_card_id):
        self.current_field_unit_state.place_unit_to_field(hand_card_id)
        print(f"Saved current field_unit state: {hand_card_id}")

    def get_current_field_unit_state(self):
        return self.current_field_unit_state.get_current_field_unit_list()

    def create_field_unit_card(self, card_id):
        index = len(self.current_field_unit_list)
        new_card = FixedFieldCard(local_translation=self.get_next_card_position(index))
        new_card.init_card(card_id)
        new_card.set_index(index)
        self.current_field_unit_list.append(new_card)

    def create_field_unit_card_list(self):
        current_field_unit = self.get_current_field_unit_state()
        print(f"current_field_unit: {current_field_unit}")

        for index, card_number in enumerate(current_field_unit):
            print(f"index: {index}, card_number: {card_number}")
            new_card = FixedFieldCard(local_translation=self.get_next_card_position(index))
            new_card.init_card(card_number)
            new_card.set_index(index)
            self.current_field_unit_list.append(new_card)

    def get_current_field_unit_list(self):
        return self.current_field_unit_list

    def get_next_card_position(self, index):
        # TODO: 배치 간격 고려
        current_y = 580
        x_increment = 170
        next_x = self.x_base + x_increment * index
        return (next_x, current_y)

    def attach_energy(self, unit_index, energy_count):
        self.attached_energy_info.add_energy_at_index(unit_index, energy_count)

    def detach_energy(self, unit_index, energy_count):
        self.attached_energy_info.remove_energy_at_index(unit_index, energy_count)

    def get_attached_energy_info(self):
        return self.attached_energy_info
