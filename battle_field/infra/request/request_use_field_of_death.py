from common.protocol import CustomProtocol


class RequestUseFieldOfDeath:
    def __init__(self, _sessionInfo, _supportCardId):
        self.__protocolNumber = CustomProtocol.USE_FIELD_ENERGY_REMOVE_SUPPORT_CARD.value
        self.__supportCardId = str(_supportCardId)
        self.__sessionInfo = _sessionInfo

    def toDictionary(self):
        return {
            "protocolNumber": self.__protocolNumber,
            "sessionInfo": self.__sessionInfo,
            "supportCardId": self.__supportCardId
        }

    def __str__(self):
        return f"RequestUseMoraleConversion(protocolNumber={self.__protocolNumber}, sessionInfo={self.__sessionInfo}, supportCardId={self.__supportCardId})"
