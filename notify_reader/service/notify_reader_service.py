import abc


class NotifyReaderService(abc.ABC):
    @abc.abstractmethod
    def readNoticeAndCallFunction(self):
        pass
