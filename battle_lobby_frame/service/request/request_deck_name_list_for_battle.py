from common.protocol import CustomProtocol
from session.repository.session_repository_impl import SessionRepositoryImpl


class RequestDeckNameListForBattle:
    def __init__(self, _sessionId):
        self.__protocolNumber = CustomProtocol.DECK_NAME_LIST.value
        self.__sessionId = _sessionId

    def toDictionary(self):
        return {
            "protocolNumber": self.__protocolNumber,
            "sessionId": self.__sessionId
        }

    def __str__(self):
        return f"RequestDeckNameListForBattle(protocolNumber={self.__protocolNumber}, sessionId={self.__sessionId})"
