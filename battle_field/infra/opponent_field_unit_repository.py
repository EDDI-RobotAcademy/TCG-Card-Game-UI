from battle_field.state.attached_energy_info import AttachedEnergyInfoState
from battle_field.state.current_field_unit import CurrentFieldUnitState
from battle_field.state.extra_effect_info import ExtraEffectInfo
from battle_field.state.harmful_status_info import HarmfulStatusInfo
from battle_field_fixed_card.fixed_field_card import FixedFieldCard


class OpponentFieldUnitRepository:
    __instance = None

    attached_energy_info = AttachedEnergyInfoState()
    extra_effect_info = ExtraEffectInfo()
    harmful_status_info = HarmfulStatusInfo()

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

    def get_field_unit_max_index(self):
        return len(self.current_field_unit_card_object_list) - 1

    def create_field_unit_card(self, field_unit_id):
        # valid_opponent_field_unit_list = [unit for unit in self.current_field_unit_card_object_list if unit is not None]
        # index = len(valid_opponent_field_unit_list)

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

    def get_current_field_unit_state(self):
        return self.current_field_unit_state

    def remove_current_field_unit_card(self, unit_index):
        # TODO: 이 부분 Memory Leak 발생 우려 (카드 구성 객체 정리 방안 구성 필요)
        # del self.current_field_unit_card_object_list[unit_index]
        # self.current_field_unit_state.delete_current_field_unit_list(unit_index)

        removed_card = self.current_field_unit_card_object_list.pop(unit_index)
        self.current_field_unit_card_object_list.insert(unit_index, None)

    def remove_card_by_multiple_index(self, card_index_list):
        for index in sorted(card_index_list, reverse=True):
            if 0 <= index < len(self.current_field_unit_card_object_list):
                # del self.current_field_unit_card_object_list[index]
                # self.current_field_unit_state.remove_field_unit_by_index(index)

                removed_card = self.current_field_unit_card_object_list.pop(index)
                self.current_field_unit_card_object_list.insert(index, None)
            else:
                print(f"Invalid index: {index}. No card removed for this index.")

        print(
            f"Removed cards at indices {card_index_list} -> current_opponent_field_list: "
            f"{self.current_field_unit_card_object_list}, "
            f"current_opponent_field_state: {self.get_current_field_unit_state()}")


    def replace_opponent_field_unit_card_position(self):
        current_y = 270
        x_increment = 170

        valid_opponent_field_unit_list = [unit for unit in self.current_field_unit_card_object_list if unit is not None]

        for index, current_field_unit_card in enumerate(valid_opponent_field_unit_list):
            next_x = self.x_base + x_increment * index
            print(f"next_x: {next_x}")
            local_translation = (next_x, current_y)

            tool_card = current_field_unit_card.get_tool_card()
            tool_card.local_translate(local_translation)

            fixed_card_base = current_field_unit_card.get_fixed_card_base()
            fixed_card_base.local_translate(local_translation)

            for attached_shape in fixed_card_base.get_attached_shapes():
                attached_shape.local_translate(local_translation)

            dark_flame_animation_panel = current_field_unit_card.get_fixed_card_dark_flame_effect_animation_panel()
            if dark_flame_animation_panel:
                print('flame animation panel set local translation', local_translation)
                dark_flame_animation_panel.local_translate(local_translation)

            freeze_effect_animation_panel = current_field_unit_card.get_fixed_card_freeze_effect_animation_panel()
            if freeze_effect_animation_panel:
                print('frozen animation panel set local translation', local_translation)
                freeze_effect_animation_panel.local_translate(local_translation)

    def attach_race_energy(self, opponent_field_unit_index, energy_race, energy_count):
        self.attached_energy_info.add_race_energy_at_index(opponent_field_unit_index, energy_race, energy_count)
        print(f"attached_energy_info after attach_race_energy: {self.attached_energy_info}")

    def detach_race_energy(self, opponent_field_unit_index, energy_race, energy_count):
        self.attached_energy_info.remove_race_energy_at_index(opponent_field_unit_index, energy_race, energy_count)

    def apply_harmful_status(self, unit_index, harmful_status_list):
        print('apply_harmful_status to opponent!!')
        self.harmful_status_info.update_harmful_status(unit_index, harmful_status_list)

    def get_harmful_status_by_index(self, index):
        return self.harmful_status_info.get_harmful_status_of_index(index)

    def get_is_index_in_harmful_status(self, index):
        return self.harmful_status_info.is_index_in_harmful_status(index)

    def remove_harmful_status_by_index(self, index):
        self.harmful_status_info.remove_harmful_status_of_index(index)

    def get_total_energy_at_index(self, index):
        return self.attached_energy_info.get_total_energy_at_index(index)

    def get_energy_info_at_index(self, index):
        return self.attached_energy_info.get_energy_info_at_index(index)

    def get_opponent_field_unit_race_energy(self, index, energy_race):
        return self.attached_energy_info.get_race_energy_at_index(index, energy_race)

    def find_opponent_field_unit_by_index(self, index):
        if 0 <= index < len(self.current_field_unit_card_object_list):
            return self.current_field_unit_card_object_list[index]
        else:
            return None

    def find_field_unit_by_index(self, index):
        if 0 <= index < len(self.current_field_unit_card_object_list):
            return self.current_field_unit_card_object_list[index]
        else:
            return None

    def get_opponent_card_id_by_index(self, index):
        card_list = self.get_current_field_unit_card_object_list()
        if index < len(card_list):
            return card_list[index].get_card_number()
        # print(f"card_list: {card_list}")
        # for card in card_list:
        #     if card:
        #         print(f'card in card_list: {card}')
        #         if card.get_index() == index:
        #             return card.get_card_number()

        return -1

    def get_attached_energy_info(self):
        return self.attached_energy_info

    def update_opponent_unit_extra_effect_at_index(self, unit_index, extra_effect_list):
        self.extra_effect_info.update_extra_effect_of_unit(unit_index, extra_effect_list)

    # def update_your_unit_extra_effect_at_index(self, unit_index, extra_effect_list):
    #     self.extra_effect_info.update_extra_effect_of_unit(unit_index, extra_effect_list)

    def get_opponent_unit_extra_ability_at_index(self, unit_index):
        return self.extra_effect_info.get_extra_effect_of_index(unit_index)

    def clear_every_resource(self):
        self.attached_energy_info = AttachedEnergyInfoState()
        self.extra_effect_info = ExtraEffectInfo()
        self.harmful_status_info = HarmfulStatusInfo()

        self.current_field_unit_state = CurrentFieldUnitState()
        self.current_field_unit_card_object_list = []
        self.current_field_unit_x_position = []

