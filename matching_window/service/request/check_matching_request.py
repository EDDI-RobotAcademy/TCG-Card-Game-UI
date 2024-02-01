from common.protocol import CustomProtocol


class CheckMatchingRequest:
    def __init__(self, sessionInfo):
        self.__protocolNumber = CustomProtocol.CHECK_MATCHING.value
        self.__sessionInfo = sessionInfo


    def toDictionary(self):
        return {
            "protocolNumber": self.__protocolNumber,
            "sessionInfo": self.__sessionInfo
        }

    def __str__(self):
        return f"CheckMatchingRequest(protocolNumber={self.__protocolNumber}, sessionInfo={self.__sessionInfo})"
