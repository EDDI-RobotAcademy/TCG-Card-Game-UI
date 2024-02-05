from battle_field_function.repository.battle_field_function_repository_impl import BattleFieldFunctionRepositoryImpl
from common.protocol import CustomProtocol


class UseItemCardRequest:
    def __init__(self, cardNumber, _sessionInfo):
        self.__protocolNumber = CustomProtocol.SURRENDER.value
        self.__roomNumber = BattleFieldFunctionRepositoryImpl.getInstance().getRoomNumber()
        self.__cardNumber = cardNumber
        self.__sessionInfo = _sessionInfo

    def toDictionary(self):
        return {
            "protocolNumber": self.__protocolNumber,
            "roomNumber": self.__roomNumber,
            "cardNumber": self.__cardNumber,
            "sessionInfo": self.__sessionInfo
        }

    def __str__(self):
        return f"UseItemCardRequest(protocolNumber={self.__protocolNumber}, roomNumber={self.__roomNumber}, \
                                   cardNumber={self.__cardNumber}, sessionInfo={self.__sessionInfo})"
