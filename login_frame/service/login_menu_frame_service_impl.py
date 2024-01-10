from login_frame.repository.login_menu_frame_repository_impl import LoginMenuFrameRepositoryImpl
from login_frame.service.login_menu_frame_service import LoginMenuFrameService


class LoginMenuFrameServiceImpl(LoginMenuFrameService):
    __instance = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
            cls.__instance.__loginMenuFrameRepository = LoginMenuFrameRepositoryImpl.getInstance()
        return cls.__instance

    @classmethod
    def getInstance(cls):
        if cls.__instance is None:
            cls.__instance = cls()
        return cls.__instance

    def createLoginUiFrame(self, rootWindow):
        return self.__loginMenuFrameRepository.createLoginMenuFrame(rootWindow)