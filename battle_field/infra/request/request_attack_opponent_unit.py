from common.protocol import CustomProtocol


class RequestAttackOpponentUnit:
    def __init__(self, _sessionInfo, _attackerUnitIndex, _targetUnitIndex):
        self.__protocolNumber = CustomProtocol.ATTACK_UNIT.value
        self.__attacker_unit_index = str(_attackerUnitIndex)
        self.__target_unit_index = str(_targetUnitIndex)
        self.__sessionInfo = _sessionInfo

    def toDictionary(self):
        return {
            "protocolNumber": self.__protocolNumber,
            "sessionInfo": self.__sessionInfo,
            "attacker_unit_index": self.__attacker_unit_index,
            "target_unit_index": self.__target_unit_index,
        }

    def __str__(self):
        return f"RequestAttackOpponentUnit(protocolNumber={self.__protocolNumber}, attacker_unit_index={self.__attacker_unit_index}, target_unit_index={self.__target_unit_index}, sessionInfo={self.__sessionInfo})"
