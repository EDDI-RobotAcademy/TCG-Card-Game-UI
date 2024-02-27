from common.protocol import CustomProtocol


class RequestAttachFieldEnergyToUnit:
    def __init__(self, _sessionInfo, _unitIndex, _energyRace, _energyCount):
        self.__protocolNumber = CustomProtocol.ATTACH_FIELD_ENERGY.value
        self.__unitIndex = str(_unitIndex)
        self.__energyRace = str(_energyRace.value)
        self.__energyCount = str(_energyCount)
        self.__sessionInfo = _sessionInfo

    def toDictionary(self):
        return {
            "protocolNumber": self.__protocolNumber,
            "sessionInfo": self.__sessionInfo,
            "unitIndex": self.__unitIndex,
            "energyRace": self.__energyRace,
            "energyCount": self.__energyCount
        }

    def __str__(self):
        return f"RequestAttachEnergyToUnit(protocolNumber={self.__protocolNumber}, unitIndex={self.__unitIndex}, sessionInfo={self.__sessionInfo}, energyRace={self.__energyRace}, energyCount={self.__energyCount})"
