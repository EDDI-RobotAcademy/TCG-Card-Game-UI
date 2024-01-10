import abc


class WindowService(abc.ABC):
    @abc.abstractmethod
    def createRootWindow(self):
        pass
