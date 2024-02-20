from common.protocol import CustomProtocol


class FreeRandomCardRequest:
    def __init__(self, sessionInfo):
        self.__protocolNumber = CustomProtocol.FREE_BUY_CARD.value
        self.__sessionInfo = sessionInfo

    def toDictionary(self):
        return {
            "protocolNumber": self.__protocolNumber,
            "sessionInfo": self.__sessionInfo

        }

    def __str__(self):
        return f"FreeRandomCardRequest(protocolNumber={self.__protocolNumber}, sessionInfo={self.__sessionInfo})"
