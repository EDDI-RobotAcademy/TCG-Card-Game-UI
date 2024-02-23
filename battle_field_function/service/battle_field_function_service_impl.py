from battle_field.infra.battle_field_repository import BattleFieldRepository
from battle_field_function.repository.battle_field_function_repository_impl import BattleFieldFunctionRepositoryImpl
from battle_field_function.service.battle_field_function_service import BattleFieldFunctionService
from battle_field_function.service.request.game_end_reward_request import GameEndRewardRequest
from battle_field_function.service.request.mulligan_request import MulliganRequest
from battle_field_function.service.request.surrender_request import SurrenderRequest
from battle_field_function.service.request.turn_end_request import TurnEndRequest
from battle_field_function.service.request.unit_attack_request import UnitAttackRequest
from battle_field_function.service.request.use_energy_card_request import UseEnergyCardRequest
from battle_field_function.service.request.use_environment_card_request import UseEnvironmentCardRequest
from battle_field_function.service.request.use_item_card_request import UseItemCardRequest
from battle_field_function.service.request.use_special_energy_card_request import UseSpecialEnergyCardRequest
from battle_field_function.service.request.use_support_card_request import UseSupportCardRequest
from battle_field_function.service.request.use_tool_card_request import UseToolCardRequest
from battle_field_function.service.request.use_trap_card_request import UseTrapCardRequest
from battle_field_function.service.request.use_unit_card_request import UseUnitCardRequest
from session.repository.session_repository_impl import SessionRepositoryImpl
from session.service.session_service_impl import SessionServiceImpl


class BattleFieldFunctionServiceImpl(BattleFieldFunctionService):
    __instance = None
    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
            cls.__instance.__battleFieldFunctionRepository = BattleFieldFunctionRepositoryImpl.getInstance()
            cls.__instance.__sessionRepository = SessionRepositoryImpl.getInstance()
            cls.__instance.__sessionService = SessionServiceImpl.getInstance()
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




    def surrender(self, switchFrameWithMenuName = None):
        print(f"battleFieldFunctionServiceImpl: Surrender")
        surrender_response = self.__battleFieldFunctionRepository.requestSurrender(
            SurrenderRequest(
                self.__sessionService.getSessionInfo()
            )
        )
        # Todo : switchFrameWithMenuName('lobby-menu') 를 호출 할 수 있어야합니다.
        if switchFrameWithMenuName is not None:
            switchFrameWithMenuName("lobby-menu")
        else:
            print(f"항복 요청함!!! 응답: {surrender_response}")
            self.gameEndReward()



    def turnEnd(self):
        try:
            turnEndResponse = self.__battleFieldFunctionRepository.requestTurnEnd(
                TurnEndRequest(
                    #_sessionInfo=self.__sessionService.getSessionInfo())
                    _sessionInfo=self.__sessionRepository.get_session_info())
            )

        except Exception as e:
            print(f"turnEnd Error: {e}")


    def gameEndReward(self):
        try:
            gameEndRewardResponse = self.__battleFieldFunctionRepository.requestGameEnd(
                GameEndRewardRequest(
                    # _sessionInfo=self.__sessionService.getSessionInfo())
                    _sessionInfo=self.__sessionRepository.get_session_info())
            )
            print(f"게임 끝! 응답: {gameEndRewardResponse}")
            if gameEndRewardResponse:
                BattleFieldRepository.getInstance().game_end()
        except Exception as e:
            print(f"turnEnd Error: {e}")


