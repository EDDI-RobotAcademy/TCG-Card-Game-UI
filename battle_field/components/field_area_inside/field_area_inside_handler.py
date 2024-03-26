from colorama import Fore, Style

from battle_field.components.field_area_inside.field_area_action import FieldAreaAction
from battle_field.components.field_area_inside.unit_action import UnitAction
from battle_field.entity.effect_animation import EffectAnimation
from battle_field.infra.request.deploy_unit_card_request import DeployUnitCardRequest
from battle_field.infra.request.drawCardByUseSupportCardRequest import DrawCardByUseSupportCardRequest
from battle_field.infra.request.request_use_overflow_of_energy import RequestUseOverflowOfEnergy
from battle_field.infra.your_deck_repository import YourDeckRepository

from battle_field.infra.your_field_unit_action_repository import YourFieldUnitActionRepository
from battle_field.infra.your_field_unit_repository import YourFieldUnitRepository
from battle_field.infra.your_hand_repository import YourHandRepository
from battle_field.infra.your_tomb_repository import YourTombRepository
from card_info_from_csv.repository.card_info_from_csv_repository_impl import CardInfoFromCsvRepositoryImpl
from common.card_grade import CardGrade
from common.card_type import CardType

# pip3 install shapely
from shapely.geometry import Point, Polygon

from common.message_number import MessageNumber
from common.target_type import TargetType
from fake_notify_reader.repository.fake_notify_reader_repository_impl import FakeNotifyReaderRepositoryImpl
from music_player.repository.music_player_repository_impl import MusicPlayerRepositoryImpl
from notify_reader.repository.notify_reader_repository_impl import NotifyReaderRepositoryImpl
from notify_reader.service.request.effect_animation_request import EffectAnimationRequest
from session.repository.session_repository_impl import SessionRepositoryImpl
from test_detector.detector import DetectorAboutTest


class FieldAreaInsideHandler:
    __instance = None

    __field_area_action = None
    __lightning_border_list = []
    __action_set_card_id = 0
    __recently_added_card_index = None

    __required_to_process_passive_skill_multiple_unit_list = []
    __required_to_process_passive_skill_multiple_unit_map = {}

    __unit_action = None
    __turn_start_action = None
    # __action_set_card_index = 0

    __your_hand_repository = YourHandRepository.getInstance()
    __your_field_unit_repository = YourFieldUnitRepository.getInstance()
    __your_deck_repository = YourDeckRepository.getInstance()
    __card_info_repository = CardInfoFromCsvRepositoryImpl.getInstance()
    __your_tomb_repository = YourTombRepository.getInstance()
    __session_info_repository = SessionRepositoryImpl.getInstance()
    __music_player_repository = MusicPlayerRepositoryImpl.getInstance()
    __notify_reader_repository = NotifyReaderRepositoryImpl.getInstance()
    __fake_notify_reader_repository = FakeNotifyReaderRepositoryImpl.getInstance()

    __your_field_unit_action_repository = YourFieldUnitActionRepository.getInstance()
    __detector_about_test = DetectorAboutTest.getInstance()

    __field_area_inside_handler_table = {}

    __width_ratio = 1
    __height_ratio = 1

    __placed_card_page = None
    __placed_card_index = None

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

    def set_placed_card_index(self, index):
        self.__placed_card_index = index

    def get_placed_card_index(self):
        return self.__placed_card_index

    def set_placed_card_page(self, page):
        self.__placed_card_page = page

    def get_placed_card_page(self):
        return self.__placed_card_page

    def reset_placed_card_index(self):
        self.__placed_card_index = None

    def reset_placed_card_page(self):
        self.__placed_card_page = None

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

    def set_field_turn_start_action(self, turn_start_action):
        self.__turn_start_action = turn_start_action

    def get_field_turn_start_action(self):
        return self.__turn_start_action

    def clear_field_turn_start_action(self):
        self.__turn_start_action = None

    def set_required_to_process_passive_skill_multiple_unit_list(self, required_to_process_passive_skill_multiple_unit_list):
        self.__required_to_process_passive_skill_multiple_unit_list = required_to_process_passive_skill_multiple_unit_list

    def get_required_to_process_passive_skill_multiple_unit_list(self):
        return self.__required_to_process_passive_skill_multiple_unit_list

    def set_required_to_process_passive_skill_multiple_unit_map(self, required_to_process_passive_skill_multiple_unit_map):
        self.__required_to_process_passive_skill_multiple_unit_map = required_to_process_passive_skill_multiple_unit_map

    def get_required_to_process_passive_skill_multiple_unit_map(self):
        return self.__required_to_process_passive_skill_multiple_unit_map

    def clear_required_to_process_passive_skill_multiple_unit_list(self):
        self.__required_to_process_passive_skill_multiple_unit_list = []

    def set_field_area_action(self, field_area_action):
        self.__field_area_action = field_area_action

    def set_unit_action(self, unit_action):
        self.__unit_action = unit_action

    def get_unit_action(self):
        return self.__unit_action

    def set_width_ratio(self, width_ratio):
        self.__width_ratio = width_ratio

    def set_height_ratio(self, height_ratio):
        self.__height_ratio = height_ratio

    def set_recently_added_card_index(self, card_index):
        self.__recently_added_card_index = card_index

    def get_recently_added_card_index(self):
        return self.__recently_added_card_index

    def handle_card_drop(self, x, y, selected_object, your_battle_field_panel):
        print("handle_card_drop()")
        if not self.is_drop_location_valid_your_unit_field(x, y, your_battle_field_panel) or not selected_object:
            return FieldAreaAction.Dummy

        placed_card_id = selected_object.get_card_number()

        card_grade = self.__card_info_repository.getCardGradeForCardNumber(placed_card_id)
        card_type = self.__card_info_repository.getCardTypeForCardNumber(placed_card_id)
        # print(f"my card type is {card_type}")

        # placed_card_index = self.__your_hand_repository.find_index_by_selected_object(selected_object)
        placed_card_page = self.__your_hand_repository.get_current_your_hand_page()
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
        # 통신 없는 테스트의 경우 바로 제낌
        deploy_your_unit_request = None

        if self.__detector_about_test.get_is_it_test() is False:
            session = self.__session_info_repository.get_session_info()
            deploy_your_unit_request = self.__your_field_unit_repository.request_to_deploy_your_unit(
                DeployUnitCardRequest(session, placed_card_id))

            print(f"{Fore.RED}deploy_your_unit_request:{Fore.GREEN} {deploy_your_unit_request}{Style.RESET_ALL}")
            deploy_is_success = deploy_your_unit_request['is_success']
            if deploy_is_success is False:
                print(f"self.__card_info_repository.getCardGradeForCardNumber(placed_card_id): {self.__card_info_repository.getCardGradeForCardNumber(placed_card_id)}")
                deploy_false_message = deploy_your_unit_request['false_message_enum']
                return deploy_false_message

        # TODO: Memory Leak에 대한 추가 작업이 필요할 수 있음
        # self.__your_hand_repository.remove_card_by_index(placed_card_index)
        self.__music_player_repository.play_sound_effect_of_unit_deploy(str(placed_card_id))
        self.__your_hand_repository.remove_card_by_index_with_page(placed_card_index)

        self.__your_field_unit_repository.create_field_unit_card(placed_card_id)
        self.__your_field_unit_repository.save_current_field_unit_state(placed_card_id)
        self.__recently_added_card_index = self.__your_field_unit_repository.get_recently_added_field_unit_index()

        # your_hand_page = self.__your_hand_repository.get_current_your_hand_page()
        # your_hand_page_card_list = self.__your_hand_repository.your_hand_page_list[your_hand_page].get_your_hand_page_card_list()
        # print(f"length of your_hand_page_card_list: {len(your_hand_page_card_list)}")

        # self.__your_hand_repository.replace_hand_card_position()
        self.__your_hand_repository.update_your_hand()
        self.__your_field_unit_repository.replace_field_card_position()

#        print(f"{Fore.RED}deploy_your_unit_request -> number_of_passive_skill_to_handle:{Fore.GREEN} {deploy_your_unit_request['number_of_passive_skill_to_handle']}{Style.RESET_ALL}")

        self.__your_field_unit_action_repository.create_field_unit_action_count(0)

        passive_skill_type = self.__card_info_repository.getCardPassiveFirstForCardNumber(placed_card_id)
        if passive_skill_type == 2:
            print("광역기")

            self.__field_area_action = FieldAreaAction.REQUIRED_FIRST_PASSIVE_SKILL_PROCESS
            if placed_card_id == 19:
                self.set_unit_action(UnitAction.NETHER_BLADE_FIRST_WIDE_AREA_PASSIVE_SKILL)

            return self.__field_area_action


        elif passive_skill_type == 1:
            print("단일기")

            self.__field_area_action = FieldAreaAction.REQUIRED_FIRST_PASSIVE_SKILL_PROCESS
            return self.__field_area_action

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
        # self.__your_hand_repository.remove_card_by_index_with_page(placed_card_index)
        self.set_placed_card_index(placed_card_index)

        self.__field_area_action = FieldAreaAction.ENERGY_BOOST
        return self.__field_area_action

    def handle_support_card_draw_deck(self, placed_card_id, placed_card_index):
        print(f"handle_support_card_draw_deck -> placed_card_id: {placed_card_id}")

        before_draw_deck_list = self.__your_deck_repository.get_current_deck_state()
        print(f"before draw 3: {before_draw_deck_list}")

        response = self.__your_deck_repository.request_use_swamp_of_dead(
            DrawCardByUseSupportCardRequest(
                _sessionInfo=self.__session_info_repository.get_session_info(),
                _cardId="20")
        )
        print(f"{Fore.RED}swamp_of_dead -> response:{Fore.GREEN} {response}{Style.RESET_ALL}")
        is_success_value = response.get('is_success', False)

        if is_success_value == False:
            is_false_message = response.get('false_message_enum')
            return is_false_message

        def swamp_of_ghost(response):
            # self.__music_player_repository.play_sound_effect_of_card_execution('swamp_of_ghost')
            # TODO: Summary와 연동하도록 재구성 필요
            # drawn_card_list = self.__your_deck_repository.draw_deck_with_count(3)
            drawn_card_list = response['player_draw_card_list_map']['You']
            print(f"{Fore.RED}drawn_card_list:{Fore.GREEN} {drawn_card_list}{Style.RESET_ALL}")

            # after_draw_deck_list = self.__your_deck_repository.get_current_deck_state()
            # print(f"after draw 3: {after_draw_deck_list}")

            after_draw_deck_list = response['updated_deck_card_list']
            print(f"{Fore.RED}after_draw_deck_list:{Fore.GREEN} {after_draw_deck_list}{Style.RESET_ALL}")

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

        effect_animation = EffectAnimation()
        effect_animation.set_animation_name('swamp_of_ghost')

        self.__notify_reader_repository.save_notify_effect_animation_request(
            EffectAnimationRequest(
                effect_animation=effect_animation,
                target_player='You',
                target_index=99999,
                target_type=TargetType.AREA,
                call_function=swamp_of_ghost,
                function_need_param=True,
                param=response
            )
        )

        self.__fake_notify_reader_repository.save_notify_effect_animation_request(
            EffectAnimationRequest(
                effect_animation=effect_animation,
                target_player='You',
                target_index=99999,
                target_type=TargetType.AREA,
                call_function=swamp_of_ghost,
                function_need_param=True,
                param=response
            )
        )

    def handle_support_card_search_unit_from_deck(self, placed_card_id, placed_card_index):
        print(f"handle_support_card_search_unit_from_deck -> placed_card_id: {placed_card_id}, placed_card_index: {placed_card_index}")

        # self.__action_set_card_id = placed_card_id
        # self.__your_hand_repository.remove_card_by_index(placed_card_index)
        # self.__your_hand_repository.remove_card_by_index_with_page(placed_card_index)
        # self.__your_tomb_repository.create_tomb_card(placed_card_id)

        self.__action_set_card_id = placed_card_id
        self.set_placed_card_index(placed_card_index)
        self.__your_deck_repository.update_deck_search_unit_card()

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
