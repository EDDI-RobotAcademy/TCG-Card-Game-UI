from fake_battle_field.infra.fake_battle_field_frame_repository import FakeBattleFieldFrameRepository


class FakeOpponentHandRepositoryImpl():
    __instance = None

    __fake_opponent_hand_list = []

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
        print("FakeOpponentHandRepositoryImpl: saveTransmitIpcChannel()")
        self.__transmitIpcChannel = transmitIpcChannel

    def injectReceiveIpcChannel(self, receiveIpcChannel):
        print("FakeOpponentHandRepositoryImpl: saveReceiveIpcChannel()")
        self.__receiveIpcChannel = receiveIpcChannel

    def save_fake_opponent_hand_list(self, fake_opponent_hand_list):
        self.__fake_opponent_hand_list = fake_opponent_hand_list

    def get_fake_opponent_hand_list(self):
        return self.__fake_opponent_hand_list

    def request_deploy_fake_opponent_unit(self, fake_opponent_deploy_unit_request):
        self.__transmitIpcChannel.put(fake_opponent_deploy_unit_request)
        return self.__receiveIpcChannel.get()
