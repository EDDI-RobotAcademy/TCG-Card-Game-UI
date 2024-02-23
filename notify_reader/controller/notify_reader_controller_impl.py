from notify_reader.controller.notify_reader_controller import NotifyReaderController
from notify_reader.service.notify_reader_service_impl import NotifyReaderServiceImpl


class NotifyReaderControllerImpl(NotifyReaderController):
    __instance = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
            cls.__instance.__notifyReaderService = NotifyReaderServiceImpl.getInstance()
            #todo : 실행되어야 할 함수 위치를 등록해주세요
        return cls.__instance

    @classmethod
    def getInstance(cls):
        if cls.__instance is None:
            cls.__instance = cls()
        return cls.__instance

    def requestToMappingNoticeWithFunction(self):
        #todo : 함수를 등록해주세요

        hand_use_function = "hand_use_function"
        self.__notifyReaderService.saveHandUseFunction(hand_use_function)

        draw_count_function = "draw_count_function"
        self.__notifyReaderService.saveDrawCountFunction(draw_count_function)

        drawn_card_list_function = "drawn_card_list_function"
        self.__notifyReaderService.saveDrawnCardListFunction(drawn_card_list_function)



    def requestToReadNotifyCommand(self):
        self.__notifyReaderService.readNoticeAndCallFunction()

    def requestToInjectNoWaitIpcChannel(self, no_wait_ipc_channel):
        self.__notifyReaderService.injectNoWaitIpcChannel(no_wait_ipc_channel)