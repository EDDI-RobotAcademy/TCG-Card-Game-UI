import abc


class LoginMenuFrameRepository(abc.ABC):
    @abc.abstractmethod
    def createLoginMenuFrame(self, rootWindow):
        pass
    