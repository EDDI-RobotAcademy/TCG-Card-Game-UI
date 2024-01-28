from common.protocol import CustomProtocol


class BuyRandomCardRequest:
    def __init__(self, sessionId, race):
        self.__protocolNumber = CustomProtocol.CARD_RANDOM.value
        self.__sessionId = sessionId
        self.__race = race

    def toDictionary(self):
        return {
            "protocolNumber": self.__protocolNumber,
            "sessionId": self.__sessionId,
            "race": self.__race
        }

    def __str__(self):
        return f"BuyRandomCardRequest(protocolNumber={self.__protocolNumber}, sessionId={self.__sessionId}race={self.__race})"
