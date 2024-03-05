import abc


class NotifyReaderService(abc.ABC):
    @abc.abstractmethod
    def readNoticeAndCallFunction(self):
        pass

    @abc.abstractmethod
    def injectNoWaitIpcChannel(self, nowaitIpcChannel):
        pass

