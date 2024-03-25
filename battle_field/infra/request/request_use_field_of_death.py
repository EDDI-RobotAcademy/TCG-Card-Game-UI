from common.protocol import CustomProtocol


class RequestUseFieldOfDeath:
    def __init__(self, _sessionInfo, _itemCardId):
        self.__protocolNumber = CustomProtocol.USE_FIELD_ENERGY_REMOVE_ITEM_CARD.value
        self.__itemCardId = str(_itemCardId)
        self.__sessionInfo = _sessionInfo

    def toDictionary(self):
        return {
            "protocolNumber": self.__protocolNumber,
            "sessionInfo": self.__sessionInfo,
            "itemCardId": self.__itemCardId
        }

    def __str__(self):
        return f"RequestUseFieldOfDeath(protocolNumber={self.__protocolNumber}, sessionInfo={self.__sessionInfo}, itemCardId={self.__itemCardId})"
