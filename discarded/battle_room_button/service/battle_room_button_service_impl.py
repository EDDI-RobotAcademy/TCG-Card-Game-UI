from battle_room_button.repository.battle_room_button_repository_impl import BattleRoomButtonRepositoryImpl
from discarded.battle_room_button.service import BattleRoomButtonService


class BattleRoomButtonServiceImpl(BattleRoomButtonService):
    __instance = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
            cls.__instance.__battleRoomButtonRepository = BattleRoomButtonRepositoryImpl.getInstance()
        return cls.__instance

    @classmethod
    def getInstance(cls):
        if cls.__instance is None:
            cls.__instance = cls()
        return cls.__instance
