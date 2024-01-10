import abc


class WindowRepository(abc.ABC):
    @abc.abstractmethod
    def createNewWindow(self, appWindowRequest):
        pass
