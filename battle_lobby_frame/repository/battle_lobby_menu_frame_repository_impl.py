from battle_lobby_frame.entity.battle_lobby_menu_frame import BattleLobbyMenuFrame
from battle_lobby_frame.repository.battle_lobby_menu_frame_repository import BattleLobbyMenuFrameRepository


class BattleLobbyMenuFrameRepositoryImpl(BattleLobbyMenuFrameRepository):
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

    def createBattleLobbyMenuFrame(self, rootWindow):
        print("BattleLobbyMenuFrameRepositoryImpl: createBattleLobbyMenuFrame()")
        battleLobbyMenuFrame = BattleLobbyMenuFrame(rootWindow)

        return battleLobbyMenuFrame
