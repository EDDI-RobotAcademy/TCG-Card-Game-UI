from account_register_frame.repository.account_register_frame_repository_impl import AccountRegisterFrameRepositoryImpl
from account_register_frame.service.account_register_frame_service import AccountRegisterFrameService


class AccountRegisterFrameServiceImpl(AccountRegisterFrameService):
    __instance = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
            cls.__instance.__accountRegisterFrameRepository = AccountRegisterFrameRepositoryImpl.getInstance()
        return cls.__instance

    @classmethod
    def getInstance(cls):
        if cls.__instance is None:
            cls.__instance = cls()
        return cls.__instance

    def createAccountRegisterUiFrame(self, rootWindow):
        return self.__accountRegisterFrameRepository.createAccountRegisterFrame(rootWindow)
