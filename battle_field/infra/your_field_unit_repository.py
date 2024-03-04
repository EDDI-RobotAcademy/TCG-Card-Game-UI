from battle_field.state.attached_energy_info import AttachedEnergyInfoState
from battle_field.state.current_field_unit import CurrentFieldUnitState
from battle_field_fixed_card.legacy.fixed_field_card import LegacyFixedFieldCard


class YourFieldUnitRepository:
    __instance = None

    # TODO: 당장 구현이 매우 촉바가므로 에너지의 경우 종족에 관련한 사항은 배제하고 수치값만 고려
    attached_energy_info = AttachedEnergyInfoState()

    current_field_unit_state = CurrentFieldUnitState()
    current_field_unit_list = []
    current_field_unit_x_position = []

    __receiveIpcChannel = None
    __transmitIpcChannel = None

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

    def save_current_field_unit_state(self, hand_card_id):
        self.current_field_unit_state.place_unit_to_field(hand_card_id)
        print(f"Saved current field_unit state: {hand_card_id}")

    def get_current_field_unit_state(self):
        return self.current_field_unit_state.get_current_field_unit_list()

    def create_field_unit_card(self, card_id):
        index = len(self.current_field_unit_list)
        print(f"create_field_unit_card() -> index: {index}")
        print(f"create_field_unit_card() -> self.current_field_unit_list: {self.current_field_unit_list}")
        new_card = LegacyFixedFieldCard(local_translation=self.get_next_card_position(index))
        new_card.init_card(card_id)
        new_card.set_index(index)
        self.current_field_unit_list.append(new_card)

    def request_to_deploy_your_unit(self, deploy_unit_card_request):
        self.__transmitIpcChannel.put(deploy_unit_card_request)
        return self.__receiveIpcChannel.get()

    def create_field_unit_card_list(self):
        current_field_unit = self.get_current_field_unit_state()
        print(f"current_field_unit: {current_field_unit}")

        for index, card_number in enumerate(current_field_unit):
            print(f"index: {index}, card_number: {card_number}")
            new_card = LegacyFixedFieldCard(local_translation=self.get_next_card_position(index))
            new_card.init_card(card_number)
            new_card.set_index(index)
            self.current_field_unit_list.append(new_card)

    def get_current_field_unit_list(self):
        return self.current_field_unit_list

    def get_next_card_position(self, index):
        # TODO: 배치 간격 고려
        current_y = 490
        x_increment = 170
        next_x = self.x_base + x_increment * index
        return (next_x, current_y)

    # TODO: Legacy <- 테스트 의존성 체크
    def attach_energy(self, unit_index, energy_count):
        self.attached_energy_info.add_energy_at_index(unit_index, energy_count)

    # TODO: Legacy <- 테스트 의존성 체크
    def detach_energy(self, unit_index, energy_count):
        self.attached_energy_info.remove_energy_at_index(unit_index, energy_count)

    def attach_race_energy(self, field_unit_index, energy_race, energy_count):
        print(f"attach_race_energy() -> field_unit_index: {field_unit_index}, race: {energy_race} count: {energy_count}")
        self.attached_energy_info.add_race_energy_at_index(field_unit_index, energy_race, energy_count)

    def detach_race_energy(self, opponent_field_unit_index, energy_race, energy_count):
        self.attached_energy_info.remove_race_energy_at_index(opponent_field_unit_index, energy_race, energy_count)

    def get_total_energy_at_index(self, index):
        return self.attached_energy_info.get_total_energy_at_index(index)

    def get_energy_info_at_index(self, index):
        return self.attached_energy_info.get_energy_info_at_index(index)

    def get_your_field_unit_race_energy(self, index, energy_race):
        return self.attached_energy_info.get_race_energy_at_index(index, energy_race)

    def find_field_unit_by_index(self, index):
        return self.get_current_field_unit_list()[index]
        # for unit in self.current_field_unit_list:
        #     if unit.get_index() == index:
        #         return unit
        # return None

    def get_attached_energy_info(self):
        return self.attached_energy_info
    def remove_card_by_id(self, card_id):
        card_list = self.get_current_field_unit_list()

        for card in card_list:
            if card.get_card_number() == card_id:
                card_list.remove(card)

        self.current_field_unit_state.delete_current_field_unit_list(card_id)

        # print(f"after clear -> current_hand_list: {self.current_field_unit_state}, current_hand_state: {self.get_current_field_unit_state()}")

    def remove_card_by_index(self, card_placed_index):
        removed_card = self.current_field_unit_list.pop(card_placed_index)
        self.current_field_unit_list.insert(card_placed_index, None)
        print(f"Removed card index {card_placed_index} -> current_hand_list: {self.current_field_unit_list}, current_hand_state: {self.get_current_field_unit_state()}")

    def replace_field_card_position(self):
        # current_y = 580
        # x_increment = 170

        current_y = 490
        x_increment = 170

        # 전투로 파괴된 유닛들 제외
        valid_field_unit_list = [unit for unit in self.current_field_unit_list if unit is not None]

        for index, current_field_unit in enumerate(valid_field_unit_list):
            next_x = self.x_base + x_increment * index
            local_translation = (next_x, current_y)
            print(f"replace_field_unit_position -> local_translation: {local_translation}")

            tool_card = current_field_unit.get_tool_card()
            tool_card.local_translate(local_translation)
            # tool_intiial_vertices = tool_card.get_initial_vertices()
            # tool_card.update_vertices(tool_intiial_vertices)

            fixed_card_base = current_field_unit.get_fixed_card_base()
            fixed_card_base.local_translate(local_translation)

            for attached_shape in fixed_card_base.get_attached_shapes():
                attached_shape.local_translate(local_translation)

            # pickable_card_base = current_field_unit.get_pickable_card_base()
            # pickable_card_base.local_translate(local_translation)
            #
            # for attached_shape in pickable_card_base.get_attached_shapes():
            #     # if isinstance(attached_shape, CircleImage):
            #     #     # TODO: 동그라미는 별도 처리해야함
            #     #     attached_circle_shape_initial_center = attached_shape.get_initial_center()
            #     #     attached_shape.update_circle_vertices(attached_circle_shape_initial_center)
            #     #     continue
            #
            #     attached_shape.local_translate(local_translation)
            #     # attached_shape_intiial_vertices = attached_shape.get_initial_vertices()
            #     # attached_shape.update_vertices(attached_shape_intiial_vertices)
            #
            # # current_hand_card.change_local_translation((next_x, current_y))
    def saveReceiveIpcChannel(self, receiveIpcChannel):
        self.__receiveIpcChannel = receiveIpcChannel

    def saveTransmitIpcChannel(self, transmitIpcChannel):
        self.__transmitIpcChannel = transmitIpcChannel