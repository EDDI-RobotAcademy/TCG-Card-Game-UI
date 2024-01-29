from battle_field_function.repository.battle_field_function_repository_impl import BattleFieldFunctionRepositoryImpl
from battle_field_function.service.battle_field_function_service import BattleFieldFunctionService
from battle_field_function.service.request.surrender_request import SurrenderRequest
from session.repository.session_repository_impl import SessionRepositoryImpl


class BattleFieldFunctionServiceImpl(BattleFieldFunctionService):
    __instance = None
    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
            cls.__instance.__battleFieldFunctionRepository = BattleFieldFunctionRepositoryImpl.getInstance()
            cls.__instance.__sessionRepository = SessionRepositoryImpl.getInstance()
        return cls.__instance

    @classmethod
    def getInstance(cls):
        if cls.__instance is None:
            cls.__instance = cls()
        return cls.__instance

    def injectTransmitIpcChannel(self, transmitIpcChannel):
        self.__battleFieldFunctionRepository.saveTransmitIpcChannel(transmitIpcChannel)

    def injectReceiveIpcChannel(self, receiveIpcChannel):
        self.__battleFieldFunctionRepository.saveReceiveIpcChannel(receiveIpcChannel)


    def surrender(self, switchFrameWithMenuName):
        print(f"battleFieldFunctionServiceImpl: Surrender")
        response = self.__battleFieldFunctionRepository.sendSurrender(
            SurrenderRequest(
                self.__sessionRepository.get_session_info()
            )
        )
        # Todo : switchFrameWithMenuName('lobby-menu') 를 호출 할 수 있어야합니다.
        switchFrameWithMenuName("lobby-menu")

