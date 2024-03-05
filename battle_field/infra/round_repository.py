class RoundRepository:
    __instance = None

    __transmitIpcChannel = None
    __receiveIpcChannel = None

    current_round_number = 1

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

    def increase_current_round_number(self):
        self.current_round_number += 1

    def get_current_round_number(self):
        return self.current_round_number

    def request_turn_end(self, turn_end_request):
        self.__transmitIpcChannel.put(turn_end_request)
        return self.__receiveIpcChannel.get()

        # turnEndResponse = self.__battleFieldFunctionRepository.requestTurnEnd(
        #     TurnEndRequest(
        #         # _sessionInfo=self.__sessionService.getSessionInfo())
        #         _sessionInfo=self.__sessionRepository.get_session_info())
        # )
