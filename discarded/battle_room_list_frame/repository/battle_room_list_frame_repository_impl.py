from battle_room_button.entity.battle_room_button import BattleRoomButton
from discarded.battle_room_list_frame.repository import BattleRoomListFrameRepository


class BattleRoomListFrameRepositoryImpl(BattleRoomListFrameRepository):
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

    def createBattleRoomListFrame(self, rootWindow, request=None):
        for room in request:
            roomButton = BattleRoomButton.getInstance().generateRoomButton(rootWindow)
            roomButton.pack()



