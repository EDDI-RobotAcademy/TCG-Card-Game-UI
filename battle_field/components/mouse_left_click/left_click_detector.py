from battle_field.entity.tomb_type import TombType


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

    def which_one_select_is_in_your_hand_list_area(self, click_point, hand_card_list, canvas_height):
        x, y = click_point
        y = canvas_height - y
        y *= -1

        for hand_card in reversed(hand_card_list):
            card_base = hand_card.get_pickable_card_base()

            if card_base.is_point_inside((x, y)):
                hand_card.selected = not hand_card.selected
                return hand_card

        return None

    def which_one_select_is_in_your_field_unit_list_area(self, click_point, field_unit_list, canvas_height):
        x, y = click_point
        y = canvas_height - y
        y *= -1

        for field_unit in reversed(field_unit_list):
            fixed_card_base = field_unit.get_fixed_card_base()

            if fixed_card_base.is_point_inside((x, y)):
                return field_unit

        return None


    def which_one_select_is_in_extra_area(self, click_point, battle_field_button_list, canvas_height):
        x, y = click_point
        y = canvas_height - y
        y *= -1
        print(f"click_point: {click_point}, button_list: {battle_field_button_list}, height: {canvas_height}")
        print(f"x: {x}, y: {y}")

        for button in battle_field_button_list:
            print(f"button: {button}")
            button_base = button.get_button_base()
            print(f"button_base: {button_base}")
            if button_base.is_point_inside((x, y)):
                return button

        return None

    def which_one_select_is_in_your_tomb_area(self, click_point, your_tomb, canvas_height):
        x, y = click_point
        y = canvas_height - y
        y *= -1

        if your_tomb.is_point_inside((x, y)):
            return your_tomb

        return None

    def which_one_select_is_in_opponent_tomb_area(self, click_point, opponent_tomb, canvas_height):
        x, y = click_point
        y = canvas_height - y
        y *= -1

        if opponent_tomb.is_point_inside((x, y)):
            return opponent_tomb

        return None

    def which_tomb_did_you_select(self, click_point, your_tomb, opponent_tomb, canvas_height):
        x, y = click_point
        y = canvas_height - y
        y *= -1

        if self.which_one_select_is_in_your_tomb_area((x, y), your_tomb, canvas_height):
            return TombType.Your

        if self.which_one_select_is_in_opponent_tomb_area((x, y), opponent_tomb, canvas_height):
            return TombType.Opponent

        return TombType.Dummy

    def which_one_select_is_in_your_lost_zone_area(self, click_point, your_lost_zone, canvas_height):
        x, y = click_point
        y = canvas_height - y
        y *= -1

        if your_lost_zone.is_point_inside((x, y)):
            return your_lost_zone

        return None

    def which_one_select_is_in_opponent_lost_zone_area(self, click_point, opponent_lost_zone, canvas_height):
        x, y = click_point
        y = canvas_height - y
        y *= -1

        if opponent_lost_zone.is_point_inside((x, y)):
            return opponent_lost_zone

        return None


    # todo : [이재승] 여기부터는 새로 짠 코드들

    def which_one_select_is_in_your_field_energy_area(self, click_point, your_field_energy_zone, canvas_height):
        x, y = click_point
        y = canvas_height - y
        y *= -1

        if your_field_energy_zone.is_point_inside((x, y)):
            return your_field_energy_zone

        return None

    def which_one_select_is_in_next_field_energy_race_area(self, click_point, next_field_energy_race_zone,
                                                           canvas_height):
        x, y = click_point
        y = canvas_height - y
        y *= -1

        if next_field_energy_race_zone.is_point_inside((x, y)):
            return next_field_energy_race_zone

        return None

    def which_one_select_is_in_prev_field_energy_race_area(self, click_point, prev_field_energy_race_zone,
                                                           canvas_height):
        x, y = click_point
        y = canvas_height - y
        y *= -1

        if prev_field_energy_race_zone.is_point_inside((x, y)):
            return prev_field_energy_race_zone

        return None

    def which_one_select_is_in_increase_to_use_field_energy_count_area(self, click_point, increase_field_energy_count_zone,
                                                                canvas_height):
        x, y = click_point
        y = canvas_height - y
        y *= -1

        if increase_field_energy_count_zone.is_point_inside((x, y)):
            return increase_field_energy_count_zone

        return None

    def which_one_select_is_in_decrease_to_use_field_energy_count_area(self, click_point, decrease_field_energy_count_zone,
                                                                canvas_height):
        x, y = click_point
        y = canvas_height - y
        y *= -1

        if decrease_field_energy_count_zone.is_point_inside((x, y)):
            return decrease_field_energy_count_zone

        return None

    def which_one_select_is_in_turn_end_area(self, click_point, turn_end_button, canvas_height):
        x, y = click_point
        y = canvas_height - y
        y *= -1

        if turn_end_button.is_point_inside((x, y)):
            return turn_end_button

        return None