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

    def request_real_battle_start(self, requestRealBattleStart):
        self.__transmitIpcChannel.put(requestRealBattleStart)
        return self.__receiveIpcChannel.get()

    def request_fake_multi_draw(self, fakeMultiDrawRequest):
        self.__transmitIpcChannel.put(fakeMultiDrawRequest)
        return self.__receiveIpcChannel.get()

    def request_attack_main_character(self, attackMainCharacterRequest):
        self.__transmitIpcChannel.put(attackMainCharacterRequest)
        return self.__receiveIpcChannel.get()

    def request_attack_opponent_unit(self, attackOpponentUnitRequest):
        self.__transmitIpcChannel.put(attackOpponentUnitRequest)
        return self.__receiveIpcChannel.get()

    def request_attack_main_character_with_active_skill(self, attackMainCharacterWithActiveSkillRequest):
        self.__transmitIpcChannel.put(attackMainCharacterWithActiveSkillRequest)
        return self.__receiveIpcChannel.get()

    def request_attack_with_non_targeting_active_skill(self, attackWithNonTargetingActiveSkill):
        self.__transmitIpcChannel.put(attackWithNonTargetingActiveSkill)
        return self.__receiveIpcChannel.get()

    def request_use_contract_of_doom(self, requestContractOfDoom):
        self.__transmitIpcChannel.put(requestContractOfDoom)
        return self.__receiveIpcChannel.get()

    def request_to_process_first_passive_skill(self, wideAreaPassiveSkillFromDeployRequest):
        self.__transmitIpcChannel.put(wideAreaPassiveSkillFromDeployRequest)
        return self.__receiveIpcChannel.get()

    def request_to_process_second_passive_skill_to_main_character(self, targetPassiveSkillToMainCharacterFromDeployRequest):
        self.__transmitIpcChannel.put(targetPassiveSkillToMainCharacterFromDeployRequest)
        return self.__receiveIpcChannel.get()