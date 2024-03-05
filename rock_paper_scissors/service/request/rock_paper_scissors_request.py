from common.protocol import CustomProtocol


class RockPaperScissorsRequest:
    def __init__(self, sessionInfo, choice):
        self.__protocolNumber = CustomProtocol.ROCKPAPERSCISSORS.value
        self.__sessionInfo = sessionInfo
        self.__choice = choice

    def toDictionary(self):
        return {
            "protocolNumber": self.__protocolNumber,
            "sessionInfo": self.__sessionInfo,
            "choice": self.__choice
        }

    def __str__(self):
        return f"RockPaperScissorsRequest(protocolNumber={self.__protocolNumber}, sessionInfo={self.__sessionInfo}, choice={self.__choice})"