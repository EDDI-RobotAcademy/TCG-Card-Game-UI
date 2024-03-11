from common.protocol import CustomProtocol


class RequestUseContractOfDoom:
    def __init__(self, _sessionInfo, _itemCardId):
        self.__protocolNumber = CustomProtocol.CONTRACT_OF_DOOM.value
        self.__sessionInfo = _sessionInfo
        self.__itemCardId = _itemCardId


    def toDictionary(self):
        return {
            "protocolNumber": self.__protocolNumber,
            "itemCardId": self.__itemCardId,
            "sessionInfo": self.__sessionInfo
        }

    def __str__(self):
        return (f"RealBattleStartRequest(protocolNumber={self.__protocolNumber}, "
                f"itemCardId={self.__itemCardId}, "
                f"sessionInfo={self.__sessionInfo}")
