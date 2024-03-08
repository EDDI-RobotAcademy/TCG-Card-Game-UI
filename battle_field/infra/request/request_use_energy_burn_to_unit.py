from common.protocol import CustomProtocol


class RequestUseEnergyBurnToUnit:
    def __init__(self, _sessionInfo, _itemCardId, _opponentTargetUnitIndex):
        self.__protocolNumber = CustomProtocol.USE_ENERGY_BURN.value
        self.__opponentTargetUnitIndex = str(_opponentTargetUnitIndex)
        self.__itemCardId = str(_itemCardId)
        self.__sessionInfo = _sessionInfo

    def toDictionary(self):
        return {
            "protocolNumber": self.__protocolNumber,
            "sessionInfo": self.__sessionInfo,
            "opponentTargetUnitIndex": self.__opponentTargetUnitIndex,
            "itemCardId" : self.__itemCardId
        }

    def __str__(self):
        return f"RequestUseDeathSiceToUnit(protocolNumber={self.__protocolNumber}, itemCardId={self.__itemCardId}, opponentTargetUnitIndex={self.__opponentTargetUnitIndex}, sessionInfo={self.__sessionInfo})"
