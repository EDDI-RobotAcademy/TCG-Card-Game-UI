import abc


class NotifyReaderController(abc.ABC):
    @abc.abstractmethod
    def startToReadNotice(self):
        pass