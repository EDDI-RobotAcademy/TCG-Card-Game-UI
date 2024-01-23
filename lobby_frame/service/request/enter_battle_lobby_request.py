from common.protocol import CustomProtocol


class EnterBattleLobbyRequest:

    def __init__(self, sessionId):
        self.__protocolNumber = CustomProtocol.ENTER_BATTLE_LOBBY.value
        self.__sessionId = sessionId

    def toDictionary(self):
        return {
            "protocolNumber": self.__protocolNumber,
            "sessionId": self.__sessionId
        }
