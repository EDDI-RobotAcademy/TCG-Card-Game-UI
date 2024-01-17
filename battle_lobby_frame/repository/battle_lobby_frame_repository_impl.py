from battle_lobby_frame.entity.battle_lobby_frame import BattleLobbyFrame
from battle_lobby_frame.repository.battle_lobby_frame_repository import BattleLobbyFrameRepository


class BattleLobbyFrameRepositoryImpl(BattleLobbyFrameRepository):
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

    def createBattleLobbyFrame(self, rootWindow):
        print("BattleLobbyFrameRepositoryImpl: createBattleLobbyFrame()")
        battleLobbyFrame = BattleLobbyFrame(rootWindow)

        return battleLobbyFrame
