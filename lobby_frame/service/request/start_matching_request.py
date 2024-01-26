from common.protocol import CustomProtocol


class StartMatchingRequest:
    def __init__(self, sessionInfo):
        self.__protocolNumber = CustomProtocol.ENTER_MATCHING.value
        self.__sessionInfo = sessionInfo


    def toDictionary(self):
        return {
            "protocolNumber": self.__protocolNumber,
            "sessionInfo": self.__sessionInfo
        }

    def __str__(self):
        return f"EnterBattleRequest(protocolNumber={self.__protocolNumber}, sessionInfo={self.__sessionInfo})"
