from common.protocol import CustomProtocol


class StartMatchingRequest:
    def __init__(self, sessionInfo):
        self.__protocolNumber = CustomProtocol.BATTLE_WAIT_QUEUE_FOR_MATCH.value
        self.__sessionInfo = sessionInfo


    def toDictionary(self):
        return {
            "protocolNumber": self.__protocolNumber,
            "sessionInfo": self.__sessionInfo
        }

    def __str__(self):
        return f"StartMatchingRequest(protocolNumber={self.__protocolNumber}, sessionInfo={self.__sessionInfo})"
