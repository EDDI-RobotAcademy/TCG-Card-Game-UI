import json

from colorama import Fore, Style

from battle_field.infra.opponent_field_energy_repository import OpponentFieldEnergyRepository
from battle_field.infra.opponent_field_unit_repository import OpponentFieldUnitRepository
from battle_field.infra.opponent_tomb_repository import OpponentTombRepository
from battle_field.infra.your_field_energy_repository import YourFieldEnergyRepository
from battle_field.infra.your_field_unit_repository import YourFieldUnitRepository
from battle_field.infra.your_hand_repository import YourHandRepository
from battle_field.infra.your_hp_repository import YourHpRepository
from battle_field.infra.your_tomb_repository import YourTombRepository
from battle_field.state.energy_type import EnergyType
from battle_field_function.service.battle_field_function_service_impl import BattleFieldFunctionServiceImpl
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

            cls.__instance.notify_callback_table['NOTIFY_DEPLOY_UNIT'] = cls.__instance.notify_deploy_unit
            cls.__instance.notify_callback_table['NOTIFY_TURN_END'] = cls.__instance.notify_turn_end
            cls.__instance.notify_callback_table['NOTIFY_USE_GENERAL_ENERGY_CARD_TO_UNIT'] = cls.__instance.notify_attach_general_energy_card
            # cls.__instance.notify_callback_table['NOTIFY_USE_GENERAL_ENERGY_CARD_TO_UNIT'] = (
            #     cls.__instance.__battle_field_function_service.useGeneralEnergyCardToUnit)
            cls.__instance.notify_callback_table['NOTIFY_USE_SPECIAL_ENERGY_CARD_TO_UNIT'] = (
                cls.__instance.__battle_field_function_service.useSpecialEnergyCardToUnit)
            cls.__instance.notify_callback_table['NOTIFY_USE_UNIT_ENERGY_REMOVE_ITEM_CARD'] = (
                cls.__instance.__battle_field_function_service.useUnitEnergyRemoveItemCard)
            cls.__instance.notify_callback_table['NOTIFY_BASIC_ATTACK_TO_MAIN_CHARACTER'] = cls.__instance.damage_to_main_character
            # cls.__instance.notify_callback_table['NOTIFY_USE_MULTIPLE_UNIT_DAMAGE_ITEM_CARD'] = cls.__instance.damage_to_multiple_unit
            cls.__instance.notify_callback_table['NOTIFY_USE_MULTIPLE_UNIT_DAMAGE_ITEM_CARD'] = (
                cls.__instance.__battle_field_function_service.useMultipleUnitDamageItemCard)

            cls.__instance.notify_callback_table['NOTIFY_BASIC_ATTACK_TO_UNIT'] = cls.__instance.damage_to_each_unit_by_basic_attack

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
        self.__notify_reader_repository.registerFunctionWithNoticeName(NoticeType.NOTIFY_HAND_CARD_USE.name, hand_card_use_function)

    def saveDrawCountFunction(self, draw_count_function):
        print(f"saveDrawCountFunction: {draw_count_function}")
        self.__notify_reader_repository.registerFunctionWithNoticeName(NoticeType.NOTIFY_DRAW_COUNT.name, draw_count_function)

    def saveDrawnCardListFunction(self, drawn_card_list_function):
        print(f"saveDrawnCardListFunction: {drawn_card_list_function}")
        self.__notify_reader_repository.registerFunctionWithNoticeName(NoticeType.NOTIFY_DRAWN_CARD_LIST.name, drawn_card_list_function)


    def saveDeckCardUseListFunction(self, deck_card_list_use_function):
        print(f"saveDeckCardListUseFunction: {deck_card_list_use_function}")
        self.__notify_reader_repository.registerFunctionWithNoticeName(NoticeType.NOTIFY_DECK_CARD_LIST_USE.name, deck_card_list_use_function)

    def saveFieldUnitEnergyFunction(self, field_unit_energy_function):
        print(f"saveFieldUnitEnergy: {field_unit_energy_function}")
        self.__notify_reader_repository.registerFunctionWithNoticeName(NoticeType.NOTIFY_FIELD_UNIT_ENERGY.name, field_unit_energy_function)

    def saveSearchCountFunction(self, search_count_function):
        print(f"saveSearchCount: {search_count_function}")
        self.__notify_reader_repository.registerFunctionWithNoticeName(NoticeType.NOTIFY_SEARCH_COUNT.name, search_count_function)

    def saveSearchCardListFunction(self, search_card_list_function):
        print(f"saveSearchCardListFunction: {search_card_list_function}")
        self.__notify_reader_repository.registerFunctionWithNoticeName(NoticeType.NOTIFY_SEARCH_CARD_LIST.name, search_card_list_function)


    def saveSpawnUnitFunction(self, spawn_unit_function):
        self.__notify_reader_repository.registerFunctionWithNoticeName(NoticeType.NOTIFY_UNIT_SPAWN.name, spawn_unit_function)

    def readNoticeAndCallFunction(self):
        #while True:
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
        print(f"{Fore.RED}notify_deploy_unit() -> whose_turn True(Your) or False(Opponent):{Fore.GREEN} {whose_turn}{Style.RESET_ALL}")

        if whose_turn is True:
            # self.__notify_reader_repository.set_is_your_turn_for_check_fake_process(not whose_turn)
            # print(f"after set whose_turn: {self.__notify_reader_repository.get_is_your_turn_for_check_fake_process()}")
            return

        card_id = (notice_dictionary.get('NOTIFY_DEPLOY_UNIT', {})
                   .get('player_hand_use_map', {})
                   .get('Opponent',{})
                   .get('card_id', None))

        print(f"{Fore.RED}notify_deploy_unit() -> Opponent deploy card_id:{Fore.GREEN} {card_id}{Style.RESET_ALL}")

        self.__opponent_field_unit_repository.create_field_unit_card(card_id)

    def notify_turn_end(self, notice_dictionary):
        print(f"{Fore.RED}notify_turn_end() -> notice_dictionary:{Fore.GREEN} {notice_dictionary}{Style.RESET_ALL}")

        whose_turn = self.__notify_reader_repository.get_is_your_turn_for_check_fake_process()
        print(f"{Fore.RED}notify_turn_end() -> whose_turn True(Your) or False(Opponent):{Fore.GREEN} {whose_turn}{Style.RESET_ALL}")

        if whose_turn is False:
            # Fake Opponent Draw
            opponent_drawn_card_list = notice_dictionary['NOTIFY_TURN_END']['player_drawn_card_list_map'].get('You', [])
            self.__fake_opponent_hand_repository.save_fake_opponent_hand_list(opponent_drawn_card_list)
            fake_opponent_hand_list = self.__fake_opponent_hand_repository.get_fake_opponent_hand_list()
            print(f"{Fore.RED}notify_turn_end() -> fake opponent hand list:{Fore.GREEN} {fake_opponent_hand_list}{Style.RESET_ALL}")

            fake_opponent_field_energy = notice_dictionary['NOTIFY_TURN_END']['player_field_energy_map'].get('You', [])
            self.__opponent_field_energy_repository.set_opponent_field_energy(fake_opponent_field_energy)
            print(f"{Fore.RED}notify_turn_end() -> fake opponent_field_energy:{Fore.GREEN} {fake_opponent_field_energy}{Style.RESET_ALL}")

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
        print(f"{Fore.RED}notify_attach_general_energy_card() -> notice_dictionary:{Fore.GREEN} {notice_dictionary}{Style.RESET_ALL}")

        whose_turn = self.__notify_reader_repository.get_is_your_turn_for_check_fake_process()
        print(f"{Fore.RED}notify_attach_general_energy_card() -> whose_turn True(Your) or False(Opponent):{Fore.GREEN} {whose_turn}{Style.RESET_ALL}")

        if whose_turn is False:
            # Fake Opponent Attach Energy
            # opponent_field_unit = self.__opponent_field_unit_repository.find_opponent_field_unit_by_index(0)
            # print(f"opponent_field_unit card_id: {opponent_field_unit.get_card_number()}")

            # fake_opponent_field_unit_energy_map = notice_dictionary['NOTIFY_USE_GENERAL_ENERGY_CARD_TO_UNIT']['player_field_unit_energy_map']['Opponent']
            # print(f"{Fore.RED}fake_opponent_field_unit_energy_map:{Fore.GREEN} {fake_opponent_field_unit_energy_map}{Style.RESET_ALL}")

            for unit_index, unit_value in notice_dictionary['NOTIFY_USE_GENERAL_ENERGY_CARD_TO_UNIT']['player_field_unit_energy_map']['Opponent']['field_unit_energy_map'].items():
                print(f"{Fore.RED}opponent_unit_index:{Fore.GREEN} {unit_index}{Style.RESET_ALL}")
                print(f"{Fore.RED}opponent_unit_value:{Fore.GREEN} {unit_value}{Style.RESET_ALL}")

                # opponent_unit_attached_undead_energy_count = unit_value['attached_energy_map']['2']

                for race_energy_number, race_energy_count in unit_value['attached_energy_map'].items():
                    print(f"{Fore.RED}energy_key:{Fore.GREEN} {race_energy_number}{Style.RESET_ALL}")
                    print(f"{Fore.RED}energy_count:{Fore.GREEN} {race_energy_count}{Style.RESET_ALL}")

                    self.__opponent_field_unit_repository.attach_race_energy(int(unit_index), EnergyType.Undead, race_energy_count)

                    opponent_field_unit = self.__opponent_field_unit_repository.find_opponent_field_unit_by_index(int(unit_index))

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

    def damage_to_multiple_unit(self, notice_dictionary):
        notify_dict_data = notice_dictionary['NOTIFY_USE_MULTIPLE_UNIT_DAMAGE_ITEM_CARD']

    def damage_to_each_unit_by_basic_attack(self, notice_dictionary):

        is_my_turn = self.__notify_reader_repository.get_is_your_turn_for_check_fake_process()
        print(f"is my turn: {is_my_turn}")
        if is_my_turn is True:
            return

        data = notice_dictionary['NOTIFY_BASIC_ATTACK_TO_UNIT']

        is_opponent_data_in_data = False
        is_your_data_in_data = False

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

                        opponent_field_card_id = opponent_field_unit.get_card_number()
                        opponent_field_card_index = opponent_field_unit.get_index()

                        print(f"opponent_hp_number: {remain_opponent_unit_hp}")

                        # TODO: n 턴간 불사 특성을 검사해야하므로 사실 이것도 summary 방식으로 빼는 것이 맞으나 우선은 진행한다.
                        # (지금 당장 불사가 존재하지 않음)
                        if remain_opponent_unit_hp <= 0:
                            break

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
