from notify_reader.controller.notify_reader_controller import NotifyReaderController
from notify_reader.service.notify_reader_service_impl import NotifyReaderServiceImpl


class NotifyReaderControllerImpl(NotifyReaderController):
    __instance = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
            cls.__instance.__notifyReaderService = NotifyReaderServiceImpl.getInstance()
        return cls.__instance

    @classmethod
    def getInstance(cls):
        if cls.__instance is None:
            cls.__instance = cls()
        return cls.__instance

    def startToReadNotice(self):
        self.__notifyReaderService.readNoticeAndCallFunction()