from battle_field_function.repository.battle_field_function_repository_impl import BattleFieldFunctionRepositoryImpl
from common.protocol import CustomProtocol


class MulliganRequest:
    def __init__(self, cardCount, _sessionInfo):
        self.__protocolNumber = CustomProtocol.MULLIGAN_CARD.value
        self.__cardCount = cardCount
        self.__roomNumber = BattleFieldFunctionRepositoryImpl.getInstance().getRoomNumber()
        self.__sessionInfo = _sessionInfo

    def toDictionary(self):
        return {
            "protocolNumber": self.__protocolNumber,
            "roomNumber": self.__roomNumber,
            "cardCount" : self.__cardCount,
            "sessionInfo": self.__sessionInfo
        }

    def __str__(self):
        return (f"SurrenderRequest(protocolNumber={self.__protocolNumber}, roomNumber={self.__roomNumber}, \
                                                    cardCount={self.__cardCount}, sessionInfo={self.__sessionInfo})")
