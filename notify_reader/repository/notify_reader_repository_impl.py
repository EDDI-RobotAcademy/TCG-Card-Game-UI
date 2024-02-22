from notify_reader.repository.notify_reader_repository import NotifyReaderRepository


class NotifyReaderRepositoryImpl(NotifyReaderRepository):
    __instance = None
    __noWaitIpcChannel = None
    __functions_called_by_notice_table = {}
    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)

        return cls.__instance

    @classmethod
    def getInstance(cls):
        if cls.__instance is None:
            cls.__instance = cls()
        return cls.__instance

    def getNotice(self):
        try:
            return self.__noWaitIpcChannel.get()
        except:
            return None

    def saveNoWaitIpcChannel(self, noWaitIpcChannel):
        self.__noWaitIpcChannel = noWaitIpcChannel


    def registerFunctionWithNoticeName(self, noticeName, function):
        self.__functions_called_by_notice_table[noticeName] = function

    def getFunctionByNoticeName(self, noticeName):
        return self.__functions_called_by_notice_table[noticeName]