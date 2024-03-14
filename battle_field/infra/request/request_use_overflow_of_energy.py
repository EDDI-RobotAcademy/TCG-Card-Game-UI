from common.protocol import CustomProtocol


class RequestUseOverflowOfEnergy:
    def __init__(self, _sessionInfo, _unitIndex, _supportCardId):
        self.__protocolNumber = CustomProtocol.USE_ENERGY_BOOST_SUPPORT_CARD.value
        self.__unitIndex = str(_unitIndex)
        self.__supportCardId = str(_supportCardId)
        self.__sessionInfo = _sessionInfo

    def toDictionary(self):
        return {
            "protocolNumber": self.__protocolNumber,
            "sessionInfo": self.__sessionInfo,
            "unitIndex": self.__unitIndex,
            "supportCardId" : self.__supportCardId
        }

    def __str__(self):
        return f"RequestUseOverflowOfEnergy(protocolNumber={self.__protocolNumber}, unitIndex={self.__unitIndex}, sessionInfo={self.__sessionInfo}, supportCardId={self.__supportCardId})"
