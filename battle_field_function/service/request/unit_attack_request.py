from battle_field_function.repository.battle_field_function_repository_impl import BattleFieldFunctionRepositoryImpl
from common.protocol import CustomProtocol


class UnitAttackRequest:
    def __init__(self, target, _sessionInfo):
        self.__protocolNumber = CustomProtocol.SURRENDER.value
        self.__roomNumber = BattleFieldFunctionRepositoryImpl.getInstance().getRoomNumber()
        self.__target = target
        self.__sessionInfo = _sessionInfo

    def toDictionary(self):
        return {
            "protocolNumber": self.__protocolNumber,
            "roomNumber": self.__roomNumber,
            "target": self.__target,
            "sessionInfo": self.__sessionInfo
        }

    def __str__(self):
        return f"UnitAttackRequest(protocolNumber={self.__protocolNumber}, roomNumber={self.__roomNumber}, \
                                target={self.__target}, sessionInfo={self.__sessionInfo})"
