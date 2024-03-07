import json

from colorama import Fore, Style

from battle_field.infra.opponent_field_energy_repository import OpponentFieldEnergyRepository
from battle_field.infra.opponent_field_unit_repository import OpponentFieldUnitRepository
from battle_field.infra.your_field_energy_repository import YourFieldEnergyRepository
from battle_field.infra.your_hand_repository import YourHandRepository
from battle_field_function.service.battle_field_function_service_impl import BattleFieldFunctionServiceImpl
from fake_battle_field.infra.fake_opponent_hand_repository import FakeOpponentHandRepositoryImpl
from notify_reader.entity.notice_type import NoticeType
from notify_reader.repository.notify_reader_repository_impl import NotifyReaderRepositoryImpl
from notify_reader.service.notify_reader_service import NotifyReaderService


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

            cls.__instance.notify_callback_table['NOTIFY_DEPLOY_UNIT'] = cls.__instance.notify_deploy_unit
            cls.__instance.notify_callback_table['NOTIFY_TURN_END'] = cls.__instance.notify_turn_end
            cls.__instance.notify_callback_table['NOTIFY_USE_GENERAL_ENERGY_CARD_TO_UNIT'] = (
                cls.__instance.__battle_field_function_service.useGeneralEnergyCardToUnit)
            cls.__instance.notify_callback_table['NOTIFY_USE_SPECIAL_ENERGY_CARD_TO_UNIT'] = (
                cls.__instance.__battle_field_function_service.useSpecialEnergyCardToUnit)
            cls.__instance.notify_callback_table['NOTIFY_USE_UNIT_ENERGY_REMOVE_ITEM_CARD'] = (
                cls.__instance.__battle_field_function_service.useUnitEnergyRemoveItemCard)


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

        # if self.__notify_reader_repository.get_is_your_turn_for_check_fake_process() is True:
        #     return
        #
        # card_id = (notice_dictionary.get('NOTIFY_DEPLOY_UNIT', {})
        #            .get('player_hand_use_map', {})
        #            .get('Opponent', {})
        #            .get('card_id', None))
        #
        # self.__opponent_field_unit_repository.create_field_unit_card(card_id)

