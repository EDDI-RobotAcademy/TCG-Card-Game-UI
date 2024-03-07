from common.protocol import CustomProtocol


class RequestUseCorpseExplosion:
    def __init__(self, _sessionInfo, _itemCardId, _unitIndex, _opponentTargetUnitIndexList):
        self.__protocolNumber = CustomProtocol.USE_CORPSE_EXPLOSION.value
        self.__opponentTargetUnitIndexList = []
        for target_index in _opponentTargetUnitIndexList:
            self.__opponentTargetUnitIndexList.append(str(target_index))

        self.__unitIndex = str(_unitIndex)
        self.__itemCardId = str(_itemCardId)
        self.__sessionInfo = _sessionInfo

    def toDictionary(self):
        return {
            "protocolNumber": self.__protocolNumber,
            "sessionInfo": self.__sessionInfo,
            "unitIndex": self.__unitIndex,
            "opponentTargetUnitIndexList": self.__opponentTargetUnitIndexList,
            "itemCardId": self.__itemCardId
        }

    def __str__(self):
        return f"RequestUseCorpseExplosion(protocolNumber={self.__protocolNumber}, unitIndex={self.__unitIndex}, itemCardId={self.__itemCardId}, opponentTargetUnitIndexList={self.__opponentTargetUnitIndexList}, sessionInfo={self.__sessionInfo})"
