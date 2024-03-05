from notify_reader.repository.notify_reader_repository import NotifyReaderRepository


class NotifyReaderRepositoryImpl(NotifyReaderRepository):
    __instance = None
    __noWaitIpcChannel = None
    __functions_called_by_notice_table = {}

    __is_your_turn_for_check_fake_process = False

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)

        return cls.__instance

    @classmethod
    def getInstance(cls):
        if cls.__instance is None:
            cls.__instance = cls()
        return cls.__instance

    def set_is_your_turn_for_check_fake_process(self, is_your_turn_for_check_fake_process):
        self.__is_your_turn_for_check_fake_process = is_your_turn_for_check_fake_process

    def get_is_your_turn_for_check_fake_process(self):
        return self.__is_your_turn_for_check_fake_process

    def getNotice(self):
        try:
            return self.__noWaitIpcChannel.get_nowait()
        except:
            return None

    def saveNoWaitIpcChannel(self, noWaitIpcChannel):
        print(f"saved waitIpcChannel: {noWaitIpcChannel}")
        self.__noWaitIpcChannel = noWaitIpcChannel

    def getNoWaitIpcChannel(self):
        return self.__noWaitIpcChannel


    def registerFunctionWithNoticeName(self, noticeName, function):
        self.__functions_called_by_notice_table[noticeName] = function

    def getFunctionByNoticeName(self, noticeName):
        return self.__functions_called_by_notice_table[noticeName]