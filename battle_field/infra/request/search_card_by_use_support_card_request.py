from common.protocol import CustomProtocol


# 망자의 늪
class SearchCardByUseSupportCardRequest:
    def __init__(self, _sessionInfo, _cardId):
        self.__protocolNumber = CustomProtocol.SEARCH_CARD_BY_SUPPORT_CARD.value
        self.__supportCardId = _cardId
        self.__sessionInfo = _sessionInfo

    def toDictionary(self):
        return {
            "protocolNumber": self.__protocolNumber,
            "supportCardId": self.__supportCardId,
            "sessionInfo": self.__sessionInfo
        }

    def __str__(self):
        return f"SearchCardByUseSupportCardRequest(protocolNumber={self.__protocolNumber}, supportCardId={self.__supportCardId}, sessionInfo={self.__sessionInfo})"
