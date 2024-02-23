from battle_field.state.attached_energy_info import AttachedEnergyInfoState
from battle_field.state.current_field_unit import CurrentFieldUnitState
from battle_field_fixed_card.fixed_field_card import FixedFieldCard


class OpponentFieldUnitRepository:
    __instance = None

    attached_energy_info = AttachedEnergyInfoState()

    current_field_unit_state = CurrentFieldUnitState()
    current_field_unit_card_object_list = []
    current_field_unit_x_position = []

    x_base = 265

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
        return cls.__instance

    @classmethod
    def getInstance(cls):
        if cls.__instance is None:
            cls.__instance = cls()
        return cls.__instance

    def place_field_unit(self, field_unit_id):
        self.current_field_unit_state.place_unit_to_field(field_unit_id)
        # print(f"Saved current field_unit state: {field_unit_id}")

    def create_field_unit_card(self, field_unit_id):
        index = len(self.current_field_unit_card_object_list)
        self.place_field_unit(field_unit_id)

        new_card = FixedFieldCard(local_translation=self.get_next_card_position(index))
        new_card.init_card(field_unit_id)
        new_card.set_index(index)

        self.current_field_unit_card_object_list.append(new_card)
        self.current_field_unit_state.place_unit_to_field(field_unit_id)

    def get_next_card_position(self, index):
        current_y = 270
        x_increment = 170
        next_x = self.x_base + x_increment * index
        return (next_x, current_y)

    def get_current_field_unit_card_object_list(self):
        return self.current_field_unit_card_object_list

    def remove_current_field_unit_card(self, unit_index):
        # TODO: 이 부분 Memory Leak 발생 우려 (카드 구성 객체 정리 방안 구성 필요)
        del self.current_field_unit_card_object_list[unit_index]
        self.current_field_unit_state.delete_current_field_unit_list(unit_index)

    def replace_opponent_field_unit_card_position(self):
        current_y = 270
        x_increment = 170

        for index, current_field_unit_card in enumerate(self.current_field_unit_card_object_list):
            next_x = self.x_base + x_increment * index
            print(f"next_x: {next_x}")
            local_translation = (next_x, current_y)

            tool_card = current_field_unit_card.get_tool_card()
            tool_card.local_translate(local_translation)

            fixed_card_base = current_field_unit_card.get_fixed_card_base()
            fixed_card_base.local_translate(local_translation)

            for attached_shape in fixed_card_base.get_attached_shapes():
                attached_shape.local_translate(local_translation)

    def attach_race_energy(self, opponent_field_unit_index, energy_race, energy_count):
        self.attached_energy_info.add_race_energy_at_index(opponent_field_unit_index, energy_race, energy_count)
        print(f"attached_energy_info after attach_race_energy: {self.attached_energy_info}")

    def detach_race_energy(self, opponent_field_unit_index, energy_race, energy_count):
        self.attached_energy_info.remove_race_energy_at_index(opponent_field_unit_index, energy_race, energy_count)

    def get_opponent_field_unit_race_energy(self, index, energy_race):
        return self.attached_energy_info.get_race_energy_at_index(index, energy_race)

    def find_opponent_field_unit_by_index(self, index):
        if 0 <= index < len(self.current_field_unit_card_object_list):
            return self.current_field_unit_card_object_list[index]
        else:
            return None


