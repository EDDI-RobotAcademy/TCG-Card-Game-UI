import json

from colorama import Fore, Style

from battle_field.infra.battle_field_repository import BattleFieldRepository
from battle_field.infra.opponent_field_energy_repository import OpponentFieldEnergyRepository
from battle_field.infra.opponent_field_unit_repository import OpponentFieldUnitRepository
from battle_field.infra.opponent_hand_repository import OpponentHandRepository
from battle_field.infra.opponent_tomb_repository import OpponentTombRepository
from battle_field.infra.your_deck_repository import YourDeckRepository
from battle_field.infra.your_field_energy_repository import YourFieldEnergyRepository
from battle_field.infra.your_field_unit_repository import YourFieldUnitRepository
from battle_field.infra.your_hand_repository import YourHandRepository
from battle_field.infra.your_hp_repository import YourHpRepository
from battle_field.infra.your_lost_zone_repository import YourLostZoneRepository
from battle_field.infra.your_tomb_repository import YourTombRepository
from battle_field.state.energy_type import EnergyType
from battle_field_function.service.battle_field_function_service_impl import BattleFieldFunctionServiceImpl
from battle_field_muligun.infra.muligun_your_hand_repository import MuligunYourHandRepository
from fake_battle_field.infra.fake_opponent_hand_repository import FakeOpponentHandRepositoryImpl
from image_shape.circle_kinds import CircleKinds
from image_shape.non_background_number_image import NonBackgroundNumberImage
from notify_reader.entity.notice_type import NoticeType
from notify_reader.repository.notify_reader_repository_impl import NotifyReaderRepositoryImpl
from notify_reader.service.notify_reader_service import NotifyReaderService
from pre_drawed_image_manager.pre_drawed_image import PreDrawedImage


class NotifyReaderServiceImpl(NotifyReaderService):
    __instance = None

    notify_callback_table = {}

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
            cls.__instance.__notify_reader_repository = NotifyReaderRepositoryImpl.getInstance()
            cls.__instance.__battle_field_function_service = BattleFieldFunctionServiceImpl.getInstance()

            cls.__instance.__opponent_field_unit_repository = OpponentFieldUnitRepository.getInstance()
            cls.__instance.__opponent_field_energy_repository = OpponentFieldEnergyRepository.getInstance()
            cls.__instance.__your_field_energy_repository = YourFieldEnergyRepository.getInstance()
            cls.__instance.__your_hand_repository = YourHandRepository.getInstance()
            cls.__instance.__fake_opponent_hand_repository = FakeOpponentHandRepositoryImpl.getInstance()
            cls.__instance.__pre_drawed_image_instance = PreDrawedImage.getInstance()
            cls.__instance.__your_hp_repository = YourHpRepository.getInstance()
            cls.__instance.__your_tomb_repository = YourTombRepository.getInstance()
            cls.__instance.__opponent_tomb_repository = OpponentTombRepository.getInstance()
            cls.__instance.__your_field_unit_repository = YourFieldUnitRepository.getInstance()
            cls.__instance.__opponent_hand_repository = OpponentHandRepository.getInstance()
            cls.__instance.__battle_field_repository = BattleFieldRepository.getInstance()
            cls.__instance.__mulligan_repository = MuligunYourHandRepository.getInstance()
            cls.__instance.__your_deck_repository = YourDeckRepository.getInstance()
            cls.__instance.__your_lost_zone_repository = YourLostZoneRepository.getInstance()

            cls.__instance.notify_callback_table['NOTIFY_DEPLOY_UNIT'] = cls.__instance.notify_deploy_unit
            cls.__instance.notify_callback_table['NOTIFY_TURN_END'] = cls.__instance.notify_turn_end
            cls.__instance.notify_callback_table[
                'NOTIFY_USE_GENERAL_ENERGY_CARD_TO_UNIT'] = cls.__instance.notify_attach_general_energy_card
            # cls.__instance.notify_callback_table['NOTIFY_USE_GENERAL_ENERGY_CARD_TO_UNIT'] = (
            #     cls.__instance.__battle_field_function_service.useGeneralEnergyCardToUnit)
            cls.__instance.notify_callback_table['NOTIFY_USE_SPECIAL_ENERGY_CARD_TO_UNIT'] = (
                cls.__instance.notify_use_special_energy_card_to_unit)
            cls.__instance.notify_callback_table['NOTIFY_USE_UNIT_ENERGY_REMOVE_ITEM_CARD'] = (
                cls.__instance.__battle_field_function_service.useUnitEnergyRemoveItemCard)
            cls.__instance.notify_callback_table[
                'NOTIFY_BASIC_ATTACK_TO_MAIN_CHARACTER'] = cls.__instance.damage_to_main_character

            cls.__instance.notify_callback_table['NOTIFY_USE_MULTIPLE_UNIT_DAMAGE_ITEM_CARD'] = (
                cls.__instance.notify_use_multiple_unit_damage_item_card
            )

            cls.__instance.notify_callback_table['NOTIFY_USE_MULTIPLE_UNIT_DAMAGE_ITEM_CARD'] = (
                cls.__instance.__battle_field_function_service.useMultipleUnitDamageItemCard)

            cls.__instance.notify_callback_table[
                'NOTIFY_BASIC_ATTACK_TO_UNIT'] = cls.__instance.damage_to_each_unit_by_basic_attack

            cls.__instance.notify_callback_table['NOTIFY_USE_SEARCH_DECK_SUPPORT_CARD'] = cls.__instance.search_card

            cls.__instance.notify_callback_table[
                'NOTIFY_USE_FIELD_ENERGY_TO_UNIT'] = cls.__instance.notify_attach_field_energy_card

            cls.__instance.notify_callback_table['NOTIFY_TARGETING_ATTACK_ACTIVE_SKILL_TO_GAME_MAIN_CHARACTER'] = (
                cls.__instance.notify_targeting_attack_active_skill_to_main_character
            )

            cls.__instance.notify_callback_table['NOTIFY_TARGETING_ATTACK_ACTIVE_SKILL_TO_UNIT'] = (
                cls.__instance.notify_targeting_attack_active_skill_to_your_unit
            )

            cls.__instance.notify_callback_table['NOTIFY_NON_TARGETING_ACTIVE_SKILL'] = (
                cls.__instance.notify_non_targeting_active_skill
            )

            cls.__instance.notify_callback_table['NOTIFY_USE_DRAW_SUPPORT_CARD'] = (
                cls.__instance.notify_use_draw_support_card
            )
            cls.__instance.notify_callback_table['NOTIFY_MULLIGAN_END'] = (
                cls.__instance.notify_mulligan_end
            )

            cls.__instance.notify_callback_table['NOTIFY_USE_CATASTROPHIC_DAMAGE_ITEM_CARD'] = (
                cls.__instance.notify_use_catastrophic_damage_item_card
            )

        return cls.__instance

    @classmethod
    def getInstance(cls):
        if cls.__instance is None:
            cls.__instance = cls()
        return cls.__instance

    def injectNoWaitIpcChannel(self, nowaitIpcChannel):
        self.__notify_reader_repository.saveNoWaitIpcChannel(nowaitIpcChannel)

    def saveHandCardUseFunction(self, hand_card_use_function):
        print(f"saveHandCardUseFunction: {hand_card_use_function}")
        self.__notify_reader_repository.registerFunctionWithNoticeName(NoticeType.NOTIFY_HAND_CARD_USE.name,
                                                                       hand_card_use_function)

    def saveDrawCountFunction(self, draw_count_function):
        print(f"saveDrawCountFunction: {draw_count_function}")
        self.__notify_reader_repository.registerFunctionWithNoticeName(NoticeType.NOTIFY_DRAW_COUNT.name,
                                                                       draw_count_function)

    def saveDrawnCardListFunction(self, drawn_card_list_function):
        print(f"saveDrawnCardListFunction: {drawn_card_list_function}")
        self.__notify_reader_repository.registerFunctionWithNoticeName(NoticeType.NOTIFY_DRAWN_CARD_LIST.name,
                                                                       drawn_card_list_function)

    def saveDeckCardUseListFunction(self, deck_card_list_use_function):
        print(f"saveDeckCardListUseFunction: {deck_card_list_use_function}")
        self.__notify_reader_repository.registerFunctionWithNoticeName(NoticeType.NOTIFY_DECK_CARD_LIST_USE.name,
                                                                       deck_card_list_use_function)

    def saveFieldUnitEnergyFunction(self, field_unit_energy_function):
        print(f"saveFieldUnitEnergy: {field_unit_energy_function}")
        self.__notify_reader_repository.registerFunctionWithNoticeName(NoticeType.NOTIFY_FIELD_UNIT_ENERGY.name,
                                                                       field_unit_energy_function)

    def saveSearchCountFunction(self, search_count_function):
        print(f"saveSearchCount: {search_count_function}")
        self.__notify_reader_repository.registerFunctionWithNoticeName(NoticeType.NOTIFY_SEARCH_COUNT.name,
                                                                       search_count_function)

    def saveSearchCardListFunction(self, search_card_list_function):
        print(f"saveSearchCardListFunction: {search_card_list_function}")
        self.__notify_reader_repository.registerFunctionWithNoticeName(NoticeType.NOTIFY_SEARCH_CARD_LIST.name,
                                                                       search_card_list_function)

    def saveSpawnUnitFunction(self, spawn_unit_function):
        self.__notify_reader_repository.registerFunctionWithNoticeName(NoticeType.NOTIFY_UNIT_SPAWN.name,
                                                                       spawn_unit_function)

    def readNoticeAndCallFunction(self):
        # while True:
        try:
            raw_notice_data = self.__notify_reader_repository.getNotice()

            if raw_notice_data:
                print(f"raw_notice_data: {raw_notice_data}")
                notice_dict = json.loads(raw_notice_data)
                print(f"notice_dict: {notice_dict}")
                notify_key = list(notice_dict.keys())[0]
                print(f"Notify key: {notify_key}")

                notify_callback_function = self.notify_callback_table[notify_key]
                notify_callback_function(notice_dict)

                # for notice_type in NoticeType:
                #     print(f"notice_type: {notice_type.name}")
                #     if notice_type.name in notice_dict:
                #         self.__notify_reader_repository.isFinish = True
                #         print(f"noticeType: {notice_type.name}")
                #         called_function = self.__notify_reader_repository.getFunctionByNoticeName(notice_type.name)
                #         called_function(notice_dict[notice_type.name])

        except Exception as e:
            self.readNoticeAndCallFunction()
            print(e)
        #  continue

    def notify_deploy_unit(self, notice_dictionary):
        print(f"notify_deploy_unit() -> notice_dictionary: {notice_dictionary}")

        whose_turn = self.__notify_reader_repository.get_is_your_turn_for_check_fake_process()
        print(
            f"{Fore.RED}notify_deploy_unit() -> whose_turn True(Your) or False(Opponent):{Fore.GREEN} {whose_turn}{Style.RESET_ALL}")

        if whose_turn is True:
            # self.__notify_reader_repository.set_is_your_turn_for_check_fake_process(not whose_turn)
            # print(f"after set whose_turn: {self.__notify_reader_repository.get_is_your_turn_for_check_fake_process()}")
            return

        card_id = (notice_dictionary.get('NOTIFY_DEPLOY_UNIT', {})
                   .get('player_hand_use_map', {})
                   .get('Opponent', {})
                   .get('card_id', None))

        print(f"{Fore.RED}notify_deploy_unit() -> Opponent deploy card_id:{Fore.GREEN} {card_id}{Style.RESET_ALL}")

        self.__battle_field_repository.set_current_use_card_id(card_id)
        self.__opponent_field_unit_repository.create_field_unit_card(card_id)

    def notify_turn_end(self, notice_dictionary):
        print(f"{Fore.RED}notify_turn_end() -> notice_dictionary:{Fore.GREEN} {notice_dictionary}{Style.RESET_ALL}")

        whose_turn = self.__notify_reader_repository.get_is_your_turn_for_check_fake_process()
        print(
            f"{Fore.RED}notify_turn_end() -> whose_turn True(Your) or False(Opponent):{Fore.GREEN} {whose_turn}{Style.RESET_ALL}")

        if whose_turn is False:
            # Fake Opponent Draw
            opponent_drawn_card_list = notice_dictionary['NOTIFY_TURN_END']['player_drawn_card_list_map'].get('You', [])
            self.__fake_opponent_hand_repository.save_fake_opponent_hand_list(opponent_drawn_card_list)
            fake_opponent_hand_list = self.__fake_opponent_hand_repository.get_fake_opponent_hand_list()
            print(
                f"{Fore.RED}notify_turn_end() -> fake opponent hand list:{Fore.GREEN} {fake_opponent_hand_list}{Style.RESET_ALL}")

            fake_opponent_field_energy = notice_dictionary['NOTIFY_TURN_END']['player_field_energy_map'].get('You', [])
            self.__opponent_field_energy_repository.set_opponent_field_energy(fake_opponent_field_energy)
            print(
                f"{Fore.RED}notify_turn_end() -> fake opponent_field_energy:{Fore.GREEN} {fake_opponent_field_energy}{Style.RESET_ALL}")

            opponent_field_energy_count = self.__opponent_field_energy_repository.get_opponent_field_energy()
            print(f"{Fore.RED}opponent_field_energy_count:{Fore.GREEN} {opponent_field_energy_count}{Style.RESET_ALL}")

            return

        self.__notify_reader_repository.set_is_your_turn_for_check_fake_process(True)

        # Your Draw
        your_drawn_card_list = notice_dictionary['NOTIFY_TURN_END']['player_drawn_card_list_map'].get('You', [])
        self.__your_hand_repository.save_current_hand_state(your_drawn_card_list)
        self.__your_hand_repository.update_your_hand()

        your_field_energy = notice_dictionary['NOTIFY_TURN_END']['player_field_energy_map'].get('You', [])
        self.__your_field_energy_repository.set_your_field_energy(your_field_energy)
        print(f"{Fore.RED}notify_turn_end() -> your_field_energy:{Fore.GREEN} {your_field_energy}{Style.RESET_ALL}")

    def notify_attach_general_energy_card(self, notice_dictionary):

        print(
            f"{Fore.RED}notify_attach_general_energy_card() -> notice_dictionary:{Fore.GREEN} {notice_dictionary}{Style.RESET_ALL}")

        whose_turn = self.__notify_reader_repository.get_is_your_turn_for_check_fake_process()
        print(
            f"{Fore.RED}notify_attach_general_energy_card() -> whose_turn True(Your) or False(Opponent):{Fore.GREEN} {whose_turn}{Style.RESET_ALL}")

        if whose_turn is False:
            # Fake Opponent Attach Energy
            # opponent_field_unit = self.__opponent_field_unit_repository.find_opponent_field_unit_by_index(0)
            # print(f"opponent_field_unit card_id: {opponent_field_unit.get_card_number()}")

            # fake_opponent_field_unit_energy_map = notice_dictionary['NOTIFY_USE_GENERAL_ENERGY_CARD_TO_UNIT']['player_field_unit_energy_map']['Opponent']
            # print(f"{Fore.RED}fake_opponent_field_unit_energy_map:{Fore.GREEN} {fake_opponent_field_unit_energy_map}{Style.RESET_ALL}")
            self.__battle_field_repository.set_current_use_card_id(93)

            for unit_index, unit_value in \
            notice_dictionary['NOTIFY_USE_GENERAL_ENERGY_CARD_TO_UNIT']['player_field_unit_energy_map']['Opponent'][
                'field_unit_energy_map'].items():
                print(f"{Fore.RED}opponent_unit_index:{Fore.GREEN} {unit_index}{Style.RESET_ALL}")
                print(f"{Fore.RED}opponent_unit_value:{Fore.GREEN} {unit_value}{Style.RESET_ALL}")

                # opponent_unit_attached_undead_energy_count = unit_value['attached_energy_map']['2']

                for race_energy_number, race_energy_count in unit_value['attached_energy_map'].items():
                    print(f"{Fore.RED}energy_key:{Fore.GREEN} {race_energy_number}{Style.RESET_ALL}")
                    print(f"{Fore.RED}energy_count:{Fore.GREEN} {race_energy_count}{Style.RESET_ALL}")

                    self.__opponent_field_unit_repository.attach_race_energy(int(unit_index), EnergyType.Undead,
                                                                             race_energy_count)

                    opponent_field_unit = self.__opponent_field_unit_repository.find_opponent_field_unit_by_index(
                        int(unit_index))

                    opponent_fixed_card_base = opponent_field_unit.get_fixed_card_base()
                    opponent_fixed_card_attached_shape_list = opponent_fixed_card_base.get_attached_shapes()

                    total_energy_count = unit_value['total_energy_count']
                    print(f"{Fore.RED}total_energy_count:{Fore.GREEN} {total_energy_count}{Style.RESET_ALL}")

                    for opponent_fixed_card_attached_shape in opponent_fixed_card_attached_shape_list:
                        if isinstance(opponent_fixed_card_attached_shape, NonBackgroundNumberImage):
                            if opponent_fixed_card_attached_shape.get_circle_kinds() is CircleKinds.ENERGY:
                                opponent_fixed_card_attached_shape.set_image_data(
                                    self.__pre_drawed_image_instance.get_pre_draw_unit_energy(
                                        total_energy_count))

    def damage_to_main_character(self, notice_dictionary):
        notify_dict_data = notice_dictionary['NOTIFY_BASIC_ATTACK_TO_MAIN_CHARACTER']

        is_my_turn = self.__notify_reader_repository.get_is_your_turn_for_check_fake_process()
        print(f"is my turn: {is_my_turn}")
        if is_my_turn is True:
            return

        target_character = list(notify_dict_data.get("player_main_character_health_point_map", {}).keys())[0]

        if target_character != "You":
            print("error : is not You")
            return

        character_hp = int(notify_dict_data.get("player_main_character_health_point_map", {})[target_character])

        if notify_dict_data.get("player_main_character_survival_map", {})[target_character] == "Survival":
            character_survival = True
        else:
            character_survival = False

        if character_survival:
            self.__your_hp_repository.change_hp(character_hp)

        else:
            print("나죽어~~~ ")

    def notify_use_multiple_unit_damage_item_card(self, notice_dictionary):
        data = notice_dictionary['NOTIFY_USE_MULTIPLE_UNIT_DAMAGE_ITEM_CARD']

        opponent_usage_card_info = (
            data)['player_hand_use_map']['Opponent']
        your_field_unit_health_point_map = (
            data)['player_field_unit_health_point_map']['You']['field_unit_health_point_map']
        your_dead_field_unit_index_list = (
            data)['player_field_unit_death_map']['You']['dead_field_unit_index_list']
        opponent_sacrificed_field_unit_index_list = (
            data)['player_field_unit_death_map']['Opponent']['dead_field_unit_index_list']

        # 사용된 카드 묘지로 보냄
        used_card_id = opponent_usage_card_info['card_id']
        self.__opponent_tomb_repository.create_opponent_tomb_card(used_card_id)
        self.__battle_field_repository.set_current_use_card_id(used_card_id)

        # 체력 정보 Update
        for unit_index, remaining_health_point in your_field_unit_health_point_map.items():
            your_field_unit = self.__your_field_unit_repository.find_field_unit_by_index(int(unit_index))
            your_fixed_card_base = your_field_unit.get_fixed_card_base()
            your_fixed_card_attached_shape_list = your_fixed_card_base.get_attached_shapes()

            if remaining_health_point <= 0:
                continue

            for your_fixed_card_attached_shape in your_fixed_card_attached_shape_list:
                if isinstance(your_fixed_card_attached_shape, NonBackgroundNumberImage):
                    if your_fixed_card_attached_shape.get_circle_kinds() is CircleKinds.HP:
                        your_fixed_card_attached_shape.set_number(int(remaining_health_point))

                        your_fixed_card_attached_shape.set_image_data(
                            self.__pre_drawed_image_instance.get_pre_draw_unit_hp(int(remaining_health_point)))

        # 죽은 유닛들 묘지에 배치 및 Replacing
        if your_dead_field_unit_index_list:
            for dead_unit_index in your_dead_field_unit_index_list:
                field_unit_id = self.__your_field_unit_repository.get_card_id_by_index(int(dead_unit_index))
                self.__your_tomb_repository.create_tomb_card(field_unit_id)
                self.__your_field_unit_repository.remove_card_by_index(int(dead_unit_index))

            self.__your_field_unit_repository.replace_field_card_position()

        if opponent_sacrificed_field_unit_index_list:
            for dead_unit_index in opponent_sacrificed_field_unit_index_list:
                field_unit_id = self.__opponent_field_unit_repository.get_opponent_card_id_by_index(int(dead_unit_index))
                self.__opponent_tomb_repository.create_opponent_tomb_card(field_unit_id)
                self.__opponent_field_unit_repository.remove_current_field_unit_card(int(dead_unit_index))

            self.__opponent_field_unit_repository.replace_opponent_field_unit_card_position()

    def search_card(self, notice_dictionary):
        notify_dict_data = notice_dictionary['NOTIFY_USE_SEARCH_DECK_SUPPORT_CARD']

        card_id = (notify_dict_data.get("player_hand_use_map", {})
                   .get("Opponent", {})
                   .get("card_id", None))

        card_kind = (notify_dict_data.get("player_hand_use_map", {})
                     .get("Opponent", {})
                     .get("card_kind", None))

        search_count = (notify_dict_data.get("player_hand_use_map", {})
                        .get("Opponent", None))

        fake_search_list = []
        for count in range(0, search_count):
            fake_search_list.append(-1)

        self.__battle_field_repository.set_current_use_card_id(card_id)

        self.__fake_opponent_hand_repository.save_fake_opponent_hand_list(fake_search_list)

        # self.__opponent_hand_repository.save_current_opponent_hand_state(fake_search_list)

    def damage_to_each_unit_by_basic_attack(self, notice_dictionary):

        is_my_turn = self.__notify_reader_repository.get_is_your_turn_for_check_fake_process()
        print(f"is my turn: {is_my_turn}")
        if is_my_turn is True:
            return

        data = notice_dictionary['NOTIFY_BASIC_ATTACK_TO_UNIT']

        is_opponent_data_in_data = False
        is_your_data_in_data = False


        self.apply_notify_data_of_harmful_status(data['player_field_unit_harmful_effect_map'])


        try:
            dead_opponent_unit_index_list = (
                data.get('player_field_unit_death_map', {})
                .get('Opponent', {})['dead_field_unit_index_list'])

            opponent_unit_index = int(list(
                data.get('player_field_unit_health_point_map', {})
                .get('Opponent', {}).get('field_unit_health_point_map', {}).keys())[0])

            remain_opponent_unit_hp = (
                data.get('player_field_unit_health_point_map', {})
                .get('Opponent', {}).get('field_unit_health_point_map', {})
                .get(str(opponent_unit_index), None))

            is_opponent_data_in_data = True
        except:
            print("opponent data is not in data")

        if is_opponent_data_in_data:

            opponent_field_unit = self.__opponent_field_unit_repository.find_opponent_field_unit_by_index(
                opponent_unit_index)
            opponent_fixed_card_base = opponent_field_unit.get_fixed_card_base()
            opponent_fixed_card_attached_shape_list = opponent_fixed_card_base.get_attached_shapes()

            for opponent_fixed_card_attached_shape in opponent_fixed_card_attached_shape_list:
                if isinstance(opponent_fixed_card_attached_shape, NonBackgroundNumberImage):
                    if opponent_fixed_card_attached_shape.get_circle_kinds() is CircleKinds.HP:
                        print("지정한 상대방 유닛 HP Circle 찾기")

                        if remain_opponent_unit_hp <= 0:
                            break

                        opponent_field_card_id = opponent_field_unit.get_card_number()
                        opponent_field_card_index = opponent_field_unit.get_index()

                        print(f"opponent_hp_number: {remain_opponent_unit_hp}")

                        # TODO: n 턴간 불사 특성을 검사해야하므로 사실 이것도 summary 방식으로 빼는 것이 맞으나 우선은 진행한다.
                        # (지금 당장 불사가 존재하지 않음)

                        print(f"공격 후 opponent unit 체력 -> hp_number: {remain_opponent_unit_hp}")
                        opponent_fixed_card_attached_shape.set_number(remain_opponent_unit_hp)

                        # opponent_fixed_card_attached_shape.set_image_data(
                        #     # TODO: 실제로 여기서 서버로부터 계산 받은 값을 적용해야함
                        #     self.pre_drawed_image_instance.get_pre_draw_number_image(opponent_hp_number))

                        opponent_fixed_card_attached_shape.set_image_data(
                            self.__pre_drawed_image_instance.get_pre_draw_unit_hp(remain_opponent_unit_hp))

            for dead_opponent_unit_index in dead_opponent_unit_index_list:
                opponent_field_card_id = self.__opponent_field_unit_repository.get_opponent_card_id_by_index(
                    dead_opponent_unit_index)

                self.__opponent_field_unit_repository.remove_current_field_unit_card(dead_opponent_unit_index)
                self.__opponent_tomb_repository.create_opponent_tomb_card(opponent_field_card_id)

            self.__opponent_field_unit_repository.replace_opponent_field_unit_card_position()

        try:
            dead_your_unit_index_list = (
                data.get('player_field_unit_death_map', {})
                .get('You', {})['dead_field_unit_index_list'])

            your_unit_index = int(list(
                data.get('player_field_unit_health_point_map', {})
                .get('You', {}).get('field_unit_health_point_map', {}).keys())[0])

            remain_your_unit_hp = (
                data.get('player_field_unit_health_point_map', {})
                .get('You', {}).get('field_unit_health_point_map', {})
                .get(str(your_unit_index), None))
            is_your_data_in_data = True
        except:
            print("your data is not in data")

        if is_your_data_in_data:

            your_field_unit = self.__your_field_unit_repository.find_field_unit_by_index(
                your_unit_index)
            your_fixed_card_base = your_field_unit.get_fixed_card_base()
            your_fixed_card_attached_shape_list = your_fixed_card_base.get_attached_shapes()

            for your_fixed_card_attached_shape in your_fixed_card_attached_shape_list:
                if isinstance(your_fixed_card_attached_shape, NonBackgroundNumberImage):
                    if your_fixed_card_attached_shape.get_circle_kinds() is CircleKinds.HP:

                        if remain_your_unit_hp <= 0:
                            break

                        print(f"공격 후 your unit 체력 -> hp_number: {remain_your_unit_hp}")
                        your_fixed_card_attached_shape.set_number(remain_your_unit_hp)

                        # your_fixed_card_attached_shape.set_image_data(
                        #     # TODO: 실제로 여기서 서버로부터 계산 받은 값을 적용해야함
                        #     self.pre_drawed_image_instance.get_pre_draw_number_image(
                        #         your_hp_number))

                        your_fixed_card_attached_shape.set_image_data(
                            self.__pre_drawed_image_instance.get_pre_draw_unit_hp(
                                remain_your_unit_hp))

            print("your 유닛 hp 갱신 완료")

            for dead_your_unit_index in dead_your_unit_index_list:
                your_field_card_id = self.__your_field_unit_repository.get_card_id_by_index(
                    dead_your_unit_index)
                self.__your_tomb_repository.create_tomb_card(your_field_card_id)
                self.__your_field_unit_repository.remove_card_by_index(dead_your_unit_index)

            self.__your_field_unit_repository.replace_field_card_position()

    def notify_attach_field_energy_card(self, notice_dictionary):

        print(
            f"{Fore.RED}notify_attach_general_energy_card() -> notice_dictionary:{Fore.GREEN} {notice_dictionary}{Style.RESET_ALL}")

        whose_turn = self.__notify_reader_repository.get_is_your_turn_for_check_fake_process()
        print(
            f"{Fore.RED}notify_attach_general_energy_card() -> whose_turn True(Your) or False(Opponent):{Fore.GREEN} {whose_turn}{Style.RESET_ALL}")

        if whose_turn is False:
            # Fake Opponent Attach Energy
            # opponent_field_unit = self.__opponent_field_unit_repository.find_opponent_field_unit_by_index(0)
            # print(f"opponent_field_unit card_id: {opponent_field_unit.get_card_number()}")

            # fake_opponent_field_unit_energy_map = notice_dictionary['NOTIFY_USE_GENERAL_ENERGY_CARD_TO_UNIT']['player_field_unit_energy_map']['Opponent']
            # print(f"{Fore.RED}fake_opponent_field_unit_energy_map:{Fore.GREEN} {fake_opponent_field_unit_energy_map}{Style.RESET_ALL}")
            self.__battle_field_repository.set_current_use_card_id(93)

            remain_opponent_field_energy = \
            notice_dictionary['NOTIFY_USE_FIELD_ENERGY_TO_UNIT']['player_field_energy_map']['Opponent']

            self.__opponent_field_energy_repository.set_opponent_field_energy(remain_opponent_field_energy)
            for unit_index, unit_value in \
                    notice_dictionary['NOTIFY_USE_FIELD_ENERGY_TO_UNIT']['player_field_unit_energy_map']['Opponent'][
                        'field_unit_energy_map'].items():
                print(f"{Fore.RED}opponent_unit_index:{Fore.GREEN} {unit_index}{Style.RESET_ALL}")
                print(f"{Fore.RED}opponent_unit_value:{Fore.GREEN} {unit_value}{Style.RESET_ALL}")

                # opponent_unit_attached_undead_energy_count = unit_value['attached_energy_map']['2']

                for race_energy_number, race_energy_count in unit_value['attached_energy_map'].items():
                    print(f"{Fore.RED}energy_key:{Fore.GREEN} {race_energy_number}{Style.RESET_ALL}")
                    print(f"{Fore.RED}energy_count:{Fore.GREEN} {race_energy_count}{Style.RESET_ALL}")

                    self.__opponent_field_unit_repository.attach_race_energy(int(unit_index), EnergyType.Undead,
                                                                             race_energy_count)

                    opponent_field_unit = self.__opponent_field_unit_repository.find_opponent_field_unit_by_index(
                        int(unit_index))

                    opponent_fixed_card_base = opponent_field_unit.get_fixed_card_base()
                    opponent_fixed_card_attached_shape_list = opponent_fixed_card_base.get_attached_shapes()

                    total_energy_count = unit_value['total_energy_count']
                    print(f"{Fore.RED}total_energy_count:{Fore.GREEN} {total_energy_count}{Style.RESET_ALL}")

                    for opponent_fixed_card_attached_shape in opponent_fixed_card_attached_shape_list:
                        if isinstance(opponent_fixed_card_attached_shape, NonBackgroundNumberImage):
                            if opponent_fixed_card_attached_shape.get_circle_kinds() is CircleKinds.ENERGY:
                                opponent_fixed_card_attached_shape.set_image_data(
                                    self.__pre_drawed_image_instance.get_pre_draw_unit_energy(
                                        total_energy_count))

    def notify_targeting_attack_active_skill_to_main_character(self, notice_dictionary):

        your_character_survival_state = \
        notice_dictionary['NOTIFY_TARGETING_ATTACK_ACTIVE_SKILL_TO_GAME_MAIN_CHARACTER'][
            'player_main_character_survival_map']['You']

        if your_character_survival_state != 'Survival':
            print('죽었습니다!!')
            return

        remain_hp = notice_dictionary['NOTIFY_TARGETING_ATTACK_ACTIVE_SKILL_TO_GAME_MAIN_CHARACTER'][
            'player_main_character_health_point_map']['You']

        self.__your_hp_repository.change_hp(remain_hp)

    def notify_targeting_attack_active_skill_to_your_unit(self, notice_dictionary):

        is_my_turn = self.__notify_reader_repository.get_is_your_turn_for_check_fake_process()
        print(f"is my turn: {is_my_turn}")
        if is_my_turn is True:
            return

        data = notice_dictionary['NOTIFY_TARGETING_ATTACK_ACTIVE_SKILL_TO_UNIT']

        self.apply_notify_data_of_harmful_status(data['player_field_unit_harmful_effect_map'])

        is_your_data_in_data = False

        try:
            dead_your_unit_index_list = (
                data.get('player_field_unit_death_map', {})
                .get('You', {})['dead_field_unit_index_list'])

            your_unit_index = int(list(
                data.get('player_field_unit_health_point_map', {})
                .get('You', {}).get('field_unit_health_point_map', {}).keys())[0])

            remain_your_unit_hp = (
                data.get('player_field_unit_health_point_map', {})
                .get('You', {}).get('field_unit_health_point_map', {})
                .get(str(your_unit_index), None))
            is_your_data_in_data = True
        except:
            print("your data is not in data")

        if is_your_data_in_data:

            your_field_unit = self.__your_field_unit_repository.find_field_unit_by_index(
                your_unit_index)
            your_fixed_card_base = your_field_unit.get_fixed_card_base()
            your_fixed_card_attached_shape_list = your_fixed_card_base.get_attached_shapes()

            for your_fixed_card_attached_shape in your_fixed_card_attached_shape_list:
                if isinstance(your_fixed_card_attached_shape, NonBackgroundNumberImage):
                    if your_fixed_card_attached_shape.get_circle_kinds() is CircleKinds.HP:

                        if remain_your_unit_hp <= 0:
                            break

                        print(f"공격 후 your unit 체력 -> hp_number: {remain_your_unit_hp}")
                        your_fixed_card_attached_shape.set_number(remain_your_unit_hp)

                        # your_fixed_card_attached_shape.set_image_data(
                        #     # TODO: 실제로 여기서 서버로부터 계산 받은 값을 적용해야함
                        #     self.pre_drawed_image_instance.get_pre_draw_number_image(
                        #         your_hp_number))

                        your_fixed_card_attached_shape.set_image_data(
                            self.__pre_drawed_image_instance.get_pre_draw_unit_hp(
                                remain_your_unit_hp))

            print("your 유닛 hp 갱신 완료")

            for dead_your_unit_index in dead_your_unit_index_list:
                your_field_card_id = self.__your_field_unit_repository.get_card_id_by_index(
                    dead_your_unit_index)
                self.__your_tomb_repository.create_tomb_card(your_field_card_id)
                self.__your_field_unit_repository.remove_card_by_index(dead_your_unit_index)

            self.__your_field_unit_repository.replace_field_card_position()

    def notify_non_targeting_active_skill(self, notice_dictionary):

        is_my_turn = self.__notify_reader_repository.get_is_your_turn_for_check_fake_process()
        print(f"is my turn: {is_my_turn}")
        if is_my_turn is True:
            return

        self.apply_notify_data_of_harmful_status(notice_dictionary['NOTIFY_NON_TARGETING_ACTIVE_SKILL']['player_field_unit_harmful_effect_map'])

        for unit_index, remain_hp in \
        notice_dictionary['NOTIFY_NON_TARGETING_ACTIVE_SKILL']['player_field_unit_health_point_map'][
            'You']['field_unit_health_point_map'].items():

            if remain_hp <= 0:
                continue

            your_field_unit = self.__your_field_unit_repository.find_field_unit_by_index(
                int(unit_index))
            your_fixed_card_base = your_field_unit.get_fixed_card_base()
            your_fixed_card_attached_shape_list = your_fixed_card_base.get_attached_shapes()

            for your_fixed_card_attached_shape in your_fixed_card_attached_shape_list:
                if isinstance(your_fixed_card_attached_shape, NonBackgroundNumberImage):
                    if your_fixed_card_attached_shape.get_circle_kinds() is CircleKinds.HP:
                        your_fixed_card_attached_shape.set_number(remain_hp)

                        your_fixed_card_attached_shape.set_image_data(
                            self.__pre_drawed_image_instance.get_pre_draw_unit_hp(
                                remain_hp))

        dead_unit_index_list = \
            notice_dictionary['NOTIFY_NON_TARGETING_ACTIVE_SKILL']['player_field_unit_death_map']['You'][
                'dead_field_unit_index_list']


        for dead_unit_index in dead_unit_index_list:
            field_unit_id = self.__your_field_unit_repository.get_card_id_by_index(
                dead_unit_index)
            self.__your_tomb_repository.create_tomb_card(field_unit_id)
            self.__your_field_unit_repository.remove_card_by_index(dead_unit_index)

        self.__your_field_unit_repository.replace_field_card_position()

    def notify_use_special_energy_card_to_unit(self, notice_dictionary):
        # 일단은 opponent 밖에 없으니 아래와 같이 처리할 수 있음
        data = notice_dictionary['NOTIFY_USE_SPECIAL_ENERGY_CARD_TO_UNIT']

        opponent_usage_card_info = (
            data)['player_hand_use_map']['Opponent']
        opponent_field_unit_energy_map = (
            data)['player_field_unit_energy_map']['Opponent']['field_unit_energy_map']
        opponent_field_unit_extra_effect_map = (
            data)['player_field_unit_extra_effect_map']['Opponent']['field_unit_extra_effect_map']

        # 사용된 카드 묘지로 보냄
        used_card_id = opponent_usage_card_info['card_id']
        self.__opponent_tomb_repository.create_opponent_tomb_card(used_card_id)
        self.__battle_field_repository.set_current_use_card_id(used_card_id)

        for opponent_unit_index, opponent_unit_energy_info in opponent_field_unit_energy_map.items():
            print(f"{Fore.RED}opponent_unit_index:{Fore.GREEN} {opponent_unit_index}{Style.RESET_ALL}")
            print(f"{Fore.RED}opponent_unit_energy_info:{Fore.GREEN} {opponent_unit_energy_info}{Style.RESET_ALL}")

            for race_energy_number, race_energy_count in opponent_unit_energy_info['attached_energy_map'].items():
                extra_effect_list = opponent_field_unit_extra_effect_map[str(opponent_unit_index)]['extra_effect_list']
                print(f"{Fore.RED}race_energy_number:{Fore.GREEN} {race_energy_number}{Style.RESET_ALL}")
                print(f"{Fore.RED}race_energy_count:{Fore.GREEN} {race_energy_count}{Style.RESET_ALL}")
                print(f"{Fore.RED}extra_effect_list:{Fore.GREEN} {extra_effect_list}{Style.RESET_ALL}")

                # if race_energy_number == EnergyType.Undead.value:

                current_opponent_field_unit_race_energy_count = (
                    self.__opponent_field_unit_repository.get_opponent_field_unit_race_energy(
                        int(opponent_unit_index), EnergyType(int(race_energy_number))))
                print(f"{Fore.RED}current_opponent_field_unit_race_energy_count:{Fore.GREEN}"
                      f" {current_opponent_field_unit_race_energy_count}{Style.RESET_ALL}")

                self.__opponent_field_unit_repository.attach_race_energy(
                    int(opponent_unit_index),
                    EnergyType(int(race_energy_number)),
                    (race_energy_count - current_opponent_field_unit_race_energy_count))

                # TODO: String 이 아닌 Enum 으로 처리해야 함
                self.__opponent_field_unit_repository.update_opponent_unit_extra_effect_at_index(
                    int(opponent_unit_index), extra_effect_list)

                opponent_field_unit = (
                    self.__opponent_field_unit_repository.find_opponent_field_unit_by_index(int(opponent_unit_index)))

                opponent_fixed_card_base = opponent_field_unit.get_fixed_card_base()
                opponent_fixed_card_attached_shape_list = opponent_fixed_card_base.get_attached_shapes()

                total_energy_count = opponent_unit_energy_info['total_energy_count']
                print(f"{Fore.RED}total_energy_count:{Fore.GREEN} {total_energy_count}{Style.RESET_ALL}")

                for opponent_fixed_card_attached_shape in opponent_fixed_card_attached_shape_list:
                    if isinstance(opponent_fixed_card_attached_shape, NonBackgroundNumberImage):
                        if opponent_fixed_card_attached_shape.get_circle_kinds() is CircleKinds.ENERGY:
                            opponent_fixed_card_attached_shape.set_image_data(
                                self.__pre_drawed_image_instance.get_pre_draw_unit_energy(
                                    total_energy_count))

                        # TODO: 특수 효과에 맞는 이미지 Setting
                        # if 'DarkFire' in extra_effect_list:
                        #     print("set_image_data: dark_fire")
                        #     opponent_fixed_card_attached_shape.set_image_data(
                        #         self.__pre_drawed_image_instance.get_pre_draw_dark_flame_energy())
                        # if 'Freeze' in extra_effect_list:
                        #     print("set_image_data: freeze")
                        #     opponent_fixed_card_attached_shape.set_image_data(
                        #         self.__pre_drawed_image_instance.get_pre_draw_freezing_energy())



    def apply_notify_data_of_your_field_unit_energy(self, player_field_unit_energy_data):
        data = {"player_field_unit_energy_map": {
                "You": {"field_unit_energy_map": {"0": {"attached_energy_map": {"2": 1}, "total_energy_count": 1}}}}}


        for unit_index, unit_value in \
                player_field_unit_energy_data['You']['field_unit_energy_map'].items():
            print(f"{Fore.RED}your_unit_index:{Fore.GREEN} {unit_index}{Style.RESET_ALL}")
            print(f"{Fore.RED}your_unit_value:{Fore.GREEN} {unit_value}{Style.RESET_ALL}")

            # your_unit_attached_undead_energy_count = unit_value['attached_energy_map']['2']

            for race_energy_number, race_energy_count in unit_value['attached_energy_map'].items():
                print(f"{Fore.RED}energy_key:{Fore.GREEN} {race_energy_number}{Style.RESET_ALL}")
                print(f"{Fore.RED}energy_count:{Fore.GREEN} {race_energy_count}{Style.RESET_ALL}")

                self.__your_field_unit_repository.attach_race_energy(int(unit_index), EnergyType.Undead,
                                                                         race_energy_count)

                your_field_unit = self.__your_field_unit_repository.find_your_field_unit_by_index(
                    int(unit_index))

                your_fixed_card_base = your_field_unit.get_fixed_card_base()
                your_fixed_card_attached_shape_list = your_fixed_card_base.get_attached_shapes()

                total_energy_count = unit_value['total_energy_count']
                print(f"{Fore.RED}total_energy_count:{Fore.GREEN} {total_energy_count}{Style.RESET_ALL}")

                for your_fixed_card_attached_shape in your_fixed_card_attached_shape_list:
                    if isinstance(your_fixed_card_attached_shape, NonBackgroundNumberImage):
                        if your_fixed_card_attached_shape.get_circle_kinds() is CircleKinds.ENERGY:
                            your_fixed_card_attached_shape.set_number(total_energy_count)
                            your_fixed_card_attached_shape.set_image_data(
                                self.__pre_drawed_image_instance.get_pre_draw_unit_energy(
                                    total_energy_count))

    def apply_notify_data_of_opponent_field_unit_energy(self, player_field_unit_energy_data):

        for unit_index, unit_value in \
                player_field_unit_energy_data['Opponent']['field_unit_energy_map'].items():
            print(f"{Fore.RED}opponent_unit_index:{Fore.GREEN} {unit_index}{Style.RESET_ALL}")
            print(f"{Fore.RED}opponent_unit_value:{Fore.GREEN} {unit_value}{Style.RESET_ALL}")

            # opponent_unit_attached_undead_energy_count = unit_value['attached_energy_map']['2']

            for race_energy_number, race_energy_count in unit_value['attached_energy_map'].items():
                print(f"{Fore.RED}energy_key:{Fore.GREEN} {race_energy_number}{Style.RESET_ALL}")
                print(f"{Fore.RED}energy_count:{Fore.GREEN} {race_energy_count}{Style.RESET_ALL}")

                self.__opponent_field_unit_repository.attach_race_energy(int(unit_index), EnergyType.Undead,
                                                                         race_energy_count)

                opponent_field_unit = self.__opponent_field_unit_repository.find_opponent_field_unit_by_index(
                    int(unit_index))

                opponent_fixed_card_base = opponent_field_unit.get_fixed_card_base()
                opponent_fixed_card_attached_shape_list = opponent_fixed_card_base.get_attached_shapes()

                total_energy_count = unit_value['total_energy_count']
                print(f"{Fore.RED}total_energy_count:{Fore.GREEN} {total_energy_count}{Style.RESET_ALL}")

                for opponent_fixed_card_attached_shape in opponent_fixed_card_attached_shape_list:
                    if isinstance(opponent_fixed_card_attached_shape, NonBackgroundNumberImage):
                        if opponent_fixed_card_attached_shape.get_circle_kinds() is CircleKinds.ENERGY:
                            opponent_fixed_card_attached_shape.set_number(total_energy_count)
                            opponent_fixed_card_attached_shape.set_image_data(
                                self.__pre_drawed_image_instance.get_pre_draw_unit_energy(
                                    total_energy_count))

    def apply_notify_data_of_field_unit_hp(self, player_field_unit_health_point_data):
        data = {
            "player_field_unit_health_point_map": {"You": {"field_unit_health_point_map": {"0": 0}},
                                                   "Opponent": {"field_unit_health_point_map": {"0": 15}}}}

        try:
            for your_unit_index, your_unit_remain_hp in player_field_unit_health_point_data['You']['field_unit_health_point_map'].items():
                if your_unit_remain_hp <= 0:
                    continue

                your_field_unit = self.__your_field_unit_repository.find_field_unit_by_index(
                    your_unit_index)
                your_fixed_card_base = your_field_unit.get_fixed_card_base()
                your_fixed_card_attached_shape_list = your_fixed_card_base.get_attached_shapes()

                for your_fixed_card_attached_shape in your_fixed_card_attached_shape_list:
                    if isinstance(your_fixed_card_attached_shape, NonBackgroundNumberImage):
                        if your_fixed_card_attached_shape.get_circle_kinds() is CircleKinds.HP:

                            your_fixed_card_attached_shape.set_number(your_unit_remain_hp)

                            your_fixed_card_attached_shape.set_image_data(
                                self.__pre_drawed_image_instance.get_pre_draw_unit_hp(
                                    your_unit_remain_hp))
        except Exception as e:
            print('no Your field unit data!! : ', e)

        try:
            for opponent_unit_index, opponent_unit_remain_hp in player_field_unit_health_point_data['Opponent']['field_unit_health_point_map'].items():

                if opponent_unit_remain_hp <= 0:
                    continue

                opponent_field_unit = (
                    self.__opponent_field_unit_repository.find_opponent_field_unit_by_index(int(opponent_unit_index)))

                opponent_fixed_card_base = opponent_field_unit.get_fixed_card_base()
                opponent_fixed_card_attached_shape_list = opponent_fixed_card_base.get_attached_shapes()

                for opponent_fixed_card_attached_shape in opponent_fixed_card_attached_shape_list:
                    if isinstance(opponent_fixed_card_attached_shape, NonBackgroundNumberImage):
                        if opponent_fixed_card_attached_shape.get_circle_kinds() is CircleKinds.HP:

                            opponent_fixed_card_attached_shape.set_number(opponent_unit_remain_hp)

                            opponent_fixed_card_attached_shape.set_image_data(
                                self.__pre_drawed_image_instance.get_pre_draw_unit_energy(
                                    opponent_unit_remain_hp))

        except Exception as e:
            print('no Opponent field unit data!! : ', e)

    def apply_notify_data_of_dead_unit(self, player_field_unit_death_data):
        data = {
            "player_field_unit_death_map": {"You": {"dead_field_unit_index_list": [0]},
                                            "Opponent": {"dead_field_unit_index_list": []}}}

        try:
            for your_unit_index in player_field_unit_death_data['You']['dead_field_unit_index_list']:
                card_id = self.__your_field_unit_repository.get_card_id_by_index(your_unit_index)
                self.__your_tomb_repository.create_tomb_card(card_id)
                self.__your_field_unit_repository.remove_card_by_index(your_unit_index)

            self.__your_field_unit_repository.replace_field_card_position()
        except Exception as e:
            print('no Your dead unit data!! ', e)

        try:
            for opponent_unit_index in player_field_unit_death_data['Opponent']['dead_field_unit_index_list']:
                card_id = self.__opponent_field_unit_repository.get_opponent_card_id_by_index(opponent_unit_index)
                self.__opponent_tomb_repository.create_opponent_tomb_card(opponent_unit_index)
                self.__opponent_field_unit_repository.remove_current_field_unit_card(opponent_unit_index)

            self.__opponent_field_unit_repository.replace_opponent_field_unit_card_position()
        except Exception as e:
            print('no Opponent dead unit data!! ', e)

    def apply_notify_data_of_harmful_status(self, player_field_unit_harmful_effect_data):

        try:
            for player, field_data in player_field_unit_harmful_effect_data.items():
                for unit_index, harmful_status_value in field_data.get('field_unit_harmful_status_map', {}).items():
                    harmful_status_list = harmful_status_value.get('harmful_status_list', [])
                    if len(harmful_status_list) == 0:
                        continue

                    if player == 'Opponent':
                        self.__opponent_field_unit_repository.apply_harmful_status(int(unit_index), harmful_status_list)
                    elif player == 'You':
                        self.__your_field_unit_repository.apply_harmful_status(int(unit_index), harmful_status_list)
        except Exception as e:
            print('An error occurred while applying harmful status data:', e)


        # try:
        #     for opponent_unit_index, harmful_status_value in player_field_unit_harmful_effect_data['Opponent']['field_unit_harmful_status_map'].items():
        #         harmful_status_list = harmful_status_value['harmful_status_list']
        #         if len(harmful_status_list) == 0:
        #             continue
        #
        #         self.__opponent_field_unit_repository.apply_harmful_status(int(opponent_unit_index), harmful_status_list)
        # except Exception as e:
        #     print('no Opponent harmful status data!! ', e)
        #
        #
        #
        # try:
        #     for your_unit_index, harmful_status_value in player_field_unit_harmful_effect_data['You'][
        #         'field_unit_harmful_status_map'].items():
        #         harmful_status_list = harmful_status_value['harmful_status_list']
        #         if len(harmful_status_list) == 0:
        #             continue
        #
        #         self.__your_field_unit_repository.apply_harmful_status(int(your_unit_index), harmful_status_list)
        # except Exception as e:
        #     print('no your harmful status data!! ', e)


    def apply_notify_data_of_field_energy(self, player_field_energy_data):
        try:
            your_energy_count =  player_field_energy_data['You']
            self.__your_field_energy_repository.set_your_field_energy(your_energy_count)
        except Exception as e:
            print('no your field energy data!! ', e)

        try:
            opponent_energy_count = player_field_energy_data['Opponent']
            self.__opponent_field_energy_repository.set_opponent_field_energy(opponent_energy_count)
        except Exception as e:
            print('no opponent field energy data!! ', e)

    def notify_use_draw_support_card(self, notice_dictionary):
        # 일단은 opponent 밖에 없으니 아래와 같이 처리할 수 있음
        data = notice_dictionary['NOTIFY_USE_DRAW_SUPPORT_CARD']

        opponent_usage_card_info = (
            data)['player_hand_use_map']['Opponent']
        opponent_draw_count = (
            data)['player_draw_count_map']['Opponent']

        # 사용된 카드 묘지로 보냄
        used_card_id = opponent_usage_card_info['card_id']
        self.__opponent_tomb_repository.create_opponent_tomb_card(used_card_id)
        self.__battle_field_repository.set_current_use_card_id(used_card_id)

        # 뒷면 카드 3장 추가
        unknown_hand_list = []
        for count in range(opponent_draw_count):
            unknown_hand_list.append(-1)

        current_opponent_hand = self.__opponent_hand_repository.get_current_opponent_hand_state()
        print(f"current_opponent_hand: {current_opponent_hand}")
        self.__opponent_hand_repository.save_current_opponent_hand_state(unknown_hand_list)

        updated_opponent_hand = self.__opponent_hand_repository.get_current_opponent_hand_state()
        print(f"updated_opponent_hand: {updated_opponent_hand}")

        # TODO: 상대 핸드 뒷면 이미지를 추가된 카드 장수 만큼 띄워야 함

    def notify_mulligan_end(self, notice_dictionary):
        is_mulligan_done = notice_dictionary['NOTIFY_MULLIGAN_END'].get('is_done')

        print(f"{Fore.RED}mulligan end?:{Fore.GREEN} {is_mulligan_done}{Style.RESET_ALL}")

        if is_mulligan_done is True:
            self.__mulligan_repository.set_is_mulligan_done(True)

    def notify_use_catastrophic_damage_item_card(self, notice_dictionary):
        data = notice_dictionary['NOTIFY_USE_CATASTROPHIC_DAMAGE_ITEM_CARD']

        opponent_usage_card_info = (
            data)['player_hand_use_map']['Opponent']
        your_field_unit_health_point_map = (
            data)['player_field_unit_health_point_map']['You']['field_unit_health_point_map']
        your_dead_field_unit_index_list = (
            data)['player_field_unit_death_map']['You']['dead_field_unit_index_list']
        your_main_character_health_point = (
            data)['player_main_character_health_point_map']['You']
        your_main_character_survival_state = (
            data)['player_main_character_survival_map']['You']
        your_deck_card_lost_list = (
            data)['player_deck_card_lost_list_map']['You']

        # 사용된 카드 묘지로 보냄
        used_card_id = opponent_usage_card_info['card_id']
        self.__opponent_tomb_repository.create_opponent_tomb_card(used_card_id)
        self.__battle_field_repository.set_current_use_card_id(used_card_id)

        # 체력 정보 Update
        for unit_index, remaining_health_point in your_field_unit_health_point_map.items():
            your_field_unit = self.__your_field_unit_repository.find_field_unit_by_index(int(unit_index))
            your_fixed_card_base = your_field_unit.get_fixed_card_base()
            your_fixed_card_attached_shape_list = your_fixed_card_base.get_attached_shapes()

            if remaining_health_point <= 0:
                continue

            for your_fixed_card_attached_shape in your_fixed_card_attached_shape_list:
                if isinstance(your_fixed_card_attached_shape, NonBackgroundNumberImage):
                    if your_fixed_card_attached_shape.get_circle_kinds() is CircleKinds.HP:
                        your_fixed_card_attached_shape.set_number(int(remaining_health_point))

                        your_fixed_card_attached_shape.set_image_data(
                            self.__pre_drawed_image_instance.get_pre_draw_unit_hp(int(remaining_health_point)))

        # 죽은 유닛들 묘지에 배치 및 Replacing
        for dead_unit_index in your_dead_field_unit_index_list:
            field_unit_id = self.__your_field_unit_repository.get_card_id_by_index(int(dead_unit_index))
            self.__your_tomb_repository.create_tomb_card(field_unit_id)
            self.__your_field_unit_repository.remove_card_by_index(int(dead_unit_index))

        self.__your_field_unit_repository.replace_field_card_position()

        # 메인 캐릭터 상태 확인 및 체력 Update
        if your_main_character_survival_state != 'Survival':
            print("Player who get notice is dead.")
            # TODO: 배틀 정리 요청을 띄우는 화면으로 넘어가야 함

        self.__your_hp_repository.change_hp(your_main_character_health_point)
        print(f"{Fore.RED}current_main_character_health:{Fore.GREEN} "
              f"{self.__your_hp_repository.get_current_your_hp_state().get_current_health()}{Style.RESET_ALL}")

        # 덱 위에서 카드 한 장 뽑아서 로스트 존 보내기
        for lost_card_id in your_deck_card_lost_list:
            self.__your_deck_repository.draw_deck()
            print(f"{Fore.RED}current_deck: {Fore.GREEN}"
                  f"{self.__your_deck_repository.get_current_deck_state()}{Style.RESET_ALL}")
            self.__your_lost_zone_repository.create_your_lost_zone_card(int(lost_card_id))
            print(f"{Fore.RED}current_lost_zone: {Fore.GREEN}"
                  f"{self.__your_lost_zone_repository.get_your_lost_zone_state()}{Style.RESET_ALL}")

    def notify_use_unit_energy_boost_support(self, notice_dictionary):
        # 수신된 정보를 대입
        data = notice_dictionary['NOTIFY_USE_UNIT_ENERGY_BOOST_SUPPORT_CARD']
        for key in data['player_hand_use_map']:
            player_who_use_card = key
            usage_card_deck_list_map = (
                data)['player_deck_card_use_list_map'][player_who_use_card]
            field_unit_energy_map = (
                data)['player_field_unit_energy_map'][player_who_use_card]['field_unit_energy_map']

            # 카드를 사용 하고, 묘지로 보냄
            for used_card_id in usage_card_deck_list_map:
                print(f"{Fore.RED}used_card_id:{Fore.GREEN} {used_card_id}{Style.RESET_ALL}")
                if player_who_use_card == "Opponent":
                    self.__opponent_tomb_repository.create_opponent_tomb_card(used_card_id)
                elif player_who_use_card == "You":
                    self.__your_tomb_repository.create_tomb_card(used_card_id)
                self.__battle_field_repository.set_current_use_card_id(used_card_id)

            # 필드 유닛 에너지 정보 호출
            for unit_index, unit_value in \
                    notice_dictionary['NOTIFY_USE_UNIT_ENERGY_BOOST_SUPPORT_CARD']['player_field_unit_energy_map'][player_who_use_card][
                        'field_unit_energy_map'].items():
                print(f"{Fore.RED}opponent_unit_index:{Fore.GREEN} {unit_index}{Style.RESET_ALL}")
                print(f"{Fore.RED}opponent_unit_value:{Fore.GREEN} {unit_value}{Style.RESET_ALL}")

                for race_energy_number, race_energy_count in unit_value['attached_energy_map'].items():
                    print(f"{Fore.RED}energy_key:{Fore.GREEN} {race_energy_number}{Style.RESET_ALL}")
                    print(f"{Fore.RED}energy_count:{Fore.GREEN} {race_energy_count}{Style.RESET_ALL}")

                    # 에너지 붙임
                    if player_who_use_card == "Opponent":
                        self.__opponent_field_unit_repository.attach_race_energy(int(unit_index), EnergyType.Undead, race_energy_count)
                    elif player_who_use_card == "You":
                        self.__your_field_unit_repository.attach_race_energy(int(unit_index), EnergyType.Undead,race_energy_count)

                     # 필드 유닛 에너지 정보 갱신
                    for field_unit_index, field_unit_energy_info in field_unit_energy_map.items():
                        print(f"{Fore.RED}field_unit_index:{Fore.GREEN} {field_unit_index}{Style.RESET_ALL}")
                        print(f"{Fore.RED}field_unit_energy_info:{Fore.GREEN} {field_unit_energy_info}{Style.RESET_ALL}")

                        if player_who_use_card == "Opponent":
                            current_opponent_field_unit_race_energy_count = (
                                self.__opponent_field_unit_repository.get_opponent_field_unit_race_energy(
                                    int(field_unit_index), int(race_energy_number)))
                            print(f"{Fore.RED}current_opponent_field_unit_race_energy_count:{Fore.GREEN}"
                                  f" {current_opponent_field_unit_race_energy_count}{Style.RESET_ALL}")

                            opponent_field_unit = (
                                self.__opponent_field_unit_repository.find_opponent_field_unit_by_index(int(field_unit_index)))
                            print(f"opponent_field_unit:{opponent_field_unit}")

                            opponent_fixed_card_base = opponent_field_unit.get_fixed_card_base()
                            opponent_fixed_card_attached_shape_list = opponent_fixed_card_base.get_attached_shapes()

                            total_energy_count = field_unit_energy_info['total_energy_count']
                            print(f"{Fore.RED}total_energy_count:{Fore.GREEN} {total_energy_count}{Style.RESET_ALL}")

                            for opponent_fixed_card_attached_shape in opponent_fixed_card_attached_shape_list:
                                if isinstance(opponent_fixed_card_attached_shape, NonBackgroundNumberImage):
                                    if opponent_fixed_card_attached_shape.get_circle_kinds() is CircleKinds.ENERGY:
                                        opponent_fixed_card_attached_shape.set_image_data(
                                            self.__pre_drawed_image_instance.get_pre_draw_unit_energy(
                                                total_energy_count))

                        elif player_who_use_card == "You":
                            current_your_field_unit_race_energy_count = (
                                self.__your_field_unit_repository.get_your_field_unit_race_energy(
                                    int(field_unit_index), int(race_energy_number)))
                            print(f"{Fore.RED}current_your_field_unit_race_energy_count:{Fore.GREEN}"
                                  f" {current_your_field_unit_race_energy_count}{Style.RESET_ALL}")

                            your_field_unit = (
                                self.__your_field_unit_repository.find_field_unit_by_index(int(field_unit_index)))

                            your_fixed_card_base = your_field_unit.get_fixed_card_base()
                            your_fixed_card_attached_shape_list = your_fixed_card_base.get_attached_shapes()

                            total_energy_count = field_unit_energy_info['total_energy_count']
                            print(f"{Fore.RED}total_energy_count:{Fore.GREEN} {total_energy_count}{Style.RESET_ALL}")

                            for your_fixed_card_attached_shape in your_fixed_card_attached_shape_list:
                                if isinstance(your_fixed_card_attached_shape, NonBackgroundNumberImage):
                                    if your_fixed_card_attached_shape.get_circle_kinds() is CircleKinds.ENERGY:
                                        your_fixed_card_attached_shape.set_image_data(
                                            self.__pre_drawed_image_instance.get_pre_draw_unit_energy(
                                                total_energy_count))

    def notify_turn_start_targeting_attack_passive_skill_to_unit(self, notice_dictionary):
        data = notice_dictionary['NOTIFY_TURN_START_TARGETING_ATTACK_PASSIVE_SKILL_TO_UNIT']

        your_field_unit_health_point_map = (
            data)['player_field_unit_health_point_map']['You']['field_unit_health_point_map']
        your_field_unit_harmful_effect_list = (
            data)['player_field_unit_harmful_effect_map']['You']['field_unit_harmful_status_map']
        your_dead_field_unit_index_list = (
            data)['player_field_unit_death_map']['You']['dead_field_unit_index_list']

        for unit_index, remaining_health_point in your_field_unit_health_point_map.items():
            your_field_unit = self.__your_field_unit_repository.find_field_unit_by_index(int(unit_index))
            your_fixed_card_base = your_field_unit.get_fixed_card_base()
            your_fixed_card_attached_shape_list = your_fixed_card_base.get_attached_shapes()

            if remaining_health_point <= 0:
                continue

            for your_fixed_card_attached_shape in your_fixed_card_attached_shape_list:
                if isinstance(your_fixed_card_attached_shape, NonBackgroundNumberImage):
                    if your_fixed_card_attached_shape.get_circle_kinds() is CircleKinds.HP:
                        your_fixed_card_attached_shape.set_number(int(remaining_health_point))

                        your_fixed_card_attached_shape.set_image_data(
                            self.__pre_drawed_image_instance.get_pre_draw_unit_hp(int(remaining_health_point)))

        for unit_index, harmful_effect_info in your_field_unit_harmful_effect_list.items():
            harmful_effect_list = harmful_effect_info['harmful_status_list']
            self.__your_field_unit_repository.apply_harmful_status(int(unit_index), harmful_effect_list)

        # 죽은 유닛들 묘지에 배치 및 Replacing
        for dead_unit_index in your_dead_field_unit_index_list:
            field_unit_id = self.__your_field_unit_repository.get_card_id_by_index(int(dead_unit_index))
            self.__your_tomb_repository.create_tomb_card(field_unit_id)
            self.__your_field_unit_repository.remove_card_by_index(int(dead_unit_index))

        self.__your_field_unit_repository.replace_field_card_position()

    def notify_deploy_targeting_attack_passive_skill_to_unit(self, notice_dictionary):
        data = notice_dictionary['NOTIFY_DEPLOY_TARGETING_ATTACK_PASSIVE_SKILL_TO_UNIT']

        your_field_unit_health_point_map = (
            data)['player_field_unit_health_point_map']['You']['field_unit_health_point_map']
        your_field_unit_harmful_effect_list = (
            data)['player_field_unit_harmful_effect_map']['You']['field_unit_harmful_status_map']
        your_dead_field_unit_index_list = (
            data)['player_field_unit_death_map']['You']['dead_field_unit_index_list']

        for unit_index, remaining_health_point in your_field_unit_health_point_map.items():
            your_field_unit = self.__your_field_unit_repository.find_field_unit_by_index(int(unit_index))
            your_fixed_card_base = your_field_unit.get_fixed_card_base()
            your_fixed_card_attached_shape_list = your_fixed_card_base.get_attached_shapes()

            if remaining_health_point <= 0:
                continue

            for your_fixed_card_attached_shape in your_fixed_card_attached_shape_list:
                if isinstance(your_fixed_card_attached_shape, NonBackgroundNumberImage):
                    if your_fixed_card_attached_shape.get_circle_kinds() is CircleKinds.HP:
                        your_fixed_card_attached_shape.set_number(int(remaining_health_point))

                        your_fixed_card_attached_shape.set_image_data(
                            self.__pre_drawed_image_instance.get_pre_draw_unit_hp(int(remaining_health_point)))

        for unit_index, harmful_effect_info in your_field_unit_harmful_effect_list.items():
            harmful_effect_list = harmful_effect_info['harmful_status_list']
            self.__your_field_unit_repository.apply_harmful_status(int(unit_index), harmful_effect_list)

        # 죽은 유닛들 묘지에 배치 및 Replacing
        for dead_unit_index in your_dead_field_unit_index_list:
            field_unit_id = self.__your_field_unit_repository.get_card_id_by_index(int(dead_unit_index))
            self.__your_tomb_repository.create_tomb_card(field_unit_id)
            self.__your_field_unit_repository.remove_card_by_index(int(dead_unit_index))

        self.__your_field_unit_repository.replace_field_card_position()

    def notify_turn_start_non_targeting_attack_passive_skill(self, notice_dictionary):
        data = notice_dictionary['NOTIFY_TURN_START_NON_TARGETING_ATTACK_PASSIVE_SKILL']

        your_field_unit_health_point_map = (
            data)['player_field_unit_health_point_map']['You']['field_unit_health_point_map']
        your_field_unit_harmful_effect_list = (
            data)['player_field_unit_harmful_effect_map']['You']['field_unit_harmful_status_map']
        your_dead_field_unit_index_list = (
            data)['player_field_unit_death_map']['You']['dead_field_unit_index_list']

        for unit_index, remaining_health_point in your_field_unit_health_point_map.items():
            your_field_unit = self.__your_field_unit_repository.find_field_unit_by_index(int(unit_index))
            your_fixed_card_base = your_field_unit.get_fixed_card_base()
            your_fixed_card_attached_shape_list = your_fixed_card_base.get_attached_shapes()

            if remaining_health_point <= 0:
                continue

            for your_fixed_card_attached_shape in your_fixed_card_attached_shape_list:
                if isinstance(your_fixed_card_attached_shape, NonBackgroundNumberImage):
                    if your_fixed_card_attached_shape.get_circle_kinds() is CircleKinds.HP:
                        your_fixed_card_attached_shape.set_number(int(remaining_health_point))

                        your_fixed_card_attached_shape.set_image_data(
                            self.__pre_drawed_image_instance.get_pre_draw_unit_hp(int(remaining_health_point)))

        for unit_index, harmful_effect_info in your_field_unit_harmful_effect_list.items():
            harmful_effect_list = harmful_effect_info['harmful_status_list']
            self.__your_field_unit_repository.apply_harmful_status(int(unit_index), harmful_effect_list)

        # 죽은 유닛들 묘지에 배치 및 Replacing
        for dead_unit_index in your_dead_field_unit_index_list:
            field_unit_id = self.__your_field_unit_repository.get_card_id_by_index(int(dead_unit_index))
            self.__your_tomb_repository.create_tomb_card(field_unit_id)
            self.__your_field_unit_repository.remove_card_by_index(int(dead_unit_index))

        self.__your_field_unit_repository.replace_field_card_position()

    def notify_deploy_non_targeting_attack_passive_skill(self, notice_dictionary):
        data = notice_dictionary['NOTIFY_DEPLOY_NON_TARGETING_ATTACK_PASSIVE_SKILL']

        your_field_unit_health_point_map = (
            data)['player_field_unit_health_point_map']['You']['field_unit_health_point_map']
        your_field_unit_harmful_effect_list = (
            data)['player_field_unit_harmful_effect_map']['You']['field_unit_harmful_status_map']
        your_dead_field_unit_index_list = (
            data)['player_field_unit_death_map']['You']['dead_field_unit_index_list']

        for unit_index, remaining_health_point in your_field_unit_health_point_map.items():
            your_field_unit = self.__your_field_unit_repository.find_field_unit_by_index(int(unit_index))
            your_fixed_card_base = your_field_unit.get_fixed_card_base()
            your_fixed_card_attached_shape_list = your_fixed_card_base.get_attached_shapes()

            if remaining_health_point <= 0:
                continue

            for your_fixed_card_attached_shape in your_fixed_card_attached_shape_list:
                if isinstance(your_fixed_card_attached_shape, NonBackgroundNumberImage):
                    if your_fixed_card_attached_shape.get_circle_kinds() is CircleKinds.HP:
                        your_fixed_card_attached_shape.set_number(int(remaining_health_point))

                        your_fixed_card_attached_shape.set_image_data(
                            self.__pre_drawed_image_instance.get_pre_draw_unit_hp(int(remaining_health_point)))

        for unit_index, harmful_effect_info in your_field_unit_harmful_effect_list.items():
            harmful_effect_list = harmful_effect_info['harmful_status_list']
            self.__your_field_unit_repository.apply_harmful_status(int(unit_index), harmful_effect_list)

        # 죽은 유닛들 묘지에 배치 및 Replacing
        for dead_unit_index in your_dead_field_unit_index_list:
            field_unit_id = self.__your_field_unit_repository.get_card_id_by_index(int(dead_unit_index))
            self.__your_tomb_repository.create_tomb_card(field_unit_id)
            self.__your_field_unit_repository.remove_card_by_index(int(dead_unit_index))

        self.__your_field_unit_repository.replace_field_card_position()