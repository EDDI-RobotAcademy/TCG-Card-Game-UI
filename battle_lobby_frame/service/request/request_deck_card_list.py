from common.protocol import CustomProtocol
from session.repository.session_repository_impl import SessionRepositoryImpl


class RequestDeckCardList:
    def __init__(self, _deckId, _sessionInfo):
        self.__protocolNumber = CustomProtocol.BATTLE_DECK_CARD.value
        self.__deckId = _deckId
        self.__sessionInfo = _sessionInfo

    def toDictionary(self):
        return {
            "protocolNumber": self.__protocolNumber,
            "deckId": self.__deckId,
            "sessionInfo": self.__sessionInfo
        }

    def __str__(self):
        return f"RequestDeckCardList(protocolNumber={self.__protocolNumber}, deckId={self.__deckId}, sessionInfo={self.__sessionInfo})"
