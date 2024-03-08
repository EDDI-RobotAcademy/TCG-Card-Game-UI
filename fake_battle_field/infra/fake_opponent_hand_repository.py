from colorama import Fore, Style

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
        for hand in fake_opponent_hand_list:
            self.__fake_opponent_hand_list.append(hand)

    def get_fake_opponent_hand_list(self):
        return self.__fake_opponent_hand_list

    def remove_card_by_index(self, card_placed_index):
        # print(f"remove_card_by_index -> self.current_hand_card_list: {self.__fake_opponent_hand_list}, card_placed_index: {card_placed_index}")
        print(f"{Fore.RED}remove_card_by_index -> self.current_hand_card_list: {Fore.GREEN} {self.__fake_opponent_hand_list}, card_placed_index: {card_placed_index}{Style.RESET_ALL}")

        if 0 <= card_placed_index < len(self.__fake_opponent_hand_list):
            removed_card = self.__fake_opponent_hand_list.pop(card_placed_index)
            print(f"Removed card index {card_placed_index}: {removed_card}")
        else:
            print(f"Invalid index: {card_placed_index}. 지울 것이 없다")

    def request_deploy_fake_opponent_unit(self, fake_opponent_deploy_unit_request):
        self.__transmitIpcChannel.put(fake_opponent_deploy_unit_request)
        return self.__receiveIpcChannel.get()

    def request_use_energy_card_to_unit(self, attach_energy_card_request):
        self.__transmitIpcChannel.put(attach_energy_card_request)
        return self.__receiveIpcChannel.get()
