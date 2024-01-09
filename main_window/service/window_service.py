import abc


class WindowService(abc.ABC):
    @abc.abstractmethod
    def createStartWindow(self, menuName):
        pass
