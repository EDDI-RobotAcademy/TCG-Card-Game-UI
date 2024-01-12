import abc


class AccountRegisterFrameService(abc.ABC):
    @abc.abstractmethod
    def createAccountRegisterFrame(self, rootWindow):
        pass
    