import abc


class WindowRepository(abc.ABC):
    @abc.abstractmethod
    def createNewWindow(self, menuName, newWindow):
        pass
