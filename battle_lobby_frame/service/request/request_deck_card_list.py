from common.protocol import CustomProtocol
from session.repository.session_repository_impl import SessionRepositoryImpl


class RequestDeckCardList:
    def __init__(self, _deckId, _sessionId):
        self.__protocolNumber = CustomProtocol.DECK_CARD_LIST.value
        self.__deckId = _deckId
        self.__sessionId = _sessionId

    def toDictionary(self):
        return {
            "protocolNumber": self.__protocolNumber,
            "deckId": self.__deckId,
            "sessionId": self.__sessionId
        }

    def __str__(self):
        return f"RequestDeckCardList(protocolNumber={self.__protocolNumber}, deckId={self.__deckId}, sessionId={self.__sessionId})"
