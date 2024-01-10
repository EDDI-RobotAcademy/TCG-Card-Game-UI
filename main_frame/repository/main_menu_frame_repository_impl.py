import tkinter

from main_frame.entity.main_menu_frame import MainMenuFrame
from main_frame.repository.main_menu_frame_repository import MainMenuFrameRepository


class MainMenuFrameRepositoryImpl(MainMenuFrameRepository):
    __instance = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
        return cls.__instance

    @classmethod
    def getInstance(cls):
        if cls.__instance is None:
            cls.__instance = cls()
        return cls.__instance

    def createMainMenuFrame(self, rootWindow):
        print("MainMenuFrameRepositoryImpl: createMainMenuFrame()")
        mainMenuFrame = MainMenuFrame(rootWindow)

        return mainMenuFrame
