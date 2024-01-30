from common.protocol import CustomProtocol


class MyGameMoneyRequest:
    def __init__(self, sessionInfo):
        self.__protocolNumber = CustomProtocol.MY_GAME_MONEY.value
        self.__sessionInfo = sessionInfo

    def toDictionary(self):
        return {
            "protocolNumber": self.__protocolNumber,
            "sessionId": self.__sessionInfo,
        }

    def __str__(self):
        return f"MyGameMoneyRequest(protocolNumber={self.__protocolNumber}, sessionId={self.__sessionInfo})"