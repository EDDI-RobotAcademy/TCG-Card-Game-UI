from common.protocol import CustomProtocol


class SurrenderRequest:
    def __init__(self, _sessionId):
        self.__protocolNumber = CustomProtocol.SURRENDER.value
        self.__sessionId = _sessionId

    def toDictionary(self):
        return {
            "protocolNumber": self.__protocolNumber,
            "sessionId": self.__sessionId
        }

    def __str__(self):
        return f"SurrenderRequest(protocolNumber={self.__protocolNumber}, sessionId={self.__sessionId})"
