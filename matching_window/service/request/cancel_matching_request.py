from common.protocol import CustomProtocol


class CancelMatchingRequest():
    def __init__(self, sessionInfo):
        self.__protocolNumber = CustomProtocol.CANCEL_MATCH.value
        self.__sessionInfo = sessionInfo


    def toDictionary(self):
        return {
            "protocolNumber": self.__protocolNumber,
            "sessionInfo": self.__sessionInfo
        }

    def __str__(self):
        return f"CancelMatchingRequest(protocolNumber={self.__protocolNumber}, sessionInfo={self.__sessionInfo})"
