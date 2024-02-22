from battle_field_function.repository.battle_field_function_repository_impl import BattleFieldFunctionRepositoryImpl
from battle_field_function.service.battle_field_function_service import BattleFieldFunctionService
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




    def surrender(self, switchFrameWithMenuName):
        print(f"battleFieldFunctionServiceImpl: Surrender")
        response = self.__battleFieldFunctionRepository.requestSurrender(
            SurrenderRequest(
                self.__sessionService.getSessionInfo()
            )
        )
        # Todo : switchFrameWithMenuName('lobby-menu') 를 호출 할 수 있어야합니다.
        switchFrameWithMenuName("lobby-menu")


    def mulligan(self, cardCount):
        try:
            mulliganResponse = self.__battleFieldFunctionRepository.requestMulligan(
                MulliganRequest(_sessionInfo=self.__sessionRepository.get_session_info(),
                                cardCount=cardCount)
            )
            #Todo : 멀리건 결과로 새로운 카드를 리턴받을것임.
            #Todo : 새로 받은 카드를 렌더링하고 메모리에 저장해두면됨

        except Exception as e:
            print(f"mulligan Error : {e}")


    def unitAttack(self, target):
        try:
            unitAttackResponse = self.__battleFieldFunctionRepository.requestUnitAttack(
                UnitAttackRequest(_sessionInfo=self.__sessionRepository.get_session_info(),
                                  target=target)
            )
            # Todo: 공격에 대한 응답을 받으면 적절하게 하면됨... ㅋ
        except Exception as e:
            print(f"unitAttack Error: {e}")

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
                TurnEndRequest(
                    # _sessionInfo=self.__sessionService.getSessionInfo())
                    _sessionInfo=self.__sessionRepository.get_session_info())
            )
        except Exception as e:
            print(f"turnEnd Error: {e}")


    def useEnvironmentCard(self, cardNumber):
        try:
            useEnvironmentCardResponse = self.__battleFieldFunctionRepository.requestUseEnvironmentCard(
                UseEnvironmentCardRequest(_sessionInfo=self.__sessionRepository.get_session_info(),
                                            cardNumber=cardNumber)
            )
        except Exception as e:
            print(f"useEnvironmentCard Error: {e}")


    def useEnergyCard(self):
        try:
            useEnergyCardResponse = self.__battleFieldFunctionRepository.requestUseEnergyCard(
                UseEnergyCardRequest(_sessionInfo=self.__sessionRepository.get_session_info())
            )
        except Exception as e:
            print(f"useEnergyCard Error: {e}")

    def useSpecialEnergyCard(self, cardNumber):
        try:
            useSpecialEnergyCardResponse = self.__battleFieldFunctionRepository.requestUseSpecialEnergyCard(
                UseSpecialEnergyCardRequest(_sessionInfo=self.__sessionRepository.get_session_info(),
                                            cardNumber=cardNumber)
            )
        except Exception as e:
            print(f"useSpecialEnergy Error: {e}")

    def useItemCard(self, cardNumber):
        try:
            useItemCardResponse = self.__battleFieldFunctionRepository.requestItemCard(
                UseItemCardRequest(_sessionInfo=self.__sessionRepository.get_session_info(),
                                   cardNumber=cardNumber)
            )
        except Exception as e:
            print(f"useItemCard Error: {e}")


    def useSupportCard(self, cardNumber):
        try:
            useSupportCardResponse = self.__battleFieldFunctionRepository.requestSupportCard(
                UseSupportCardRequest(_sessionInfo=self.__sessionRepository.get_session_info(),
                                      cardNumber=cardNumber)
            )
        except Exception as e:
            print(f"useSupportCard Error: {e}")


    def useToolCard(self, cardNumber):
        try:
            useToolCardResponse = self.__battleFieldFunctionRepository.requestToolCard(
                UseToolCardRequest(_sessionInfo=self.__sessionRepository.get_session_info(),
                                   cardNumber=cardNumber)
            )
        except Exception as e:
            print(f"useToolCard Error: {e}")


    def useTrapCard(self, cardNumber):
        try:
            useTrapCardResponse = self.__battleFieldFunctionRepository.requestTrapCard(
                UseTrapCardRequest(_sessionInfo=self.__sessionRepository.get_session_info(),
                                   cardNumber=cardNumber)
            )
        except Exception as e:
            print(f"useTrapCard Error: {e}")


    def useUnitCard(self, cardNumber):
        try:
            useUnitCardResponse = self.__battleFieldFunctionRepository.requestUnitCard(
                UseUnitCardRequest(_sessionInfo=self.__sessionRepository.get_session_info(),
                                   cardNumber=cardNumber)
            )
        except Exception as e:
            print(f"useUnitCard Error: {e}")