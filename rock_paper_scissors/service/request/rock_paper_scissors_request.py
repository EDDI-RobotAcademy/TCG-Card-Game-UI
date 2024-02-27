from common.protocol import CustomProtocol


class CheckGameMoneyRequest:
    def __init__(self, sessionInfo, choice):
        self.__protocolNumber = CustomProtocol.SHOP_DATA.value
        self.__sessionInfo = sessionInfo
        self.__choice = choice

    def toDictionary(self):
        return {
            "protocolNumber": self.__protocolNumber,
            "sessionInfo": self.__sessionInfo,
        }

    def __str__(self):
        return f"CheckGameMoneyRequest(protocolNumber={self.__protocolNumber}, sessionInfo={self.__sessionInfo})"