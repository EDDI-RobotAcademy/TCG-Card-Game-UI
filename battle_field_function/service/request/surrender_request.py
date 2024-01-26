from common.protocol import CustomProtocol


class SurrenderRequest:
    def __init__(self, _sessionInfo):
        self.__protocolNumber = CustomProtocol.SURRENDER.value
        self.__sessionInfo = _sessionInfo

    def toDictionary(self):
        return {
            "protocolNumber": self.__protocolNumber,
            "sessionInfo": self.__sessionInfo
        }

    def __str__(self):
        return f"SurrenderRequest(protocolNumber={self.__protocolNumber}, sessionInfo={self.__sessionInfo})"
