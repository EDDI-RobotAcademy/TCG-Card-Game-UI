from fake_battle_field.infra.fake_battle_field_frame_repository import FakeBattleFieldFrameRepository


class FakeBattleFieldFrameRepositoryImpl(FakeBattleFieldFrameRepository):
    __instance = None

    __transmitIpcChannel = None
    __receiveIpcChannel = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
        return cls.__instance

    @classmethod
    def getInstance(cls):
        if cls.__instance is None:
            cls.__instance = cls()
        return cls.__instance

    def injectTransmitIpcChannel(self, transmitIpcChannel):
        print("FakeBattleFieldFrameRepositoryImpl: saveTransmitIpcChannel()")
        self.__transmitIpcChannel = transmitIpcChannel

    def injectReceiveIpcChannel(self, receiveIpcChannel):
        print("FakeBattleFieldFrameRepositoryImpl: saveReceiveIpcChannel()")
        self.__receiveIpcChannel = receiveIpcChannel

    def requestCreateFakeBattleRoom(self, createFakeBattleRoomRequest):
        print(f"FakeBattleFieldFrameRepositoryImpl: requestCreateFakeBattleRoom() -> {createFakeBattleRoomRequest}")

        self.__transmitIpcChannel.put(createFakeBattleRoomRequest)
        return self.__receiveIpcChannel.get()

    def request_deck_name_list_for_fake_battle(self, requestDeckNameListForBattle):
        self.__transmitIpcChannel.put(requestDeckNameListForBattle)
        return self.__receiveIpcChannel.get()

    def request_card_list(self, requestDeckNameListForBattle):
        self.__transmitIpcChannel.put(requestDeckNameListForBattle)
        return self.__receiveIpcChannel.get()


