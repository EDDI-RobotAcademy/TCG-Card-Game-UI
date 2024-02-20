from battle_field.components.field_area_inside.field_area_action import FieldAreaAction
from common.card_type import CardType

# pip3 install shapely
from shapely.geometry import Point, Polygon

class FieldAreaInsideHandler:
    __instance = None

    __field_area_action = None
    __lightning_border_list = []
    __action_set_card_id = 0

    __field_area_inside_handler_table = {}

    def __new__(cls,
                your_hand_repository,
                your_field_unit_repository,
                card_info,
                your_tomb_repository):

        if cls.__instance is None:
            cls.__instance = super().__new__(cls)

            cls.__instance.your_hand_repository = your_hand_repository
            cls.__instance.your_field_unit_repository = your_field_unit_repository
            cls.__instance.card_info = card_info
            cls.__instance.your_tomb_repository = your_tomb_repository

            cls.__field_area_inside_handler_table[2] = cls.__instance.handle_support_card_energy_boost

        return cls.__instance

    @classmethod
    def getInstance(cls,
                    your_hand_repository,
                    your_field_unit_repository,
                    card_info,
                    your_tomb_repository):

        if cls.__instance is None:
            cls.__instance = cls(your_hand_repository,
                                 your_field_unit_repository,
                                 card_info,
                                 your_tomb_repository)
        return cls.__instance

    def get_lightning_border_list(self):
        return self.__lightning_border_list

    def clear_lightning_border_list(self):
        self.__lightning_border_list = []

    def get_action_set_card_id(self):
        return self.__action_set_card_id

    def clear_action_set_card_id(self):
        self.__action_set_card_id = 0

    def get_field_area_action(self):
        print(f"get_field_area_action: {self.__field_area_action}")
        return self.__field_area_action

    def clear_field_area_action(self):
        self.__field_area_action = None

    def handle_card_drop(self, x, y, selected_object):
        if not self.is_drop_location_valid_your_unit_field(x, y) or not selected_object:
            return None

        placed_card_id = selected_object.get_card_number()
        print(f"my card number is {placed_card_id}")
        card_type = self.card_info.getCardTypeForCardNumber(placed_card_id)
        print(f"my card type is {card_type}")

        if card_type == CardType.UNIT.value:
            return self.handle_unit_card(placed_card_id)
        elif card_type == CardType.SUPPORT.value:
            return self.handle_support_card(placed_card_id)
        else:
            return FieldAreaAction.Dummy

    def handle_unit_card(self, placed_card_id):
        # TODO: Memory Leak에 대한 추가 작업이 필요할 수 있음
        self.your_hand_repository.remove_card_by_id(placed_card_id)
        self.your_field_unit_repository.create_field_unit_card(placed_card_id)
        self.your_field_unit_repository.save_current_field_unit_state(placed_card_id)

        self.your_hand_repository.replace_hand_card_position()

        self.__field_area_action = FieldAreaAction.PLACE_UNIT
        return self.__field_area_action

    def handle_support_card_energy_boost(self, placed_card_id):
        print(f"handle_support_card_energy_boost -> placed_card_id: {placed_card_id}")
        for fixed_field_unit_card in self.your_field_unit_repository.get_current_field_unit_list():
            card_base = fixed_field_unit_card.get_fixed_card_base()
            self.__lightning_border_list.append(card_base)

        self.__action_set_card_id = placed_card_id
        self.your_hand_repository.remove_card_by_id(placed_card_id)

        self.__field_area_action = FieldAreaAction.ENERGY_BOOST
        return self.__field_area_action

    def handle_support_card(self, placed_card_id):
        print("서포트 카드 사용 감지!")

        support_card_handler = self.__field_area_inside_handler_table[placed_card_id]
        support_card_action = support_card_handler(placed_card_id)

        tomb_state = self.your_tomb_repository.current_tomb_state
        tomb_state.place_unit_to_tomb(placed_card_id)
        self.your_hand_repository.replace_hand_card_position()

        return support_card_action

    def is_drop_location_valid_your_unit_field(self, x, y):
        valid_area_vertices = [(300, 580), (1600, 580), (1600, 730), (300, 730)]
        poly = Polygon(valid_area_vertices)
        point = Point(x, y)

        return point.within(poly)


    #     return self.point_inside_polygon(x, y, valid_area_vertices)
    #
    # def point_inside_polygon(self, x, y, poly):
    #     n = len(poly)
    #     inside = False
    #
    #     p1x, p1y = poly[0]
    #     for i in range(1, n + 1):
    #         p2x, p2y = poly[i % n]
    #         if y > min(p1y, p2y):
    #             if y <= max(p1y, p2y):
    #                 if x <= max(p1x, p2x):
    #                     if p1y != p2y:
    #                         xinters = (y - p1y) * (p2x - p1x) / (p2y - p1y) + p1x
    #                     if p1x == p2x or x <= xinters:
    #                         inside = not inside
    #         p1x, p1y = p2x, p2y
    #
    #     return inside
