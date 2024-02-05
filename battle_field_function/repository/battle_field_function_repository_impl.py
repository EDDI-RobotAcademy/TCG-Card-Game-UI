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

    def sendSurrender(self, surrenderRequest):
        print(f"battleFieldFunctionRepositoryImpl: surrender")
        print(f"battleFieldFunctionRepositoryImpl: {surrenderRequest}")
        self.__transmitIpcChannel.put(surrenderRequest)
        return self.__receiveIpcChannel.get()

