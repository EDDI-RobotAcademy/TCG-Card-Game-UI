from tkinter import ttk, CENTER

from lobby_frame.entity.lobby_menu_frame import LobbyMenuFrame
from lobby_frame.repository.lobby_menu_frame_repository import LobbyMenuFrameRepository


class LobbyMenuFrameRepositoryImpl(LobbyMenuFrameRepository):
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

    def createLobbyMenuFrame(self, rootWindow):
        print("MainMenuFrameRepositoryImpl: createLobbyMenuFrame()")
        lobbyMenuFrame = LobbyMenuFrame(rootWindow)

        return lobbyMenuFrame

