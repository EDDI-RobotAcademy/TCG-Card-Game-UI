from battle_room_button.entity.battle_room_button import BattleRoomButton
from discarded.battle_room_button.repository.battle_room_button_repository import BattleRoomButtonRepository


class BattleRoomButtonRepositoryImpl(BattleRoomButtonRepository):
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

    # TODO : text값의 디폴트 값을 삭제 할 필요가 있음
    def createBattleRoomButton(self, rootFrame, text="hello"):
        room = BattleRoomButton(rootFrame)
        room.configure(padx=400, pady=50, text=text, font=("Arial", 10))
        return room