from common.protocol import CustomProtocol


class SessionLoginRequest:
    def __init__(self, sessionInfo):
        self.__protocolNumber = CustomProtocol.SESSION_LOGIN.value
        self.__sessionInfo = sessionInfo

    def toDictionary(self):
        return {
            "protocolNumber": self.__protocolNumber,
            "sessionInfo": self.__sessionInfo,
        }

    def __str__(self):
        return f"SessionLoginRequest(protocolNumber={self.__protocolNumber}, sessionInfo={self.__sessionInfo})"
