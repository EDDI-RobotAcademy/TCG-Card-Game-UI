from common.protocol import CustomProtocol


class CheckMatchingRequest:
    def __init__(self, sessionInfo):
        self.__protocolNumber = CustomProtocol.BATTLE_READY.value
        self.__sessionInfo = sessionInfo


    def toDictionary(self):
        return {
            "protocolNumber": self.__protocolNumber,
            "sessionInfo": self.__sessionInfo
        }

    def __str__(self):
        return f"CheckMatchingRequest(protocolNumber={self.__protocolNumber}, sessionInfo={self.__sessionInfo})"
