from common.protocol import CustomProtocol


class CheckMatchingRequest:
    def __init__(self, sessionId):
        self.__protocolNumber = CustomProtocol.CHECK_MATCHING.value
        self.__sessionId = sessionId


    def toDictionary(self):
        return {
            "protocolNumber": self.__protocolNumber,
            "sessionId": self.__sessionId
        }

    def __str__(self):
        return f"EnterBattleRequest(protocolNumber={self.__protocolNumber}, sessionId={self.__sessionId})"
