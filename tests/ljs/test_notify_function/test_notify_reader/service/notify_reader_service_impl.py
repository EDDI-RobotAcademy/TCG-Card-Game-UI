import json

from tests.ljs.test_notify_function.test_notify_reader.entity.notice_type import NoticeType
from tests.ljs.test_notify_function.test_notify_reader.repository.notify_reader_repository_impl import NotifyReaderRepositoryImpl
from tests.ljs.test_notify_function.test_notify_reader.service.notify_reader_service import NotifyReaderService


class NotifyReaderServiceImpl(NotifyReaderService):
    __instance = None



    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
            cls.__instance.__notify_reader_repository = NotifyReaderRepositoryImpl.getInstance()
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

                    for notice_type in NoticeType:
                        if notice_type.name in notice_dict:
                            self.__notify_reader_repository.isFinish = True
                            print(f"noticeType: {notice_type.name}")
                            called_function = self.__notify_reader_repository.getFunctionByNoticeName(notice_type.name)
                            called_function(notice_dict[notice_type.name])

            except Exception as e:
                self.readNoticeAndCallFunction()
                print(e)
              #  continue