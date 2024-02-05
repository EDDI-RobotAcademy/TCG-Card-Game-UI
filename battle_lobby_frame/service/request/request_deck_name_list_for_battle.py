from common.protocol import CustomProtocol
from session.repository.session_repository_impl import SessionRepositoryImpl


class RequestDeckNameListForBattle:
    def __init__(self, sessionInfo):
        self.__protocolNumber = CustomProtocol.BATTLE_DECK_LIST.value
        self.__sessionInfo = sessionInfo

    def toDictionary(self):
        return {
            "protocolNumber": self.__protocolNumber,
            "sessionInfo": self.__sessionInfo
        }

    def __str__(self):
        return f"RequestDeckNameListForBattle(protocolNumber={self.__protocolNumber}, sessionInfo={self.__sessionInfo})"
