from common.protocol import CustomProtocol


class MuligunRequest:
    def __init__(self, sessionInfo, cardList):
        self.__protocolNumber = CustomProtocol.CHANGE_FIRST_HAND.value
        self.__sessionInfo = sessionInfo
        self.__cardList = cardList

    def toDictionary(self):
        return {
            "protocolNumber": self.__protocolNumber,
            "sessionInfo": self.__sessionInfo,
            "cardList": self.__cardList
        }

    def __str__(self):
        return (f"CardListRequest(protocolNumber={self.__protocolNumber},"
                f"sessionInfo={self.__sessionInfo}),"
                f"cardList={self.__cardList})")