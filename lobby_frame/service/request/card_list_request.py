from common.protocol import CustomProtocol


class CardListRequest:
    def __init__(self, sessionInfo):
        self.__protocolNumber = CustomProtocol.ACCOUNT_CARD_LIST.value
        self.__sessionInfo = sessionInfo

    def toDictionary(self):
        return {
            "protocolNumber": self.__protocolNumber,
            "sessionInfo": self.__sessionInfo
        }

    def __str__(self):
        return (f"CardListRequest(protocolNumber={self.__protocolNumber},"
                f"sessionInfo={self.__sessionInfo})")