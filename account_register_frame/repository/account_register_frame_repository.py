import abc


class AccountRegisterFrameRepository(abc.ABC):
    @abc.abstractmethod
    def createAccountRegisterFrame(self, rootWindow):
        pass
    