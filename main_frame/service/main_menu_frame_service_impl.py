from main_frame.repository.main_menu_frame_repository_impl import MainMenuFrameRepositoryImpl
from main_frame.service.main_menu_frame_service import MainMenuFrameService


class MainMenuFrameServiceImpl(MainMenuFrameService):
    __instance = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
            cls.__instance.__mainMenuFrameRepository = MainMenuFrameRepositoryImpl.getInstance()
        return cls.__instance

    @classmethod
    def getInstance(cls):
        if cls.__instance is None:
            cls.__instance = cls()
        return cls.__instance

    def createMainUiFrame(self, rootWindow):
        self.__mainMenuFrameRepository.createMainMenuFrame(rootWindow)


