import abc


class FakeNotifyReaderController(abc.ABC):
    @abc.abstractmethod
    def requestToReadNotifyCommand(self):
        pass

    @abc.abstractmethod
    def requestToInjectNoWaitIpcChannel(self, no_wait_ipc_channel):
        pass

    @abc.abstractmethod
    def requestToMappingNoticeWithFunction(self):
        pass