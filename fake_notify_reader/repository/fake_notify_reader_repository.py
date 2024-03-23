import abc


class FakeNotifyReaderRepository(abc.ABC):
    @abc.abstractmethod
    def getNotice(self):
        pass

    @abc.abstractmethod
    def saveNoWaitIpcChannel(self, noWaitIpcChannel):
        pass

    @abc.abstractmethod
    def registerFunctionWithNoticeName(self, noticeName, function):
        pass
    @abc.abstractmethod
    def getFunctionByNoticeName(self, noticeName):
        pass