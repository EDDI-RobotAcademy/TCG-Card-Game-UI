from session.repository.session_repository_impl import SessionRepositoryImpl


class RequestEnterRandomMatch:
    __deckIndex = None
    __sessionId = None

    def __init__(self, _deckIndex, _sessionId):
        self.__deckIndex = _deckIndex
        self.__sessionId = _sessionId

