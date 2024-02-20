from battle_field_function.repository.battle_field_function_repository import BattleFieldFunctionRepository


class BattleFieldFunctionRepositoryImpl(BattleFieldFunctionRepository):
    __instance = None
    __roomNumber = None


    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
        return cls.__instance

    @classmethod
    def getInstance(cls):
        if cls.__instance is None:
            cls.__instance = cls()
        return cls.__instance


    def saveRoomNumber(self, roomNumber):
        self.__roomNumber = roomNumber


    def getRoomNumber(self):
        return self.__roomNumber

    def saveReceiveIpcChannel(self, receiveIpcChannel):
        self.__receiveIpcChannel = receiveIpcChannel

    def saveTransmitIpcChannel(self, transmitIpcChannel):
        self.__transmitIpcChannel = transmitIpcChannel

    def requestSurrender(self, surrenderRequest):
        print(f"battleFieldFunctionRepositoryImpl: surrender")
        print(f"battleFieldFunctionRepositoryImpl: {surrenderRequest}")
        self.__transmitIpcChannel.put(surrenderRequest)
        return self.__receiveIpcChannel.get()


    def requestTurnEnd(self, turnEndRequest):
        print(f"턴 종료 요청함 : {turnEndRequest}")
        self.__transmitIpcChannel.put(turnEndRequest)
        return self.__receiveIpcChannel.get()



    def requestUseUnitCard(self, useUnitCardRequest):
        self.__transmitIpcChannel.put(useUnitCardRequest)
        return self.__receiveIpcChannel.get()


    def requestUnitAttack(self, unitAttackRequest):
        self.__transmitIpcChannel.put(unitAttackRequest)
        return self.__receiveIpcChannel.get()


    def requestUseEnergyCard(self, useEnergyCardRequest):
        self.__transmitIpcChannel.put(useEnergyCardRequest)
        return self.__receiveIpcChannel.get()


    def requestUseSpecialEnergyCard(self, useSpecialEnergyCardRequest):
        self.__transmitIpcChannel.put(useSpecialEnergyCardRequest)
        return self.__receiveIpcChannel.get()


    def requestUseEnvironmentCard(self, useEnvironmentCardRequest):
        self.__transmitIpcChannel.put(useEnvironmentCardRequest)
        return self.__receiveIpcChannel.get()


    def requestUseItemCard(self, useItemCardRequest):
        self.__transmitIpcChannel.put(useItemCardRequest)
        return self.__receiveIpcChannel.get()


    def requestUseSupportCard(self, useSupportCardRequest):
        self.__transmitIpcChannel.put(useSupportCardRequest)
        return self.__receiveIpcChannel.get()


    def requestUseToolCard(self, useToolCardRequest):
        self.__transmitIpcChannel.put(useToolCardRequest)
        return self.__receiveIpcChannel.get()


    def requestUseTrapCard(self, useTrapCardRequest):
        self.__transmitIpcChannel.put(useTrapCardRequest)
        return self.__receiveIpcChannel.get()
