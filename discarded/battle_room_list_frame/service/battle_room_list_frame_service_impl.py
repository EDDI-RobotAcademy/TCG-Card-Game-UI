from discarded.battle_room_list_frame.repository import BattleRoomListFrameRepositoryImpl
from battle_room_list_frame.service.battle_room_list_frame_service import BattleRoomListFrameService


class BattleListFrameServiceImpl(BattleRoomListFrameService):
    __instance = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
            cls.__instance.__battleRoomListFrameRepository = BattleRoomListFrameRepositoryImpl.getInstance()
        return cls.__instance

    @classmethod
    def getInstance(cls):
        if cls.__instance is None:
            cls.__instance = cls()
        return cls.__instance