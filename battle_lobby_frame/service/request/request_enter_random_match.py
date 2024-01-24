from common.protocol import CustomProtocol
from session.repository.session_repository_impl import SessionRepositoryImpl


class RequestEnterRandomMatch:
    def __init__(self, _deckName, _sessionId):
        self.__protocolNumber = CustomProtocol.ENTER_MATCH.value
        self.__deckName = _deckName
        self.__sessionId = _sessionId

    def toDictionary(self):
        return {
            "protocolNumber": self.__protocolNumber,
            "deckName": self.__deckName,
            "sessionId": self.__sessionId
        }

    def __str__(self):
        return f"RequestEnterRandomMatch(protocolNumber={self.__protocolNumber}, deckName={self.__deckName}, sessionId={self.__sessionId})"
