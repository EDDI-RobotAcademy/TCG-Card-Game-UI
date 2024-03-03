from common.protocol import CustomProtocol


class CheckRockPaperScissorsWinnerRequest:
    def __init__(self, sessionInfo):
        self.__protocolNumber = CustomProtocol.CHECK_ROCKPAPERSCISSORS_WINNER.value
        self.__sessionInfo = sessionInfo

    def toDictionary(self):
        return {
            "protocolNumber": self.__protocolNumber,
            "sessionInfo": self.__sessionInfo
        }

    def __str__(self):
        return f"CheckRockPaperScissorsWinnerRequest(protocolNumber={self.__protocolNumber}, sessionInfo={self.__sessionInfo})"
