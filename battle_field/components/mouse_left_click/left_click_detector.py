class LeftClickDetector:
    __instance = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
        return cls.__instance

    @classmethod
    def getInstance(cls):
        if cls.__instance is None:
            cls.__instance = cls()
        return cls.__instance

    def which_one_select_is_in_hand_list_area(self, click_point, hand_card_list, canvas_height):
        x, y = click_point
        y = canvas_height - y
        y *= -1

        for hand_card in reversed(hand_card_list):
            card_base = hand_card.get_pickable_card_base()

            if card_base.is_point_inside((x, y)):
                hand_card.selected = not hand_card.selected
                return hand_card

        return None

    def which_one_select_is_in_field_unit_list_area(self, click_point, field_unit_list, canvas_height):
        x, y = click_point
        y = canvas_height - y
        y *= -1

        for field_unit in reversed(field_unit_list):
            fixed_card_base = field_unit.get_fixed_card_base()

            if fixed_card_base.is_point_inside((x, y)):
                return field_unit

        return None