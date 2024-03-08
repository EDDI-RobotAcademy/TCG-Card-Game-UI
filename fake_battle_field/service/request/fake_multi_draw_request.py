from common.protocol import CustomProtocol


class FakeMultiDrawRequest:
    def __init__(self, sessionInfo):
        self.__protocolNumber = CustomProtocol.FAKE_MULTI_DRAW.value
        self.__sessionInfo = sessionInfo

    def toDictionary(self):
        return {
            "protocolNumber": self.__protocolNumber,
            "sessionInfo": self.__sessionInfo
        }

    def __str__(self):
        return f"FakeMultiDrawRequest(protocolNumber={self.__protocolNumber}, sessionInfo={self.__sessionInfo})"