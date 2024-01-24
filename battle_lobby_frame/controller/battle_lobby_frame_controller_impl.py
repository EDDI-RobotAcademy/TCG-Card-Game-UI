from battle_lobby_frame.controller.battle_lobby_frame_controller import BattleLobbyFrameController
from battle_lobby_frame.service.battle_lobby_frame_service_impl import BattleLobbyFrameServiceImpl


class BattleLobbyFrameControllerImpl(BattleLobbyFrameController):
    __instance = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
            cls.__instance.__battleLobbyFrameService = BattleLobbyFrameServiceImpl.getInstance()
        return cls.__instance

    @classmethod
    def getInstance(cls):
        if cls.__instance is None:
            cls.__instance = cls()
        return cls.__instance

    def createDeckButtons(self, response):
        self.__battleLobbyFrameService.createBattleLobbyMyDeckButton(response)


    def startCheckTime(self):
        self.__battleLobbyFrameService.checkTimeForDeckSelection()

