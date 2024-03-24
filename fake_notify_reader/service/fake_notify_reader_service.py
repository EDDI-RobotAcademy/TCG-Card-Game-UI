import abc


class FakeNotifyReaderService(abc.ABC):
    @abc.abstractmethod
    def readNoticeAndCallFunction(self):
        pass

    @abc.abstractmethod
    def injectNoWaitIpcChannel(self, nowaitIpcChannel):
        pass

