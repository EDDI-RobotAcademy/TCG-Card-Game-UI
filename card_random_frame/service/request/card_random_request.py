from common.protocol import CustomProtocol


class CardRandomRequest:
    def __init__(self):
        self.__protocolNumber = CustomProtocol.CARD_RANDOM.value

    def toDictionary(self):
        return {
            "protocolNumber": self.__protocolNumber
        }

    def __str__(self):
        return f"CardRandomRequest(protocolNumber={self.__protocolNumber})"
