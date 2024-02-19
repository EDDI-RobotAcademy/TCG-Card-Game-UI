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

    def which_one_select_is_in_hand_list_area(self, click_point, card_list, canvas_height):
        x, y = click_point
        y = canvas_height - y
        y *= -1
        print(f"click_point: {click_point}, card_list: {card_list}, height: {canvas_height}")
        print(f"x: {x}, y: {y}")

        selected_object = None

        for card in reversed(card_list):
            card_base = card.get_pickable_card_base()

            if card_base.is_point_inside((x, y)):
                print("is it inside hand!")
                card.selected = not card.selected
                selected_object = card
                return selected_object

        return selected_object
