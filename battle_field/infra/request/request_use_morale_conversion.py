from common.protocol import CustomProtocol


class RequestUseMoraleConversion:
    def __init__(self, _sessionInfo, _unitIndex, _itemCardId):
        self.__protocolNumber = CustomProtocol.USE_FIELD_ENERGY_INCREMENT_WITH_SACRIFICE_UNIT_ITME_CARD.value
        self.__unitIndex = str(_unitIndex)
        self.__itemCardId = str(_itemCardId)
        self.__sessionInfo = _sessionInfo

    def toDictionary(self):
        return {
            "protocolNumber": self.__protocolNumber,
            "sessionInfo": self.__sessionInfo,
            "unitIndex": self.__unitIndex,
            "itemCardId" : self.__itemCardId
        }

    def __str__(self):
        return f"RequestUseMoraleConversion(protocolNumber={self.__protocolNumber}, unitIndex={self.__unitIndex}, sessionInfo={self.__sessionInfo}, itemCardId={self.__itemCardId})"
