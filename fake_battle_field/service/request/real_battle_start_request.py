from common.protocol import CustomProtocol


class RealBattleStartRequest:
    def __init__(self, sessionInfo):
        self.__protocolNumber = CustomProtocol.REAL_BATTLE_START.value
        self.__sessionInfo = sessionInfo


    def toDictionary(self):
        return {
            "protocolNumber": self.__protocolNumber,
            "sessionInfo": self.__sessionInfo,
        }

    def __str__(self):
        return (f"RealBattleStartRequest(protocolNumber={self.__protocolNumber}, "
                f"sessionInfo={self.__sessionInfo}")
