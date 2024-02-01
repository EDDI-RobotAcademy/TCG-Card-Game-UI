from lobby_frame.controller.lobby_menu_frame_controller import LobbyMenuFrameController
from lobby_frame.service.lobby_menu_frame_service_impl import LobbyMenuFrameServiceImpl


class LobbyMenuFrameControllerImpl(LobbyMenuFrameController):
    __instance = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
            cls.__instance.__lobbyMenuFrameService = LobbyMenuFrameServiceImpl.getInstance()
        return cls.__instance

    @classmethod
    def getInstance(cls):
        if cls.__instance is None:
            cls.__instance = cls()
        return cls.__instance

    def switchFrameToBattleLobby(self, windowToDestroy):
        self.__lobbyMenuFrameService.switchToBattleLobby(windowToDestroy)

