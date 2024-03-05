from battle_field.components.field_area_inside.field_area_action import FieldAreaAction
from battle_field.infra.legacy.circle_image_legacy_your_deck_repository import CircleImageLegacyYourDeckRepository
from battle_field.infra.your_field_unit_action_repository import YourFieldUnitActionRepository
from battle_field.infra.legacy.circle_image_legacy_your_field_unit_repository import CircleImageLegacyYourFieldUnitRepository
from battle_field.infra.legacy.circle_image_legacy_your_hand_repository import CircleImageLegacyYourHandRepository
from battle_field.infra.legacy.circle_image_legacy_your_tomb_repository import CircleImageLegacyYourTombRepository
from card_info_from_csv.repository.card_info_from_csv_repository_impl import CardInfoFromCsvRepositoryImpl
from common.card_type import CardType

# pip3 install shapely
from shapely.geometry import Point, Polygon

from session.repository.session_repository_impl import SessionRepositoryImpl


class CircleImageLegacyFieldAreaInsideHandler:
    __instance = None

    __field_area_action = None
    __lightning_border_list = []
    __action_set_card_id = 0
    # __action_set_card_index = 0

    __your_hand_repository = CircleImageLegacyYourHandRepository.getInstance()
    __your_field_unit_repository = CircleImageLegacyYourFieldUnitRepository.getInstance()
    __your_deck_repository = CircleImageLegacyYourDeckRepository.getInstance()
    __card_info_repository = CardInfoFromCsvRepositoryImpl.getInstance()
    __your_tomb_repository = CircleImageLegacyYourTombRepository.getInstance()
    __session_info_repository = SessionRepositoryImpl.getInstance()

    __your_field_unit_action_repository = YourFieldUnitActionRepository.getInstance()

    __field_area_inside_handler_table = {}

    __width_ratio = 1
    __height_ratio = 1

    def __new__(cls):

        if cls.__instance is None:
            cls.__instance = super().__new__(cls)

            cls.__field_area_inside_handler_table[2] = cls.__instance.handle_support_card_energy_boost
            cls.__field_area_inside_handler_table[20] = cls.__instance.handle_support_card_draw_deck
            cls.__field_area_inside_handler_table[30] = cls.__instance.handle_support_card_search_unit_from_deck
            cls.__field_area_inside_handler_table[36] = cls.__instance.handle_nothing

        return cls.__instance

    @classmethod
    def getInstance(cls):

        if cls.__instance is None:
            cls.__instance = cls()
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
        # print(f"get_field_area_action: {self.__field_area_action}")
        return self.__field_area_action

    def clear_field_area_action(self):
        self.__field_area_action = None

    def set_width_ratio(self, width_ratio):
        self.__width_ratio = width_ratio

    def set_height_ratio(self, height_ratio):
        self.__height_ratio = height_ratio

    def handle_card_drop(self, x, y, selected_object, your_battle_field_panel):
        print("handle_card_drop()")
        if not self.is_drop_location_valid_your_unit_field(x, y, your_battle_field_panel) or not selected_object:
            return None

        placed_card_id = selected_object.get_card_number()

        card_grade = self.__card_info_repository.getCardGradeForCardNumber(placed_card_id)
        card_type = self.__card_info_repository.getCardTypeForCardNumber(placed_card_id)
        # print(f"my card type is {card_type}")

        # placed_card_index = self.__your_hand_repository.find_index_by_selected_object(selected_object)
        placed_card_index = self.__your_hand_repository.find_index_by_selected_object_with_page(selected_object)

        if card_type == CardType.UNIT.value:
            return self.handle_unit_card(placed_card_id, placed_card_index)
        elif card_type == CardType.SUPPORT.value:
            return self.handle_support_card(placed_card_id, placed_card_index)
        else:
            return FieldAreaAction.Dummy

    def handle_nothing(self, placed_card_id, placed_card_index):
        return FieldAreaAction.Dummy

    def handle_unit_card(self, placed_card_id, placed_card_index):
        # TODO: 실제 통합 테스트에서는 네트워크 연동이 필요함
        # session = self.__session_info_repository.get_session_info()
        # deploy_your_unit_request = self.__your_field_unit_repository.request_to_deploy_your_unit(
        #     DeployUnitCardRequest(session, placed_card_id))
        #
        # print(f"deploy_your_unit_request: {deploy_your_unit_request}")
        # deploy_is_success = deploy_your_unit_request['is_success']
        # if deploy_is_success is False:
        #     return FieldAreaAction.Dummy

        # TODO: Memory Leak에 대한 추가 작업이 필요할 수 있음
        # self.__your_hand_repository.remove_card_by_index(placed_card_index)
        self.__your_hand_repository.remove_card_by_index_with_page(placed_card_index)

        self.__your_field_unit_repository.create_field_unit_card(placed_card_id)
        self.__your_field_unit_repository.save_current_field_unit_state(placed_card_id)

        # your_hand_page = self.__your_hand_repository.get_current_your_hand_page()
        # your_hand_page_card_list = self.__your_hand_repository.your_hand_page_list[your_hand_page].get_your_hand_page_card_list()
        # print(f"length of your_hand_page_card_list: {len(your_hand_page_card_list)}")

        # self.__your_hand_repository.replace_hand_card_position()
        self.__your_hand_repository.update_your_hand()
        self.__your_field_unit_repository.replace_field_card_position()

        passive_skill_type = self.__card_info_repository.getCardPassiveFirstForCardNumber(placed_card_id)
        if passive_skill_type == 2:
            print("광역기")
        elif passive_skill_type == 1:
            print("단일기")

        self.__your_field_unit_action_repository.create_field_unit_action_count(0)

        self.__field_area_action = FieldAreaAction.PLACE_UNIT
        return self.__field_area_action

    def handle_support_card_energy_boost(self, placed_card_id, placed_card_index):
        print(f"handle_support_card_energy_boost -> placed_card_id: {placed_card_id}")
        for fixed_field_unit_card in self.__your_field_unit_repository.get_current_field_unit_list():
            if fixed_field_unit_card is None:
                continue

            card_base = fixed_field_unit_card.get_fixed_card_base()
            self.__lightning_border_list.append(card_base)

        self.__action_set_card_id = placed_card_id
        # self.__your_hand_repository.remove_card_by_index(placed_card_index)
        self.__your_hand_repository.remove_card_by_index_with_page(placed_card_index)

        self.__field_area_action = FieldAreaAction.ENERGY_BOOST
        return self.__field_area_action

    def handle_support_card_draw_deck(self, placed_card_id, placed_card_index):
        print(f"handle_support_card_draw_deck -> placed_card_id: {placed_card_id}")

        before_draw_deck_list = self.__your_deck_repository.get_current_deck_state()
        print(f"before draw 3: {before_draw_deck_list}")

        # TODO: Summary와 연동하도록 재구성 필요
        drawn_card_list = self.__your_deck_repository.draw_deck_with_count(3)

        after_draw_deck_list = self.__your_deck_repository.get_current_deck_state()
        print(f"after draw 3: {after_draw_deck_list}")

        self.__your_deck_repository.update_deck(after_draw_deck_list)

        # TODO: 테스트인 경우와 실제 통신하는 경우를 스마트하게 분리 할 필요가 있음 (아래는 통신)
        # try:
        #     draw_card_response = self.__your_hand_repository.requestDrawCardByUseSupportCard(
        #         DrawCardByUseSupportCardRequest(_sessionInfo=self.__session_info_repository.get_session_info(),
        #                                         _cardId=placed_card_id)
        #     )
        #
        #     if draw_card_response is not None:
        #         drawn_card_list = draw_card_response
        #
        # except Exception as e:
        #     print(f"draw_card Error! {e}")

        # self.__your_hand_repository.create_additional_hand_card_list(drawn_card_list)
        # self.__your_hand_repository.remove_card_by_index(placed_card_index)
        self.__your_hand_repository.remove_card_by_index_with_page(placed_card_index)
        self.__your_hand_repository.save_current_hand_state(drawn_card_list)
        self.__your_hand_repository.update_your_hand()

        self.__your_tomb_repository.create_tomb_card(20)
        print(
            f"handle_support_card_draw_deck() -> current_tomb_unit_list: {self.__your_tomb_repository.get_current_tomb_state()}")

        self.__field_area_action = FieldAreaAction.DRAW_DECK
        return self.__field_area_action

    def handle_support_card_search_unit_from_deck(self, placed_card_id, placed_card_index):
        print(f"handle_support_card_search_unit_from_deck -> placed_card_id: {placed_card_id}, placed_card_index: {placed_card_index}")

        # self.__action_set_card_id = placed_card_id
        # self.__your_hand_repository.remove_card_by_index(placed_card_index)
        self.__your_hand_repository.remove_card_by_index_with_page(placed_card_index)
        self.__your_tomb_repository.create_tomb_card(placed_card_id)

        self.__field_area_action = FieldAreaAction.SEARCH_UNIT_CARD
        return self.__field_area_action

    def handle_support_card(self, placed_card_id, placed_card_index):
        print("서포트 카드 사용 감지! handle_support_card() -> ")

        support_card_handler = self.__field_area_inside_handler_table[placed_card_id]
        support_card_action = support_card_handler(placed_card_id, placed_card_index)

        # tomb_state = self.__your_tomb_repository.current_tomb_state
        # tomb_state.place_unit_to_tomb(placed_card_id)
        self.__your_hand_repository.replace_hand_card_position()

        return support_card_action

    def is_drop_location_valid_your_unit_field(self, x, y, your_battle_field_panel):
        print(
            f"is_drop_location_valid_your_unit_field -> x: {x}, y: {y}, your_battle_field_panel: {your_battle_field_panel}")
        # valid_area_vertices = [(300, 580), (1600, 580), (1600, 730), (300, 730)]
        valid_your_field = your_battle_field_panel.get_vertices()
        print(f"valid_your_field: {valid_your_field}")

        # width_ratio = your_battle_field_panel.get_width_ratio()
        # height_ratio = your_battle_field_panel.get_height_ratio()
        ratio_applied_valid_your_field = [(x * self.__width_ratio, y * self.__height_ratio) for x, y in
                                          valid_your_field]
        print(f"ratio_applied_valid_your_field: {ratio_applied_valid_your_field}")
        print(f"x: {x * self.__width_ratio}, y: {y * self.__height_ratio}")

        # ratio_applied_valid_your_field = [
        #     (valid_your_field[0][0] * self.__width_ratio, valid_your_field[0][1] * self.__height_ratio)
        # ]
        # print(f"ratio_applied_valid_your_field: {ratio_applied_valid_your_field}")

        poly = Polygon(ratio_applied_valid_your_field)
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
