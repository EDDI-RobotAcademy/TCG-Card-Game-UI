from common.protocol import CustomProtocol


class CheckGameMoneyRequest:
    def __init__(self, sessionInfo):
        self.__protocolNumber = CustomProtocol.CHECK_MONEY.value
        self.__sessionInfo = sessionInfo

    def toDictionary(self):
        return {
            "protocolNumber": self.__protocolNumber,
            "sessionInfo": self.__sessionInfo,
        }

    def __str__(self):
        return f"BuyRandomCardRequest(protocolNumber={self.__protocolNumber}, sessionInfo={self.__sessionInfo})"
