from ui_frame.repository.login_menu_frame.login_menu_frame_repository_impl import LoginMenuFrameRepositoryImpl
from ui_frame.repository.ui_frame_repository_impl import UiFrameRepositoryImpl
from ui_frame.service.ui_frame_service import UiFrameService


class UiFrameServiceImpl(UiFrameService):
    __instance = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
            cls.__instance.__uiFrameRepository = UiFrameRepositoryImpl.getInstance()
            cls.__instance.__loginMenuFrameRepository = LoginMenuFrameRepositoryImpl.getInstance()
        return cls.__instance

    @classmethod
    def getInstance(cls):
        if cls.__instance is None:
            cls.__instance = cls()
        return cls.__instance

    def registerMainMenuUiFrame(self, mainMenuFrame):
        print("UiFrameServiceImpl: createMainUiFrame()")
        self.__uiFrameRepository.registerUiFrame("main-menu", mainMenuFrame)

    def registerLoginMenuUiFrame(self, loginMenuFrame):
        print("UiFrameServiceImpl: createLoginUiFrame()")
        self.__uiFrameRepository.registerUiFrame("login-menu", loginMenuFrame)





