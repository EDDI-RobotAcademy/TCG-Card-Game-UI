from common.protocol import CustomProtocol


class CheckPrepareBattleRequest():
    def __init__(self, sessionInfo):
        self.__protocolNumber = CustomProtocol.CHECK_BATTLE_PREPARE.value
        self.__sessionInfo = sessionInfo


    def toDictionary(self):
        return {
            "protocolNumber": self.__protocolNumber,
            "sessionInfo": self.__sessionInfo
        }

    def __str__(self):
        return f"CheckPrepareBattleRequest(protocolNumber={self.__protocolNumber}, sessionInfo={self.__sessionInfo})"
