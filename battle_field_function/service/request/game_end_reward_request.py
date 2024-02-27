from battle_field.infra.battle_field_repository import BattleFieldRepository
from common.protocol import CustomProtocol


class GameEndRewardRequest:
    def __init__(self, _sessionInfo):
        self.__protocolNumber = CustomProtocol.TURN_END.value
      #  self.__roomNumber = BattleFieldFunctionRepositoryImpl.getInstance().getRoomNumber()
        self.__isWinner = BattleFieldRepository.getInstance().is_win
        self.__sessionInfo = _sessionInfo

    def toDictionary(self):
        return {
            "protocolNumber": self.__protocolNumber,
          #  "roomNumber": self.__roomNumber,
            "sessionInfo": self.__sessionInfo
        }

    def __str__(self):
        #return f"TurnEndRequest(protocolNumber={self.__protocolNumber}, roomNumber={self.__roomNumber}, sessionInfo={self.__sessionInfo})"
        return f"GameEndRewardRequest(protocolNumber={self.__protocolNumber}, isWinner={self.__isWinner}, sessionInfo={self.__sessionInfo})"
