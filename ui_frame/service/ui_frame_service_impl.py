from ui_frame.entity.main_menu_frame import MainMenuFrame
from ui_frame.repository.main_menu_frame.main_menu_frame_repository_impl import MainMenuFrameRepositoryImpl
from ui_frame.repository.ui_frame_repository_impl import UiFrameRepositoryImpl
from ui_frame.service.ui_frame_service import UiFrameService


class UiFrameServiceImpl(UiFrameService):
    __instance = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
            cls.__instance.__uiFrameRepository = UiFrameRepositoryImpl.getInstance()
            cls.__instance.__mainMenuFrameRepository = MainMenuFrameRepositoryImpl.getInstance()
        return cls.__instance

    @classmethod
    def getInstance(cls):
        if cls.__instance is None:
            cls.__instance = cls()
        return cls.__instance

    def createUiFrame(self, rootWindow):
        print("UiFrameServiceImpl: createUiFrame()")
        mainMenuFrame = self.__mainMenuFrameRepository.createMainMenuFrame(rootWindow)
        self.__uiFrameRepository.registerUiFrame("main-menu", mainMenuFrame)



