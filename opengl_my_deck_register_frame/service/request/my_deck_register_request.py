from common.protocol import CustomProtocol

class MyDeckRegisterRequest:
    def __init__(self, sessionInfo, myDecckName):
        self.__protocolNumber = CustomProtocol.ACCOUNT_DECK_REGISTER.value
        self.__sessionInfo = sessionInfo
        self.__myDeckName = myDecckName

    def toDictionary(self):
        return {
            "protocolNumber": self.__protocolNumber,
            "sessionInfo": self.__sessionInfo,
            "deckName": self.__myDeckName
        }

    def __str__(self):
        return (f"MyDeckConstructionRequest(protocolNumber={self.__protocolNumber}, "
                f"sessionInfo={self.__sessionInfo}, deckName={self.__myDeckName})")