from common.card_type import CardType


class FixedUnitCardInsideHandler:
    __instance = None

    def __new__(cls,
                your_hand_repository,
                your_field_unit_repository,
                card_info):

        if cls.__instance is None:
            cls.__instance = super().__new__(cls)

            cls.__instance.your_hand_repository = your_hand_repository
            cls.__instance.your_field_unit_repository = your_field_unit_repository
            cls.__instance.card_info = card_info

        return cls.__instance

    @classmethod
    def getInstance(cls,
                    your_hand_repository,
                    your_field_unit_repository,
                    card_info):

        if cls.__instance is None:
            cls.__instance = cls(your_hand_repository,
                                 your_field_unit_repository,
                                 card_info)
        return cls.__instance

    def handle_pickable_card_inside_unit(self, selected_object, x, y):
        field_unit_list = self.your_field_unit_repository.get_current_field_unit_list()

        for unit_index, field_unit in enumerate(field_unit_list):
            if field_unit.get_fixed_card_base().is_point_inside((x, y)):
                self.handle_inside_field_unit(selected_object, unit_index)
                return True

        return False

    def handle_inside_field_unit(self, selected_object, unit_index):
        placed_card_id = selected_object.get_card_number()
        card_type = self.card_info.getCardTypeForCardNumber(placed_card_id)

        if card_type == CardType.TOOL.value:
            self.handle_tool_card(placed_card_id)
        elif card_type == CardType.ENERGY.value:
            self.handle_energy_card(placed_card_id, unit_index)

    def handle_tool_card(self, placed_card_id):
        print("도구를 붙입니다!")
        self.your_hand_repository.remove_card_by_id(placed_card_id)
        self.your_hand_repository.replace_hand_card_position()

    def handle_energy_card(self, placed_card_id, unit_index):
        print("에너지를 붙입니다!")
        self.your_hand_repository.remove_card_by_id(placed_card_id)
        self.your_field_unit_repository.get_attached_energy_info().add_energy_at_index(unit_index, 1)
        self.your_hand_repository.replace_hand_card_position()
        # TODO: attached_energy 값 UI에 표현 (이미지 작업 미완료)
        # TODO: 특수 에너지 붙인 것을 어떻게 표현 할 것인가 ? (아직 미정)
