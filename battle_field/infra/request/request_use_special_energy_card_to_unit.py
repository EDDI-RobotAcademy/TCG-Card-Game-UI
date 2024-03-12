from common.protocol import CustomProtocol


class RequestUseSpecialEnergyCardToUnit:
    def __init__(self, _sessionInfo, _unitIndex, _energyCardId):
        self.__protocolNumber = CustomProtocol.USE_SPECIAL_ENERGY_CARD.value
        self.__unitIndex = str(_unitIndex)
        self.__energyCardId = str(_energyCardId)
        self.__sessionInfo = _sessionInfo

    def toDictionary(self):
        return {
            "protocolNumber": self.__protocolNumber,
            "sessionInfo": self.__sessionInfo,
            "unitIndex": self.__unitIndex,
            "energyCardId" : self.__energyCardId
        }

    def __str__(self):
        return f"RequestUseSpecialEnergyCardToUnit(protocolNumber={self.__protocolNumber}, unitIndex={self.__unitIndex}, sessionInfo={self.__sessionInfo}, energyCardId={self.__energyCardId})"
