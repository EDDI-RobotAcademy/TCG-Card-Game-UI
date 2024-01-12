import abc


class AccountRegisterFrameService(abc.ABC):
    @abc.abstractmethod
    def createAccountRegisterUiFrame(self, rootWindow):
        pass
