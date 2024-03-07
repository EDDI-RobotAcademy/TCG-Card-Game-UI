from common.protocol import CustomProtocol


class RequestUseCallOfLeonic:
    def __init__(self, _sessionInfo, _supportCardId, _targetUnitCardIndexList):
        self.__protocolNumber = CustomProtocol.SEARCH_UNIT_CARD.value
        self.__supportCardId = str(_supportCardId)
        self.__targetUnitCardIndexList = _targetUnitCardIndexList
        self.__sessionInfo = _sessionInfo

    def toDictionary(self):
        return {
            "protocolNumber": self.__protocolNumber,
            "supportCardId": self.__supportCardId,
            "targetUnitCardIndexList": self.__targetUnitCardIndexList,
            "sessionInfo": self.__sessionInfo
        }

    def __str__(self):
        return (f"RequestUseCallOfLeonic(protocolNumber={self.__protocolNumber}, "
                f"supportCardId={self.__supportCardId}, "
                f"targetUnitCardIndexList={self.__targetUnitCardIndexList}, "
                f"sessionInfo={self.__sessionInfo})")