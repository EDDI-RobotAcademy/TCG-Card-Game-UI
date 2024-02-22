import json

from notify_reader.entity.notice_type import NoticeType
from notify_reader.repository.notify_reader_repository_impl import NotifyReaderRepositoryImpl
from notify_reader.service.notify_reader_service import NotifyReaderService


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

    def saveHandUseFunction(self, hand_use_function):
        self.__notify_reader_repository.registerFunctionWithNoticeName(NoticeType.NOTIFY_HAND_USE.name, hand_use_function)

    def saveDrawCountFunction(self, draw_count_function):
        self.__notify_reader_repository.registerFunctionWithNoticeName(NoticeType.NOTIFY_DRAW_COUNT.name, draw_count_function)

    def saveDrawnCardListFunction(self, drawn_card_list_function):
        self.__notify_reader_repository.registerFunctionWithNoticeName(NoticeType.NOTIFY_DRAWN_CARD_LIST, drawn_card_list_function)



    def readNoticeAndCallFunction(self):
        while True:
            try:
                raw_notice_data = self.__notify_reader_repository.getNotice()
                notice_dict = json.loads(raw_notice_data)
                for notice_type in NoticeType:
                    if notice_type.name in notice_dict:
                        called_function = self.__notify_reader_repository.callFunctionByNoticeName(notice_type.name)
                        called_function(notice_dict[notice_type.name])
            except:
                continue