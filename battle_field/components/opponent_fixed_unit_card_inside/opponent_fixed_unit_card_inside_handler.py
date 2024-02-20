from common.card_type import CardType


class OpponentFixedUnitCardInsideHandler:
    __instance = None

    def __new__(cls,
                your_hand_repository,
                opponent_field_unit_repository,
                card_info):

        if cls.__instance is None:
            cls.__instance = super().__new__(cls)

            cls.__instance.your_hand_repository = your_hand_repository
            cls.__instance.opponent_field_unit_repository = opponent_field_unit_repository
            cls.__instance.card_info = card_info

        return cls.__instance

    @classmethod
    def getInstance(cls,
                    your_hand_repository,
                    opponent_field_unit_repository,
                    card_info):

        if cls.__instance is None:
            cls.__instance = cls(your_hand_repository,
                                 opponent_field_unit_repository,
                                 card_info)
        return cls.__instance

    def handle_pickable_card_inside_unit(self, selected_object, x, y):
        print(f"handle_pickable_card_inside_unit: {selected_object}, {x}, {y}")
        card_type = self.card_info.getCardTypeForCardNumber(selected_object.get_card_number())
        print(f"card_type: {card_type}")

        if card_type not in [CardType.ITEM.value]:
            return

        opponent_field_unit_list = self.opponent_field_unit_repository.get_current_field_unit_card_object_list()

        for opponent_unit_index, opponent_field_unit in enumerate(opponent_field_unit_list):
            if opponent_field_unit.get_fixed_card_base().is_point_inside((x, y)):
                self.handle_inside_field_unit(selected_object, opponent_unit_index)
                return True

        return False

    def handle_inside_field_unit(self, selected_object, opponent_unit_index):
        placed_card_id = selected_object.get_card_number()
        card_type = self.card_info.getCardTypeForCardNumber(placed_card_id)

        if card_type == CardType.ITEM.value:
            self.handle_item_card(placed_card_id, opponent_unit_index)

    def handle_item_card(self, placed_card_id, unit_index):
        print("아이템 카드를 사용합니다!")

        self.your_hand_repository.remove_card_by_id(placed_card_id)
        self.opponent_field_unit_repository.remove_current_field_unit_card(unit_index)
        self.your_hand_repository.replace_hand_card_position()


